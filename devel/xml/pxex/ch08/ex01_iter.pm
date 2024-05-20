package XML::DOMIterator;

sub new {
  my $class = shift;
  my $self = {@_};
  $self->{ Node } = undef;
  return bless( $self, $class );
}

# move forward one node in the tree
#
sub forward {
  my $self = shift;

  # try to go down to the next level
  if( $self->is_element and
      $self->{ Node }->getFirstChild ) {
    $self->{ Node } = $self->{ Node }->getFirstChild;

  # try to go to the next sibling, or an acestor's sibling
  } else {
    while( $self->{ Node }) {
      if( $self->{ Node }->getNextSibling ) {
	$self->{ Node } = $self->{ Node }->getNextSibling;
	return $self->{ Node };
      }
      $self->{ Node } = $self->{ Node }->getParentNode;
    }
  }
}

# move backward one node in the tree
#
sub backward {
  my $self = shift;

  # go to the previous sibling and descend to the last node in its tree
  if( $self->{ Node }->getPreviousSibling ) {
    $self->{ Node } = $self->{ Node }->getPreviousSibling;
    while( $self->{ Node }->getLastChild ) {
      $self->{ Node } = $self->{ Node }->getLastChild;
    }

  # go up
  } else {
    $self->{ Node } = $self->{ Node }->getParentNode;
  }
  return $self->{ Node };
}

# return a reference to the current node
#
sub node {
  my $self = shift;
  return $self->{ Node };
}

# set the current node
#
sub reset {
  my( $self, $node ) = @_;
  $self->{ Node } = $node;
}

# test if current node is an element
#
sub is_element {
  my $self = shift;
  return( $self->{ Node }->getNodeType == 1 );
}
