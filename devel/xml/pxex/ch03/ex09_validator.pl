use XML::LibXML;
use IO::Handle;

# initialize the parser
my $parser = new XML::LibXML;

# open a filehandle and parse
my $fh = new IO::Handle;
if( $fh->fdopen( fileno( STDIN ), "r" )) {
    my $doc = $parser->parse_fh( $fh );
    if( $doc and $doc->is_valid ) {
        print "Yup, it's valid.\n";
    } else {
        print "Yikes! Validity error.\n";
    }
    $fh->close;
}
