package tst;
use myDBI;
#############################################################################
sub getSubTables
{ 
  my ($self,$form,$table,$id) = @_;
#warn "getSubTables: table=${table}, id=${id}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out = '';
  foreach my $table ( myDBI->getDetTables($table) )
  {
    my $DETID = myDBI->getTableConfig($table,'DETAILID');
    my $s = $dbh->prepare("select * from ${table} where ${DETID}='${id}'");
    $s->execute() || myDBI->dberror("getSubTables: select ${table} ${DETID}=${id}");
    if ( my $r = $s->fetchrow_hashref )
    {
      my $query = DBA->genInsert($form,$table,$r);
      $out .= $query.";\n";
#warn "getSubTables: table=${table}, DETID=${DETID}, id=${id}\n";
      if ( myDBI->getDetTables($table) )
      {
        my $RECID = myDBI->getTableConfig($table,'RECID');
#warn qq|DetTables OF: $table, $RECID\n|;
        my $sNext = $dbh->prepare("select ${RECID} from ${table} where ${DETID}='${id}'");
        $sNext->execute() || myDBI->dberror("getSubTables: select ${table} ${DETID}=${id}");
        while ( my ($ID) = $sNext->fetchrow_array )
        {
#warn qq|DBA->getSubTables($table,$ID)\n|;
          $out .= tst->getSubTables($form,$table,$ID);
        }
        $sNext->finish();
      }
    }
    $s->finish();
#warn qq|loop: ${table} where ${DETID}='${id}'");|;
  }
#warn "getSubTables: RETURN: list=\n@list\n";
  return($out);
}
#############################################################################
1;
