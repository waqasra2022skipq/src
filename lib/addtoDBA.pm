
# set xml textvalue from multiple values in field; loop through field chr(253); xref to xtable
sub setTextxrefMV
{
  my ($self,$form,$xtable,$multivalues,$cat,$tag,$tab,$flds) = @_;
  my ($xml,$text,$spc,$dlm) = ('','','','; ');;
  foreach my $value ( split(chr(253),$multivalues) )
  {
    $text .= qq|${spc}| . DBA->getxref($form,$xtable,$value,$flds);
    $spc = $dlm;
  }
  $xml = qq|${tab}<${tag}>|.DBA->subxml($text).qq|</${tag}>\n|;
  return($xml);
}
# set xml textvalue from multiple fields in record; loop through xtabel for field=Value
sub setTextxrefMF
{
  my ($self,$form,$xtable,$r,$cat,$tag,$tab) = @_;
#warn qq|xtable=$xtable, dlm=$dlm, cat=$cat, tag=$tag, tab=$tab\n|; 
  my ($xml,$spc,$vals,$dlm) = ('','','','; ');
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my $sx = $cdbh->prepare("select * from ${xtable} order by Num,Descr");
  $sx->execute();
  while ( $rx = $sx->fetchrow_hashref )
  { if ( $rx->{'theValue'} eq $r->{$rx->{'theField'}} ) { $vals .= qq|${spc}$rx->{'Descr'}|; $spc = $dlm; } }
##warn qq|Descr=$rx->{'Descr'}, theValue=$rx->{'theValue'}, theField=$rx->{'theField'}, Field=$r->{$rx->{'theField'}}\n|; 
#warn qq|vals=$vals= cat=$cat=\n|; 
  $vals .= qq| ${cat}| unless ( $cat eq '' );
#warn qq|vals=$vals= \n|; 
  $xml = $tag eq '' ? $vals : qq|${tab}<${tag}>|.DBA->subxml(${vals}).qq|</${tag}>\n|;
  return($xml);
}
