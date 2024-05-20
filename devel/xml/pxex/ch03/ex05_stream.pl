use XML::Parser;

# initialize the parser
my $parser = XML::Parser->new( Handlers => 
                                     {
                                      Start=>\&handle_start,
			              End=>\&handle_end,
                                     });
$parser->parsefile( shift @ARGV );

my @element_stack;		# remember which elements are open

# process a start-of-element event: print message about element
#
sub handle_start {
    my( $expat, $element, %attrs ) = @_;

    # ask the expat object about our position
    my $line = $expat->current_line;

    print "I see an $element element starting on line $line!\n";

    # remember this element and its starting position by pushing a
    # little hash onto the element stack
    push( @element_stack, { element=>$element, line=>$line });

    if( %attrs ) {
        print "It has these attributes:\n";
        while( my( $key, $value ) = each( %attrs )) {
            print "\t$key => $value\n";
	}
    }
}

# process an end-of-element event
#
sub handle_end {
    my( $expat, $element ) = @_;

    # We'll just pop from the element stack with blind faith that
    # we'll get the correct closing element, unlike what our
    # homebrewed well-formedness did, since XML::Parser will scream
    # bloody murder if any well-formedness errors creep in.
    my $element_record = pop( @element_stack );
    print "I see that $element element that started on line ",
          $$element_record{ line }, " is closing now.\n";
}
