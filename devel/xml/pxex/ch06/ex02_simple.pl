use XML::Simple;

my $simple = XML::Simple->new();             # initialize the object
my $tree = $simple->XMLin( './data.xml' );   # read, store document

# test access to the tree
print "The user prefers the font " . $tree->{ font }->{ name } . " at " .
    $tree->{ font }->{ size } . " points.\n";
