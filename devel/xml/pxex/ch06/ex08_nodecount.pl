use XML::Parser;
use XML::Parser::Grove;
use XML::Grove;

my $parser = XML::Parser->new( Style => 'grove', NoExpand => '1' );
my $grove = $parser->parsefile( shift @ARGV );

# tabulate elements and other nodes
my %dist;
foreach( @{$grove->contents} ) {
  tabulate( $_, \%dist );
}
print "\nNODES:\n\n";
foreach( sort keys %dist ) {
  print "$_: " . $dist{$_} . "\n";
}

# given a node and a table, find out what the node is, add to the count,
# and recurse if necessary
#
sub tabulate {
  my( $node, $table ) = @_;

  my $type = ref( $node );
  if( $type eq 'XML::Grove::Element' ) {
    $table->{ 'element' }++;
    $table->{ 'element (' . $node->name . ')' }++;
    foreach( keys %{$node->attributes} ) {
      $table->{ "attribute ($_)" }++;
    }
    foreach( @{$node->contents} ) {
      tabulate( $_, $table );
    }

  } elsif( $type eq 'XML::Grove::Entity' ) {
    $table->{ 'entity-ref (' . $node->name . ')' }++;

  } elsif( $type eq 'XML::Grove::PI' ) {
    $table->{ 'PI (' . $node->target . ')' }++;

  } elsif( $type eq 'XML::Grove::Comment' ) {
    $table->{ 'comment' }++;

  } else {
    $table->{ 'text-node' }++
  }
}
