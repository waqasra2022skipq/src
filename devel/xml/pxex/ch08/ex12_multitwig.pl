use XML::Twig;

my $twig = new XML::Twig( TwigRoots => { 'chapter/title' => \&output_title });
$twig->parsefile( shift @ARGV );

sub output_title {
  my( $tree, $elem ) = @_;
  print $elem->text, "\n";
}
