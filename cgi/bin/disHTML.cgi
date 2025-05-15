#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myDBI;
use myConfig;
use myHTML;
use File::stat;
use Time::localtime;

############################################################################
my $form = myForm->new();

#foreach my $f ( sort keys %{$form} ) { warn "dif: form-$f=$form->{$f}\n"; }
#unless ( SysAccess->chkPriv($form,'Agent') ) { myDBI->error("Page DENIED!"); }

my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

my $text;
my $title;
if ( $form->{'action'} eq 'read' ) {
    my $file     = $form->{'IDs'};
    my $SRCBIN   = myConfig->cfg('SRCBIN');
    my $dirname  = $form->{'page'};
    my $dir      = myConfig->cfg($dirname);
    my $subdir   = $form->{'subpage'};
    my $filepath = qq|${dir}/${subdir}/${file}|;
    my $filedt   = ctime( stat($filepath)->mtime );
    my $process  = $form->{'process'};
    if ( $process eq '' ) { $text = DBUtil->ReadFile($filepath); }
    else {
        my $tmpname =
            $form->{'DOCROOT'} . '/tmp/'
          . $form->{'LOGINID'} . '_'
          . DBUtil->genToken() . '_'
          . DBUtil->Date( '', 'stamp' ) . '.txt';
        warn qq|tmpname=${tmpname}\n|;
        system(
"${SRCBIN}/${process} DBNAME=$form->{'DBNAME'}\\&filepath=${filepath}\\&mlt=$form->{mlt}\\&debug=${debug} > ${tmpname}"
        );
        $text = DBUtil->ReadFile($tmpname);
    }

    $title  = $form->{'IDs'};
    $header = qq|
  ${file}
  <BR>
  ${filedt}
|;
}
else {
    my $table = $form->{'action'};
    my $id    = $form->{'IDs'};
    my $fld   = $form->{'page'};

    #warn "PrintHTML: table=${table}: id=${id}, fld=${fld}\n";
    my $s = $dbh->prepare("select * from ${table} where ID='${id}'");
    $s->execute() || $form->dberror("select ${table}: ID='${ID}'");
    my $r = $s->fetchrow_hashref;
    $s->finish();
    $title = qq|Insurance Remarks from reconciliation|;
    $text  = $r->{$fld};
}
############################################################################
# Start out the display.
my $html =
  myHTML->newHTML( $form, $title, 'CheckPopupWindow noclock countdown_5' ) . qq|
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  return true;
}
</SCRIPT>

<DIV CLASS="main hdrcol title" >
  ${header}
</DIV>

<DIV CLASS="home strcol title" >
<PRE>
${text}
</PRE>
</DIV>
<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</BODY>
</HTML>
|;

#<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
#<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
#<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >

myDBI->cleanup();

print $html;
exit;
############################################################################
