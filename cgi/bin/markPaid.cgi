#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use File::Copy;
use DBI;
use DBForm;
use DBUtil;
use SysAccess;

############################################################################
$pwd  = cwd();
$form = DBForm->new();
if ( !SysAccess->verify( $form, 'Privilege=Payroll' ) ) {
    $form->error("MarkPaid / Access Denied");
}
chdir("$form->{DOCROOT}/reports2");

############################################################################
#warn qq|\n${PGM}: begin: $form->{submit}, $form->{cancel}, $form->{mlt}\n|;
#warn qq|${PGM}: begin: $form->{MarkFile}\n|;
if ( $form->{submit} ) { main->submit( $form, $form->{MarkFile} ); }
else                   { main->check($form); }
$form->complete();
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

    #warn qq|\n\nENTER markPaid: check:\np1=$p1, p2=$p2\n|;
    #warn qq|\nType=$Type, ProvID=$ProvID, Stamp=$Stamp, Token=$Token\n|;
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
    my ( $self, $form, $markfile ) = @_;
    if ( $markfile eq '' ) {
        $form->error("MarkPaid / Access Denied: file name is NULL!");
    }

    my $text = main->mark( $form, $markfile );

    #warn qq|\n\nENTER markPaid: submit:\nmarkfile=$markfile\n|;
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>Marked Payroll</TITLE> 
<script language="JavaScript">
window.opener.location.href = window.opener.location.href;
</script>
</HEAD>
<BODY >
<H3>Marked Payroll</H3>
<FORM NAME="submit" ACTION="/src/cgi/bin/markPaid.cgi" METHOD="POST">
<P>${text}</P>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}
############################################################################
sub mark {
    my ( $self, $form, $markfile ) = @_;
    my $text;
    my $MarkDate = $form->{MarkDate} ? $form->{MarkDate} : $form->{TODAY};
    my ( $p1, $p2 ) = $markfile =~ m/(.*)\.(.*)$/;

    # '95_Payroll_MarkPaid_20090429220714_S3fqZb.xls';
    my ( $ProvID, $Name, $Type, $Stamp, $Token ) = split( '_', $p1, 5 );

    #warn qq|\n\nENTER markPaid: ${MarkDate}, mark:\np1=$p1, p2=$p2\n|;
    #warn qq|\nType=$Type, ProvID=$ProvID, Stamp=$Stamp, Token=$Token\n|;
    if ( $ProvID != $form->{LOGINPROVID} ) {
        $form->error("MarkPaid / Access Denied: not owner of file!");
    }

    my $dbh = $form->dbconnect();
    $qMarkTran =
qq|update NoteTrans set PaidDate='${MarkDate}' where ID=? and PaidDate is null|;
    $sMarkTran = $dbh->prepare($qMarkTran);
    $qMarkNote =
qq|update Treatment set PaidDate='${MarkDate}' where TrID=? and PaidDate is null|;
    $sMarkNote = $dbh->prepare($qMarkNote);
    $qMarkPaid =
qq|update NotePaid set PaidDate='${MarkDate}' where TrID=? and PaidDate is null|;
    $sMarkPaid = $dbh->prepare($qMarkPaid);

    if ( open( MARKFILE, $markfile ) ) {
        my @items;
        my $trans = 0;
        my $notes = 0;
        while (<MARKFILE>) { chomp($_); push( @items, split( ' ', $_ ) ); }
        my $Cnt = 0;
        foreach my $ID (@items) {
            if    ( $ID eq 'TRANSACTIONS:' ) { $trans = 1; }
            elsif ( $ID eq 'TREATMENTS:' )   { $trans = 0; $notes = 1; }
            elsif ($trans) {
                $sMarkTran->execute($ID) || $form->dberror($qMarkTran);
            }
            elsif ($notes) {
                $sMarkNote->execute($ID) || $form->dberror($qMarkNote);
                $sMarkPaid->execute($ID) || $form->dberror($qMarkPaid);
                $Cnt++;
            }
        }
        $text .= qq|<BR>${Cnt} notes marked paid with date: ${MarkDate}.|;

#warn qq|markPaid: Cnt=$Cnt notes marked paid.\n|;
#warn qq|markPaid: p1=$p1, p2=$p2\nType=$Type, ProvID=$ProvID, Stamp=$Stamp, Token=$Token\n|;
        my $Marked = DBUtil->Date( '', 'stamp' );
        my $MarkedFile =
"../payroll/${ProvID}_Payroll_MarkedPaid_${Stamp}_${Token}_${Marked}.${p2}";
        $text .= qq|<BR>move MarkPaid_${Stamp} to MarkedPaid_${Marked}|;
        move( $markfile, $MarkedFile )
          or $text .= "<<< ERROR >>>: Move ${file} failed: $!";
        my $SummaryFrom = "${ProvID}_Payroll_Summary_${Stamp}_${Token}.xls";
        my $SummaryTo =
"../payroll/${ProvID}_Payroll_Summary_${Stamp}_${Token}_${Marked}.xls";
        $text .= qq|<BR>move Summary_${ProvID} to Summary_${Marked}|;
        move( $SummaryFrom, $SummaryTo )
          or $text .= "<<< ERROR >>>: Move ${SummaryFrom} failed: $!";
        my $DetailFrom = "${ProvID}_Payroll_Detail_${Stamp}_${Token}.xls";
        my $DetailTo =
          "../payroll/${ProvID}_Payroll_Detail_${Stamp}_${Token}_${Marked}.xls";
        $text .= qq|<BR>move Detail_${Stamp} to Detail_${Marked}|;
        move( $DetailFrom, $DetailTo )
          or $text .= "<<< ERROR >>>: Move ${DetailFrom} failed: $!";
    }
    else { $form->dberror("Can't find file $markfile: $!"); }
    return ($text);
}
