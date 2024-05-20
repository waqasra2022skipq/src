package PopUp;
use DBA;
############################################################################
sub makeSelect
{
  my ($self,$list,$num) = @_;
  my $SelStmt = '';
  my @names = $num ? sort {$a <=> $b} keys %{$list}
                   : sort {lc($a) cmp lc($b)} keys %{$list};
#warn qq|makeSelect: num=${num}\n|;
  foreach my $name ( @names )
  {
#warn qq|makeSelect: name=${name}\n|;
    my $val = $list->{$name}->{val};
#warn qq|makeSelect: val=${val}\n|;
    my $match = $list->{$name}->{match};
#warn qq|makeSelect: match=${match}\n|;
    if ( $match eq '' )
    { $SelStmt .= qq|<OPTION VALUE="$val" >$name\n|; }
    else
    { $SelStmt .= qq|<OPTION SELECTED VALUE="$val" >$name\n|; }
#warn qq|makeSelect: SelStmt=${SelStmt}\n|;
  }
  return($SelStmt);
}
sub matchSelect
{
  my ($self,$values,$key) = @_;
  foreach my $val ( split(chr(253),$values) )
  { return($val) if ( $val eq $key ); }
  return('');
}
# change unMatched to not select if not 'table' given?? so MySQL does not blow out...
#   table is null  my $unSel = $self->unMatched($form,$SelectedIDs,$found,'table??');
sub unMatched
{
  my ($self,$form,$values,$found,$table,$flds) = @_;
#warn "PopUp-unMatched: values=${values}, table=${table}\n";
  my $SelStmt = '';
  if ( $values eq '' )
  { $SelStmt .= qq|<OPTION SELECTED VALUE="" >unselected\n|; }
  else
  {
    $SelStmt .= qq|<OPTION VALUE="" >unselected\n|;
    foreach my $key ( split(chr(253),$values) )
    {
#warn "key=$key, found=$found->{$key}\n";
      unless ( $found->{$key} )
      {
        my $dbh = DBA->checkDBH($form,$table);
        my $s = $dbh->prepare("select * from ${table} where ID='${key}'");
        $s->execute() || $form->dberror("unMatched: select $table ID=$key");
        my $cnt = $s->rows;
        my $r = $s->fetchrow_hashref;
        my ($desc,$dlm) = ('','');
        foreach my $fld ( split(' ',$flds) )
        { $desc .= $dlm.$r->{$fld}; $dlm=' | '; }
        my $add = $cnt ? $r->{Active} ? '' : ' (expired}' : $key.' (not in list)';
        $SelStmt .= qq|<OPTION SELECTED VALUE="${key}" >${desc}${add}\n|;
        $s->finish();
      }
    }
  }
  return($SelStmt);
}
sub selHL7
{
  my ($self,$form,$SelectedIDs,$Tag) = @_;
#warn qq|selHL7: IDs=$SelectedIDs, Tag=$Tag\n|;
  my $items = ();
  my $found = ();
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
#warn "select * from xHL7 where Tag='${Tag}' and Popup=1\n";
  my $s = $cdbh->prepare("select * from xHL7 where Tag='${Tag}' and Popup=1");
  $s->execute() || $form->dberror("selxHL7: select xHL7 Tag=${Tag}");
  while ( my $r = $s->fetchrow_hashref )
  {
    my $name = $r->{'ConceptName'};
    my $val = $r->{'ConceptCode'};
    my $match = PopUp->matchSelect($SelectedIDs,$val);
#warn qq|selHL7: id=$id, name=$name, val=$val, match=$match\n|;
    $items->{$name}->{name} = ${name};
    $items->{$name}->{val} = ${val};
    $items->{$name}->{match} = ${match};
    $found->{$match}->{name} = $name if ( $match ne '' );
  }
  my $unSel = PopUp->unMatched($form,$SelectedIDs,$found,'xHL7','ConceptCode ConceptName');
# just uses items->{name} to sort
  my $SelStmt = PopUp->makeSelect($items,$bynum);
  $s->finish();
  return($unSel.$SelStmt);
}
############################################################################
# only called twice from CARSReview.cgi and Months.html
sub selYearMonth
{
  my ($self,$form,$SelectedIDs,$StartDate) = @_;
#warn qq|PopUp: selYearMonth: SelectedIDs=$SelectedIDs, StartDate=$StartDate\n|;
  my $BeginDate = DBUtil->Date('',-6);
  my ($yr,$mon,$day) = split('-',$BeginDate);
  my $items = ();
  my $found = ();
  $num = 18;   # number of months in popup.
  for (my $i = 1; $i <= $num; $i++)
  {
    my $MON = ('',January,February,March,April,May,June,July,August,September,October,November,December)[$mon];
    my $name = "${i}. ${MON}/${yr}";
#warn "name=${name}=\n";
    my $val = "${yr}-${mon}";
#warn "val=${val}=\n";
    my $match = $self->matchSelect($SelectedIDs,$val);
#warn "match=${match}=\n";
    $items->{$name}->{name} = ${name};
    $items->{$name}->{val} = ${val};
    $items->{$name}->{match} = ${match};
    $found->{$match}->{name} = $name if ( $match ne '' );
    $mon++;
    if ( $mon > 12 ) { $mon=1; $yr++; }
    $mon = length($mon) == 1 ? '0'.$mon : $mon;
  }
  my $unSel='';   # Not in select list, must choose something.
  my $SelStmt = $self->makeSelect($items,1);
  return($SelStmt."\n".$unSel);
}
############################################################################
1;
