use XML::LibXSLT;
use XML::LibXML;

# the arguments for this command are stylesheet and source files
my( $style_file, @source_files ) = @ARGV;

# initialize the parser and XSLT processor
my $parser = XML::LibXML->new();
my $xslt = XML::LibXSLT->new();
my $stylesheet = $xslt->parse_stylesheet_file( $style_file );

# for each source file: parse, transform, print out result
foreach my $file ( @source_files ) {
  my $source_doc = $parser->parse_file( $source_file );
  my $result = $stylesheet->transform( $source_doc );
  print $stylesheet->output_string( $result );
}

