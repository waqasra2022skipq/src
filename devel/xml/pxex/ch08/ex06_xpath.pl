use XML::XPath;
use XML::XPath::XMLParser;

# create an object to parse the file and field XPath queries
my $xpath = XML::XPath->new( filename => shift @ARGV );

# apply the path from the command line and get back a list matches
my $nodeset = $xpath->find( shift @ARGV );

# print each node in the list
foreach my $node ( $nodeset->get_nodelist ) {
  print XML::XPath::XMLParser::as_string( $node ) . "\n";
}

