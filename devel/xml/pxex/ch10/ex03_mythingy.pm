package XML::MyThingy;

use strict; use warnings;
use XML::SomeSortOfParser;

sub new {
  # Ye Olde Constructor
  my $invocant = shift;
  my $self = {};
  if (ref($invocant)) {
    bless ($self, ref($invocant));
  } else {
    bless ($self, $invocant);
  }
  # Now we make an XML parser...
  my $parser = XML::SomeSortOfParser->new or die "Oh no, I couldn't
make an XML parser. How very sad.";
  # ...and stick it on this object, for later reference.
  $self->{xml} = $parser;
  return $self;
}

sub parse_file {
  # We'll just pass on the user's request to our parser object (which
  # just happens to have a method named parse_file)...
  my $self = shift;
  my $result = $self->{xml}->parse_file;
  # What happens now depends on whatever a XML::SomeSortOfParser
  # object does when it parses a file. Let's say it modifies itself and
  # returns a success code, so we'll just keep hold of the now-modified
  # object under this object's 'xml' key, and return the code.
  return $result;
}
