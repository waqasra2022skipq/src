use XML::Twig;

# initalize the twig, parse, and output the revised twig
my $twig = new XML::Twig( TwigHandlers => { chapter => \&process_chapter });
$twig->parsefile( shift @ARGV );
$twig->print;

# handler for chapter elements: process and then flush up the chapter
sub process_chapter {
  my( $tree, $elem ) = @_;
  &process_element( $elem );
  $tree->flush_up_to( $elem );  # comment out this line to waste memory
}

# append 'foo' to the name of an element
sub process_element {
  my $elem = shift;
  $elem->set_gi( $elem->gi . 'foo' );
  my @children = $elem->children;
  foreach my $child ( @children ) {
    next if( $child->gi eq '#PCDATA' );
    &process_element( $child );
  }
}
