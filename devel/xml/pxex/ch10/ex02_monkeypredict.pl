#!/usr/bin/perl

# This program takes an action specified on the command line, and
# applies it to every monkey listed in a monkey-list XML document
# (whose filename is also supplied on the command line)

use warnings;
use strict;

use XML::LibXML;
use XML::MonkeyML;

my ($filename, $action) = @ARGV;

unless ($filename and $action) {
  die "Usage: $0 monkey-list-file action\n";
}

my $parser = XML::LibXML->new;
my $doc = $parser->parse_file($filename);

# Get all of the 
my @monkey_nodes = $parser->documentElement->findNodes("//monkey/description/mm:monkey");

foreach (@monkey_nodes) {
  my $monkeyml = XML::MonkeyML->parse_string($_->toString);
  my $name = $monkeyml->name . " the " . $monkeyml->color . " monkey";
  print "$name would react in the following fashion:\n";
  # The magic MonkeyML 'action' object method takes an English
  # description of an action performed on this monkey, and returns a
  # phrase describing the monkey's reaction.
  print $monkeyml->action($action); print "\n";
}
