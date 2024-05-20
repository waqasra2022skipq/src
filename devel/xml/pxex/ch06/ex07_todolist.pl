use XML::TreeBuilder;
use XML::Element;
use Getopt::Std;

# command line options
# -i         immediate
# -l         long-term
#
my %opts;
getopts( 'il', \%opts );

# initialize tree
my $data = 'data.xml';
my $tree;

# if file exists, parse it and build the tree
if( -r $data ) {
    $tree = XML::TreeBuilder->new();
    $tree->parse_file($data);

# otherwise, create a new tree from scratch
} else {
    print "Creating new data file.\n";
    my @now = localtime;
    my $date = $now[4] . '/' . $now[3];
    $tree = XML::Element->new( 'todo-list', 'date' => $date );
    $tree->push_content( XML::Element->new( 'immediate' ));
    $tree->push_content( XML::Element->new( 'long-term' ));
}

# add new entry and update file
if( %opts ) {
    my $item = XML::Element->new( 'item' );
    $item->push_content( shift @ARGV );
    my $place;
    if( $opts{ 'i' }) {
	$place = $tree->find_by_tag_name( 'immediate' );
    } elsif( $opts{ 'l' }) {
	$place = $tree->find_by_tag_name( 'long-term' );
    }
    $place->push_content( $item );
}
open( F, ">$data" ) or die( "Couldn't update schedule" );
print F $tree->as_XML;
close F;

# output schedule
print "To-do list for " . $tree->attr_get_i( 'date' ) . ":\n";
print "\nDo right away:\n";
my $immediate = $tree->find_by_tag_name( 'immediate' );
my $count = 1;
foreach my $item ( $immediate->find_by_tag_name( 'item' )) {
    print $count++ . '. ' . $item->as_text . "\n";
}
print "\nDo whenever:\n";
my $longterm = $tree->find_by_tag_name( 'long-term' );
$count = 1;
foreach my $item ( $longterm->find_by_tag_name( 'item' )) {
    print $count++ . '. ' . $item->as_text . "\n";
}
