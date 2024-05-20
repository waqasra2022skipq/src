use XML::Parser;
use XML::SimpleObject;

# parse the data file and build a tree object
my $file = shift @ARGV;
my $parser = XML::Parser->new( ErrorContext => 2, Style => "Tree" );
my $tree = XML::SimpleObject->new( $parser->parsefile( $file ));

# output a text description
print "My ancestry starts with ";
begat( $tree->child( 'ancestry' )->child( 'ancestor' ), '' );

# describe a generation of ancestry
sub begat {
    my( $anc, $indent ) = @_;

    # output the ancestor's name
    print $indent . $anc->child( 'name' )->value;

    # if there are children, recurse over them
    if( $anc->child( 'children' ) and $anc->child( 'children' )->children ) {
	print " who begat...\n";
	my @children = $anc->child( 'children' )->children;
	foreach my $child ( @children ) {
	    begat( $child, $indent . '   ' );
	}
    } else {
	print "\n";
    }
}
