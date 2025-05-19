package myTables;
use DBA;
use SysAccess;
use myForm;
use myDBI;

############################################################################
sub htmLocked
{
  my ($self,$form,$locked,$table) = @_;
#warn qq|myTables: htmLocked: locked=$locked, table=$table, add=$add\n|;
  my $Agent = SysAccess->chkPriv($form,'Agent');
$locked = 0 if ( $form->{'LOGINPROVID'} == 91);
  my $delmsg = $table eq 'ClientTrPlan' 
             ? 'Are you sure you want to delete this ENTIRE Treatment Plan INCLUDING Problems/Goals AND Objectives?'
             : 'Are you sure you want to delete this entire record?';
  my $upd = $locked
     ? qq|    No Updates Allowed
      <A HREF="/src/cgi/bin/mis.cgi?misPOP=1&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}" ONMOUSEOVER="textMsg.show('BackUp');" ONMOUSEOUT="textMsg.hide()" ><IMG SRC="|.myConfig->cfgfile('undo_green.png',1).qq|" HEIGHT="30" WIDTH="40" BORDER="0" ></A>\n|
     : qq|    <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">|;
  my $add = '';
# DELETE button??
  if ( $table =~ /PDDom|ClientTrPlan|PrAuthRVU/ )
  {
    $add .= qq|      <INPUT TYPE="submit" ONCLICK="return vDELETE('${delmsg}');" NAME="${table}_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete"> | if ( !$locked && $Agent ); 
  }
  elsif ( $table eq 'ClientPrAuth' || $table eq 'ClientDischarge' )
  {
#foreach my $f ( sort keys %{$form} ) { warn qq|${table}: form-$f=$form->{$f}\n|; }
    my $AuthRVUs = SysAccess->chkPriv($form,'AuthRVUs');
    my $HDRID=$form->{"${table}_ID_1"};
    my $TransType=$form->{"${table}CDC_TransType_1"};
    my $CDCOK=$form->{"${table}CDC_CDCOK_1"};
    my $Status=$form->{"${table}CDC_Status_1"};
    my $view = $table eq 'ClientPrAuth'
             ? $TransType == 21 || $TransType == 27 
               ? 'CDC21.cgi'
               : 'CDC.cgi'
             : 'DISCDC.cgi';
#warn qq|myTables: htmLocked: TransType=$TransType, view=$view\n|;
    my $link = myForm->genLink("${table}CDC",$view);
    if ( $CDCOK )
    { $upd = qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">| if ( !$locked ); }
    else
    { $upd = qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&${link}&updLINKIDcur=1" VALUE="Add/Update -> Verify CDC"> | if ( !$locked ); }
    $add .= qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1&CLOSE=${HDRID}" VALUE="Close">| if ( $AuthRVUs && ($Status eq 'New' || $Status eq 'Pending' || $Status eq 'Rejected') );
    $add .= qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1&REOPEN=${HDRID}" VALUE="Reopen">| if ( $AuthRVUs && $Status eq 'Closed' );
    if ( $table eq 'ClientPrAuth' )
    {
      my $link = myForm->genLink('PDDom','PDDom.cgi');
      $add .= qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&${link}" VALUE="Add/Update -> CAR Scores"> | if ( !$locked );
      my $link = myForm->genLink('ClientPrAuth','ClientPADatesInp.cgi');
      $add .= qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&${link}" VALUE="ExtendPA"> | if ( $Agent );
    }
    if ( $AuthRVUs )
    {
      my $dbh = myDBI->dbconnect($form->{'DBNAME'});
      my $CDCID=$form->{"${table}CDC_ID_1"};
      my $sCount = $dbh->prepare("select count(*) from ${table}CDCSent where ${table}CDCID='${CDCID}'");
      $sCount->execute() || myDBI->dberror("selTransType: select count ${table}");
      my ($cntsent) = $sCount->fetchrow_array;
      $sCount->finish();
      $add .= qq|      <INPUT TYPE="submit" ONCLICK="return vDELETE('${delmsg}');" NAME="${table}_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete"> | unless ( $cntsent ); 
    }
  }
# DON'T CARE if locked.
  if ( $table =~ /PrAuthRVU/ )
  {
    $upd = qq|    <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">|;
  }
#warn qq|myTables: htmLocked: locked=$locked, table=$table, add=$add\n|;
  my $html = $add.$upd;
  return($html);
}
sub notLocked
{
  my ($self,$form,$table,$id,$record) = @_;
  my $locked = 0;
  my $ID = myDBI->getTableConfig($table,'RECID');
#warn qq|myTables-notLocked: table=$table, id=$id, rid: ${ID}=$record->{$ID}\n|;
#foreach my $f ( sort keys %{$record} ) { warn qq|notLocked: $f=$record->{$f}\n|; }
  if ( $record->{$ID} )                # passed the record
  { $locked = $record->{'Locked'}; }
  else                                 # otherwise, read the record
  {
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $s = $dbh->prepare("select Locked from ${table} where ${ID}='$id'");
    $s->execute() || myDBI->dberror("myTables-notLocked: ${table}/${id}");
    ($locked) = $s->fetchrow_array;
    $s->finish();
  }
  my $notlocked = $locked ? 0 : 1;
  return($notlocked);
}
############################################################################
1;
