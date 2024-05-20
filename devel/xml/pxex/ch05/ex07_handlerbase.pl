use XML::Parser::PerlSAX;
use XML::Handler::Subs

#
# initialize the parser
#
use XML::Parser::PerlSAX;
my $parser = XML::Parser::PerlSAX->new( Handler => H1_grabber->new() );
$parser->parse( Source => {SystemId => shift @ARGV} );

## Handler object: H1_grabber
##
package H1_grabber;
use base( 'XML::Handler::Subs' );

sub new {
    my $type = shift;
    my $self = {@_};
    return bless( $self, $type );
}

#
# handle start of document
#
sub start_document {
  SUPER::start_document();
  print "Summary of file:\n";
}

#
# handle start of <h1>: output bracket as delineator
#
sub s_h1 {
  print "[";
}

#
# handle start of <h1>: output bracket as delineator
#
sub e_h1 {
  print "]\n";
}

#
# handle start of <h1>: output bracket as delineator
#
sub characters {
  my( $self, $props ) = @_;
  my $data = $props->{Data};
  print $data if( $self->in_element( h1 ));
}
