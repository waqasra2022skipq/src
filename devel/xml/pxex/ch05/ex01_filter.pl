# initialize the parser
#
use XML::Parser::PerlSAX;
my $parser = XML::Parser::PerlSAX->new( Handler => MyHandler->new() );
if( my $file = shift @ARGV ) {
    $parser->parse( Source => {SystemId => $file} );
} else {
    my $input = "";
    while( <STDIN> ) { $input .= $_; }
    $parser->parse( Source => {String => $input} );
}
exit;

#
# global variables
#
my @element_stack;                # remembers element names
my $in_intset;                    # flag: are we in the internal subset?

###
### Document Handler Package
###
package MyHandler;

#
# initialize the handler package
#
sub new {
    my $type = shift;
    return bless {}, $type;
}

#
# handle a start-of-element event: output start tag and attributes
#
sub start_element {
    my( $self, $properties ) = @_;
    # note: the hash table %{$properties} will lose attribute order

    # close internal subset if still open
    &output( "]>\n" ) if( $in_intset );
    $in_intset = 0;

    # remember the name by pushing onto the stack
    push( @element_stack, $properties->{'Name'} );

    # output the tag and attributes UNLESS it's a <literal>
    # inside a <programlisting>
    unless( &stack_top( 'literal' ) and
	    &stack_contains( 'programlisting' )) {
	&output( "<" . $properties->{'Name'} );
	my %attributes = %{$properties->{'Attributes'}};
	foreach( keys( %attributes )) {
	    &output( " $_=\"" . $attributes{$_} . "\"" );
	}
	&output( ">" );
    }
} 

#
# handle an end-of-element event: output end tag UNLESS it's from a
# <literal> inside a <programlisting>
#
sub end_element {
    my( $self, $properties ) = @_;
    &output( "</" . $properties->{'Name'} . ">" )
 	unless( &stack_top( 'literal' ) and
		&stack_contains( 'programlisting' ));
    pop( @element_stack );
}

#
# handle a character data event
#
sub characters {
    my( $self, $properties ) = @_;
    # parser unfortunately resolves some character entities for us,
    # so we need to replace them with entity references again
    my $data = $properties->{'Data'};
    $data =~ s/\&/\&amp;/;
    $data =~ s/</\&lt;/;
    $data =~ s/>/\&gt;/;
    &output( $data );
}

#
# handle a comment event: turn into a <comment> element
#
sub comment {
    my( $self, $properties ) = @_;
    &output( "<comment>" . $properties->{'Data'} . "</comment>" );
}

#
# handle a PI event: delete it
#
sub processing_instruction {
  # do nothing!
}

#
# handle internal entity reference (we don't want them resolved)
#
sub entity_reference {
    my( $self, $properties ) = @_;
    &output( "\&" . $properties->{'Name'} . ";" );
}

sub stack_top {
    my $guess = shift;
    return $element_stack[ $#element_stack ] eq $guess;
}

sub stack_contains {
    my $guess = shift;
    foreach( @element_stack ) {
	return 1 if( $_ eq $guess );
    }
    return 0;
}

sub output {
    my $string = shift;
    print $string;
}

1;
