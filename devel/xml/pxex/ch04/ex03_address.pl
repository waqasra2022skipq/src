# initialize the parser with references to handler routines
#
use XML::Parser;
my $parser = XML::Parser->new( Handlers => {
    Init =>    \&handle_doc_start,
    Final =>   \&handle_doc_end,
    Start =>   \&handle_elem_start,
    End =>     \&handle_elem_end,
    Char =>    \&handle_char_data,
});

#
# globals
#
my $record;       # points to a hash of element contents
my $context;      # name of current element
my %records;      # set of address entries

#
# read in the data and run the parser on it
#
my $file = shift @ARGV;
if( $file ) {
    $parser->parsefile( $file );
} else {
    my $input = "";
    while( <STDIN> ) { $input .= $_; }
    $parser->parse( $input );
}
exit;


###
### Handlers
###

#
# As processing starts, output the beginning of an HTML file.
# 
sub handle_doc_start {
    print "<html><head><title>addresses</title></head>\n";
    print "<body><h1>addresses</h1>\n";
}

#
# save element name and attributes
#
sub handle_elem_start {
    my( $expat, $name, %atts ) = @_;
    $context = $name;
    $record = {} if( $name eq 'entry' );
} 

#
# collect character data into the recent element's buffer
#
sub handle_char_data {
    my( $expat, $text ) = @_;
    $record->{ $context } .= $text;
}

#
# if this is an <entry>, collect all the data into a record
#
sub handle_elem_end {
    my( $expat, $name ) = @_;
    return unless( $name eq 'entry' );
    my $fullname = $record->{'last'} . $record->{'first'};
    $records{ $fullname } = $record;
}

#
# Output the close of the file at the end of processing.
#
sub handle_doc_end {
    print "<table border='1'>\n";
    print "<tr><th>name</th><th>phone</th><th>address</th></tr>\n";
    foreach( sort( keys( %records ))) {
	my $key = $_;
	print "<tr><td>" . $records{ $key }->{ 'first' } . ' ';
	print $records{ $key }->{ 'last' } . "</td><td>";
	print $records{ $key }->{ 'phone' } . "</td><td>";
	print $records{ $key }->{ 'street' } . ', ';
	print $records{ $key }->{ 'city' } . ', ';
	print $records{ $key }->{ 'state' } . ' ';
	print $records{ $key }->{ 'zip' } . "</td></tr>\n";
    }
    print "</table>\n</div>\n</body></html>\n";
}
