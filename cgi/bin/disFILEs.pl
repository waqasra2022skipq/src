#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use Cwd;
use DBI;
use DBA;
use myForm;
use myDBI;
use myHTML;
use gXML;
use XML::LibXSLT;
use XML::LibXML;
binmode STDOUT, ":utf8";

############################################################################
# usage:
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
my $ProvID   = $form->{'ProvID'};
my $ClientID = $form->{'ClientID'};
my $TrID     = $form->{'TrIDs'};
my $Agent    = SysAccess->verify( $form, 'Privilege=Agent' );
unless ($Agent) { myDBI->error("Page DENIED!"); }
##
chdir("$form->{DOCROOT}");
my $out = '';
$Names = "tmp/FILEs/CQM*/*";
my @Files = glob($Names);

foreach $file (@Files) {
    my $type = $file =~ /XML_/ ? 'XML' : 'QRDA';
    $out .= qq|
  <TR>
    <TD CLASS="strcol" >
      <A HREF="javascript:ReportWindow('/${file}','File')" >display ${file} ${type}</A>
    </TD>
  </TR>
|;
}

# now output the html screen to select the created documents...
my $html =
  myHTML->newHTML( $form, 'Send CCDA', 'CheckPopupWindow noclock countdown_1' )
  . qq|
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  return true;
}
</SCRIPT>

<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Display QRDA</TD> </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
${out}
</TABLE>
  
    </TD>
  </TR>
</TABLE>
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</BODY>
</HTML>
|;
print $html;

myDBI->cleanup();
exit;
############################################################################
