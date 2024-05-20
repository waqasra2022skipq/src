#!/usr/bin/perl

use warnings;
use strict;

use XML::Generator::DBI;
use XML::Handler::YAWriter;

use DBI;

my $ya = XML::Handler::YAWriter->new(AsFile => "-");
my $dbh = DBI->connect("dbi:mysql:dbname=test", "jmac", "");
my $generator = XML::Generator::DBI->new(
                               Handler => $ya,
                               dbh => $dbh
                               );
my $sql = "select * from cds";

$generator->execute($sql);
