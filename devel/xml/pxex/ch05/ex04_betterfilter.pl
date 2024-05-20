# handle xml declaration
#
sub xml_decl {
    my( $self, $properties ) = @_;
    &output( "<?xml version=\"" . $properties->{'Version'} . "\"" );
    my $encoding = $properties->{'Encoding'};
    &output( " encoding=\"$encoding\"" ) if( $encoding );
    my $standalone = $properties->{'Standalone'};
    &output( " standalone=\"$standalone\"" ) if( $standalone );
    &output( "?>\n" );
}

#
# handle doctype declaration:
# try to duplicate the original
#
sub doctype_decl {
    my( $self, $properties ) = @_;
    &output( "\n<!DOCTYPE " . $properties->{'Name'} . "\n" );
    my $pubid = $properties->{'PublicId'};
    if( $pubid ) {
	&output( "  PUBLIC \"$pubid\"\n" );
	&output( "  \"" . $properties->{'SystemId'} . "\"\n" );
    } else {
	&output( "  SYSTEM \"" . $properties->{'SystemId'} . "\"\n" );
    }
    my $intset = $properties->{'Internal'};
    if( $intset ) {
	$in_intset = 1;
	&output( "[\n" );
    } else {
	&output( ">\n" );
    }
}

#
# handle entity declaration in internal subset:
# recreate the original declaration as it was
#
sub entity_decl {
    my( $self, $properties ) = @_;
    my $name = $properties->{'Name'};
    &output( "<!ENTITY $name " );
    my $pubid = $properties->{'PublicId'};
    my $sysid = $properties->{'SystemId'};
    if( $pubid ) {
	&output( "PUBLIC \"$pubid\" \"$sysid\"" );
    } elsif( $sysid ) {
	&output( "SYSTEM \"$sysid\"" );
    } else {
	&output( "\"" . $properties->{'Value'} . "\"" );
    }
    &output( ">\n" );
}
