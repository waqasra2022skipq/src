#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use JSON::PP;
use myDBI;

my $cgi = CGI->new;
my $file_to_delete = $cgi->param('filepath');
my $response = {};

my $dbname = $cgi->param('dbname');
my $dbh = myDBI->dbconnect($dbname);

if ($file_to_delete) {
    # We also need to delete the entry from Database
    $sDelete = $dbh->prepare("DELETE FROM `ProviderEDocs` WHERE Path = ?");
    $sDelete->execute($file_to_delete);
    
    if (-e $file_to_delete && unlink $file_to_delete) {
        $response->{success} = "File $file_to_delete has been deleted.";
    } else {
        $response->{error} = "Failed to delete $file_to_delete: $!";
    }
} else {
    $response->{error} = "Missing file parameter.";
}


print $cgi->header('application/json');
print encode_json($response);