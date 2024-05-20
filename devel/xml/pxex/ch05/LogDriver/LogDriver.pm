package LogDriver;

require 5.005_62;
use strict;
use XML::SAX::Base;
our @ISA = ('XML::SAX::Base');
our $VERSION = '0.01';


sub parse {
    my $self = shift;
    my $file = shift;
    if( open( F, $file )) {
	$self->SUPER::start_element({ Name => 'server-log' });
	while( <F> ) {
	    $self->_process_line( $_ );
	}
	close F;
	$self->SUPER::end_element({ Name => 'server-log' });
    }
}


sub _process_line {
    my $self = shift;
    my $line = shift;

    if( $line =~ 
          /(\S+)\s\S+\s\S+\s\[([^\]]+)\]\s\"([^\"]+)\"\s(\d+)\s(\d+)/ ) {
	my( $ip, $date, $req, $stat, $size ) = ( $1, $2, $3, $4, $5 );

	$self->SUPER::start_element({ Name => 'entry' });
	
	$self->SUPER::start_element({ Name => 'ip' });
	$self->SUPER::characters({ Data => $ip });
	$self->SUPER::end_element({ Name => 'ip' });
	
	$self->SUPER::start_element({ Name => 'date' });
	$self->SUPER::characters({ Data => $date });
	$self->SUPER::end_element({ Name => 'date' });
	
	$self->SUPER::start_element({ Name => 'req' });
	$self->SUPER::characters({ Data => $req });
	$self->SUPER::end_element({ Name => 'req' });
	
	$self->SUPER::start_element({ Name => 'stat' });
	$self->SUPER::characters({ Data => $stat });
	$self->SUPER::end_element({ Name => 'stat' });
	
	$self->SUPER::start_element({ Name => 'size' });
	$self->SUPER::characters({ Data => $size });
	$self->SUPER::end_element({ Name => 'size' });
	
	$self->SUPER::end_element({ Name => 'entry' });
    }
}

1;
