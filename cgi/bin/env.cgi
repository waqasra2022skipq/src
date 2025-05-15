#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
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
print "<HTML>
<HEAD><TITLE>Environment Varibles</TITLE></HEAD>
<BODY BGCOLOR=\"FFFFFF\"
<CENTER><H1>Environment Variables</H1></CENTER>
<P>";
print qq|isHTML: ${isHTML}<BR>\n|;
print qq|FORM Variables<BR>\n|;
foreach $var ( sort keys %{$form} ) { print "$var = $form->{$var}<BR>\n"; }
print qq|ENVIRONMENT Variables<BR>\n|;
print qq|REQUEST_METHOD=$ENV{REQUEST_METHOD}<BR>\n|;
foreach $var ( sort keys %ENV ) { print "$var = $ENV{$var}<BR>\n"; }
print qq|SERVER Variables<BR>\n|;
print qq|AUTH_USER = $_SERVER{PHP_AUTH_USER}<BR>\n|;
foreach $var (@_SERVER) { print "$var = $_SERVER[$var]<BR>\n"; }
print qq|form Variables<BR>\n|;
foreach $var ( sort keys %$form ) { print "$var = $form->{$var}<BR>\n"; }

print "</BODY></HTML>\n";

myDBI->cleanup();
exit;
############################################################################
