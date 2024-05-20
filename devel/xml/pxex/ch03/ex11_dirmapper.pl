use XML::Writer;
my $wr = new XML::Writer( DATA_MODE => 'true', DATA_INDENT => 2 );
&as_xml( shift @ARGV );
$wr->end;

# recursively map directory information into XML
#
sub as_xml {
    my $path = shift;
    return unless( -e $path );

    # if this is a directory, create an element and
    # stuff it full of items
    if( -d $path ) {
        $wr->startTag( 'directory', name => $path );

        # Load the names of all things in this
        # directory into an array
        my @contents = ();
        opendir( DIR, $path );
        while( my $item = readdir( DIR )) {
            next if( $item eq '.' or $item eq '..' );
            push( @contents, $item );
        }
        closedir( DIR );

        # recurse on items in the directory
        foreach my $item ( @contents ) {
            &as_xml( "$path/$item" );
        }

        $wr->endTag( 'directory' );

    # We'll lazily call anything that's not a directory a file.
    } else {
        $wr->emptyTag( 'file', name => $path );
    }
}
