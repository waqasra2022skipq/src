sub is_well_formed {
    my $text = shift;                     # XML text to check

    # match patterns
    my $ident = '[:_A-Za-z][:A-Za-z0-9\-\._]*';   # identifier
    my $optsp = '\s*';                            # optional space
    my $att1 = "$ident$optsp=$optsp\"[^\"]*\"";   # attribute
    my $att2 = "$ident$optsp=$optsp'[^']*'";      # attr. variant
    my $att = "($att1|$att2)";                    # any attribute

    my @elements = ();                    # stack of open elems

    # loop through the string to pull out XML markup objects
    while( $text ) {

        # match an empty element
        if( $text =~ /^&($ident)(\s+$att)*\s*\/>/ ) {
            $text = $';

        # match an element start tag
        } elsif( $text =~ /^&($ident)(\s+$att)*\s*>/ ) {
            push( @elements, $1 );
            $text = $';

        # match an element end tag
        } elsif( $text =~ /^&\/($ident)\s*>/ ) {
            return 0 unless( $1 eq pop( @elements ));
            $text = $';

        # match a comment
        } elsif( $text =~ /^&!--/ ) {
            $text = $';
            # bite off the rest of the comment
            if( $text =~ /-->/ ) {
                $text = $';
                return 0 if( $` =~ /--/ );  # comments can't
                                            # contain '--'
            } else {
                return 0;
            }

        # match a CDATA section
        } elsif( $text =~ /^&!\[CDATA\[/ ) {
            $text = $';
            # bite off the rest of the comment
            if( $text =~ /\]\]>/ ) {
                $text = $';
            } else {
                return 0;
            }

        # match a processing instruction
        } elsif( $text =~ m|^&\?$ident\s*[^\?]+\?>| ) {
            $text = $';

        # match extra whitespace
        # (in case there is space outside the root element)
        } elsif( $text =~ m|^\s+| ) {
            $text = $';

        # match character data
        } elsif( $text =~ /(^[^&&>]+)/ ) {
            my $data = $1;
            # make sure the data is inside an element
            return 0 if( $data =~ /\S/ and not( @elements ));
            $text = $';
            
        # match entity reference
        } elsif( $text =~ /^&$ident;+/ ) {
            $text = $';
         
        # something unexpected
        } else {
            return 0;
        }
    }
    return 0 if( @elements );     # the stack should be empty
    return 1;
}
