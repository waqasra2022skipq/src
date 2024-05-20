use XML::LibXML;

my $parser = XML::LibXML->new();
my $doc = $parser->parse_file( shift @ARGV );

my $mathuri = 'http://www.w3.org/1998/Math/MathML';
my $root = $doc->getDocumentElement;
purge_nselems( $root );
print $doc->toString;

sub purge_nselems {
  my $elem = shift;
  return unless( ref( $elem ) =~ /Element/ );
  if( $elem->prefix ) {
    my $parent = $elem->parentNode;
    $parent->removeChild( $elem );
  } elsif( $elem->hasChildNodes ) {
    my @children = $elem->getChildnodes;
    foreach my $child ( @children ) {
      &amp;purge_nselems( $child );
    }
  }
}
