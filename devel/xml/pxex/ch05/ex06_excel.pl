#!/usr/bin/perl -w

use XML::SAXDriver::Excel;

# get the file name to process
die( "Must specify an input file" ) unless( @ARGV );
my $file = shift @ARGV;
print "Parsing $file...\n";

# initialize the parser
my $handler = new Excel_SAX_Handler;
my %props = ( Source => { SystemId => $file },
              Handler => $handler );
my $driver = XML::SAXDriver::Excel->new( %props );

# start parsing
$driver->parse( %props );

# The handler package we define to print out the XML
# as we receive SAX events.
package Excel_SAX_Handler;

# initialize the package
sub new {
    my $type = shift;
    my $self = {@_};
    return bless( $self, $type );
}

# create the outermost element
sub start_document {
    print "<doc>\n";
}

# end the document element
sub end_document {
    print "</doc>\n";
}

# handle any character data

sub characters {
    my( $self, $properties ) = @_;
    my $data = $properties->{'Data'};
    print $data;
}

# start a new element, outputting the start tag
sub start_element {
    my( $self, $properties ) = @_;
    my $name = $properties->{'Name'};
    print "<$name>";
}

# end the new element
sub end_element {
    my( $self, $properties ) = @_;
    my $name = $properties->{'Name'};
    print "</$name>";
}

1;
