package XML::ComicsML;

# A helper module for parsing and generating ComicsML documents.

use XML::LibXML;
use base qw(XML::LibXML);

# PARSING

# We catch the output of all XML::LibXML parsing methods in our hot
# little hands, then proceed to rebless selected nodes into our own
# little clasees

sub parse_file {
  # Parse as usual, but then rebless the root element and return it.
  my $self = shift;
  my $doc = $self->SUPER::parse_file(@_);
  my $root = $doc->documentElement;
  return $self->rebless($root);
}

sub parse_string {
  # Parse as usual, but then rebless the root element and return it.
  my $self = shift;
  my $doc = $self->SUPER::parse_string(@_);
  my $root = $doc->documentElement;
  return $self->rebless($root);
}

sub rebless {
  # Accept  some kind of XML::LibXML::Node (or a subclass
  # thereof) and, based on its name, rebless it into one of
  # our ComicsML classes.
  my $self = shift;
  my ($node) = @_;
  # Define a has of interesting element types. (hash for easier searching.)
  my %interesting_elements = (comic=>1,
			      person=>1,
			      panel=>1,
			      panel-desc=>1,
			      line=>1,
			      strip=>1,
			     );
  # Toss back this node unless it's an Element, and Interesting. Else,
  # carry on.
    my $name = $node->getName;
    return $node unless ( (ref($node) eq 'XML::LibXML::Element') and (exists($interesting_elements{$name})) );
    
    # It is an interesting element! Figure out what class it gets, and rebless it.
    my $class_name = $self->element2class($name);
    bless ($node, $class_name);
  return $node;
}

sub element2class {
  # Munge an XML element name into something resembling a class name.
  my $self = shift;
  my ($class_name) = @_;
  $class_name = ucfirst($class_name);
  $class_name =~ s/-(.?)/uc($1)/e;
  $class_name = "XML::ComicsML::$class_name";
}

package XML::ComicsML::Element;

# This is an abstract class for all ComicsML Node types.
use base qw(XML::LibXML::Element);
use vars qw($AUTOLOAD @elements @attributes);

sub AUTOLOAD {
  my $self = shift;
  my $name = $AUTOLOAD;
  $name =~ s/^.*::(.*)$/$1/;
  my @elements = $self->elements;
  my @attributes = $self->attributes;
  if (grep (/^$name$/, @elements)) {
    # This is an element accessor.
    if (my $new_value = $_[0]) {
      # Set a value, overwriting that of any current element of this type.
      my $new_node = XML::LibXML::Element->new($name);
      my $new_text = XML::LibXML::Text->new($new_value);
      $new_node->appendChild($new_text);
      my @kids = $new_node->childNodes;
      if (my ($existing_node) = $self->findnodes("./$name")) {
	$self->replaceChild($new_node, $existing_node);
      } else {
	$self->appendChild($new_node);
      }
    }
    # Return the named child's value.
    if (my ($existing_node) = $self->findnodes("./$name")) {
      return $existing_node->firstChild->getData;
    } else {
      return '';
    }
  } elsif (grep (/^$name$/, @attributes)) {
    # This is an attribute accessor.
    if (my $new_value = $_[0]) {
      # Set a value for this attribute.
      $self->setAttribute($name, $new_value);
    }
    # Return the names attribute's value.
    return $self->getAttribute($name) || '';
    # These next two could use some error-checking.
  } elsif ($name =~ /^add_(.*)/) {
    my $class_to_add = XML::ComicsML->element2class($1);
    my $object = $class_to_add->new;
    $self->appendChild($object);
    return $object;
  } elsif ($name =~ /^remove_(.*)/) {
    my ($kid) = @_;
    $self->removeChild($kid);
    return $kid;
  }

}

# Stubs
	 
sub elements {
  return ();
}

sub attributes {
  return ();
}

package XML::ComicsML::Comic;
use base qw(XML::ComicsML::Element);

sub elements {
  return qw(version title icon description url);
}

sub new {
  my $class = shift;
  return $class->SUPER::new('comic');
}

sub strips {
  # Return a list of all strip objects that are children of this comic.
  my $self = shift;
  return map {XML::ComicsML->rebless($_)}  $self->findnodes("./strip");
}

sub get_strip {
  # Given an ID, fetch a strip with that 'id' attribute.
  my $self = shift;
  my ($id) = @_;
  unless ($id) {
    warn "get_strip needs a strip id as an argument!";
    return;
  }
  my (@strips) = $self->findnodes("./strip[attribute::id='$id']");
  if (@strips > 1) {
    warn "Uh oh, there is more than one strip with an id of $id.\n";
  }
  return XML::ComicsML->rebless($strips[0]);
}
