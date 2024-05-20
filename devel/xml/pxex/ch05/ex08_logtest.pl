#!/usr/bin/perl -w

use XML::SAX::ParserFactory;
use LogDriver;
my $handler = new MyHandler;
my $parser = XML::SAX::ParserFactory->parser( Handler => $handler );
$parser->parse( shift @ARGV );


package MyHandler;

# initialize object with options
#
sub new {
    my $class = shift;
    my $self = {@_};
    return bless( $self, $class );
}


sub start_element {
    my $self = shift;
    my $data = shift;
    print "<", $data->{Name}, ">";
    print "\n" if( $data->{Name} eq 'entry' );
    print "\n" if( $data->{Name} eq 'server-log' );
}

sub end_element {
    my $self = shift;
    my $data = shift;
    print "<", $data->{Name}, ">\n";
}

sub characters {
    my $self = shift;
    my $data = shift;
    print $data->{Data};
}


