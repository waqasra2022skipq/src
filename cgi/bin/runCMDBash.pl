#!C:/Strawberry/perl/bin/perl.exe

use lib 'C:/xampp/htdocs/src/lib';

use CGI::Carp qw(fatalsToBrowser);
use DBI;
use myForm;
use myHTML;

############################################################################
my $form = myForm->new();

############################################################################
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;
my $html = myHTML->close( 1, $form->{'mlt'} );

############################################################################
my $SBIN = myConfig->cfg('SRCSBIN');
$cmd      = qq|${SBIN}/rebill/rebill|;
$AgencyID = $form->{'AgencyID'};

$cmd .= qq| "DBNAME=$form->{'DBNAME'}&mlt=$form->{'mlt'}&AgencyID=$AgencyID"|;
system("${cmd}");
print $html;
exit;
############################################################################
