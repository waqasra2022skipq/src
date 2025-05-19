#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use DBUtil;
use SysAccess;

my $PGM = "copyProviderPay.cgi";
############################################################################
# to copy from one Provider to another all payrates
# ./copyProviderPay.cgi DBNAME=okmis_oays\&submit=1\&FromProvID=156\&ToProvID=1139
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
if ( !SysAccess->verify( $form, 'Privilege=Payroll' ) ) {
    myDBI->error("MarkPaid / Access Denied");
}
chdir("$form->{DOCROOT}/reports3");

############################################################################
warn qq|\n${PGM}: begin: $form->{submit}, $form->{cancel}, $form->{mlt}\n|;
warn qq|${PGM}: begin: $form->{FromProvID}, $form->{ToProvID}\n|;
if   ( $form->{submit} ) { main->submit($form); }
else                     { main->check($form); }

myDBI->cleanup();
exit;

############################################################################
sub check {
    my ( $self, $form ) = @_;
    my ( $p1,   $p2 )   = $form->{MarkFile} =~ m/(.*)\.(.*)$/;

    # '95_Payroll_MarkPaid_20090429220714_S3fqZb.xls';
    my ( $ProvID, $Name, $Type, $Stamp, $Token ) = split( '_', $p1, 5 );
    my $Y     = substr( $Stamp, 0, 4 );
    my $M     = substr( $Stamp, 4, 2 );
    my $D     = substr( $Stamp, 6, 2 );
    my $SDATE = DBUtil->Date( "$Y-$M-$D", 'fmt', 'MM/DD/YYYY' );
    my $h     = substr( $Stamp, 8,  2 );
    my $m     = substr( $Stamp, 10, 2 );
    my $s     = substr( $Stamp, 12, 2 );
    my $STIME = $h . ':' . $m . ':' . $s;
    warn qq|\n\nENTER markPaid: check:\np1=$p1, p2=$p2\n|;
    warn qq|\nType=$Type, ProvID=$ProvID, Stamp=$Stamp, Token=$Token\n|;
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>Mark Payroll as Paid</TITLE> </HEAD>
<BODY >
<H3>Mark Payroll as Paid</H3>
<FORM NAME="submit" ACTION="/src/cgi/bin/markPaid.cgi" METHOD="POST">
<P>
from file dated ${SDATE} @ ${STIME}
<BR>(${Name} ${Type})
</P>
<INPUT TYPE="submit" NAME="submit" VALUE="yes" >
<INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
<INPUT TYPE="hidden" NAME="MarkFile" VALUE="$form->{MarkFile}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}

sub submit {
    my ( $self, $form ) = @_;
    my $FromID    = $form->{FromProvID};
    my $ToID      = $form->{ToProvID};
    my $qProvider = qq|select * from Provider where Provider.ProvID=?|;
    my $sProvider = $dbh->prepare($qProvider);
    $sProvider->execute($FromID) || myDBI->dberror("select Provider $FromID");
    my $rFrom = $sProvider->fetchrow_hashref;
    $sProvider->execute($ToID) || myDBI->dberror("select Provider $ToID");
    my $rTo = $sProvider->fetchrow_hashref;
    $sProvider->finish();

    my $text = main->copy( $form, $rFrom, $rTo );
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>Copy Payroll</TITLE> 
<script language="JavaScript">
window.opener.location.href = window.opener.location.href;
</script>
</HEAD>
<BODY >
<H3>Copy Payroll</H3>
<FORM NAME="submit" ACTION="/src/cgi/bin/copyProviderPay.cgi" METHOD="POST">
<P>${text}</P>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}
############################################################################
sub copy {
    my ( $self, $form, $rFrom, $rTo ) = @_;
    my $text;
    my $FromProvID = $rFrom->{ProvID};
    my $FromName   = qq|$rFrom->{FName} $rFrom->{LName}|;
    my $ToProvID   = $rTo->{ProvID};
    my $ToName     = qq|$rTo->{FName} $rTo->{LName}|;
    if ( $FromProvID eq '' || $ToProvID eq '' ) {
        $text .= qq|<BR>Missing From/To Provider!|;
        return ($text);
    }

    my $q = qq|select * from ProviderPay where ExpDate is null and ProvID=?|;
    my $s = $dbh->prepare($q);
    $s->execute($FromProvID)
      || myDBI->dberror("select ProviderPay $FromProvID");
    my $Cnt = $s->rows;
    while ( my $r = $s->fetchrow_hashref ) {
        delete $r->{ID};
        delete $r->{CreateDate};
        delete $r->{CreateProvID};
        delete $r->{RecDOLC};
        delete $r->{ChangeProvID};
        $r->{ProvID} = $ToProvID;
        my $qNew = DBA->genInsert( $form, 'ProviderPay', $r );
        my $sNew = $dbh->prepare($qNew);
        $sNew->execute()
          || myDBI->dberror("insert ProviderPay $FromProvID/$ToProvID");
        $sNew->finish();
    }
    $s->finish();
    $text .=
      qq|<BR>Copy from '${FromName}' to '${ToName}' <BR>$Cnt records copied.|;
    if ( $Cnt == 0 ) { $text .= qq|<BR>No records found.|; }
    return ($text);
}
