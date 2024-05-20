#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use strict;
use warnings;

use CGI::Carp qw(fatalsToBrowser);
use myForm;
my $form = myForm->new();
my $filename = $form->{'filepath'};

my $q = CGI->new();
print $q->header;

use myConfig;
use X12::Parser;

my $ADMINDIR = myConfig->cfg('MIS');
my ($adminpath, $admindir) = $ADMINDIR =~ m/(.*\/)(.*)$/;
my $dirpath = qq|${ADMINDIR}/cf|;

# Create an X12 parser
my $parser = X12::Parser->new;
my %files_835_271 = (
                      "271", "271_004010X092.cf",
                      "835", "835_004010X091.cf",
                      "837", "837_004010X098.cf"
                    );

my $resp_File = $files_835_271{$form->{"Type"}};

# Parse the file
my $file;
open($file, $filename);
$parser->parse("handle"=>$file, "conf"=> "$dirpath/$resp_File");
while  (my $loop = $parser->get_next_loop) {
  my @loop = $parser->get_loop_segments;
  print $loop[0];
  print "<br>";
}



