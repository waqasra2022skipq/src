#!/usr/bin/perl

use warnings;
use strict;
use CGI qw(:standard);
use XML::LibXML;

my $parser = XML::XPath;
my $doc = $parser->parse_file('monkeys.xml');

print header;
print start_html("My Pet Monkeys");
print h1("My Pet Monkeys");
print p("I have the following monkeys in my house:");
print "<ul>\n";
foreach my $name_node ($doc->documentElement->findnodes("//mm:name")) {
 print "<li>" . $name_node->firstChild->getData ."</li>\n";
}
print end_html;
