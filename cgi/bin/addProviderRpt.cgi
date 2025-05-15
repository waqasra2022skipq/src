#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $cdbh = myDBI->dbconnect('okmis_config');
if ( !SysAccess->chkPriv( $form, 'HRReports' ) ) {
    myDBI->error("Add Provider Report / Access Denied!");
}

############################################################################
warn qq|${PGM}: begin: $form->{submit}, $form->{cancel}, $form->{mlt}\n|;
if   ( $form->{submit} ) { main->submit(); }
else                     { main->check(); }

myDBI->cleanup();
exit;

############################################################################
sub check {
    my $sxReports = $cdbh->prepare("select * from xReports where Name=?");
    $sxReports->execute( $form->{Name} )
      || myDBI->dberror("execute error: addProviderRpts/check1");
    my $rxReports = $sxReports->fetchrow_hashref;
    my $text;
    my $sProviderRpts =
      $dbh->prepare("select * from ProviderRpts where ProvID=? and Name=?");
    $sProviderRpts->execute( $form->{LOGINPROVID}, $form->{Name} )
      || myDBI->dberror("execute error: addProviderRpts/check2");
    if ( my $rProviderRpts = $sProviderRpts->fetchrow_hashref ) {
        $text =
qq|This report is set to run automatically. Do you wish to cancel it?|;
    }
    else {
        $text =
qq|This report is not setup to run automatically. Do you wish to add it?|;
    }
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>$rxReports->{Descr}</TITLE> </HEAD>
<BODY >
<H3>$rxReports->{Descr}</H3>
<FORM NAME="submit" ACTION="/cgi/bin/addProviderRpt.cgi" METHOD="POST">
<P>${text}</P>
<INPUT TYPE="submit" NAME="submit" VALUE="yes" >
<INPUT TYPE="button" NAME="cancel" VALUE="forget it" ONCLICK="javascript: window.close()" >
<INPUT TYPE="hidden" NAME="Name" VALUE="$form->{Name}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}

sub submit {
    my $q, $text;
    my $sProviderRpts =
      $dbh->prepare("select * from ProviderRpts where ProvID=? and Name=?");
    $sProviderRpts->execute( $form->{LOGINPROVID}, $form->{Name} )
      || myDBI->dberror("execute error: addProviderRpts/check2");
    if ( my $rProviderRpts = $sProviderRpts->fetchrow_hashref ) {
        $q =
qq|delete from ProviderRpts where ProvID='$form->{LOGINPROVID}' and Name='$form->{Name}'|;
        $text = qq|$form->{Name} report removed.|;
        my $val = $rProviderRpts->{ID};
    }
    else {
        $q =
qq|insert into ProviderRpts (ProvID,Name,CreateProvID,CreateDate,ChangeProvID) VALUES ('$form->{LOGINPROVID}','$form->{Name}','$form->{LOGINPROVID}','$form->{TODAY}','$form->{LOGINPROVID}')|;
        $text = qq|$form->{Name} report added.|;
    }
    my $s = $dbh->prepare($q);
    $s->execute() || myDBI->dberror("execute error: addProviderRpts/$q");
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>$rxReports->{Descr}</TITLE> 
<script language="JavaScript">
window.opener.location.href = window.opener.location.href;
</script>
</HEAD>
<BODY >
<H3>$rxReports->{Descr}</H3>
<FORM NAME="submit" ACTION="/cgi/bin/addProviderRpt.cgi" METHOD="POST">
<P>${text}</P>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}
