sub get_bgcolor {
    my @keys = $doc->getElementsByTagName( 'key' );
    foreach my $key ( @keys ) {
        if( $key->getFirstChild->getData eq 'BGColor' ) {
            return $key->getNextSibling->getData;
        }
    }
    return undef;
}
