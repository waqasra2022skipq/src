use XML::Parser;

# initialize parser and read the file
$parser = new XML::Parser( Style => 'Tree' );
my $tree = $parser->parsefile( shift @ARGV );

# serialize the structure
use Data::Dumper;
print Dumper( $tree );
