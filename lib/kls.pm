package kls;
our $HANDLES;
our @LINES;
############################################################################
sub readFILE 
{
  my ($self,$filepath,$delm) = @_;
  my ($directory,$filename) = $filepath =~ m#((?:[^/]*/)*)(.*)#;
#print qq|path=${filepath}\n|;
#print qq|dir=${directory}, name=${filename}\n|;
  my $fh;
  if ( $HANDLES->{$filename}->{'HANDLE'} )
  {
    $fh = $HANDLES->{$filename}->{'HANDLE'}; 
#print qq|exists: fh=${fh}\n|;
  }
  else
  {
    if ( !open($fh, "<", "${filepath}") )
    { myDBI->dberror("readFILE: Can't open ${filename} ($!)."); }
    $HANDLES->{$filename}->{CONNECT} = 1;
    $HANDLES->{$filename}->{HANDLE} = $fh;
#print qq|open: fh=${fh}\n|;
  }
  my $line = <$fh>;
  foreach my $str ( split($delm,$line) ) { push(@LINES,$str); }
  my $text = shift @LINES;
#print qq|return: line=${line}\n|;
  return($text);
}
############################################################################
1;
