#!/usr/bin/perl
#############################################################################
print "ENV=".$ENV{DOCUMENT_ROOT}."\n";
foreach $var (sort keys %ENV) { print "$var = $ENV{$var}<BR>\n"; }
#use lib "$ENV{DOCUMENT_ROOT}/lib";
use lib "$ENV{MISLIB}";
use DBUtil;

#############################################################################
my $DT=localtime();
warn qq|DT=$DT\n|;
my $html = qq|ENV=$ENV{DOCUMENT_ROOT}<BR>IT WORKED|;
print qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>TEST HTML</TITLE></HEAD>\n<BODY >\n|
      . $html . qq|\n</BODY>\n</HTML>\n|;
exit;

#############################################################################
