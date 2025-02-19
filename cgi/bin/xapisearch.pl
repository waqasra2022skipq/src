#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use myHTML;

############################################################################
my $form = myForm->new();
$NextLocation =
  qq|Location: /cgi/bin/xapi.pl?mlt=$form->{mlt}&action=search\n\n|;
print $NextLocation;
myDBI->cleanup();
exit;
############################################################################
