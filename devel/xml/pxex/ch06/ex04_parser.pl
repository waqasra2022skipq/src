# initialize parser and read the file
use XML::Parser;
$parser = new XML::Parser( Style => 'Tree' );
my $tree = $parser->parsefile( shift @ARGV );

# dump the structure
use Data::Dumper;
print Dumper( $tree );
