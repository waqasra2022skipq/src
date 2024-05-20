use XML::DOM;

process_file( shift @ARGV );

sub process_file {
    my $infile = shift;
    my $dom_parser = new XML::DOM::Parser;            # create a parser object
    my $doc = $dom_parser->parsefile( $infile );      # make it parse a file
    add_links( $doc );                                # perform our changes
    print $doc->toString;                             # output the tree again
    $doc->dispose;                                    # clean up memory
}

sub add_links {
    my $doc = shift;                                  

    # find all the <p> elements
    my $paras = $doc->getElementsByTagName( "p" );
    for( my $i = 0; $i < $paras->getLength; $i++ ) {
        my $para = $paras->item( $i );

	# for each child of a <p>, if it is a text node, process it
        my @children = $para->getChildNodes;
        foreach my $node ( @children ) {
	    fix_text( $node ) if( $node->getNodeType eq TEXT_NODE );
        }
    }
}

sub fix_text {
    my $node = shift;
    my $text = $node->getNodeValue;
    if( $text =~ /(monkeys)/i ) {

	# split the text node into 2 text nodes around the monkey word
	my( $pre, $orig, $post ) = ( $`, $1, $' );
	my $tnode = $node->getOwnerDocument->createTextNode( $pre );
	$node->getParentNode->insertBefore( $tnode, $node );
	$node->setNodeValue( $post );

	# insert an <a> element between the two nodes
	my $link = $node->getOwnerDocument->createElement( 'a' );
	$link->setAttribute( 'href', 'http://www.monkeystuff.com/' );
	$tnode = $node->getOwnerDocument->createTextNode( $orig );
	$link->appendChild( $tnode );
	$node->getParentNode->insertBefore( $link, $node );

	# recurse on the rest of the text node 
	# in case the word appears again
	fix_text( $node );
    }
}
