#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBA;
use myForm;
use myDBI;
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#&Forms::FormGet(\%FORM);
############################################################################
my $isHTML = 0;
if ( $ENV{HTTP_USER_AGENT} ) { $isHTML = 1; }
print "content-type: text/html\n\n";
print "ENV=" . $ENV{DOCUMENT_ROOT} . "<BR>\n";

foreach $var ( sort keys %ENV ) { print "$var = $ENV{$var}<BR>\n"; }

#use lib "$ENV{DOCUMENT_ROOT}/lib";
# use lib "$ENV{MISLIB}";
# use DBUtil;

#############################################################################
my $DT = localtime();
warn qq|DT=$DT\n|;
my $html = qq|ENV=$ENV{DOCUMENT_ROOT}<BR>IT WORKED|;
print
qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>TEST HTML</TITLE></HEAD>\n<BODY >\n|
  . $html
  . qq|\n</BODY>\n</HTML>\n|;

myDBI->cleanup();
exit;
############################################################################
