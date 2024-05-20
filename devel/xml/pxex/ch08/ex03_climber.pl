use XML::LibXML;

my $dom = new XML::LibXML;
my $doc = $dom->parse_file( shift @ARGV );
my $docelem = $doc->getDocumentElement;
$docelem->iterator( \&find_PI );

sub find_PI {
  my $node = shift;
  return unless( $node->nodeType == &XML_PI_NODE );
  print "Found processing instruction: ", $node->nodeName, "\n";
}
