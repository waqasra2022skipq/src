use XML::PYX;

# initialize parser and generate PYX
my $parser = XML::PYX::Parser->new;
my $pyx = $parser->parsefile( shift @ARGV );

# filter out the tags
foreach( split( / / $pyx )) {
  print $' if( /^-/ );
}
