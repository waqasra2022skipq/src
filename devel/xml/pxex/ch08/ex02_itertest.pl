use XML::DOM;

# initialize parser and iterator
my $dom_parser = new XML::DOM::Parser;
my $doc = $dom_parser->parsefile( shift @ARGV );
my $iter = new XML::DOMIterator;
$iter->reset( $doc->getDocumentElement );

# print all the nodes from start to end of a document
print "\nFORWARDS:\n";
my $node = $iter->node;
my $last;
while( $node ) {
  describe( $node );
  $last = $node;
  $node = $iter->forward;
}

# print all the nodes from end to start of a document
print "\nBACKWARDS:\n";
$iter->reset( $last );
describe( $iter->node );
while( $iter->backward ) {
  describe( $iter->node );
}

# output information about the node
#
sub describe {
  my $node = shift;
  if( ref($node) =~ /Element/ ) {
    print 'element: ', $node->getNodeName, "\n";
  } elsif( ref($node) =~ /Text/ ) {
    print "other node: \"", $node->getNodeValue, "\"\n";
  }
}
