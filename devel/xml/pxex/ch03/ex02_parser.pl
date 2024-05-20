use XML::Parser;

my $xmlfile = shift @ARGV;              # the file to parse

# initialize parser object and parse the string
my $parser = XML::Parser->new( ErrorContext => 2 );
eval { $parser->parsefile( $xmlfile ); };

# report any error that stopped parsing, or announce success
if( $@ ) {
    $@ =~ s/at \/.*?$//s;               # remove module line number
    print STDERR "\nERROR in '$file':\n$@\n";
} else {
    print STDERR "'$file' is well-formed\n";
}
