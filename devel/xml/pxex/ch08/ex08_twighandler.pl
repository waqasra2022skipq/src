use XML::Twig;

# buffers for holding text
my $catbuf = '';
my $itembuf = '';

# initialize parser with handlers for node processing
my $twig = new XML::Twig( TwigHandlers => { 
                             "/inventory/category"    => \&category,
			     "name[\@style='latin']"  => \&latin_name,
			     "name[\@style='common']" => \&common_name,
			     "category/item"          => \&item,
					  });

# parse, handling nodes on the way
$twig->parsefile( shift @ARGV );

# handle a category element
sub category {
  my( $tree, $elem ) = @_;
  print "CATEGORY: ", $elem->att( 'type' ), "\n\n", $catbuf;
  $catbuf = '';
}

# handle an item element
sub item {
  my( $tree, $elem ) = @_;
  $catbuf .= "Item: " . $elem->att( 'id' ) . "\n" . $itembuf . "\n";
  $itembuf = '';
}

# handle a latin name
sub latin_name {
  my( $tree, $elem ) = @_;
  $itembuf .= "Latin name: " . $elem->text . "\n";
}

# handle a common name
sub common_name {
  my( $tree, $elem ) = @_;
  $itembuf .= "Common name: " . $elem->text . "\n";
}
