#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;
use myHTML;
use PopUp;

############################################################################
my $form = myForm->new();
if ( !SysAccess->chkPriv( $form, 'QAReports' ) ) {
    myDBI->error("HL7 Report / Access Denied!");
}
my $cdbh = myDBI->dbconnect('okmis_config');

############################################################################
if   ( $form->{submit} ) { main->submit(); }
else                     { main->check(); }
myDBI->cleanup();
exit;

############################################################################
sub check {
    my $html = myHTML->newHTML(
        $form,
        'Report HL7 Tags',
        'CheckPopupWindow noclock countdown_10'
      )
      . qq|
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<H3>Report HL7 Tags</H3>
<P>
  Select a Tag to report
  <SELECT ID="HL7Tag" NAME="HL7Tag" ONFOCUS="select();" ONCHANGE="callAjax('HL7Report',this.value,this.id,'');" >
        | . main->selHL7Tags($form) . qq|
  </SELECT> 
</P>
<SPAN ID="HL7Tag_display" >report appears here</SPAN>
<P>
<INPUT TYPE="button" NAME="cancel" VALUE="Close" ONCLICK="javascript: window.close()" >
</P>
</BODY>
</HTML>
|;
    print $html;
    return ();
}

sub submit {
    my $q, $text;
    my $text = qq|SUBMIT: $form->{Name} report.|;
    print qq|Content-type: text/html\n\n
<HTML>
<HEAD> <TITLE>$rxHL7->{Tag}</TITLE> 
<script language="JavaScript">
window.opener.location.href = window.opener.location.href;
</script>
</HEAD>
<BODY >
<H3>$rxHL7->{Tag}</H3>
<FORM NAME="submit" ACTION="/cgi/bin/GenReport.cgi" METHOD="POST">
<P>${text}</P>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FORM>
</BODY>
</HTML>
|;
    return ();
}

sub selHL7Tags {
    my ( $self, $form ) = @_;
    my $items = ();
    my $s     = $cdbh->prepare("select Tag from xHL7 group by Tag");
    $s->execute() || myDBI->dberror("selHL7Tag: group by Tag");
    while ( my $r = $s->fetchrow_hashref ) {
        my $name = $r->{'Tag'};
        my $val  = $r->{'Tag'};
        $items->{$name}->{name} = ${name};
        $items->{$name}->{val}  = ${val};
    }
    my $unSel = PopUp->unMatched();

    # just uses items->{name} to sort
    my $SelStmt = PopUp->makeSelect( $items, $bynum );
    $s->finish();
    return ( $unSel . $SelStmt );
}
