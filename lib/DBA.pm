package DBA;
use Cwd;
use myConfig;
use CGI qw(:standard escape);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use myForm;
use myDBI;
use MgrTree;
use SysAccess;
use cBill;
use DBUtil;
use CDC;
use PopUp;
use MIME::Base64;
%XTABLE_SET = ();
############################################################################
# No Nulls are used for Secondary keys that SQL says cannot be NULL
#   but can be ''.
##
%NoNULLs = (
#           BillDate        => 'yes',
#           MgrRevDate      => 'yes',
           kls             => 'yes',
);

############################################################################
sub locked
{
  my ($self,$form,$inTable,$ID) = @_;
  my $locked = 0;    # not locked.
  if ( $inTable eq 'ClientPrAuth'
    || $inTable eq 'PDDiag'
    || $inTable eq 'PDDom' )
  {
    return(0) if ( $form->{'LOGINPROVID'} == 90 );
    return(0) if ( SysAccess->verify($form,'Privilege=Agent') );
    my $PrAuthID = $ID ? $ID : $form->{'ClientPrAuth_ID_1'};
    $locked = CDC->isLocked($form,$PrAuthID);
    $form->{'ClientPrAuth_LOCKED_1'} = $locked;                  # return for html 
  }
#warn "DBA->locked: ClientPrAuth_LOCKED_1=$form->{'ClientPrAuth_LOCKED_1'}\n";
#warn "DBA->locked: locked=$locked\n";
  return($locked);
}
############################################################################
sub selData
{
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my $self = {};
#  bless $self, $class;
  my ($form, $inTable, $query, @execute_with) = @_;

  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn "DBA selData: stmt=\n$query\n";
  my $s = $dbh->prepare($query);
  $s->execute(@execute_with) || myDBI->dberror($query);
  while ( my $r = $s->fetchrow_hashref )
  { $IDval = $r->{$ID};
#warn "IDval=$IDval\n";
    $self->{$IDval} = $r; 
    push(@{ $self->{'SELORDER'} },$IDval);
  }
  $s->finish();

  return($self);
}
############################################################################
############################################################################
sub setPrAuthReqType
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientIntake = $dbh->prepare("select * from ClientIntake where ClientID=?");
  $sClientIntake->execute($ClientID) || $self->dberror("setPrAuthReqType: select ClientIntake ${ClientID}");
  my $rClientIntake  = $sClientIntake ->fetchrow_hashref;
  $sClientIntake->finish();
  my $sClientRelations = $dbh->prepare("select * from ClientRelations where ClientID=?");
  $sClientRelations->execute($ClientID) || $self->dberror("setPrAuthReqType: select ClientRelations ${ClientID}");
  my $rClientRelations  = $sClientRelations ->fetchrow_hashref;
  my $ResDescr = DBA->getxref($form,'xResidence',$rClientRelations->{'Residence'},'Descr');
  $sClientRelations->finish();
#warn "setPrAuthReqType: ClientID=$ClientID, ServiceFocus=$rClientIntake->{'ServiceFocus'}, ResDescr=${ResDescr}\n";
  if    ( $ResDescr =~ /icf\/mr/i ) { return('MR'); }
  elsif ( DBA->isIndMedicaid($form,$ClientID) ) { return('IP'); }
  elsif ( $rClientIntake->{'ServiceFocus'} == 2             # Substance Abuse
       || $rClientIntake->{'ServiceFocus'} == 3             # Drug Court
        ) { return('SA'); }
  elsif ( $rClientIntake->{'ServiceFocus'} == 6             # Mental Health and Substance Abuse
       || $rClientIntake->{'ServiceFocus'} == 9             # Special Populations Treatment Units
       || $rClientIntake->{'ServiceFocus'} == 13            # Co-Occuring (integrated)
        ) { return('IN'); }
  elsif ( $rClientIntake->{'ServiceFocus'} == 19            # Gambling
       || $rClientIntake->{'ServiceFocus'} == 21            # Gambling Substance Abuse
       || $rClientIntake->{'ServiceFocus'} == 20            # Gambling Mental Health
        ) { return('GA'); }
  return('BH');
}
############################################################################
sub mustSignTrPlan
{
  my ($self, $form, $ProvID, $ClientID) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my $ForClientID = $ClientID ? $ClientID : $form->{Client_ClientID};
#warn qq|ProvID=$ForProvID, ClientID=$ForClientID\n|;
  return(-1) unless ( $ForProvID && $ForClientID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# is there a current PA for this Client?
  my $qPrAuth = qq|select ID from ClientPrAuth where ClientID=? and (curdate() between EffDate and ExpDate) order by EffDate, ExpDate|; 
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute($ForClientID) || myDBI->dberror($qPrAuth);
  if ( my ($PrAuthID) = $sPrAuth->fetchrow_array )
  {
#warn qq|PA=$PrAuthID\n|;
    $sPrAuth->finish();
#   did this Provider sign it?
    my $qTrPlanS = qq|select TrPlanS.ID, TrPlan.TrPlanID from TrPlanS left join TrPlan on TrPlan.TrPlanID=TrPlanS.TrPlanID where TrPlan.PrAuthID=$PrAuthID and TrPlanS.ProvID=$ForProvID|; 
    my $sTrPlanS = $dbh->prepare($qTrPlanS);
    $sTrPlanS->execute() || myDBI->dberror($qTrPlanS);
    my ($TrPlanSID) = $sTrPlanS->fetchrow_array;
    $sTrPlanS->finish();
#warn qq|$qTrPlanS\nTrPlanSID=$TrPlanSID\n|;
    return(0) if ( $TrPlanSID );

#   does this Provider need to sign it?
#   does if Provider has notes?
    my $qTreatment = qq|select TrID from Treatment where ClientID=$ForClientID and ProvID=$ForProvID|;
    my $sTreatment = $dbh->prepare($qTreatment);
    $sTreatment->execute() || myDBI->dberror($qTreatment);
    my ($TrID) = $sTreatment->fetchrow_array;
    $sTreatment->finish();
#warn qq|$qTreatment\nTrID=$TrID\n|;
    return(1) if ( $TrID );

#   does if Provider signed a TrPlan before?
    my $qTrPlanS = qq|select ID from TrPlanS where ClientID=$ForClientID and ProvID=$ForProvID|; 
    my $sTrPlanS = $dbh->prepare($qTrPlanS);
    $sTrPlanS->execute() || myDBI->dberror($qTrPlanS);
    my ($SignedID) = $sTrPlanS->fetchrow_array;
    $sTrPlanS->finish();
#warn qq|$qTrPlanS\nSignedID=$SignedID\n|;
    return(1) if ( $SignedID );
  }
  else { warn qq|no PA\n|; $sPrAuth->finish(); }
#warn qq|return 0\n|;
  return(0);
}
sub setTrPlanMsg
{
  my ($self, $form) = @_;
  my $out = qq|  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Signature Dates</TD></TR>\n|;
  my $signed = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select * from TrPlanS left join Provider on Provider.ProvID=TrPlanS.ProvID where TrPlanS.ClientID=? and TrPlanS.TrPlanID=? order by Provider.LName, Provider.FName|; 
  my $s = $dbh->prepare($q);
  $s->execute($form->{Client_ClientID},$form->{TrPlan_TrPlanID}) || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    my $SignDate = DBUtil->Date($r->{'SignDate'},'fmt','MM/DD/YYYY');
    my $SignTime = DBUtil->AMPM($r->{'SignTime'});
    my $when = $SignTime eq '' ? $SignDate : qq|${SignDate} @ ${SignTime}|;
    $out .= qq|  <TR ><TD CLASS="strcol" >** Signed by $r->{FName} $r->{LName} ${when}</TD></TR>\n|;
    if ( $r->{ProvID} == $form->{LOGINPROVID} )      # they already signed it.
    {
      $signed = 'TrPlanSigned_' . $r->{ProvID};
      $form->{$signed} = $r->{SignDate};
    }
  }
  $s->finish();
#warn "signed=$signed\n";
  if ( $signed eq '' )
  {
    $out .= qq|  <TR ><TD CLASS="strcol" >** Treatment Plan needs to be signed by $form->{LOGINUSERNAME} (check box below and click Update)</TD></TR>\n|;
  }
#  if ( !$form->{"OPENTABLE:TrPlanS"} ) { $form->TBLread('TrPlanS'); }
  $out .= qq|  <TR ><TD CLASS="strcol" >&nbsp;</TD></TR>\n|;
  return($out);
}
sub setTrPlanSign
{
  my ($self,$form) = @_;
  my $out;
  my $signed = 'TrPlanSigned_' . $form->{LOGINPROVID};
  if ( SysAccess->verify($form,'hasClientAccess') && !$form->{$signed} )
  { 
    $out .= qq|
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Check box below for $form->{LOGINUSERNAME} to sign Treatment Plan</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Sign Treatment Plan</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="TrPlan_Sign" VALUE="1" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD></TR>
|;
  }
  return($out);
}
sub getNoteView
{
  my ($self, $form, $TrID) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $Type = 1;                # default to Progress.
  if ( $TrID eq 'new' )
  {
    if ( $form->{NoteType} ) { $Type = $form->{NoteType}; }
    else
    {
      my $q = qq|
  select Insurance.InsIDNum, xInsurance.Descr, xInsurance.Name, xInsurance.NoteType
    from Insurance 
      left join xInsurance on xInsurance.ID=Insurance.InsID
    where Insurance.ClientID=?
      and Insurance.Priority=1
      and Insurance.InsNumEffDate<=curdate()
      and (curdate()<=Insurance.InsNumExpDate or
           Insurance.InsNumExpDate is NULL)
    order by Insurance.InsNumEffDate desc
|;
      my $s=$dbh->prepare($q);
      $s->execute($form->{Client_ClientID});
      if ( my $r = $s->fetchrow_hashref )
      { $Type = $r->{NoteType}; }
      $s->finish();
    }
#    if ( ${Type} == 3 )  # for Electronic Type?
#    {
#      $form->{Provider_ProvID} = $form->{LOGINPROVID};
#      return('NoteUpload.cgi');
#    }
  }
  else
  {
    my $s = $dbh->prepare("select Type from Treatment where TrID=${TrID}");
    $s->execute() || myDBI->dberror("getNoteView: select Type for TrID=${TrID}");
    ($Type) = $s->fetchrow_array;
    $s->finish();
  }
  my ($num,$def) = $self->noteType($Type);
  my $view = $def . '.cgi';
  return($view);
}
sub noteType
{
  my ($self, $in) = @_;
  my $num = ($in =~ /Progress/i ? 1 :
             $in =~ /Physician/i ? 2 :
             $in =~ /Electronic/i ? 3 :
             $in =~ /Medicare/i ? 4 :
             $in =~ /TFC/i ? 5 : $in);
  my $def = ($num == 1 ? 'Progress' :
             $num == 2 ? 'Physician' :
             $num == 3 ? 'Electronic' :
             $num == 4 ? 'Medicare' :
             $num == 5 ? 'TFC' : $num);
  return($num,$def);
}
sub noteNum
{
  my ($self,$num) = @_;
  my $def = ($num == 1 ? 'Progress' :
             $num == 2 ? 'Physician' :
             $num == 3 ? 'Electronic' :
             $num == 4 ? 'Treatment' :
             $num == 5 ? 'TFC' : $num);
  return($def);
}
############################################################################
sub EligibleDate
{
  my ($self,$form,$in) = @_;
  my $EDate = $form->{TODAY};
  if ( $in ) { $EDate = DBUtil->Date('today',0,9); }
  {
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $s = $dbh->prepare("select FromDate from Eligible order by FromDate desc");
    $s->execute() || myDBI->dberror("EligibleDate: select");
    ($EDate) = $s->fetchrow_array;
    $s->finish();
  }
  return($EDate);
}
sub getLastID
{
  my ($self,$form,$inTable,$where,$order) = @_;
#warn qq|getLastID: where=$where\n|;
  return('') if ( $where eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $q = $order eq '' ? qq|select ${inTable}.${ID} from ${inTable} where ${where}|
                       : qq|select ${inTable}.${ID} from ${inTable} where ${where} order by ${order}|;
#warn qq|getLastID: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  my ($LastID) = $s->fetchrow_array;
  $s->finish();
  return($LastID);
}
##
# these will also getPREV depending on the inSort.
##
sub getLASTID
{
  my ($self,$form,$CurID,$inTable,$inWith,$inSort) = @_;
  my $r = $self->getLAST($form,$CurID,$inTable,$inWith,$inSort,'ID');
  my $ID = myDBI->getTableConfig($inTable,'RECID');
#warn qq|ID=$ID,$r->{$ID}\n|;
  return($r->{$ID});
}
sub getLAST
{
  my ($self,$form,$CurID,$inTable,$inWith,$inSort,$inList) = @_;
  my $match = 0;
  my $rLast = ();
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $HDRID = myDBI->getTableConfig($inTable,'DETAILID');
  my $HDRTABLE = myDBI->getTableConfig($inTable,'HEADERTABLE');
  my $HDRTABLEID = myDBI->getTableConfig($HDRTABLE,'RECID');
  my $q = $inList eq '' ? qq|select ${inTable}.* from ${inTable} |
          : $inList =~ /^id$/i ? qq|select ${inTable}.${ID} from ${inTable} |
          : qq|select ${inList} from ${inTable} |;
  $q .= $HDRTABLE eq '' ? '' : qq| left join ${HDRTABLE} on ${HDRTABLE}.${HDRTABLEID}=${inTable}.${HDRID} ${inWith} |;
  $q .= $inSort eq '' ? '' : $inSort =~ /^date$/i ? qq| order by ${inTable}.EffDate desc, ${inTable}.ExpDate desc | : $inSort;
#warn qq|getLAST: q=$q\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  { 
#foreach my $f ( sort keys %{$r} ) { warn ": r-$f=$r->{$f}\n"; }
#warn qq|getLAST: CurID=$CurID, ID=$r->{ID}, PrevID=$rLast->{$ID}\n|;
    if ( $CurID eq '' ) { $rLast = $r; last; }
    elsif ( $r->{$ID} == $CurID ) { $match = 1; }
    elsif ( $match ) { $rLast = $r; last; }
  }
  $s->finish();
  return($rLast);
}
############################################################################
############################################################################
############################################################################
# this one is an ordered array
sub getTableFields
{
  my ($self,$form,$table,$dbname) = @_;
  my @flds = ();
  my $db = $dbname eq '' ? $form->{'DBNAME'} : $dbname;
#warn qq|DBA: getTableFields: table=${table}\n|;
  my $dbh = myDBI->dbconnect($db);
  my $s = $dbh->prepare("show fields from ${table}");
  $s->execute() || myDBI->dberror("getTableFields: show fields from ${table}");
  while ( my $r = $s->fetchrow_hashref )
  { push(@flds,$r->{'Field'}); }
  $s->finish();
  return(@flds);
}
# this NOT used anywhere...
sub getFldLen
{
  my ($self, $form, $inTable) = @_;
  my @flds = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $query = qq|show fields from ${inTable}|;
  my $s = $dbh->prepare($query);
  $s->execute() || myDBI->dberror($query);
  while ( my $r = $s->fetchrow_hashref )
  {
    my ($name, $args) = split(/\(/,$r->{Type},2);
    my ($len, $rest) = split(/\)/,$args,2);
    push(@flds,[$r->{'Field'},$len]);
  }
  $s->finish();
  return(@flds);
}
# this one is an hashed array
sub getFieldDefs
{ 
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my ($form, $inTable) = @_;
  my $flds = {};

  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
  my $dbh = myDBI->dbconnect($DBNAME);
  my $query = qq|show fields from ${inTable}|;
  my $s = $dbh->prepare($query);
  $s->execute() || myDBI->dberror($query);
  while ( my $r = $s->fetchrow_hashref )
  {
    my ($name, $args) = split(/\(/,$r->{Type},2);
    my ($len, $rest) = split(/\)/,$args,2);
#    $flds->{$r->{'Field'}} = $r->{'Type'};
    $flds->{$r->{'Field'}} = $len eq '' ? $name : $len;
  }
#foreach my $f ( sort keys %{$flds} ) { warn "getFieldDefs: flds-$f=$flds->{$f}\n"; }
  $s->finish();
  return($flds);
}
############################################################################
# NEW ROUTINE NOT YET USED, IF EVER?
sub setFields
{ 
  my ($self,$form,$table,$r) = @_;
#warn "setFields: table=$table\n";
  my $TableFieldDefs = $self->getFieldDefs($form,$table);
  foreach my $fld (sort keys %{$r} )
  { 
#warn qq|$fld=$r->{$fld}\n|;
    next unless ( exists($TableFieldDefs->{$fld}) );
    next if ( $fld eq 'FormID' );
    next if ( $fld eq 'CreateDate' );
    next if ( $fld eq 'CreateProvID' );
    my $key = qq|${table}_${fld}_1|;
    $form->{$key} = $r->{$fld};
#warn qq|$key=$form->{$key}\n|;
  }
#warn "setFields: $table, FormID=$r->{FormID}, FORMID=$form->{FORMID}\n";
  return($form);
}
sub clrFields
{ 
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my ($form, $inTable) = @_;

#warn "clrFields: inTable=$inTable\n";
  foreach my $key (sort keys %{$form} )
  { 
    my ($table, $field, $num) = $key =~ /(.+)_(.+)_(\d+)/;
    next if ( $table ne $inTable );          # this will ignore Table_Field...types
#warn "clrFields: table=$table, field=$field, val=$form->{$key} (num=$num)\n";
    delete $form->{$key};
  }
#warn "clrFields: $inTable\n";
  return(1);
}
############################################################################
sub getFields
{ 
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my ($form, $inTable) = @_;
  my $flds = {};

#warn "getFields: inTable=$inTable\n";
  my ($FOUND, $NOTNULL) = (0,0);
  foreach my $key (sort keys %{$form} )
  { 
##
#   Must match the format TABLE_FIELD_NUMBER or else InTable ne table.
##
#warn qq|$key=$form->{$key}\n|;
    my ($table, $field, $num) = $key =~ /(.+)_(.+)_(\d+)/;
#warn "getFields: table=$table, field=$field, val=$form->{$key} (num=$num)\n";
    next if ( $table ne $inTable );
    next if ( $field eq 'RecDOLC' );
    next if ( $field eq 'ChangeDate' );
    next if ( $field eq 'LOCKED' );
    next if ( $field eq 'Locked' );
    next if ( $field eq 'NOACCESS' );
#warn "getFields: PASSED: table=$table, field=$field, val=$form->{$key} (num=$num)\n";

    $flds->{$field} = $form->{$key};
    $FOUND =1;
    $NOTNULL = 1 if ( $form->{$key} ne '' );
  }
  if ( $NOTNULL ) { $flds->{FormID} = $form->{FORMID} . "_1"; }
  else { $FOUND = 0; } 

#warn "getFields: $inTable, FormID=$flds->{FormID}, FORMID=$form->{FORMID}\n";
  return($flds);
}
############################################################################
# see if record already exists in db.
sub recExist
{  
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my ($form, $inTable, $inData) = @_;

  my $RECID = myDBI->getTableConfig($inTable,'RECID');
  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
  my $dbh = myDBI->dbconnect($DBNAME);

# 1 = existed before this session (by FormID) (Back Button?).
##  NOT USED except on INSERT
  my $qFormID = qq|select * from $inTable where FormID='$inData->{FormID}'|;
#warn "WATCH:recExist? q=\n$qFormID\n";
  my $sFormID = $dbh->prepare($qFormID);
  $sFormID->execute() || myDBI->dberror($qFormID);
  if ( my $rFormID = $sFormID->fetchrow_hashref )
  {
    $sFormID->finish();
#foreach my $f ( sort keys %{$rFormID} ) { warn "recExist: form-$f=$rFormID->{$f}\n"; }
warn "WATCH:recExist? inTable=$inTable, FormID=$inData->{FormID} RETURNING $ID=$rFormID->{$RECID}\n";
    $inData->{$RECID} = $rFormID->{$RECID};
    my $f = $inTable . '_' . $RECID;
    $form->{$f} = $rFormID->{$RECID};
    $form->{$f . '_1'} = $rFormID->{$RECID};
    return($rFormID);
  }
  $sFormID->finish();

# 2 = we were called but not given anything.
#warn "recExist: inData-ID=$inData->{$RECID}\n";   # nothing to select for
  return('') if ( $inData->{$RECID} eq '' );   # nothing to select for

# 3 = select from inTable (by RECID).
                                           # search by record RECID
  $qByID = qq|select * from $inTable where $RECID='$inData->{$RECID}'|;
#warn "recExist: qByID=$qByID\n";
  $sByID = $dbh->prepare($qByID);
  $sByID->execute() || myDBI->dberror($qByID);
  $rByID = $sByID->fetchrow_hashref;
  $sByID->finish();
#warn "recExist: BY $RECID=$rByID->{$RECID} rByID=$rByID\n";
  return($rByID);
}
############################################################################
sub difFields
{ 
  my ($self,$form,$inTable,$iData,$eData) = @_;

  my $uFlag = '';
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $chgKey = "${inTable}_CHANGED";
  my $uData = ();
  $uData->{$ID} = $iData->{$ID};
  $form->{$chgKey} = 0;
#warn "difFields: $inTable, $ID= old=$eData->{$ID}, new=$iData->{$ID}, DELETE=$iData->{'DELETE'}\n";

  # This one flaged to delete.
  if ( $iData->{'DELETE'} )
  {
    if ( $eData->{$ID} ) { $uFlag = 'delete'; $form->{$chgKey} = 1; }
    return($uFlag,$uData);
  }

  my $TableFieldDefs = $self->getFieldDefs($form,$inTable);
  foreach my $key ( sort keys %{$iData} )
  {
#warn "difFields: ($key) org=$eData->{$key}, new=$iData->{$key}\n";
    if ( !exists($TableFieldDefs->{$key}) )
    { 
      warn ">>>FIELD DOES NOT exists! $inTable: ${key}=$iData->{$key} (ClientID=$iData->{ClientID}\n" if ( $key ne 'DELETE' );
      delete $iData->{$key};
    }
    next if ( ${key} eq 'FormID' );
    next if ( ${key} eq 'CreateDate' );
    next if ( ${key} eq 'CreateProvID' );

    if ( ! $eData->{$ID} ) { $uFlag = 'insert'; $form->{$chgKey} = 1; }
    elsif ( $iData->{$key} ne $eData->{$key} )
    { $uFlag = 'update'; $form->{$chgKey} = 1; $uData->{$key} = $iData->{$key};
#warn "Field undef: new $key=$iData->{$key}" if ! defined($iData->{$key});
#warn "Field undef: old $key=$eData->{$key}" if ! defined($eData->{$key});
    }
  }
  if ( $inTable eq 'Provider' )                   # any tables now using ExpDate but set with Active
  {
    $iData->{ExpDate} = '' if ( $iData->{Active} == 1 );
    $iData->{ExpDate} = $form->{TODAY} if ( $iData->{Active} == 0 && $eData->{Active} == 1 );
  }
#warn "difFields: $inTable, return uFlag=$uFlag\n";
  return($uFlag,$uData);
}
############################################################################
## These defaults are needed when adding or changing a record.
##   These are changed after difFields because they DO NOT affect the 
##   decision to insert/update.
sub setDefaults
{ 
  my $self = shift;
  my ($form, $inTable, $inData,$uData) = @_;

## WATCH OUT FOR PDPsyStat, ITS EFFDATE AND EXPDATE NAMES ARE NOT SET RIGHT
## EffDate and ExpDate are hard coded.

  my $RECID = myDBI->getTableConfig($inTable,'RECID');
  my $DETID = myDBI->getTableConfig($inTable,'DETAILID');
  my $TableFieldDefs = $self->getFieldDefs($form,$inTable);
  my $HDRTABLE = myDBI->getTableConfig($inTable,'HEADERTABLE');
  my $HDRTABLEID = myDBI->getTableConfig($HDRTABLE,'RECID');
  my $TOPTABLE = myDBI->getTopTable($inTable);
#warn "setDefaults: inTable=$inTable, ClientID=$form->{Client_ClientID_1}, RECID=$RECID, DETID=$DETID\n";
  if ( $inData->{'DELETE'} ) { null; }
  else
  { 
#warn "setDefaults: set ClientID? inData-ClientID=$inData->{ClientID}\n";
##
# this is for our 2 main tables Provider and Client
#   it is needed because some sub-sub-tables have ProvID or ClientID. 
##
    if ( ${inTable} ne 'Provider' && ${TOPTABLE} eq 'Provider' )
    { 
      if ( exists($TableFieldDefs->{ProvID}) )
      {
        $inData->{ProvID} = $form->{Provider_ProvID_1}; 
        $uData->{ProvID} = $form->{Provider_ProvID_1}; 
#warn "setDefaults: inData-ProvID=$inData->{ProvID}\n";
        $form->{"${inTable}_ProvID_1"} = $form->{Provider_ProvID_1};
      }
      if ( exists($TableFieldDefs->{ProviderID}) )
      {
        $inData->{ProviderID} = $form->{Provider_ProvID_1}; 
        $uData->{ProviderID} = $form->{Provider_ProvID_1}; 
#warn "setDefaults: inData-ProviderID=$inData->{ProviderID}\n";
        $form->{"${inTable}_ProviderID_1"} = $form->{Provider_ProvID_1};
      }
    }
    if ( ${inTable} ne 'Client' && ${TOPTABLE} eq 'Client' && exists($TableFieldDefs->{ClientID}) )
    { 
      $inData->{ClientID} = $form->{Client_ClientID_1}; 
      $uData->{ClientID} = $form->{Client_ClientID_1}; 
#warn "setDefaults: inData-ClientID=$inData->{ClientID}\n";
      $form->{"${inTable}_ClientID_1"} = $form->{Client_ClientID_1};
    }
    if ( exists($TableFieldDefs->{ChangeProvID}) )
    {
      $inData->{ChangeProvID} = $form->{LOGINPROVID};
      $uData->{ChangeProvID} = $form->{LOGINPROVID};
#warn "setDefaults: inData-ChangeProvID=$inData->{ChangeProvID}\n";
      $form->{"${inTable}_ChangeProvID_1"} = $form->{LOGINPROVID};
    }
    if ( exists($TableFieldDefs->{EffDate}) && $inData->{EffDate} eq '' )
    { 
      $inData->{EffDate} = $form->{TODAY}; 
      $uData->{EffDate} = $form->{TODAY}; 
#warn "setDefaults: inData-EffDate=$inData->{EffDate}\n";
      $form->{"${inTable}_EffDate_1"} = $form->{TODAY};
    }
#warn "setDefaults: inData-Active=$inData->{Active}, ID=$inData->{$RECID}\n";
    if ( exists($TableFieldDefs->{Active}) )
    {
      my $org = $inData->{'Active'};
      if ( exists($TableFieldDefs->{ExpDate}) )
      {
        if ( $inData->{ExpDate} eq '' ) { $inData->{Active} = '1'; }
        else { $inData->{Active} = '0'; }
      }
      elsif ( $inData->{$RECID} eq '' ) { $inData->{Active} = '1'; }
      $uData->{Active} = $inData->{Active} if ( $inData->{'Active'} ne $org );
      $form->{"${inTable}_Active_1"} = $inData->{Active};
    }
##
# Set the backward and forward link (Header->Detail->Header)
##
#warn "setDefaults: DETID=${DETID}\n";
    if ( $DETID ne '' )
    {
      my $org = $inData->{$DETID};
#warn "setDefaults: set org=$org, inData-${DETID}=form-${HDRTABLE}_${HDRTABLEID}_1\n";
      $inData->{$DETID} = $form->{"${HDRTABLE}_${HDRTABLEID}_1"};
#warn qq|${DETID} = $inData->{$DETID}, org=$org\n|;
      $uData->{$DETID} = $inData->{$DETID} if ( $inData->{$DETID} ne $org );
#warn "setDefaults: inData-${DETID}=$inData->{$DETID},$uData->{$DETID}\n";
      $form->{"${inTable}_${DETID}_1"} = $inData->{$DETID};
#warn qq|setDefaults: form-${inTable}_${DETID}_1=$form->{"${inTable}_${DETID}_1"}\n|;
    }
    else { warn "setDefaults: ${inTable} NO DETID.\n" unless ( $inTable eq 'Client' ); }
  }
  return(1);
}

sub setUpdates
{ 
  my ($self,$form,$inTable,$inData) = @_;
#warn "setUpdates BEGIN: inTable=$inTable\n";
#foreach my $f ( sort keys %{$inData} ) { warn "setUpdates: inData-$f=$inData->{$f}\n"; }
  if ( $inData->{'DELETE'} ) { null; }
  else
  { 
    if ( $inTable eq 'Treatment' )
    {
#warn "setUpdates: Treatment: $form->{Treatment_TrID_1}, $form->{Treatment_Units_1}\n";
      if ( $form->{'Treatment_BillStatus_1'} !~ /3|4|5/ )              # inprocess/scholar/reconcile
      {
        my $rxSC = cBill->getServiceCode($form,$form->{Treatment_SCID_1},$form->{Treatment_ContLogDate_1},$form->{Treatment_ContLogBegTime_1},$form->{Treatment_ContLogEndTime_1},$form->{Treatment_TrID_1});
        $inData->{Units} = $rxSC->{Units};
        $form->{Treatment_Units_1} = $rxSC->{Units};
# update Amts in PostUpd->updNote with setBilledAmt.
#warn "setUpdates: Treatment: $form->{Treatment_TrID_1}, $form->{Treatment_Units_1}\n";
      }
    }
    elsif ( $inTable eq 'ClientIntake' )
    {
#warn "setUpdates: ClientIntake: inData-ICISID=$inData->{ICISID}\n";
      $inData->{ICISID} = DBA->getICISID($form,$inData);
      $form->{ClientIntake_ICISID_1} = $inData->{ICISID};
      $form->{ClientIntake_FamilyID_1} = $inData->{ICISID} . 'P';
#warn "setUpdates: ClientIntake: inData-ICISID=$inData->{ICISID}, form-ICISID=$form->{ClientIntake_ICISID_1}\n";
    }
  }
#warn "setUpdates END: inTable=$inTable\n";
#foreach my $f ( sort keys %{$inData} ) { warn "setUpdates: inData-$f=$inData->{$f}\n"; }
  return(1);
}
############################################################################
sub expPrev
{ 
  my ($self,$form,$inTable,$inData) = @_;
#warn "expPrev: $inTable\n";
  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
  my $dbh = myDBI->dbconnect($DBNAME);
  my $DETID = myDBI->getTableConfig($inTable,'DETAILID');
  my $q = qq|update ${inTable}|;
  if ( $inTable eq 'Insurance' )
  {
###
### Works only for Insurance table until I reset all InsNumEffDate/InsNumExpDate
###   to EffDate/ExpDate.
###
    return(0) if ( !exists($inData->{InsNumEffDate}) );
    return(0) if ( $inData->{InsNumEffDate} eq '' );
    return(0) if ( !exists($inData->{InsNumExpDate}) );

    # ExpDate is EffDate -1 day.
    my $ExpDate = DBUtil->Date($inData->{InsNumEffDate},0,-1);
    $q .= qq| set InsNumExpDate='$ExpDate' where ${DETID}=$inData->{$DETID}|;
    $q .= qq| and Priority=$inData->{Priority} and InsID=$inData->{InsID} and InsNumExpDate is null|;
  }
  elsif ( $inTable eq 'ProviderPay' )
  {
#warn "expPrev: check isMgr: $inData->{isMgr}\n";
    return(0) if ( $inData->{isMgr} );
    # ExpDate is EffDate -1 day.
    my $ExpDate = DBUtil->Date($inData->{EffDate},0,-1);
    $q .= qq| set ExpDate='$ExpDate' where ${DETID}=$inData->{$DETID}|;
    my $SCID = $inData->{SCID} ? $inData->{SCID} : 'NULL';
    $q .= qq| and isMgr=0 and SCID=${SCID} and ExpDate is null|;
  }
#warn "expPrev: q=\n=$q\n";
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  $s->finish();
  return(1);
}
############################################################################
############################################################################
############################################################################
sub xSQL
{ 
  my ($self,$form,$TYPE,$inTable,$inData,$uData) = @_;

  my $RECID = myDBI->getTableConfig($inTable,'RECID');
#warn qq|xSQL: TYPE=$TYPE, inTable=$inTable, $RECID=$inData->{$RECID}\n|;
#foreach my $f ( sort keys %{$uData} ) { warn "xSQL: uData-$f=$uData->{$f}\n"; }
#foreach my $f ( sort keys %{$inData} ) { warn "xSQL: inData-$f=$inData->{$f}\n"; }
  my @FieldList = ();
  my $Result = '';
  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
#warn qq|xSQL: inTable=$inTable, DBCFGNAME=${DBCFGNAME}, DBNAME=${DBNAME}\n|;
  my $dbh = myDBI->dbconnect($DBNAME);
  ##########################################################
  if ( $TYPE =~ /insert/i )
  {
#   expire all other records for this Detail.
    DBA->expPrev($form,$inTable,$inData) if ( myDBI->getTableConfig($inTable,'EXPFIRST') );

#warn "xSQL: insert $inTable with $RECID=$inData->{$RECID}, ClientID=$inData->{ClientID}, ProvID=$inDate->{ProvID}\n";
#foreach my $f ( sort keys %{$inData} ) { warn "xSQL: insert: inData-$f=$inData->{$f}\n"; }
    delete $inData->{$RECID} if ( $inTable ne 'UserLogin' && $inTable ne 'Manager' );
    my $query = $self->genInsert($form,$inTable,$inData);
#warn qq|xSQL: insert: query=\n$query\n|;
    my $sql = $dbh->prepare($query);
    $sql->execute() || myDBI->dberror($query);
    my $NEWID = $sql->{'mysql_insertid'};
    $sql->finish();
#warn "xSQL: insert $inTable $NEWID=$NEWID\n";
##
# update the Data buffers to reflect this 'new' record.
    $inData->{$RECID} = $NEWID;
    my $fld = $inTable . '_' . $RECID;
    $form->{$fld} = $NEWID;
    $form->{$fld . '_1'} = $NEWID;
    my $fld1 = $inTable.'_'.$RECID.'_1';
#warn "xSQL: insert $inTable $fld=$form->{$fld},$fld1=$form->{$fld1}\n";
#warn "xSQL: insert updLINKIDnew=$form->{updLINKIDnew},LINKID=$form->{LINKID}\n";
#warn "xSQL: insert updLINKIDcur=$form->{updLINKIDcur}\n";
##
# update the links...
    myForm->updLINK($form->{updLINKIDnew},"${fld}=new","${fld}=${NEWID}");
    myForm->updLINK($form->{LINKID},"${fld}=new","${fld}=${NEWID}")
      if ( $form->{'updLINKIDcur'} );
    my $HDRTABLE = myDBI->getTableConfig($inTable,'HEADERTABLE');
    if ( $HDRTABLE )        # make sure link has new changed for header table.
    {                       #   don't leave link with =new for header table.
      my $DETID = myDBI->getTableConfig($inTable,'DETAILID');
      my $DETFLD = $inTable . '_' . $DETID . '_1';
      my $HDRID = myDBI->getTableConfig($HDRTABLE,'RECID');
      my $HDRFLD = $HDRTABLE . '_' . $HDRID;
      myForm->updLINK($form->{updLINKIDnew},"${HDRFLD}=new","${HDRFLD}=$form->{$DETFLD}");
      myForm->updLINK($form->{LINKID},"${HDRFLD}=new","${HDRFLD}=$form->{$DETFLD}")
        if ( $form->{'updLINKIDcur'} );
    }
    $Result = qq|<LI>$inTable information INSERTED.<BR>|;
    $form->{'NEWPROVIDER'} = 1 if ( ${inTable} eq 'Provider' );       # flag for post_update.
  }
  ##########################################################
  elsif ( $TYPE =~ /update/i )
  {
#warn "xSQL: update $inTable with $RECID=$inData->{$RECID}, ClientID=$inData->{ClientID}, ProvID=$inDate->{ProvID}\n";
    DBA->insLog($form,$inTable,$RECID,$inData->{$RECID}) if ( myDBI->getTableLogFlag($form,$inTable) );
    my $query = $self->genUpdate($form,$inTable,$uData);
    my $sql = $dbh->prepare($query);
    $sql->execute() || myDBI->dberror("xSQL: ${query}");
    $sql->finish();

    $Result = qq|<LI>$inTable information UPDATED.<BR>|;
    $form->{'UPDACCESS'} = 1 if ( ${inTable} eq 'Provider' );         # flag for post_update.
    $form->{'UPDACCESS'} = 1 if ( ${inTable} eq 'Manager' );          # flag for post_update.
  }
  ##########################################################
  elsif ( $TYPE =~ /delete/i )
  {
#warn "xSQL: delete $inTable with $RECID=$inData->{$RECID}, ClientID=$inData->{ClientID}, ProvID=$inDate->{ProvID}\n";
    DBA->insLog($form,$inTable,$RECID,$inData->{$RECID}) if ( myDBI->getTableLogFlag($form,$inTable) );
# record the deletes to delete the SubTables AFTER post_updates
#   otherwise the post_updates routines may update things
    $form->{'RECORDDELETES'} = qq|${inTable}-$inData->{$RECID}|;
    $Result .= qq|<LI>$inTable information DELETED.<BR>|;

#   Email the DELETEs to support. I want to know about deletes!
    my $insert = $self->genInsert($form,$inTable,$inData);
    my $Text = qq|$form->{DBNAME}\n$form->{LOGINID}; $form->{LOGINUSERNAME}\n${query}\n${insert}|;
    DBUtil->email($form,'support@okmis.com',"SQL delete",$Text,'','');
  }
  else
  { return("${TYPE}-${inTable}"); }
  ##########################################################
  return($Result);
}
##
# save to a log before updating.
##
sub insLog
{
  my ($self,$form,$inTable,$RECID,$ID,$logTable) = @_;
#warn "DBA:insLog: inTable=$inTable,RECID=$RECID,ID=$ID\n";
  my $NEWID = '';                 # normally Log then tablename.
  my $log = $logTable ? $logTable : 'Log' . $inTable;
  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
#warn qq|insLog: inTable=$inTable, DBCFGNAME=${DBCFGNAME}, DBNAME=${DBNAME}\n|;
  my $dbh = myDBI->dbconnect($DBNAME);
  my $qLog = qq|select * from ${inTable} where $RECID="$ID"|;
  my $sLog = $dbh->prepare($qLog);
  $sLog->execute() || myDBI->dberror($qLog);
  while ( my $rLog = $sLog->fetchrow_hashref )
  {
    my $q = $self->genInsert($form,$log,$rLog);
#warn "DBA:insLog: q=\n$q\n";
    my $s = $dbh->prepare($q);
    $s->execute() || myDBI->dberror("insLog: $q");
    $NEWID = $s->{'mysql_insertid'};
    $s->finish();
  }
  $sLog->finish();
  return($NEWID);
}
##
# because the replace would error if record not there.
#   used by genBilling only
##
sub replace
{
  my ($self, $form, $Match, $inTable, $inData) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $RECID = myDBI->getTableConfig($inTable,'RECID');
#foreach my $f ( sort keys %{$inData} ) { warn "replace: inData-$f=$inData->{$f}\n"; }
#warn "replace: Match=$Match, inTable=$inTable, $RECID=$inData->{$RECID}\n";
  my @NameList = ();
  my @FieldList = ();
  my ($sql, $NEWID) = ('','');

  my $qExist=qq|select * from ${inTable} |;
  my $conj = qq|where|;
  foreach my $fld ( split(':',$Match) )
  { 
    if ( $inData->{$fld} eq '' ) { $qExist .= qq| ${conj} ${fld} is null|; }
    else { $qExist .= qq| ${conj} ${fld}='$inData->{$fld}'|; }
    $conj = qq|and|;
  }
#warn qq|qExist=\n$qExist\n|;
  my $sExist=$dbh->prepare($qExist);
  $sExist->execute() || myDBI->dberror($qExist);
  if ( my $rExist = $sExist->fetchrow_hashref )
  {
    $inData->{$RECID} = $rExist->{$RECID};
    foreach my $f ( sort keys %{$inData} )
    { 
      next if ( ${f} eq ${RECID} );
      if ( $inData->{$f} eq '' )
      { push( @FieldList, qq|${f}=NULL| ); }
      else
      { push( @FieldList, qq|${f}=| . $dbh->quote($inData->{$f}) ); }
    }
    my $query = qq|update $inTable set | . join(',', @FieldList) . qq| where $RECID='$inData->{$RECID}'|;
#warn "replace: update=\n$query\n";
    $sql = $dbh->prepare($query);
    $sql->execute || myDBI->dberror($query);
  }
  else
  {
    foreach my $f ( sort keys %{$inData} )
    { 
      next if ( ${f} eq ${RECID} );
      if ( $inData->{$f} eq '' )
      { push( @FieldList, qq|NULL| ); }
      else
      { push( @FieldList, $dbh->quote($inData->{$f}) ); }
      push( @NameList, $f);
    }
    my $query = "insert into $inTable (" . join(',', @NameList) . ") "
                            . "VALUES (" . join(',', @FieldList) . ")";
#warn "replace: insert=\n$query\n";
    $sql = $dbh->prepare($query);
    $sql->execute || myDBI->dberror($query);
    $NEWID = $sql->{'mysql_insertid'};
  }
  $sExist->finish();
  $sql->finish();
  return($NEWID);
}
##
# because the update would error if record not there.
##
sub update
{
  my ($self, $form, $inTable, $Match, $old, $new) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $RECID = myDBI->getTableConfig($inTable,'RECID');
#foreach my $f ( sort keys %{$old} ) { warn "update: old-$f=$old->{$f}\n"; }
#warn "update: Match=$Match, inTable=$inTable, $RECID=$old->{$RECID}\n";
  my @NameList = ();
  my @FieldList = ();
  my ($sql, $NEWID) = ('','');

  my $qExist=qq|select * from ${inTable} |;
  my $conj = qq|where|;
  foreach my $fld ( split(':',$Match) )
  { 
    if ( $old->{$fld} eq '' ) { $qExist .= qq| ${conj} ${fld} is null|; }
    else { $qExist .= qq| ${conj} ${fld}='$old->{$fld}'|; }
    $conj = qq|and|;
  }
#warn qq|qExist=\n$qExist\n|;
#foreach my $f ( sort keys %{$new} ) { warn "update: new-$f=$new->{$f}\n"; }
  my $sExist=$dbh->prepare($qExist);
  $sExist->execute() || myDBI->dberror($qExist);
  if ( my $rExist = $sExist->fetchrow_hashref )
  {
    $new->{$RECID} = $rExist->{$RECID};
    foreach my $f ( sort keys %{$new} )
    { 
      next if ( ${f} eq ${RECID} );
      if ( $new->{$f} eq '' )
      { push( @FieldList, qq|${f}=NULL| ); }
      else
      { push( @FieldList, qq|${f}=| . $dbh->quote($new->{$f}) ); }
    }
    my $query = qq|update $inTable set | . join(',', @FieldList) . qq| where $RECID='$new->{$RECID}'|;
#warn "update: update=\n$query\n";
    $sql = $dbh->prepare($query);
    $sql->execute || myDBI->dberror($query);
  }
  else
  {
    foreach my $f ( sort keys %{$new} )
    { 
      next if ( ${f} eq ${RECID} );
      if ( $new->{$f} eq '' )
      { push( @FieldList, qq|NULL| ); }
      else
      { push( @FieldList, $dbh->quote($new->{$f}) ); }
      push( @NameList, $f);
    }
    my $query = "insert into $inTable (" . join(',', @NameList) . ") "
                            . "VALUES (" . join(',', @FieldList) . ")";
#warn "update: insert=\n$query\n";
    $sql = $dbh->prepare($query);
    $sql->execute || myDBI->dberror($query);
    $NEWID = $sql->{'mysql_insertid'};
  }
  $sExist->finish();
  $sql->finish();
  return($NEWID);
}
sub delSubTables
{ 
  my ($self,$form,$inTable,$id) = @_;
#warn "delSubTables: inTable=${inTable}, id=${id}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $msg = '';
  foreach my $table ( myDBI->getDetTables($inTable) )
  {
    my $DETID = myDBI->getTableConfig($table,'DETAILID');
#warn "delSubTables: table=${table}, DETID=${DETID}, id=${id}\n";
    if ( myDBI->getDetTables($table) )
    {
      my $RECID = myDBI->getTableConfig($table,'RECID');
#warn qq|DetTables OF: $table, $RECID\n|;
      my $sNext = $dbh->prepare("select ${RECID} from ${table} where ${DETID}='${id}'");
      $sNext->execute() || myDBI->dberror("delSubTables: select ${table} ${DETID}=${id}");
      while ( my ($ID) = $sNext->fetchrow_array )
      {
#warn qq|DBA->delSubTables($table,$ID)\n|;
        $msg .= DBA->delSubTables($form,$table,$ID);
      }
      $sNext->finish();
    }
#warn qq|loop: prepare("delete from ${table} where ${DETID}='${id}'");|;
    my $sDelete = $dbh->prepare("delete from ${table} where ${DETID}='${id}'");
    $sDelete->execute() || myDBI->dberror("delSubTables: delete ${table} ${DETID}=${id}");
    $sDelete->finish();
    $msg .= qq|<LI>${table} information DELETED.<BR>|;
    delete $form->{'OPENTABLE:'. $table};
    DBA->clrFields($form,$table);
  }
#warn "delSubTables: msg=\n$msg\n";
  return($msg);
}
# doRead: use foreach (while loop never exits)
#         takes care of the DBI info from the form.
sub doRead
{
  my ($self,$form,$table,$where) = @_;
  my @records = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from ${table} where ${where}");
  $s->execute() || myDBI->dberror("doRead: select ${table} where ${where}");
  while ( my $r = $s->fetchrow_hashref ) { push(@records,$r); }
  $s->finish();
  return(@records);
}
# doSQL: use foreach (while loop never exits)
sub doSQL
{
  my ($self,$form,$sql,$where) = @_;
  my @records = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|doSQL: sql=${sql}\n|;
  my $s = $dbh->prepare($sql);
  $s->execute() || myDBI->dberror("doSQL: ${sql}");
  while ( my $r = $s->fetchrow_hashref ) { push(@records,$r); }
  $s->finish();
  return(@records);
}
sub selSQL
{
  my ($self,$form,$select) = @_;

  my $text;
  (my $str = $select) =~ s/^\s*(.*?)\s*$/$1/g;
  my ($s1,$s2) = split(' ',$str,2);                # split select ....
  my $fldstr = substr($s2,0,index($s2,' from '));  # substr only fields.
  my @fields = ();
  foreach my $fld ( split(',',$fldstr) )
  { 
    (my $name = $fld) =~ s/^\s*(.*?)\s*$/$1/g;
    next if ( index($name,'(') >= 0 );             # MySQL functions MUST have 'as'
    if ( index($name,')') >= 0 ) 
    { ($function,$name) = split('\)',$name,2); }
    if ( index($name,'.') >= 0 ) 
    { ($table,$name) = split('\.',$name,2); }
    if ( index($name,' as ') >= 0 ) 
    { ($orgname,$name) = split(' as ',$name,2); }
    push(@fields,$name);
  }
  my $dlm = '';
  foreach my $field ( @fields )
  { $text .= qq|${dlm}${field}|; $dlm = "\t"; }
  $text .= qq|\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare($select);
  $s->execute() || myDBI->dberror($select);
  while (my $r = $s->fetchrow_hashref)
  {
    my $dlm = '';
    foreach my $field ( @fields )
    { $text .= qq|${dlm}$r->{$field}|; $dlm = "\t"; }
    $text .= qq|\n|;
  }
  $s->finish();
  return($text);
}
# get the ID (or LastID) from table
# call: DBA->doUpdate($form,'CDC',$r,"PrAuthID=$PrAuthID","ChangeDate desc");
# only means only update, don't insert...
sub doUpdate
{
  my ($self,$form,$table,$record,$where,$order,$only) = @_;
#warn qq|\n\ndoUpdate: table=$table\n|;
#foreach my $f ( sort keys %{$record} ) { warn "doUpdate: record-$f=$record->{$f}\n"; }
#warn qq|doUpdate: where=$where\n|;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $RTNID = '';
  my $RECID = myDBI->getTableConfig($table,'RECID');
  if ( $where eq '' )      # doInsert
  {
    return() if ( $only );
    delete $record->{$RECID};
    delete $record->{'ChangeDate'};
    delete $record->{'RecDOLC'};
    delete $record->{'Locked'};
    my $qInsert = $self->genInsert($form,$table,$record);
#warn qq|doUpdate: where is null: qInsert=$qInsert\n|;
    my $sInsert = $dbh->prepare($qInsert);
    $sInsert->execute() || myDBI->dberror("INSERT ERROR: ${table}: ${qInsert}");
    $RTNID = $sInsert->{'mysql_insertid'};
    $sInsert->finish();
    return($RTNID);
  }

  my $q = $order eq '' ? qq|select ${table}.${RECID} from ${table} where ${where}|
                       : qq|select ${table}.${RECID} from ${table} where ${where} order by ${order}|;
#warn qq|doUpdate: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  if ( my ($LastID) = $s->fetchrow_array )
  {
    DBA->insLog($form,$table,$RECID,$LastID) if ( myDBI->getTableLogFlag($form,$table) );
    $record->{$RECID} = $LastID; 
    # we should not update these...
    delete $record->{'CreateProvID'};
    delete $record->{'CreateDate'};
    delete $record->{'ChangeDate'};
    delete $record->{'RecDOLC'};
    delete $record->{'Locked'};
    my $qUpdate = $self->genUpdate($form,$table,$record);
#warn qq|doUpdate: qUpdate=$qUpdate\n|;
    my $sUpdate = $dbh->prepare($qUpdate);
    $sUpdate->execute() || myDBI->dberror("INSERT ERROR: ${table}: ${qUpdate}");
    $RTNID = $LastID; 
    $sUpdate->finish();
  }
  elsif ( $only ) { return(); }
  else
  {
    delete $record->{$RECID};
    delete $record->{'ChangeDate'};
    delete $record->{'RecDOLC'};
    delete $record->{'Locked'};
    my $qInsert = $self->genInsert($form,$table,$record);
#warn qq|doUpdate: qInsert=$qInsert\n|;
    my $sInsert = $dbh->prepare($qInsert);
    $sInsert->execute() || myDBI->dberror("INSERT ERROR: ${table}: ${qInsert}");
    $RTNID = $sInsert->{'mysql_insertid'};
    $sInsert->finish();
  }
  return($RTNID);
}
sub genReplace
{
  my ($self,$form,$dbh,$table,$record,$where,$recid) = @_;
#warn qq|genReplace: table=$table, record=$record, where=$where, recid=$recid\n|;
  my $str = '';
  my $RECID = $recid eq '' ? myDBI->getTableConfig($table,'RECID') : $recid;
  if ( $where eq '' )
  { $str = $self->genInsert($form,$table,$record); }
  else
  {
    my $s = $dbh->prepare("select * from ${table} where ${where}");
#warn "genReplace: select * from ${table} where ${where}\n";
    $s->execute() || myDBI->dberror("genReplace: select ${table} where ${where}");
    if ( my $tst = $s->fetchrow_hashref )
    { $record->{$RECID} = $tst->{$RECID}; $str = $self->genUpdate($form,$table,$record,$recid); }
    else
    { $str = $self->genInsert($form,$table,$record); }
    $s->finish();
  }
  return($str);
}
sub genInsert
{
  my ($self,$form,$table,$record) = @_;
#warn qq|genInsert: table=$table, record=$record\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my @names = ();
  my @flds = ();
  foreach my $fld ( sort keys %{$record} )
  {
#   setting value=NULL blows out 'NOT NULL' in table
#   but not setting value=NULL will skip the check for 'NOT NULL'
#   so I skip setting value=NULL because it does not matter on insert
    if ( $record->{$fld} ne '' )
    {
      push( @flds, $dbh->quote($record->{$fld}) );
      push( @names, "`".$fld."`" );
    }
  }
  my $str = "insert into $table (" . join(',', @names) . ") VALUES (" . join(',', @flds) . ")";
#warn qq|genInsert: str=$str\n|;
  utf8::upgrade($str); # UTF-8 fix for DBD::mysql

  return($str);
}
sub genUpdate
{
  my ($self,$form,$table,$record,$recid) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $RECID = $recid eq '' ? myDBI->getTableConfig($table,'RECID') : $recid;
  my @flds = ();
  foreach my $fld ( sort keys %{$record} )
  {
    if ( $fld eq $RECID ) { null; }
    elsif ( $table eq 'xTableFields' && $fld eq 'TableID' ) { null; }
    elsif ( $record->{$fld} eq '' ) { push( @flds, "`${fld}`=NULL" ); }
    else { push( @flds, "`${fld}`=" . $dbh->quote($record->{$fld}) ); }
  }
  my $str = qq|update $table set | . join(',', @flds) . qq| where `${RECID}`='$record->{$RECID}'|;
#warn qq|genUpdate: str=$str\n|;
  utf8::upgrade($str); # UTF-8 fix for DBD::mysql

  return($str);
}
############################################################################
############################################################################
sub updProvider
{
  my ($self, $form) = @_;
  my $result = '';
  my $ProvID = $form->{Provider_ProvID_1};
#warn "updProvider: ProvID=${ProvID}, UPDACCESS=$form->{UPDACCESS}\n";
  if ( $form->{NEWPROVIDER} )
  { $result .= $self->newProvider($form); }
  elsif ( ! $form->{Provider_Active_1} )
  { 
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    # reset the password
    my $token = DBUtil->genToken();
    my $s = $dbh->prepare("update UserLogin set Password='${token}' where UserID='${ProvID}'");
    $s->execute() || myDBI->dberror("updProvider: update UserLogin Password ${ProvID}");
    $s = $dbh->prepare("update Provider set Email=NULL where ProvID='${ProvID}'");
    $s->execute() || myDBI->dberror("updProvider: update Provider Email ${ProvID}");
    $result = 'Emails & Password updated';
#warn "updProvider: token=${token}\n";
    $s->finish();
  }
#warn "updProvider: AGAIN: UPDACCESS=$form->{UPDACCESS}\n";
  if ( $form->{'UPDACCESS'} || $form->{'NEWPROVIDER'} )
  {
# set the real ClientACL table for this client
#   all Client Access based on ClientACl, so we need to update it...
#   it uses the Providers SiteACL + the ClientAccess to update ClientACL...
    SysAccess->setSiteACL($form,$ProvID);
    SysAccess->setClientACL($form,1,$ProvID);
    SysAccess->setManagerTree($form,$ProvID);
    if ( $form->{'NEWPROVIDER'} && $ProvID != $form->{'LOGINPROVID'} )
    {
      SysAccess->setSiteACL($form,$form->{'LOGINPROVID'});
      SysAccess->setClientACL($form,1,$form->{'LOGINPROVID'});
      SysAccess->setManagerTree($form,$form->{'LOGINPROVID'});
    }
#warn "sysfile=$ProvID, DBNAME=$form->{DBNAME}, LOGINID=$form->{LOGINID}\n";
    #DBUtil->sysfile('SetACL',$form->{DBNAME},$form->{LOGINID});
  }
  return($result);
}
sub newProvider
{
  my ($self,$form) = @_;
  
#warn "newProvider: check NEWPROVIDER: $form->{NEWPROVIDER}, self=$self\n";
#foreach my $f ( sort keys %{$form} ) { warn "newProvider: form-$f=$form->{$f}\n"; }
  return('') if ( ! $form->{NEWPROVIDER} );
  my $ProvLName = $form->{'Provider_LName_1'};
  my $ProvFName = $form->{'Provider_FName_1'};
  my $ProvID = $form->{'Provider_ProvID_1'};
  my $Type = $form->{'Provider_Type_1'};
#warn "passed NEWPROVIDER: ProvID=$ProvID, LName=$ProvLName, FName=$ProvFName\n";

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $loginid = $self->genLoginID($form,'',$ProvFName,$ProvLName);
  my $password = $self->genPassword();
#warn "LoginID=$loginid, password=$password\n";
  my $q = qq|insert into UserLogin (ID,loginid,Password,UserID,dbname,loginscreen,type,renew,FormID) values ('$form->{DBNAME}:${ProvID}','${loginid}','${password}','${ProvID}','$form->{DBNAME}','ManagerTree',0,1,'${loginid}')|;
#warn "q=\n$q\n";
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  $q = qq|insert into Manager (ProviderID,ManagerID) values ('${ProvID}','$form->{LOGINPROVID}')|;
#warn "q=\n$q\n";
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  $q = qq|INSERT INTO `ProviderPrivs` (`ProvID`, `Type`, `Rank`, `CreateProvID`, `CreateDate`, `ChangeProvID`, `ChangeDate`, `FormID`) VALUES ('${ProvID}','ClinicProvider','1','$form->{LOGINPROVID}','$form->{TODAY}','$form->{LOGINPROVID}',NULL,NULL)|;
#warn "q=\n$q\n";
  $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  $s->finish();

# update the timeout/logoff...
  my $minToLogOut = 60;
  if ( $Type < 3 ) { $minToLogOut = 60; }     # Group/Agency
  else
  {
    my $sAgency = $dbh->prepare("select minToLogOut from ProviderControl where ProvID='$form->{LOGINAGENCY}'");
    $sAgency->execute() || myDBI->dberror("newProvider: select Agency $form->{'LOGINAGENCY'}");
    ($minToLogOut) = $sAgency->fetchrow_array;
    $minToLogOut = $minToLogOut eq '' ? 60 : $minToLogOut;
    $sAgency->finish();
  }
  $q = qq|insert into ProviderControl (ProvID,minToLogOut) values ('${ProvID}','${minToLogOut}')|;
#warn "q=\n$q\n";
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);

  my $result = qq|New Provider Login: <FONT COLOR=red>${loginid}</FONT> with Password: <FONT COLOR=red>${password}</FONT><BR>Please give this new Login/Password to <FONT COLOR=blue>$form->{Provider_FName_1} $form->{Provider_LName_1}</FONT> to use to login in order to change the password to a new permanent password.|;
  return($result);
}
sub genLoginID
{
  my ($self,$form,$NewID,$FName,$LName) = @_;

#warn qq|DBA: genLoginID: NewID=$NewID, FName=$FName, LName=$LName\n|;
  ($mFName = $FName) =~ s/[\\()'"]//g;
  ($mLName = $LName) =~ s/[\\()'"]//g;
  my @StringsToTry = (
                      lc($mFName . $mLName),
                      lc($mFName . '.' . $mLName),
                      lc($mFName . '_' . $mLName),
                      lc(substr( $mFName, 0, 1 ) . $mLName),
                      lc(substr( $mFName, 0, 2 ) . $mLName),
                      lc($mFName . substr( $mLName, 0, 1 )),
                      lc($mLName . substr( $mFName, 0, 1 )),
                      lc($mLName),
                      lc($mFName)
                     );
  (my $ID = $NewID) =~ s/[- ]//g;       # no spaces
#warn qq|DBA: genLoginID: ID=$ID, NewID=$NewID, FName=$FName, LName=$LName\n|;
  @StringsToTry = ($ID, @StringsToTry) if ( $ID );

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sUserLogin = $dbh->prepare("select * from UserLogin where loginid=?");
  my $UserName = '';
  foreach $User ( @StringsToTry )
  {
    $sUserLogin->execute($User);
    next if $r = $sUserLogin->fetchrow_hashref;
    $UserName = $User;
    last;
  }
  # Don't stop till we get a user name...by adding a counter to name
  my $Str = @StringsToTry[0];
  my $Cnt = 0;
  while ( $UserName eq '' )
  {
    $Cnt++;
    $User = $Str . $Cnt;
#warn qq|DBA: genLoginID: Str=$Str, Cnt=$Cnt, User=$User\n|;
    $sUserLogin->execute($User);
    next if $r = $sUserLogin->fetchrow_hashref;
    $UserName = $User;
  }
  $sUserLogin->finish();
#warn qq|DBA: genLoginID: UserName=$UserName\n|;
  return($UserName);
} 
############################################################################
sub genPassword
{
  my ($self) = @_;
  @Chars = ('A' .. 'N', 'P' .. 'Z', 
            'a' .. 'k', 'm' .. 'z', 
            '2' .. '9', '@', '#', '%', '=', '+', ':');
   $Cnt = scalar @Chars;
   $Password = '';
   for ( my $i = 0; $i < 6; $i++ ) { $Password .= $Chars[int(rand($Cnt))]; }
   return($Password);
}
############################################################################
sub matchNoteInt
{ 
  my ($self, $form, $Type, $inValue) = @_;
  my $SelStmt, $inTable;
  if ( $Type )
  {
    $inTable = 'xNoteInt' . $Type;
    $SelStmt = $self->getxref($form, $inTable, $inValue, $displayFields);
  }
  return($SelStmt);
}
sub selxNoteInt
{ 
  my ($self,$form,$Type,$inValue) = @_;
  my $SelStmt, $inTable;
  if ( $Type )
  {
    $inTable = 'xNoteInt'.$Type;
    $SelStmt = $self->selxTable($form,$inTable,$inValue);
  }
  return($SelStmt);
}
# new xTable from okmis_config, always ID, need sort and store??
sub selxTable
{
  my ($self,$form,$xtable,$SelectedIDs,$dFields,$bynum,$sValue,$with) = @_;
#warn qq|selxTable: xtable=$xtable, IDs=$SelectedIDs, dFields=$dFields, bynum=$bynum\n|;
  my $cnt = DBA->setxref($form,$xtable,$with);
#warn qq|selxTable: xtable=${xtable}, with=${with}, cnt=${cnt}\n|;
#my $size = `ps h -o vsz $$`;
#warn "selxTable size=${size}=\n";
  my $FLDS = $dFields eq '' ? 'Descr' : $dFields;
  my $ID = $sValue eq '' ? 'ID' : $sValue;
  my $items = ();
  my $found = ();
#warn qq|selxTable: FLDS=$FLDS, ID=$ID\n|;
  foreach my $id ( sort keys %{ $$xtable } )
  {
#warn qq|selxTable: id=$id, Active=$$xtable->{$id}{Active}\n|;
    next if ( $id eq '_cnt_' );
    my ($name,$dlm) = ('','');
    foreach my $fld ( split(' ',$FLDS) )
    { $name .= $dlm.$$xtable->{$id}->{$fld}; $dlm=' | '; }
    my $val = $$xtable->{$id}->{$ID};
    my $match = PopUp->matchSelect($SelectedIDs,$val);
#warn qq|selxTable: id=$id, name=$name, val=$val, match=$match\n|;
    $items->{$name}->{name} = ${name};
    $items->{$name}->{val} = ${val};
    $items->{$name}->{match} = ${match};
    $found->{$match}->{name} = $name if ( $match ne '' );
  }
  my $unSel = PopUp->unMatched($form,$SelectedIDs,$found,$xtable,$FLDS);
# just uses items->{name} to sort
  my $SelStmt = PopUp->makeSelect($items,$bynum);
  return($unSel.$SelStmt);
}
# Build list on just the ones that match SelectedIDs (input select xTable)
sub iselxTable
{
  my ($self,$form,$xtable,$SelectedIDs,$dFields,$bynum) = @_;
#warn qq|iselxTable: xtable=$xtable, IDs=$SelectedIDs, dFields=$dFields, bynum=$bynum\n|;
  return('<OPTION SELECTED VALUE="" >unselected') if ( $SelectedIDs eq '' );
  my $FLDS = $dFields eq '' ? 'Descr' : $dFields;
  my $items = ();
  my $found = ();
  my ($ID,$where,$conj) = ('ID','where (','');
  foreach my $id ( split(chr(253),$SelectedIDs) )
  { $where .= qq|${conj} ${ID}='${id}' |; $conj = ' or '; }
  $where .= ')';
#warn qq|iselxTable: xtable=${xtable}, where=${where}\n|;
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my $s=$cdbh->prepare("select * from ${xtable} ${where}");
  $s->execute();
  while ( my $r = $s->fetchrow_hashref )
  {
    my ($name,$dlm) = ('','');
    foreach my $fld ( split(' ',$FLDS) )
    { $name .= $dlm.$r->{$fld}; $dlm=' | '; }
    my $match = PopUp->matchSelect($SelectedIDs,$r->{$ID});
#warn qq|iselxTable: name=$name, r->{$ID}=$r->{$ID}, match=$match\n|;
    $items->{$name}->{name} = $name;
    $items->{$name}->{val} = $r->{$ID};
    $items->{$name}->{match} = $match;
    $found->{$match}->{name} = $name if ( $match ne '' );
  }
  $s->finish();
  my $unSel = PopUp->unMatched($form,$SelectedIDs,$found,$xtable,$FLDS);
  my $SelStmt = PopUp->makeSelect($items,$bynum);    # just uses items->{name} to sort
#warn qq|iselxTable: SelStmt=${SelStmt}=\n|;
  return($unSel.$SelStmt);
}
sub ichkxTable
{
  my ($self,$form,$xtable,$SelectedIDs,$dFields,$checkboxname) = @_;
#warn qq|ichkxTable: xtable=$xtable, IDs=$SelectedIDs, dFields=$dFields, checkboxname=$checkboxname\n|;
  my $unsel = qq|  <INPUT TYPE="radio" NAME="${checkboxname}" VALUE="" DISABLED > unselected<BR><BR>\n|;
  return($unsel) if ( $SelectedIDs eq '' );
  my $FLDS = $dFields eq '' ? 'Descr' : $dFields;
  my ($html,$ID,$where,$conj) = ('','ID','where (','');
  foreach my $id ( split(chr(253),$SelectedIDs) )
  { $where .= qq|${conj} ${ID}='${id}' |; $conj = ' or '; }
  $where .= ')';
#warn qq|ichkxTable: xtable=${xtable}, where=${where}\n|;
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my $s=$cdbh->prepare("select * from ${xtable} ${where}");
  $s->execute();
  while ( my $r = $s->fetchrow_hashref )
  {
    my ($name,$dlm) = ('','');
    foreach my $fld ( split(' ',$FLDS) )
    { $name .= $dlm.$r->{$fld}; $dlm=' | '; }
    my $match = PopUp->matchSelect($SelectedIDs,$r->{$ID});
#warn qq|ichkxTable: name=$name, r->{$ID}=$r->{$ID}, match=$match\n|;
    my $checked = $match eq '' ? '' : 'CHECKED';
    $html .= qq|  <INPUT TYPE="radio" NAME="${checkboxname}" VALUE="$r->{$ID}" ${checked} > ${name}<BR><BR>\n|;
  }
  return($html);
}
sub getxref
{
  my ($self,$form,$xtable,$idvalues,$theflds,$thedlm,$with,$thespc,$idsep) = @_;
  my $flds = $theflds eq '' ? 'Descr' : $theflds;
  my $dlm = $thedlm eq '' ? '; ' : $thedlm;
  my $thespc = $thespc eq '' ? ' ' : $thespc;
  my $idsep = $idsep eq '' ? chr(253) : $idsep;
#warn qq|getxref: =$xtable= =$idvalues= =$flds=\n|;
  my $cnt = DBA->setxref($form,$xtable,$with);
  my ($retval,$sep, $spc) = ('','','');
  foreach my $idvalue ( split($idsep,$idvalues) )
  {
#warn qq|getxref: sep=$sep= spc=$spc= \n|;
#foreach my $fld ( split(' ',$flds) ) { warn qq|fld=${fld}, idvalue=$$xtable->{$idvalue}{$fld}\n|; }
    $spc = '';
    foreach my $fld ( split(' ',$flds) ) { $retval .= qq|${sep}${spc}$$xtable->{$idvalue}{$fld}|; $spc = $thespc; }
    $sep = $dlm;
  }
#my $size = `ps h -o vsz $$`;
#warn "getxref size=${size}=\n";
#warn qq|getxref: retval=$retval=\n|;
  return($retval);
}
sub getxrefWithDef
{
  my ($self,$form,$xtable,$idvalues,$theflds,$thedlm,$with,$thespc,$idsep) = @_;
  my $flds = $theflds eq '' ? 'Descr' : $theflds;
  my $dlm = $thedlm eq '' ? '; ' : $thedlm;
  my $thespc = $thespc eq '' ? ' ' : $thespc;
  my $idsep = $idsep eq '' ? chr(253) : $idsep;
#warn qq|getxref: =$xtable= =$idvalues= =$flds=\n|;
  my $cnt = DBA->setxref($form,$xtable,$with);
  my ($retval,$sep, $spc) = ('','','');
  foreach my $idvalue ( split($idsep,$idvalues) )
  {
#warn qq|getxref: sep=$sep= spc=$spc= \n|;
#foreach my $fld ( split(' ',$flds) ) { warn qq|fld=${fld}, idvalue=$$xtable->{$idvalue}{$fld}\n|; }
    $spc = '';
    if ($$xtable->{$idvalue} eq '')
    {
      $retval .= qq|${sep}$idvalue|;
    }
    else
    {
      foreach my $fld ( split(' ',$flds) ) { $retval .= qq|${sep}${spc}$$xtable->{$idvalue}{$fld}|; $spc = $thespc; }
    }
    $sep = $dlm;
  }
#my $size = `ps h -o vsz $$`;
#warn "getxref size=${size}=\n";
#warn qq|getxref: retval=$retval=\n|;
  return($retval);
}
sub getxxref
{
  my ($self,$form,$xtable,$xxtable,$idvalues,$theflds,$thedlm,$with,$thespc) = @_;
  my $flds = $theflds eq '' ? 'Descr' : $theflds;
  my $dlm = $thedlm eq '' ? '; ' : $thedlm;
  my $thespc = $thespc eq '' ? ' ' : $thespc;
#warn qq|getxref: =$xtable= =$idvalues= =$flds=\n|;
  my $cnt = DBA->setxref($form,$xtable,$with);
  my $cntx = DBA->setxref($form,$xxtable);
  my ($retval, $spc) = ('','');
  if ($$xtable->{$idvalues} eq '')
  {
    $retval .= qq|${sep}$idvalue|;
  }
  else
  {
    foreach my $fld ( split(' ',$flds) )
    {
      my $xxid = $$xtable->{$idvalues}{$fld};
      $retval .= qq|${spc}$$xxtable->{$xxid}{'Descr'}|;
      $spc = $thespc;
    }
  }
#my $size = `ps h -o vsz $$`;
#warn "getxref size=${size}=\n";
#warn qq|getxref: retval=$retval=\n|;
  return($retval);
}
# USED ONLY FOR xNPI and xVALUESET
sub selxref
{
  my ($self,$form,$xtable,$id,$val,$fld) = @_;
#  return() unless ( $val );
#warn qq|selxref: xtable=$xtable, id=$id, val=$val, fld=$fld\n|;
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
#warn qq|selxref: select * from ${xtable} where ${id}='${val}'\n|;
  my $s=$cdbh->prepare("select * from ${xtable} where ${id}='${val}'");
  $s->execute();
  my $r = $s->fetchrow_hashref;
  $s->finish();
  my $rtn = $fld eq '' ? $r : $r->{$fld};
#warn qq|selxref: rtn=$rtn\n|;
  return($rtn);
}
# USED ONLY FOR xVALUESET
# THIS select GIVES US ALL THE INSURANCE PAYERS (idea can be used for other categories)
# select * from xVALUESET 
#   where MeasureIdentifier='2'
#     and Category='Encounter'
#     and Concept='9999999'
#   order by Concept
sub getVALUESET
{
  my ($self,$form,$MeasureIdentifier,$Category,$Concept) = @_;
warn qq|getVALUESET: MeasureIdentifier=${MeasureIdentifier}, Category=${Category}, Concept=${Concept}\n|;
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my @records = ();
  my ($where,$conj,$cnt) = ('','where',0);
##  if ( $MeasureIdentifier ne '' ) { $where .= qq|${conj} MeasureIdentifier='${MeasureIdentifier}'|; $conj = ' and'; }
##  if ( $Category ne '' ) { $where .= qq|${conj} Category='${Category}'|; $conj = ' and'; }
##  if ( $Concept ne '' ) { $where .= qq|${conj} Concept='${Concept}'|; }
# decided must have values: so we don't return a big list.
  $where .= qq|where MeasureIdentifier='${MeasureIdentifier}' and Category='${Category}' and Concept='${Concept}'|;
warn qq|getVALUESET: where=${where}\n|;
  my $s=$cdbh->prepare("select * from xVALUESET ${where}");
  $s->execute();
  while ( my $r = $s->fetchrow_hashref )
  { push(@records,$r); $cnt++; }
  $s->finish();
warn qq|getVALUESET: cnt=$cnt\n|;
# at least 1 loop (array element) so calling routine will loop at least once.
  unless ( $cnt ) { my $r->{'ID'} = 'NONE'; push(@records,$r); }
warn qq|getVALUESET: name=$name\n|;
  return(@records);
}
sub setxref
{
  my ($self,$form,$xtable,$with) = @_;
#warn qq|\nsetxref: CHECK $xtable, with=${with}\n|;
# remove/delete stored/memory of table select
#  because if it is stored the 'with clause' will not happen
#  when using the 'with clause', subsequent call may need
#  it because the stored values will be there
#  i.e.: 'Active is not null' then next call for table
#        will also have it so call again with 'Active=1'
#  my $ewith = $XTABLE_SET{$xtable}{'_with_'};
#warn qq|setxref: with=${with}, ewith=${ewith}\n|;
  if ( $XTABLE_SET{$xtable}{'_with_'} ne $with )
  {
#warn qq|setxref: DELETE ${xtable}\n|;
    delete $XTABLE_SET{$xtable};
  }
  unless ( $XTABLE_SET{$xtable}{'_cnt_'} )
  {
#warn qq|setxref: READ ${xtable}\n|;
    my $dbh = DBA->checkDBH($form,$xtable);
    my $ID = myDBI->getTableConfig($xtable,'RECID');
    $ID = 'ID' if ( $ID eq '');
    my $where = $with eq '' ? 'where Active=1' : 'where '.$with;
#warn qq|setxref: select * from ${xtable} ${where}\n|;
    my $s=$dbh->prepare("select * from ${xtable} ${where}");
    $s->execute();
    while (my $r = $s->fetchrow_hashref) { $$xtable->{$r->{$ID}} = $r; }
    $XTABLE_SET{$xtable}{'_cnt_'} = $s->rows;
    $XTABLE_SET{$xtable}{'_with_'} = $with;
    $s->finish();
  }
  return($$xtable);
}
sub checkDBH
{
  my ($self,$form,$table) = @_;
#warn qq|checkDBH: ${table}...\n|;
  my $dbh;
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my $sCheck = $cdbh->prepare("show tables like ?");
  $sCheck->execute($table) || myDBI->dberror("checkDBH: show $table");
  if ( my $rCheck = $sCheck->fetchrow_hashref )     # found table in okmis_config
  {
    $dbh = myDBI->dbconnect('okmis_config');        # return okmis_config connection.
#warn qq|checkDBH: ${table} from okmis_config\n|;
  }
  else
  {
    $dbh = myDBI->dbconnect($form->{'DBNAME'});     # return DBNAME connection.
#warn qq|checkDBH: ${table} from $form->{DBNAME}\n|;
  }
  $sCheck->finish();
  return($dbh);
}
############################################################################
sub selSupervisingPhysicians
{
  my ($self,$form,$SelectedIDs,$rtnList) = @_;
#warn qq|selSupervisingPhysicians: SelectedIDs=$SelectedIDs=\n|;
  my %list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where Active=1 and Type=4 and Role IN ('Licensed Prescriber','Midlevel Prescriber','Supervising Doctor')");
  $sProvider->execute() || myDBI->dberror("selSupervisingPhysicians: select Provider");
  while ( my $rProvider = $sProvider->fetchrow_hashref )
  {
    my $ProvName = $rProvider->{ScreenName}
                 ? $rProvider->{ScreenName}
                 : qq| $rProvider->{LName}, $rProvider->{FName}|;
#warn qq|selSupervisingPhysicians: ProvID=$rProvider->{ProvID}, ProvName=$ProvName\n|;
    $list->{"${ProvName} ($rProvider->{ProvID})"} = $rProvider->{ProvID};
  }
  return($list) if ( $rtnList );
#foreach my $f ( sort keys %{$list} ) { warn "selSP: list-$f=$list->{$f}\n"; }
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'Provider','LName:FName');
  return($SelStmt);
}
# Routine to get all the Providers this Provider does NOT Manage
#   used in ProviderACL.cgi <SELECT NAME="Manager_ManagerID_1" >
sub selNotManagerOf
{
  my ($self, $form, $ProvID, $SelectedIDs, $rtnList) = @_;
# NOT OK if called with a NULL Provider.

#warn qq|SelectedIDs=$SelectedIDs=\n|;
  my %list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select ProvID, Name, LName, FName, Type from Provider where ProvID=?|;
  my $s = $dbh->prepare($q);
##
# insert the Agency into the list.
  foreach my $a ( SysAccess->getAgencys($form,$form->{LOGINPROVID}) )
  {
#warn qq|q=\n$q, $a\n|;
    $s->execute($a) || myDBI->dberror($q);
    if ( my ($AgencyID, $Name, $LName, $FName, $Type) = $s->fetchrow_array )
    {
      if ( $Type == 4 && $Name eq '' )       # 4 = Provider
      { $list->{"${LName}, ${FName}"} = ${AgencyID}; }
      elsif ( $Type == 4 )       # 4 = Provider
      { $list->{"${Name}"} = ${AgencyID}; }
      else
      { $list->{"${Name} (${LName}, ${FName})"} = ${AgencyID}; }
    }
    $s->finish();
    foreach my $r ( MgrTree->getProviders($form,$a,0) )
    {
      next unless ( $r->{Active} == 1 );
#warn "selNotManagerOf: match: $r->{ProvID}=${ProvID}\n";
      next if ( $r->{ProvID} == ${ProvID} );
      my $skip = 0;
      foreach my $Mgr ( MgrTree->getManagers($form,$r->{ProvID},0) )
      { 
        $skip = 1 if ( $Mgr->{ProvID} == ${ProvID} ); 
#warn qq|selNotManagerOf: check: Mgr=$Mgr->{ProvID}, ProvID=$ProvID, ProvID=$r->{ProvID}, skip=$skip\n|; 
        last if ( $skip );
#warn qq|selNotManagerOf: not skipped:\n|; 
      }
#warn qq|selNotManagerOf: end skip=$skip\n|; 
      next if ( $skip );
      if ( $r->{Type} == 4 && $r->{Name} eq '' )       # 4 = Provider
      { $list->{"$r->{LName}, $r->{FName} ($r->{ProvID})"} = $r->{ProvID}; }
      elsif ( $r->{Type} == 4 )       # 4 = Provider
      { $list->{"$r->{Name} ($r->{ProvID})"} = $r->{ProvID}; }
      else
      { $list->{"$r->{Name} ($r->{LName}, $r->{FName})"} = $r->{ProvID}; }
    }
  }
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'Provider','FName:LName:ProvID');
  return($SelStmt);
}
sub setProvCreds
{
  my ($self,$form,$ProvID,$InsID,$D,$T) = @_;

  my ($out,$ST) = ('','OK');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|setProvCreds: ProvID=$ProvID, InsID=$InsID, D=$D, T=$T\n|;
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($ProvID) || myDBI->dberror("setProvCreds: select Provider $ProvID");
  my $rProvider = $sProvider->fetchrow_hashref;

  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=? and ProviderLicenses.State=? and ProviderLicenses.LicEffDate<? and (?<=ProviderLicenses.LicExpDate or ProviderLicenses.LicExpDate is null)");
  $sProviderLicenses->execute($ProvID,$ST,$D,$D) || myDBI->dberror($qProviderLicenses);
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  my $License = $rProviderLicenses->{'LicType'};
  $License .= $rProviderLicenses->{'LicNumber'} eq '' ? ' #pending' : ' '.$rProviderLicenses->{'LicNumber'};

  my $sCredentials = $dbh->prepare("select Credentials.*, xCredentials.Descr from Credentials left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID where Credentials.ProvID=? and Credentials.InsID=? order by Credentials.Rank, Credentials.Restriction desc");
  $sCredentials->execute($ProvID,$InsID) || myDBI->dberror($qCredentials);
  my $rCredentials = $sCredentials->fetchrow_hashref;
#warn qq|Cred: ID=$rCredentials->{ID}, CredID=$rCredentials->{CredID}, Rest=$rCredentials->{'Restriction'}\n|;
  my $Cred = DBA->getxref($form,'xCredentials',$rCredentials->{CredID},'Descr');
  my $Rest = DBA->getxref($form,'xSCRestrictions',$rCredentials->{Restriction},'Descr');

  $sProvider->finish();
  $sProviderLicenses->finish();
  $sCredentials->finish();

  $out = qq|$rProvider->{'LName'}, $rProvider->{'FName'} / ${License}| if ( $ProvID );
  $out .= qq| / ${Cred} ${Rest}| if ( $ProvID );
  $out .= qq| / (${ProvID})| if ( $ProvID );
  $out .= qq| ${D}| unless ( $D eq '' );
  $out .= qq| @ ${T}| unless ( $T eq '' );
  return($out);
}
# Individual LBHP / Psycholigist for Medicaid
#  DON't warn because of $r returned is then positive
sub isIndMedicaid
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rCredentials = undef;
  my $sInsurance = $dbh->prepare("select Insurance.*,xInsurance.Descr,Client.ProvID as PrimaryProvID from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID left join Client on Client.ClientID=Insurance.ClientID where Insurance.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%' order by Insurance.InsNumEffDate desc");
  $sInsurance->execute() || myDBI->dberror("isIndMedicaid: select ${ClientID}");
  if ( my $rInsurance = $sInsurance->fetchrow_hashref )
  {
    my $ProvID=$rInsurance->{'DesigProvID'} ?
               $rInsurance->{'DesigProvID'} :
               $rInsurance->{'PrimaryProvID'};
##
# BEWARE!! warn $rCredentials CHANGES it to TRUE!
##
    my $sCredentials = $dbh->prepare("select Credentials.*,ProviderControl.NPI,xInsurance.Descr,xCredentials.Abbr from Credentials left join ProviderControl on ProviderControl.ProvID=Credentials.ProvID left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID left join xInsurance on xInsurance.ID=Credentials.InsID where Credentials.ProvID=? and (xCredentials.Abbr='indlbhp' or xCredentials.Abbr='indlbhp usup' or xCredentials.Abbr='indpsych' or xCredentials.Abbr='indpsych usup') and xInsurance.Descr LIKE '%medicaid%' order by Credentials.Rank");
    $sCredentials->execute($ProvID)
         || myDBI->dberror("isIndMedicaid: select Credentials ${ProvID}");
    $rCredentials = $sCredentials->fetchrow_hashref;
    $sCredentials->finish();
  }
  $sInsurance->finish();
  return($rCredentials);
}
sub idDMH
{
  my ($self,$form,$PIN,$Agency) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $table = $Agency ? 'Contracts' : 'Credentials';
  my $s = $dbh->prepare("select DMHuserid2,DMHpassword2 from ${table} where PIN=?");
  $s->execute($PIN) || myDBI->dberror("idDMH: select ${table} ${PIN}");
  my ($user,$pw) = $s->fetchrow_array;
  $s->finish();
#warn qq|idDMH: PIN=${PIN}, Agency=${Agency}, user=${user}, pw=${pw}\n|;
  return($user,$pw);
}
sub isDMH
{
  my ($self,$form,$ClientID,$TANF) = @_;
  my $rtnflg = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $where = $TANF ? " and Contracts.SourceCode like '44%'" : " and Contracts.SourceCode is not null";
  my $sContracts = $dbh->prepare("select Client.ClientID,xInsurance.Descr,Contracts.SourceCode from Insurance left join Client on Client.ClientID=Insurance.ClientID left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID left join xInsurance on xInsurance.ID=Insurance.InsID where Client.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%' ${where} order by Insurance.InsNumEffDate desc");
#warn "isDMH: select Client.ClientID,xInsurance.Descr,Contracts.SourceCode from Insurance left join Client on Client.ClientID=Insurance.ClientID left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID left join xInsurance on xInsurance.ID=Insurance.InsID where Client.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%' ${where} order by Insurance.InsNumEffDate desc";
  $sContracts->execute() || myDBI->dberror("isDMH: select Contracts ${ClientID}");
# DMH TANF only
  if ( my $rContracts = $sContracts->fetchrow_hashref ) { $rtnflg = 1; }
  $sContracts->finish();
#warn qq|isDMH: ClientID=$ClientID, rtnflg=$rtnflg\n|;
  return($rtnflg);
}
sub isIndividual
{
  my ($self,$form,$ProvID) = @_;
#warn qq|isIndividual: ProvID=$ProvID\n|;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  return(1) if ( SysAccess->chkPriv($form,'Agent',$ForProvID) );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $sIndividual = $dbh->prepare("select count(*)
 from Credentials
  left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID
 where Credentials.ProvID=?
  and (Descr LIKE '%Psychologist%' 
    or Descr LIKE '%LCSW%' 
    or Descr LIKE '%Physician%' 
    or Descr LIKE '%Individual%' 
    or Descr LIKE '%LPC%' 
    or Descr LIKE '%LMFT%'
    or Descr LIKE '%Nurse%')");
  $sIndividual->execute($ForProvID);
  my ($Individual) = $sIndividual->fetchrow_array;
  $sIndividual->finish();
  return($Individual);
}
sub isPhysician
{
  my ($self,$form,$ProvID) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  return(1) if ( SysAccess->chkPriv($form,'Agent',$ForProvID) );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $sPhysician = $dbh->prepare("select count(*)
 from Credentials
  left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID
 where Credentials.ProvID=?
  and (Descr LIKE '%Physician%' 
    or Descr LIKE '%Nurse%')");
  $sPhysician->execute($ForProvID);
  my ($Physician) = $sPhysician->fetchrow_array;
  $sPhysician->finish();
  return($Physician);
}
# calculate for any insurance,
#  but look for those insurances with PAgroup
sub calcLOS
{
  my ($self,$form,$InsID,$PAgroup) = @_;
#warn qq|calcLOS: InsID=${InsID},PAgroup=${PAgroup}\n|;
  my $InsDescr = DBA->getxref($form,'xInsurance',$InsID,'Descr');
  my $LengthType = DBA->getxref($form,'xPAgroups',$PAgroup,'Length1');
  my $ServiceLength = DBA->getxref($form,'xPAgroups',$PAgroup,'Length2');
#warn qq|calcLOS: InsDescr=${InsDescr},LengthType=${LengthType},ServiceLength=${ServiceLength}\n|;
  my $days = $LengthType eq 'day' ? $ServiceLength : -1;
  my $months = $LengthType eq 'month' ? $ServiceLength 
             : $LengthType eq '' && $InsDescr =~ /medicare|mhnet|tricare|cars/ ? 6
             : $LengthType eq '' ? 12 : 0;
#warn qq|calcLOS: days=${days},months=${months}\n|;
  return($months,$days);
}
sub getContractInfo
{
  my ($self,$form,$ClinicID,$InsID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qContracts = qq|
select Contracts.*, xInsurance.Descr as InsDescr
     , Clinic.Name as ClinicName, Control.NPI
  from Contracts 
    left join xInsurance on xInsurance.ID=Contracts.InsID
    left join Provider as Clinic on Clinic.ProvID=Contracts.ProvID
    left join ProviderControl as Control on Control.ProvID=Contracts.ProvID
  where Contracts.ProvID=? and Contracts.InsID=?|;
  my $sContracts = $dbh->prepare($qContracts);
  $sContracts->execute($ClinicID,$InsID) || myDBI->dberror($qContracts);
#warn qq|qContracts=$qContracts\nClinicID=$ClinicID,InsID=$InsID\n|;
  my $rContracts = $sContracts->fetchrow_hashref;
  $sContracts->finish();
#foreach my $f ( sort keys %{$rContracts} ) { warn "getContractInfo: rContracts-$f=$rContracts->{$f}\n"; }
  return($rContracts);
}
#############################################################################
##
# selects Clinics for Agency and puts in a popup SELECT
##
sub selClinics
{
  my ($self,$form,$inProvID,$SelectedIDs,$rtnList,$Active) = @_;

  my $ForProvID = $inProvID ? $inProvID : $form->{LOGINPROVID};
  my $list = ();
##
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qProvider = qq|select ProvID, Name from Provider where ProvID=?|;
  $qProvider .= qq| and Active=1 | if ( $Active );
  my $sProvider = $dbh->prepare($qProvider);
#warn qq|selClinics: qProvider=\n$qProvider, $ForProvID,$SelectedIDs,$rtnList,$Active\n|;
  foreach my $ClinicID ( DBA->getAgencyClinics($form,$ForProvID) )
  {
    $sProvider->execute($ClinicID) || myDBI->dberror($qProvider);
    if ( my ($ProvID, $Name) = $sProvider->fetchrow_array )
    { $list->{"${Name} (${ProvID})"} = ${ProvID}; }
  }
  $sProvider->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'Provider','Name:ProvID');
  return($SelStmt);
}
# ALL Providers (reguardless of access) for the Agency they have access to.
sub selProviders
{
  my ($self, $form, $SelectedIDs, $rtnList) = @_;

#warn qq|selProviders: Sel=$SelectedIDs\n|;
  my $list = ();
  foreach my $a ( SysAccess->getAgencys($form) )
  {
    foreach my $r ( MgrTree->getProviders($form,$a,0) )
    {
      next unless ( $r->{Active} == 1 );
      next unless ( $r->{Type} == 4 );       # 4 = Provider
      my $ProvName = $r->{ScreenName} ? $r->{ScreenName} : qq| $r->{LName}, $r->{FName}|;
      $list->{"${ProvName} ($r->{ProvID})"} = $r->{ProvID};
    }
  }
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'Provider','LName:FName');
  return($SelStmt);
}
sub selClinicProvider
{
  my ($self, $form, $SelectedIDs, $rtnList) = @_;
#warn "selClinicProvider: SelectedIDs=$SelectedIDs, rtnList=$rtnList\n";

  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q=qq|select * from ProviderPrivs where ProvID=? and Type='ClinicProvider'|;
  my $s=$dbh->prepare($q);
  foreach my $a ( SysAccess->getAgencys($form) )
  {
    foreach my $r ( MgrTree->getProviders($form,$a,0) )
    {
      next unless ( $r->{Active} == 1 );
      next unless ( $r->{Type} == 4 );       # 4 = Provider
      $s->execute($r->{ProvID}) || myDBI->dberror($q);
      if ( my $test = $s->fetchrow_hashref )
      { $list->{"$r->{LName}, $r->{FName} ($r->{ProvID})"} = $r->{ProvID}; }
    }
  }
  $s->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list);
  return($SelStmt);
}
sub selClinicManager
{
  my ($self, $form, $SelectedIDs, $rtnList) = @_;
#warn "selClinicManager: SelectedIDs=$SelectedIDs, rtnList=$rtnList\n";

  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q1=qq|select * from ProviderPrivs where ProvID=? and Type='ClinicProvider'|;
  my $s1=$dbh->prepare($q1);
  my $q2=qq|select * from ProviderPrivs where ProvID=? and Type='ClinicManager'|;
  my $s2=$dbh->prepare($q2);
  foreach my $r ( MgrTree->getProviders($form,$form->{LOGINAGENCY},0) )
  {
    next unless ( $r->{Active} == 1 );
    next unless ( $r->{Type} == 4 );       # 4 = Provider
    $s1->execute($r->{ProvID}) || myDBI->dberror($q1);
    if ( my $test = $s1->fetchrow_hashref )
    {
      $s2->execute($r->{ProvID}) || myDBI->dberror($q2);
      if ( my $test = $s2->fetchrow_hashref )
      { $list->{"$r->{LName}, $r->{FName} ($r->{ProvID})"} = $r->{ProvID}; }
    }
    else
    { $list->{"$r->{LName}, $r->{FName} ($r->{ProvID})"} = $r->{ProvID}; }
  }
  $s1->finish();
  $s2->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list);
  return($SelStmt);
}
sub selProviderIns
{
  my ($self, $form, $SelectedIDs, $rtnList) = @_;

  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select * from ProviderIns where ProvID=?|;
  my $s = $dbh->prepare($q);
##
# select based on the Agency.
  my $AgencyID = MgrTree->getAgency($form,$form->{Provider_ProvID_1});
  $s->execute($AgencyID) || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    next unless ( $r->{Active} );
    $list->{"$r->{Descr} ($r->{Type})"} = $r->{ID};
  }
  $s->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'ProviderIns','Descr:Type');
  return($SelStmt);
}
sub selInsurance
{
  my ($self,$form,$SelectedIDs,$rtnList) = @_;
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|selInsurance: Sel=$SelectedIDs\n|;
  my $s=$dbh->prepare("select xInsurance.ID,xInsurance.Descr,xInsurance.Name from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID group by xInsurance.Name");
  $s->execute() || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    my $ClientName = qq| $r->{LName}, $r->{FName}|;
    $list->{"$r->{Name}"} = $r->{ID};
  }
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'xInsurance','Name');
  return($SelStmt);
}
sub selClients
{
  my ($self,$form,$SelectedIDs,$rtnList,$ProvID,$Active) = @_;

  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
#warn qq|selProviders: Sel=$SelectedIDs\n|;
  my $active = $Active ? qq|and Client.Active=1| : '';
  my $q = qq|
select *
 from Client 
  left join ClientACL on ClientACL.ClientID=Client.ClientID
 where ClientACL.ProvID='${ForProvID}'
 order by LName,FName|;
  my $s=$dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    ##next unless ( SysAccess->hasClientAccess($form,$r->{ClientID}) );
    my $ClientName = qq| $r->{LName}, $r->{FName}|;
    $list->{"${ClientName} ($r->{ClientID})"} = $r->{ClientID};
  }
  $s->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'Client','LName:FName');
  return($SelStmt);
}
sub makeSelect
{
  my ($self, $form, $inValues, $list, $lookuptable, $displayfields) = @_;

  my $SelStmt = '';
  my @inValues = split(chr(253),$inValues);
  my $SelFlag = 0;
  my $Found = ();
  my @findValues = ();
  foreach my $key (sort keys %{$list} )
  {
#warn "value=$list->{$key}, key=$key\n";
    my $OneSet = 0;
    foreach my $inValue ( @inValues )
    { 
      if ( $list->{$key} eq $inValue )
      { 
        $SelStmt .= qq|<OPTION SELECTED VALUE="$list->{$key}" >$key\n|;
        $Found->{$inValue} = 1;
        $OneSet = 1;
        $SelFlag = 1;
      }
    }
    $SelStmt .= qq|<OPTION VALUE="$list->{$key}" >$key\n| if ( !$OneSet );
  }
  foreach my $inValue ( @inValues )
  { push(@findValues,$inValue) if ( !$Found->{$inValue} ); }
##
# set inValues from table if not found in provided list
##
#my $cnt=scalar(@findValues);
#warn qq|@findValues, cnt=$cnt, lookuptable=$lookuptable\n|;
  if ( scalar(@findValues) && $lookuptable ne '' )
  {
    my $ID = myDBI->getTableConfig($lookuptable,'RECID');
    $ID = 'ID' if ( $ID eq '' );
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $q = qq|select * from ${lookuptable} where ${ID}=?|;
#warn qq|makeSelect q=$q\n|;
    my $s = $dbh->prepare($q);
    foreach my $inValue ( @findValues )
    { 
      $s->execute($inValue) || myDBI->dberror($q);
      if ( my $r = $s->fetchrow_hashref )
      {
        my $desc;
        foreach my $fld ( split(':',$displayfields) )
        { $desc .= qq|$r->{$fld} |; }
        $desc .= qq| (notactive)| if ( $r->{'Active'} eq '0' );
        $SelStmt .= qq|<OPTION SELECTED VALUE="$r->{$ID}" >$desc\n|;
        $SelFlag = 1;
      }
      else { $SelStmt .= qq|<OPTION SELECTED VALUE="${inValue}" >NOT IN LIST! ${inValue}\n|; $SelFlag = 1; }
    }
  }
  if ( $SelFlag )
  { $SelStmt = qq|\n<OPTION VALUE="">unselected\n${SelStmt}|; }
  else
  { $SelStmt = qq|\n<OPTION SELECTED VALUE="">unselected\n${SelStmt}|; }
  return($SelStmt);
}
##
# used in displaying Emergency information for Physician/Hospital.
##
sub setAddress
{
  my ($self, $form, $Type) = @_;
#warn "setAddress: $Type\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  if ( $Type eq 'Physician' && $form->{ClientEmergency_PhysNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_PhysNPI_1'});
    $form->{'PhysAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'PhysCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'PhysPh'} = $r->{'WkPh'};
    $form->{'PhysFax'} = $r->{'Fax'};
  }
  elsif ( $Type eq 'Hospital' && $form->{ClientEmergency_DesigHospNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_DesigHospNPI_1'});
    $form->{'HospAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'HospCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'HospPh'} = $r->{'WkPh'};
    $form->{'HospFax'} = $r->{'Fax'};
  }
  elsif ( $Type eq 'Pharmacy' && $form->{ClientEmergency_PharmacyNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_PharmacyNPI_1'});
    $form->{'PharmacyAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'PharmacyCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'PharmacyPh'} = $r->{'WkPh'};
    $form->{'PharmacyFax'} = $r->{'Fax'};
  }
  elsif ( $Type eq 'Dentist' && $form->{ClientEmergency_DentistNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_DentistNPI_1'});
    $form->{'DentistAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'DentistCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'DentistPh'} = $r->{'WkPh'};
    $form->{'DentistFax'} = $r->{'Fax'};
  }
  elsif ( $Type eq 'Vision' && $form->{ClientEmergency_VisionNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_VisionNPI_1'});
    $form->{'VisionAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'VisionCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'VisionPh'} = $r->{'WkPh'};
    $form->{'VisionFax'} = $r->{'Fax'};
  }
  elsif ( $Type eq 'Hearing' && $form->{ClientEmergency_HearingNPI_1} )
  {
    my $r = DBA->selxref($form,'xNPI','NPI',$form->{'ClientEmergency_HearingNPI_1'});
    $form->{'HearingAddr'} = "$r->{'Addr1'} $r->{'Addr2'}";
    $form->{'HearingCSZ'} = "$r->{'City'}, $r->{'ST'}  $r->{'Zip'}";
    $form->{'HearingPh'} = $r->{'WkPh'};
    $form->{'HearingFax'} = $r->{'Fax'};
  }
  return('');
}
sub getDeductionPaid
{
  my ($self, $form, $ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# select for Type=Deductible.
  my ($FromDate,$ToDate) = DBUtil->Date('','annual');
  my $qInsPaid = qq|select * from InsPaid where ClientID=? and Type='Deductible' and TransDate between '${FromDate}' and '${ToDate}' order by TransDate|;
#warn "getDeductionPaid: ClientID=$ClientID\nq=$qInsPaid\n";
  my $sInsPaid = $dbh->prepare($qInsPaid);
  $sInsPaid->execute($ClientID);
  my $AmtCollected = 0;
  while ( $rInsPaid = $sInsPaid->fetchrow_hashref )
  { $AmtCollected += $rInsPaid->{PaidAmt}; }
#warn "getDeductionPaid: AmtCollected=$AmtCollected\n";
  $AmtCollected = sprintf("%.2f", $AmtCollected);
  $sInsPaid->finish();
  return($AmtCollected);
}
##
# rData is passed in and is the $rData->{$ID} where entire record is stored.
##
sub getDeductionRemaining
{
  my ($self, $form, $rData) = @_;
#warn "getDeductionRemaining: ClientID=$rData->{ClientID}, Deductible=$rData->{Deductible}\n";
  return(0) if $rData->{Deductible} == 0;
  my $AmtRemaining = $rData->{Deductible} - $self->getDeductionPaid($form,$rData->{ClientID});
  $AmtRemaining = sprintf("%.2f", $AmtRemaining);
#warn "getDeductionRemaining: AmtRemaining=$AmtRemaining\n";
  return($AmtRemaining);
}
sub getBMI
{
  my ($self,$form,$rData) = @_;

  my $height = ($rData->{'HeightFeet'} * 12) + $rData->{'HeightInches'};
  my $bmi = 0;
  if ( $height > 0 ) { $bmi = ( $rData->{'Weight'} / ( $height * $height ) ) * 703; }
  else { $msg = 'Need Height'; }

  if($rData->{'BMI'} > 0) {
    $bmi = $rData->{'BMI'};
  }
  $bmi = sprintf("%.2f",$bmi);
#warn qq|getBMI: height=$height, $rData->{'Weight'}, bmi=$bmi\n|;
  return($bmi);
}
sub getBSA
{
  my ($self,$form,$rData) = @_;
  my $height = ($rData->{'HeightFeet'} * 12) + $rData->{'HeightInches'};
  my $heightcm = $height * 2.54;
  my $weightkg = $rData->{'Weight'} * 0.45359237;
  my $bsa = 0.007184 * $weightkg * $heightcm;
  $bsa = sprintf("%.2f",$bsa);
#warn qq|getBMI: height=$height, $rData->{'Weight'}, cm=$heightcm, kg=$weightkg, bsa=$bsa\n|;
  return($bsa);
}
sub getClientMedCount
{
  my ($self,$form,$ClientID,$table) = @_;
  my $TotalAmt = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sMed = $dbh->prepare("select count(*) from ${table} where ClientID=?");
  $sMed->execute($ClientID);
  my ($Num) = $sMed->fetchrow_array;
  $sMed->finish();
  my $out = $Num ? "Total: ${Num}" : "None";
  return($out);
}
sub getClientIncome
{
  my ($self, $form, $ClientID) = @_;
#warn "getClientIncome: $ClientID\n";
  my $TotalAmt = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qClientIncome = qq|
select * from ClientIncome
  where ClientID=?
    and ClientIncome.EffDate<=curdate()
    and (ClientIncome.ExpDate>=curdate() or ClientIncome.ExpDate is null)
  order by EffDate
|;
#warn "getClientIncome:\n$qClientIncome\n";
  my $sClientIncome = $dbh->prepare($qClientIncome);
  $sClientIncome->execute($ClientID);
  while ( $rClientIncome = $sClientIncome->fetchrow_hashref ) { $TotalAmt += $rClientIncome->{Amt}; }
  $sClientIncome->finish();
  $TotalAmt = sprintf("%.2f",$TotalAmt);
  return($TotalAmt);
}
sub getClinicProviderSelection
{ 
  my ($self, $form, $ProvID, $Field, $Join) = @_;
  my $query = $Join eq 'where' ? 'where (' : 'and (';
  my $conj = '';
  if ( $form->{Report_Clinics} )
  {
    foreach my $ClinicID ( split(chr(253),$form->{Report_Clinics}) )
    { $query .= qq|${conj} ${Field}=${ClinicID} |; $conj = ' or '; }
  }
  else
  {
    foreach my $ClinicID ( SysAccess->getACL($form,$ProvID,'Clinic:Provider') )
    { $query .= qq|${conj} ${Field}=${ClinicID} |; $conj = 'or'; }
  }
  if ( $conj ) { $query .= ')'; }
  else { $query .= qq|${Field}='NOCLINIC' )|; }
#warn qq|query=$query\n|;
  return($query);
}
sub getClinicSelection
{ 
  my ($self, $form, $ProvID, $Field, $Join) = @_;
  my $query = $Join eq 'where' ? 'where (' : 'and (';
  my $conj = '';
#warn qq|Report_Clinics=$form->{Report_Clinics}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "getClinicSelection: form-$f=$form->{$f}\n"; }
  if ( $form->{Report_Clinics} )
  {
    foreach my $ClinicID ( split(chr(253),$form->{Report_Clinics}) )
    { $query .= qq|${conj} ${Field}=${ClinicID} |; $conj = ' or '; }
  }
  else
  {
    foreach my $ClinicID ( SysAccess->getACL($form,$ProvID,'Clinic') )
    { $query .= qq|${conj} ${Field}=${ClinicID} |; $conj = 'or'; }
  }
  if ( $conj ) { $query .= ')'; }
  else { $query .= qq|${Field}='NOCLINIC' )|; }
#warn qq|query=$query\n|;
  return($query);
}
sub getProviderSelection
{ 
  my ($self, $form, $ForProvID, $Field, $Join) = @_;
  my $query = $Join eq 'where' ? 'where (' : 'and (';
  my $conj = '';
  foreach my $ProvID ( $ForProvID,SysAccess->getACL($form,$ForProvID,'Provider') )
  { $query .= qq|${conj} ${Field}=${ProvID} |; $conj = 'or'; }
  if ( $conj ) { $query .= ')'; }
  else { $query .= qq|${Field}='NOPROVIDER' )|; }
  return($query);
}
# use withClinicProvider below instead...this is the (not) new one.
sub getForProvID
{ 
  my ($self,$form,$ForProvID,$Join,$CField,$PField) = @_;
  my $query = '';
  my $delm = $Join eq 'where' ? 'where ' : 'and ';
  if ( $form->{ClinicIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ClinicID ( split(chr(253),$form->{ClinicIDs}) )
    { $stmt .= qq|${conj} ${CField}=${ClinicID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and ' }
  }
  if ( $form->{ProvIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ProvID ( split(chr(253),$form->{ProvIDs}) )
    { $stmt .= qq|${conj} ${PField}=${ProvID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
  if ( $query eq '' )
  {
    # first test access to Clinics
    if ( $CField ne '' )
    {
      my ($stmt,$conj) = ('','');
      foreach my $ClinicID ( SysAccess->getClinics($form,$ForProvID) )
      { $stmt .= qq|${conj} ${CField}=${ClinicID} |; $conj = 'or'; }
      if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
    }
    if ( $PField ne '' )
    {
      my ($stmt,$conj) = ('','');
      foreach my $ProvID ( SysAccess->getProviders($form,$ForProvID) )
      { $stmt .= qq|${conj} ${PField}=${ProvID} |; $conj = 'or'; }
      if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
    }
  }
  if ( $query eq '' ) { $query .= qq|${delm} ( ${CField}='ACCESSNONE' )|; }
#warn qq|query=$query\n|;
  return($query);
}
sub getInsuranceSelection
{ 
 my ($self, $form, $InsID, $InsDescr, $Field, $Join) = @_;
  my ($conj,$select) = ('','');
  if ( $InsID ) { $select = qq|where xInsurance.ID=$InsID|; }
  elsif ( $InsDescr ) { $select = qq|where xInsurance.InsDescr="$InsInsDescr"|; }
  else { return (''); }
  my $query = $Join eq 'where' ? 'where (' : 'and (';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from xInsurance ${select}");
  $s->execute();
  while ( my $r = $s->fetchrow_hashref ) 
  { $query .= qq|${conj} ${Field}=$r->{ID} |; $conj = 'or'; }
  if ( $conj ) { $query .= ')'; }
  else { $query .= qq|${Field}='NONE' )|; }
#warn qq|query=$query\n|;
  return($query);
}
############################################################################
# Recursive routine to get all the sub-Managers.
#   used in ProviderPay.htm <SELECT NAME="ProviderPay_MgrID_1" >
#   THIS IS NOT MULTI-VALUED
sub selPayMgrIDs
{
  my ($self, $form, $SelectedIDs, $rtnList) = @_;
#warn "selPayMgrIDs: SelectedIDs=$SelectedIDs, rtnList=$rtnList\n";

  my $inlist = 0;
  my $list = ();
  my $counter = ();
  my @acclist = $form->{LOGINPROVID}; # defaults for login, 91(root) is Type=1, not 4.
  if ( $form->{LOGINUSERTYPE} == 4 )      # normal provider
  {
    @acclist = SysAccess->getACL($form,$form->{LOGINPROVID},'Agency'); 
#warn qq|selPayMgrIDs: acclist=@acclist\n|;
    if ( scalar(@acclist) == 0 ) { @acclist = SysAccess->getACL($form,$form->{LOGINPROVID},'Clinic'); }
    if ( scalar(@acclist) == 0 ) { @acclist = $form->{LOGINPROVID}; }
  }
  foreach my $id ( @acclist )
  {
    foreach my $r ( $self->getPayMgrs($form, $id, '', 0) )
    {
      next if ( $r->{ExpDate} );
      my $cnt = $r->{Index} + 1;
      $counter{$cnt}+=1;
      my $dots = '.' x ${cnt};
      $list->{"${cnt} $counter{$cnt}${dots}$r->{LName}, $r->{FName} $r->{Rate} ($r->{Commission})"} = $r->{ID};
      $inlist = 1 if ( $SelectedIDs == $r->{ID} );
    }
  }
  if ( ! $inlist && $SelectedIDs )
  {
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $s = $dbh->prepare("
        select ProviderPay.*, Provider.LName, Provider.FName
          from ProviderPay
            left outer join Provider on Provider.ProvID=ProviderPay.ProvID
          where ProviderPay.ID = ?
");
    $s->execute($SelectedIDs);
    if ( my $r = $s->fetchrow_hashref ) 
    { $list->{"$r->{LName}, $r->{FName} $r->{Rate} ($r->{Commission})"} = $r->{ID}; }
  }
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list);
  return($SelStmt);
}
sub selTransType
{
  my ($self,$form,$ClientID,$TransType,$type) = @_;
#warn qq|selTransType: ClientID=$ClientID, TransType=$TransType, type=$type\n|;
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $AYEARAGO = DBUtil->Date($form->{TODAY},-12);
  my $sCnt = $dbh->prepare("select count(*) from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID left join xInsurance on xInsurance.ID=Insurance.InsID where ClientPrAuth.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%'");
  $sCnt->execute() || myDBI->dberror("selTransType: select Cnt ClientPrAuth");
  my ($Cnt) = $sCnt->fetchrow_array;
  my $s21 = $dbh->prepare("select ClientPrAuth.ID,xInsurance.Descr,ClientPrAuthCDC.TransType from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID left join xInsurance on xInsurance.ID=Insurance.InsID left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%' and ClientPrAuthCDC.TransType='21' and ClientPrAuthCDC.TransDate>'${AYEARAGO}'");
  $s21->execute() || myDBI->dberror($qPrAuth);
  my ($T21) = $s21->fetchrow_array;
  my $s23 = $dbh->prepare("select ClientPrAuth.ID,xInsurance.Descr,ClientPrAuthCDC.TransType from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID left join xInsurance on xInsurance.ID=Insurance.InsID left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ClientID='${ClientID}' and xInsurance.Descr LIKE '%medicaid%' and (ClientPrAuthCDC.TransType='23' or ClientPrAuthCDC.TransType='42') and ClientPrAuth.PAnumber is not null");
  $s23->execute() || myDBI->dberror($qPrAuth);
  my ($T23) = $s23->fetchrow_array;
  my $q=qq|select * from okmis_config.xCDCTransTypes where Active=1|;
  my $s=$dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    #next if ( $TransType != 21 && $T21 && $r->{ID} == 21 ); # don't allow 21 if already 21 unless this is a 21
    #next if ( !$Cnt && !$T23 && $r->{ID} == 42 );            # don't allow 42 if no Approved 23
    #next if ( $type =~ /dis/i && $r->{ID} < 60 );           # allow 60's only on a discharge
    #next if ( $type !~ /dis/i && $r->{ID} >= 60 );          # don't allow 60's unless a discharge
    $list->{"$r->{Descr}"} = $r->{ID};
  }
  $s->finish();
  $sCnt->finish();
  $s21->finish();
  $s23->finish();
  my $SelStmt = DBA->makeSelect($form,$TransType,$list,'okmis_config.xCDCTransTypes','ID:Descr');
  return($SelStmt);
}
############################################################################
# Recursive routine to get all the sub-Managers in the pay tree.
#   it retrieves only those that are subordinate to the LOGINPROVID.
sub getPayMgrs
{
  my ($self, $form, $ProvID, $MgrID, $Index) = @_;
#warn "getPayMgrs: enter: $ProvID, $MgrID, $Index\n";

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my @Result;
  if ( $Index == 0 )                 # first time in, calls all others.
  { 
    my $q = qq|
  select ProviderPay.*, Provider.LName, Provider.FName
    from ProviderPay
      left outer join Provider on Provider.ProvID=ProviderPay.ProvID
    where ProviderPay.isMgr = 1
      and ProviderPay.ExpDate is null
      and ProviderPay.ProvID = ?
|;
#warn "getPayMgrs: start1: $q\n$ProvID\n";
    my $s = $dbh->prepare($q);
    $s->execute($ProvID);
    while (my $r = $s->fetchrow_hashref) 
    { 
#warn "getPayMgrs: push1: $r->{ProvID}, $r->{Rate}\n";
      $r->{'Index'} = $Index;
      push @Result, $r;
      push @Result, $self->getPayMgrs($form, $r->{'ProvID'}, $r->{'ID'}, 1);
    }
    $s->finish();
  }
  else                               # recursive calls from above.
  { 
    return(@Result) if ( $MgrID eq '' );
    my $SubIndex = $Index + 1;
    my $q = qq|
  select ProviderPay.*, Provider.LName, Provider.FName
    from ProviderPay
      left outer join Provider on Provider.ProvID=ProviderPay.ProvID
    where ProviderPay.isMgr = 1
      and ProviderPay.ExpDate is null
      and ProviderPay.MgrID = ?
    order by Provider.LName, Provider.FName
|;
#warn "getPayMgrs: start2: $q\n$MgrID\n";
    my $s = $dbh->prepare($q);
    $s->execute($MgrID);
    while (my $r = $s->fetchrow_hashref) 
    { 
      $r->{'Index'} = $Index;
#warn "getPayMgrs: push2: $r->{ProvID}, $r->{ID}\n";
      push @Result, $r;
      push @Result, $self->getPayMgrs($form, $r->{'ProvID'}, $r->{'ID'}, $SubIndex);
    }
    $s->finish();
  }
  return(@Result);
}
sub getInsSC
{
  my ($self,$form,$rData) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qInsSC = qq|
  select xSC.ServiceType, xSC.SCNum, xSC.SCName, xInsurance.Name
        ,xCredentials.Abbr, xSCRestrictions.Descr from xSC 
     left join xInsurance on xInsurance.ID=xSC.InsID 
     left join okmis_config.xCredentials on xCredentials.ID=xSC.CredID
     left join okmis_config.xSCRestrictions on xSCRestrictions.ID=xSC.Restriction
    where xSC.SCID=?
|;
  my $sInsSC = $dbh->prepare($qInsSC);
  $sInsSC->execute($rData->{SCID});
  my $InsSC = '';
  if ( $rInsSC = $sInsSC->fetchrow_hashref )
  { $InsSC = $rInsSC->{Name} . ' ' . $rInsSC->{ServiceType} . ' ' . $rInsSC->{SCName} . ' ' . $rInsSC->{SCNum} . ' (' . $rInsSC->{Abbr} . ') (' . $rInsSC->{Descr} . ')'; }
#warn "getInsSC: q=\n$qInsSC\nSCID=$rData->{SCID}, InsSC=$InsSC\n";
  return($InsSC);
}
sub getICISID
{
  my ($self, $form, $rClientIntake) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ICISID = $rClientIntake->{'ICISID'};
#warn qq|getICISID: ID=$ICISID\n|;
  if ( $ICISID eq '' )
  {
    my $sClient = $dbh->prepare("select * from Client where ClientID=?");
    $sClient->execute($rClientIntake->{ClientID}) 
           || myDBI->dberror("getICISID->select Client=$rClientIntake->{ClientID}");
    if ( my $rClient = $sClient->fetchrow_hashref )
    {
      my $P1 = '';
      if ( $rClient->{'MaidenName'} eq '' )
      { $P1 = substr($rClient->{'LName'},0,1) . substr($rClient->{'FName'},0,1) . $rClient->{'Gend'}; }
      else
      { $P1 = substr($rClient->{'MaidenName'},0,1) . substr($rClient->{'FName'},0,1) . $rClient->{'Gend'}; }
      my $P2 = DBUtil->Date($rClient->{'DOB'},'fmt','MMDDYY');
      $ICISID=uc($P1 . $P2);
#warn qq|getICISID: ICISID=$ICISID\n|;
      my $s = $dbh->prepare("select ICISID from ClientIntake where ICISID=?");
      $s->execute($ICISID) || myDBI->dberror("getICISID->select ICISID=$ICISID");
      while ( my ($ICISID) = $s->fetchrow_array )
      {
        $P2+=120000; $ICISID=uc($P1 . $P2);
#warn qq|getICISID: Loop: ICISID=$ICISID\n|;
        $s->execute($ICISID) || myDBI->dberror("getICISID->select ICISID=$ICISID");
      }
      $s->finish();
    }
    $sClient->finish();
  }
  return($ICISID);
}
sub getAgencyClinics
{
  my ($self,$form,$ProvID) = @_;
  my @Clinics = ();
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  foreach my $a ( SysAccess->getACL($form,$ForProvID,'Agency') )
  {
    foreach my $c ( SysAccess->getACL($form,$a,'Clinic') )
    { push(@Clinics,$c); }
  }
  return(@Clinics);
}
sub getAgencyProvs
{
  my ($self, $form, $ProvID) = @_;
  my @Provs = ();
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  foreach my $a ( SysAccess->getACL($form,$ForProvID,'Agency') )
  {
    foreach my $p ( SysAccess->getACL($form,$a,'Provider') )
    { push(@Provs,$p); }
  }
  return(@Provs);
}
sub getAgencyClients
{
  my ($self, $form, $AgencyID) = @_;
  my @Clients = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClient = $dbh->prepare("select * from Client where clinicClinicID=? and Active=1");
  foreach my $c ( SysAccess->getACL($form,$AgencyID,'Clinic') )
  {
    $sClient->execute($c) || myDBI->dberror("getAgencyClients->select clinicClinicID=$c");
    while ( my $rClient = $sClient->fetchrow_hashref )
    { push(@Clients,$rClient->{ClientID}); }
  }
  $sClient->finish();
  return(@Clients);
}
sub selServiceCodes
{
  my ($self,$form,$SelectedIDs,$rtnList,$ProvID,$ClientID,$ReqAccess,$with) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
#warn qq|selServiceCodes: ProvID=${ProvID},${ForProvID}; ClientID=${ClientID}; ReqAccess=${ReqAccess},\nwith=${with}\n|;
  my $ClientInsPriority = ();
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select xSC.SCID, xSC.SCNum, xSC.InsID, xInsurance.Name, xSC.SCName, xSC.ServiceType, xCredentials.Abbr, xSCRestrictions.Descr as ResDescr, xSC.Restriction from xSC left join xInsurance on xInsurance.ID=xSC.InsID left join okmis_config.xCredentials on xCredentials.ID=xSC.CredID left join okmis_config.xSCRestrictions on xSCRestrictions.ID=xSC.Restriction where xSC.Active=1 |;
  if ( $ReqAccess =~ /INSID=ALL/i ) { null; }    # allow call for all insurance service codes - ProviderPay
  elsif ( $ReqAccess =~ /INSID=/i )              # allow call for one insurance service codes - xSC etc.
  { my ($tag,$InsID) = split('=',$ReqAccess); $q .= qq|and xSC.InsID='${InsID}' |; }
  else
  {
    $q .= $self->withCredIDs($form,$ForProvID,'xSC','and');

    my $selInsIDs = qq|xSC.InsID is null|;
    foreach my $r ( $self->getClientInsurances($form,$ClientID,1) )
    {
      $selInsIDs .= qq| or xSC.InsID='$r->{InsID}'|; 
      $ClientInsPriority->{$r->{'InsID'}} = $r->{'Priority'} == 1 ? 'Primary' 
                                          : $r->{'Priority'} == 2 ? 'Secondary'
                                          : $r->{'Priority'} == 3 ? 'Tertiary' : 'NoPriority';
    }
    $q .= 'and (' . $selInsIDs . ')';
  }
  $q .= qq| ${with} order by xInsurance.Name, xSC.ServiceType, xSC.SCName, xSC.SCNum|;
#warn qq|selServiceCodes: q=$q\n|;
  my $s=$dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  if ( $ForProvID == 91 )
  {
    while ( my $r = $s->fetchrow_hashref )
    {
      my $Priority = $ClientInsPriority->{$r->{'InsID'}};
      my $SCName = length($r->{SCName}) > 60 ? substr($r->{SCName},0,60).'...' : $r->{SCName};
      $list->{"${Priority} $r->{Name} $r->{SCNum} $r->{SCID} $r->{ServiceType} ${SCName} ($r->{Abbr}) ($r->{ResDescr})"} = $r->{SCID}; 
    }
  } else {
    while ( my $r = $s->fetchrow_hashref )
    {
#warn qq|selServiceCodes: SCID: $r->{SCID}: $r->{Name}: $r->{ServiceType}: $r->{SCName}: $r->{SCNum}: $r->{Abbr}: $r->{ResDescr}:\n|; 
#warn qq|selServiceCodes: InsID=$r->{'InsID'}, Priority=${Priority}\n|;
      my $Priority = $ClientInsPriority->{$r->{'InsID'}};
      my $SCName = length($r->{SCName}) > 60 ? substr($r->{SCName},0,60).'...' : $r->{SCName};
      $list->{"${Priority} $r->{Name} $r->{ServiceType} ${SCName} $r->{SCNum} ($r->{Abbr}) ($r->{ResDescr})"} = $r->{SCID};
    }
  }
  $s->finish();
  return($list) if ( $rtnList );
#foreach my $f ( sort keys %{$list} ) { warn ": list-$f=$list->{$f}\n"; }
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list,'xSC','SCNum:SCName');
  return($SelStmt);
}
sub selNoteServiceTypes
{
  my ($self,$form,$SelectedIDs,$rtnList) = @_;
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select ServiceType from xSC where ServiceType is not null group by ServiceType|;
  my $s=$dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
    my $ServiceName = 'Unknown ' . $r->{'ServiceType'};
    if ( $r->{'ServiceType'} eq 'DMGA' ) { $ServiceName = 'Contract Gambling'; }
    elsif ( $r->{'ServiceType'} eq 'DMHH' ) { $ServiceName = 'Contract Health Home'; }
    elsif ( $r->{'ServiceType'} eq 'DMIN' ) { $ServiceName = 'Contract Integrated'; }
    elsif ( $r->{'ServiceType'} eq 'DMMH' ) { $ServiceName = 'Contract Mental Health'; }
    elsif ( $r->{'ServiceType'} eq 'DMSA' ) { $ServiceName = 'Contract Substance Abuse'; }
    elsif ( $r->{'ServiceType'} eq 'GA' ) { $ServiceName = 'Medicaid Gambling'; }
    elsif ( $r->{'ServiceType'} eq 'IN' ) { $ServiceName = 'Medicaid Integrated'; }
    elsif ( $r->{'ServiceType'} eq 'MH' ) { $ServiceName = 'Medicaid Mental Health'; }
    elsif ( $r->{'ServiceType'} eq 'SA' ) { $ServiceName = 'Medicaid Substance Abuse'; }
    elsif ( $r->{'ServiceType'} eq 'SOCMH' ) { $ServiceName = 'Medicaid System Of Care'; }
    $list->{"$ServiceName"} = $r->{'ServiceType'};
  }
  $s->finish();
  return($list) if ( $rtnList );
  my $SelStmt = $self->makeSelect($form,$SelectedIDs,$list);
  return($SelStmt);
}
sub withCredIDs
{
  my ($self,$form,$ProvID,$Table,$Join) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
#warn qq|withCredIDs: ProvID=$ProvID,$ForProvID; Table=$Table\n|;

  # No restriction on Credentials; give them all Credentials...
  return('') if ( SysAccess->chkPriv($form,'BillingAdmin',$ForProvID) );

  my $table = $Table eq '' ? '' : $Table . '.';
  my $query = "${table}CredID is null";
  foreach my $r ( $self->getCredentials($form,$ForProvID) )
  {
    $query .= qq| or (${table}InsID='$r->{InsID}' and ${table}CredID='$r->{CredID}'|;
    $query .= $r->{Restriction} ? qq| and (${table}Restriction='$r->{Restriction}' or ${table}Restriction is null))| : ')';
  }
#warn qq|withCredIDs: query=$query\n|;
  return($Join eq 'where' ? 'where (' . $query . ')' : 'and (' . $query . ')');
}
sub getCredentials
{
  my ($self,$form,$ProvID) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my @records = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qCredentials = qq|select Credentials.* from Credentials left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID where ProvID='${ForProvID}' order by Credentials.Rank|;
#warn qq|getCredentials: qCredentials=$qCredentials\n|;
  my $sCredentials = $dbh->prepare($qCredentials);
  $sCredentials->execute() || myDBI->dberror("getCredentials->select ForProvID=$ForProvID");
  while ( my $rCredentials = $sCredentials->fetchrow_hashref )
  { push(@records,$rCredentials); }
  $sCredentials->finish();
  return(@records);
}
sub withClientInsIDs
{
  my ($self,$form,$ClientID,$Active,$Table,$Join) = @_;
  my $table = $Table eq '' ? '' : $Table . '.';
  my $query = "${table}InsID is null";
  foreach my $r ( $self->getClientInsurances($form,$ClientID,$Active) )
  { $query .= qq| or ${table}InsID='$r->{InsID}'|; }
  return($Join eq 'where' ? 'where (' . $query . ')' : 'and (' . $query . ')');
}
sub withNoteAccess
{
  my ($self,$form,$ProvID,$Table) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my $query = SysAccess->chkPriv($form,'OtherProvNotes',$ForProvID) 
            ? qq| ClientACL.ProvID='${ForProvID}' | 
            : qq| (ClientACL.ProvID='${ForProvID}' and ${Table}.ProvID=ClientACL.ProvID) |;
  return($query);
}
# New - used to check for clinic/provider selection needed (ClinicIDs/ProvIDs)
sub withClinicProvider
{ 
  my ($self,$form,$Join,$CField,$PField) = @_;
  my $query = '';
  my $delm = $Join eq 'where' ? 'where ' : 'and ';
  if ( $form->{ClinicIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ClinicID ( split(chr(253),$form->{ClinicIDs}) )
    { $stmt .= qq|${conj} ${CField}=${ClinicID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and ' }
  }
  if ( $form->{ProvIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ProvID ( split(chr(253),$form->{ProvIDs}) )
    { $stmt .= qq|${conj} ${PField}=${ProvID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
  if ( $form->{InsIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $InsID ( split(chr(253),$form->{InsIDs}) )
    { $stmt .= qq|${conj} xInsurance.ID=${InsID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
#warn qq|query=$query\n| if ( $form->{LOGINPROVID} == 91 );
  return($query);
}
# NEWEST - used to convert clinic/provider/client/trid to header
sub withSelectionHeader
{ 
  my ($self,$form) = @_;
  my $header = '';
  if ( $form->{ClinicIDs} )
  {
#warn qq|withSelectionHeader: ClinicIDs=$form->{ClinicIDs}\n| if ( $form->{LOGINPROVID} == 91 );
    foreach my $ClinicID ( split(chr(253),$form->{ClinicIDs}) )
    { $header .= DBA->getxref($form,'Provider',$ClinicID,'Name').' '; }
  }
  if ( $form->{ProvIDs} )
  {
#warn qq|withSelectionHeader: ProvIDs=$form->{ProvIDs}\n| if ( $form->{LOGINPROVID} == 91 );
    foreach my $ProvID ( split(chr(253),$form->{ProvIDs}) )
    { $header .= DBA->getxref($form,'Provider',$ProvID,'FName LName').' '; }
  }
  if ( $form->{InsID} )
  {
    $header .= DBA->getxref($form,'xInsurance',$form->{'InsID'},'Name').' ';
  }
  if ( $form->{InsIDs} )
  {
#warn qq|withSelectionHeader: InsIDs=$form->{InsIDs}\n| if ( $form->{LOGINPROVID} == 91 );
    foreach my $InsID ( split(chr(253),$form->{InsIDs}) )
    { $header .= DBA->getxref($form,'xInsurance',$InsID,'Name').' '; }
  }
#warn qq|withSelectionHeader: header=$header\n| if ( $form->{LOGINPROVID} == 91 );
  return($header);
}
# NEWEST - used to convert clinic/provider/client/trid to selection
sub withSelection
{ 
  my ($self,$form,$Join,$clinicField,$providerField,$clientField,$tridField) = @_;
  my $query = '';
  my $delm = $Join eq 'where' ? 'where ' : 'and ';
  if ( $form->{ClinicIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ClinicID ( split(chr(253),$form->{ClinicIDs}) )
    { $stmt .= qq|${conj} ${clinicField}=${ClinicID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and ' }
  }
  if ( $form->{ProvIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ProvID ( split(chr(253),$form->{ProvIDs}) )
    { $stmt .= qq|${conj} ${providerField}=${ProvID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
  if ( $form->{InsID} )
  {
    my ($stmt,$conj) = ('','');
    $stmt .= qq|${conj} xInsurance.ID=$form->{InsID} |;
    $query .= "${delm} ( ${stmt} )"; $delm = ' and ';
  }
  if ( $form->{InsIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $InsID ( split(chr(253),$form->{InsIDs}) )
    { $stmt .= qq|${conj} xInsurance.ID=${InsID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
  if ( $form->{ClientIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $ClientID ( split(chr(253),$form->{ClientIDs}) )
    { $stmt .= qq|${conj} ${clientField}=${ClientID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
  if ( $form->{TrIDs} )
  {
    my ($stmt,$conj) = ('','');
    foreach my $TrID ( split(chr(253),$form->{TrIDs}) )
    { $stmt .= qq|${conj} ${tridField}=${TrID} |; $conj = ' or '; }
    if ( $stmt ) { $query .= "${delm} ( ${stmt} )"; $delm = ' and '; }
  }
#warn qq|query=$query\n| if ( $form->{LOGINPROVID} == 91 );
  return($query);
}
sub getClientInsurances
{
  my ($self,$form,$ClientID,$Active) = @_;
  my @records = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qInsurance = qq|select * from Insurance where ClientID='${ClientID}' |;
  $qInsurance .= qq| and InsNumEffDate<=curdate() and (curdate()<=InsNumExpDate or InsNumExpDate is NULL) | if ( $Active );
  $qInsurance .= qq| order by InsNumEffDate desc, InsNumExpDate|;
#warn qq|getClientInsurance: qInsurance=$qInsurance\n|;
  my $sInsurance = $dbh->prepare($qInsurance);
  $sInsurance->execute() || myDBI->dberror("getClientInsurances->select ClientID=$ClientID,$Active");
  while ( my $rInsurance = $sInsurance->fetchrow_hashref )
  { push(@records,$rInsurance); }
  $sInsurance->finish();
  return(@records);
}
sub getMeds
{
  my ($self,$form,,$ClientID) = @_;
  my ($out,$cnt1,$cnt2) = ('',0,0);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $r = ();
  my $sClientMeds = $dbh->prepare("select * from ClientMeds where ClientID=? order by PrescriptionDate");
  $sClientMeds->execute($ClientID);
  while ( $rClientMeds = $sClientMeds->fetchrow_hashref )
  {
    $cnt1++;
    $r->{$cnt1}->{'ID'} = $rClientMeds->{'ID'};
    $r->{$cnt1}->{'PhysicianName'} = $rClientMeds->{'PhysicianName'};
    $r->{$cnt1}->{'DrugInfo'} = $rClientMeds->{'DrugInfo'};
    $r->{$cnt1}->{'DrugType'} = $rClientMeds->{'PatientFriendlySIG'};
    $r->{$cnt1}->{'DrugDate'} = $rClientMeds->{'PrescriptionDate'};
## NEEDED    $r->{$cnt1}->{'Reason'} = $rClientMeds->{'PharmacyFullInfo'};
#warn qq|getMeds: PhysicianName=$r->{'PhysicianName'}, cnt1=${cnt1}\n|;
  }
  $sClientMeds->finish();
  return($r) if ( $cnt1 );

  my $sPDMed = $dbh->prepare("select * from PDMed where ClientID=? order by MedEffDate");
  $sPDMed->execute($ClientID);
  while ( $rPDMed = $sPDMed->fetchrow_hashref )
  {
    $cnt2++;
    $r->{$cnt2}->{'ID'} = $rPDMed->{'ID'};
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$rPDMed->{'PhysNPI'});
    my $PhysicianName = $rxNPI->{'ProvLastName'};
    $PhysicianName .= ', ' . substr($rxNPI->{'ProvFirstName'},0,1) if ( $rxNPI->{'ProvFirstName'} ne '' );
    $r->{$cnt2}->{'PhysicianName'} = $PhysicianName;
    $r->{$cnt2}->{'DrugInfo'} = DBA->getxref($form,'xMedNames',$rPDMed->{MedID},'TradeName');
    my $DrugType = DBA->getxref($form,'xMedType',$rPDMed->{MedType},'Abbr').' '
                 . $rPDMed->{'MedDos'}.' '
                 . DBA->getxref($form,'xMedRoute',$rPDMed->{Route},'Descr').' '
                 . $rPDMed->{'MedFreq'};
    $r->{$cnt2}->{'DrugType'} = $DrugType;
    $r->{$cnt2}->{'DrugDate'} = $rPDMed->{StartDate};
#warn qq|getMeds: PhysicianName=$r->{'PhysicianName'}, cnt2=${cnt2}\n|;
  }
  $sPDMed->finish();
  return($r);
}
sub processNewCrop
{
  my ($self,$form,$ClientID) = @_;
  chdir("$form->{DOCROOT}/tmp");
  my $cmd = qq|/var/www/okmis/src/bin/gp6 DBNAME=$form->{DBNAME}\\&mlt=$form->{mlt}\\&ClientID=${ClientID}|;
  my $diskfile = DBUtil->ExecCmd($cmd);
  my $out = DBUtil->ReadFile($diskfile);
  return('<PRE>'.$out.'</PRE>');
}

############################################################################
# Update information in SQL Tables.
sub updSQLdone
{
  my ($self, $form) = @_;
  return(0) if ( $form->{'FORMID'} eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $q = qq|select * from UpdDone where FORMID=$form->{'FORMID'}|;
#warn qq|DBA:updSQLdone: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  if ( my $r = $s->fetchrow_hashref )
  {
    $form->{prompt} .= chr(253) . qq|Multiple 'Submit', 'Back Button' or 'Refresh' used.\\nNo Updates performed, already done.|;
#warn qq|DBA:updSQLdone: YES, prompt=$form->{prompt}\n|;
    $s->finish();
    return(1);
  }
  $q = qq|insert into UpdDone (FORMID,LOGINID) values ('$form->{FORMID}','$form->{LOGINID}')|;
#warn qq|DBA:updSQLdone: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  $s->finish();
#warn qq|DBA:updSQLdone: NO, prompt=$form->{prompt}\n|;
  return(0);
}
##
# used by mis.cgi UpdateTables section.
##
sub updSQL
{
  my ($self,$form) = @_;

#foreach my $f ( sort keys %{$form} ) { warn "updSQL: form-$f=$form->{$f}\n"; }
#warn qq|DBA:updSQL: UpdateTables=$form->{UpdateTables}, OPENTABLES=$form->{OPENTABLES}\n|;
  return('') if ( DBA->updSQLdone($form) );
#warn qq|DBA:updSQL:inside: UpdateTables=$form->{UpdateTables}, OPENTABLES=$form->{OPENTABLES}\n|;

  my @TABLES = ();
  my @DELETES = (); 
  delete $form->{'RECORDDELETES'};

  
  if ( $form->{'UpdateTables'} eq 'all' )
  { @TABLES = split(/,/,$form->{'OPENTABLES'}); }
  else
  { 
    foreach my $t ( split(/,/,$form->{'UpdateTables'}) )
    { push(@TABLES,$t); }
  }

##
# WATCH for any pre_update routines that may insert/update tables that are LOCKED!
##
#warn "updSQL: pre_update=$form->{'pre_update'}\n";
  $pre_update = myDBI->exFunc($form,$form->{'pre_update'}) if ( defined($form->{"pre_update"}) );
  delete $form->{'pre_update'};
##
  foreach my $TABLE ( @TABLES )
  {
#warn qq|DBA:updSQL:loop: table=$TABLE\n|;
    next if ( DBA->locked($form,$TABLE) );

#warn "mis: UPDATE getFields=$TABLE, ClientID=$form->{Client_ClientID}/$form->{Client_ClientID_1}\n";
    my $rData = DBA->getFields($form,$TABLE);
#warn "rData=$rData\n";
#foreach my $f ( sort keys %{$rData} ) { warn "mis: rData-$f=$rData->{$f}\n"; }
    my $eData = DBA->recExist($form,$TABLE,$rData);
#warn "eData=$eData\n";
#foreach my $f ( sort keys %{$eData} ) { warn "mis: eData-$f=$eData->{$f}\n"; }
#warn "NOT eData!\n" if ( !$eData );
#warn "YES eData!\n" if ( $eData );
#warn "rData->FormID=$rData->{FormID}, eData->FormID=$eData->{FormID}\n";
    DBA->setUpdates($form,$TABLE,$rData);
#warn "rData->BilledAmt=$rData->{BilledAmt}, eData->BilledAmt=$eData->{BilledAmt}\n";
    my ($UpdFlag,$uData) = DBA->difFields($form,$TABLE,$rData,$eData);
#foreach my $f ( sort keys %{$uData} ) { warn "updSQL: uData-$f=$uData->{$f}\n"; }
#warn "updSQL: UpdFlag = $UpdFlag!\n";
    if ( $UpdFlag )
    {
      DBA->setDefaults($form,$TABLE,$rData,$uData);
      DBA->xSQL($form,$UpdFlag,$TABLE,$rData,$uData);
      push(@DELETES,$form->{'RECORDDELETES'}) unless ( $form->{'RECORDDELETES'} eq '' );
    }
  } 
##
# WATCH for any post_update routines that may insert/update tables that are LOCKED!
#warn "CALL POST_UPDATE: $form->{'post_update'}\n";
  my $function = $form->{'post_update'};
#warn "updSQL: post_update=${function}\n";
  delete $form->{'post_update'};
  $post_update = myDBI->exFunc($form,$function) if ( defined($function) );
# this was moved from xSQL 'delete' section to here
#   because the post_update may update records and recreate them
#   so delete them after post_updates.
#warn "updSQL: DELETES=@DELETES\n";
  foreach my $d ( @DELETES )
  {
    my ($table,$id) = split('-',$d);
#warn "updSQL: BEFORE delSubTables: d=${d}, table=${table},id=${id}\n";
    my $RECID = myDBI->getTableConfig($table,'RECID');
    my $DBCFGNAME = myDBI->getTableConfig($table,'DBCFGNAME');
    my $DBNAME = $DBCFGNAME eq '' ? $form->{'DBNAME'} : $DBCFGNAME;
#warn qq|updSQL: inTable=$inTable, DBCFGNAME=${DBCFGNAME}, DBNAME=${DBNAME}\n|;
    my $dbh = myDBI->dbconnect($DBNAME);
#warn qq|prepare("delete from ${table} where ${RECID}='${id}'");\n|;
    my $s = $dbh->prepare("delete from ${table} where ${RECID}='${id}'");
    $s->execute() || myDBI->dberror("delete from ${table} where ${RECID}='${id}'");
    $s->finish();
    my $delmsg = DBA->delSubTables($form,$table,$id);
  }

#warn "DONE POST_UPDATE: $post_update\n";
##
# Close/Clear our internal array.
#   Do this AFTER updates to leave Header tables Open for Detail tables to use.
##
  foreach my $TABLE ( @TABLES )
  { DBA->clrFields($form,$TABLE); delete $form->{'OPENTABLE:'. $TABLE}; }
  delete $form->{'OPENTABLES'};
  delete $form->{'UpdateTables'};
  delete $form->{'updLINKIDcur'};
#foreach my $f ( sort keys %{$form} ) { warn "after clrFields: form-$f=$form->{$f}\n"; }
#warn "mis: IN UpdateTables view=$form->{view}\n";
  return($post_update);
}
############################################################################
sub isADULT
{
  my ($self,$form,$DOB,$inDate) = @_;
  my $asofDate = $inDate eq '' ? $form->{'TODAY'} : $inDate;
  my $Age = DBUtil->Date($DOB,'age',$asofDate);
  my $isADULT = $Age >= 18 ? 1 : 0;
#warn "DBA: isADULT: DOB=${DOB}, Age=${Age}, isADULT=${isADULT}\n";
  return($isADULT);
}
sub isCHILD
{
  my ($self,$form,$DOB,$inDate) = @_;
  my $asofDate = $inDate eq '' ? $form->{'TODAY'} : $inDate;
  my $Age = DBUtil->Date($DOB,'age',$asofDate);
  my $isCHILD = $Age < 18 ? 1 : 0;
#warn "DBA: isCHILD: DOB=${DOB}, Age=${Age}, isCHILD=${isCHILD}\n";
  return($isCHILD);
}
sub checkFields
{
  my ($self, $form, $r) = @_;
  my $result = qq|
<HR WIDTH=100% >
<TABLE CLASS="homeheading" > <TR > <TD CLASS="portsublabel" >
<HR WIDTH=100% >
|;
  foreach my $f ( sort keys %{$form} )
  {
    warn "checkFields: form-$f=$form->{$f}\n";
    $result .= qq|checkFields: form-$f=$form->{$f}<BR>|;
  }
  foreach my $f ( sort keys %{$r} )
  {
    warn "checkFields: r-$f=$r->{$f}\n";
    $result .= qq|checkFields: r-$f=$r->{$f}<BR>|;
  }
  $result .= qq|
</TD> </TR> </TABLE>
<HR WIDTH=100% >
|;
  return($result);
}
############################################################################
sub setClientASI
{
  my ($self,$form) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $form->{'Client_ClientID'};
  # refresh these if record empty.
  my $s = $dbh->prepare("select Client.SSN,ClientRelations.ResAdmitDate,Client.Gend,Client.DOB,Client.Race from Client left join ClientRelations on ClientRelations.ClientID=Client.ClientID where Client.ClientID=?");
  $s->execute($ClientID) || myDBI->dberror("setClientASI: select Client/ClientRelations ${ClientID}");
  my ($SSN,$ResAdmitDate,$Gend,$DOB,$Race) = $s->fetchrow_array;
  $q = qq|select StaffID from ClientIntake where ClientID='$ClientID'|;
#warn qq|setClientASI: q=$q\n|;
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  my ($StaffID) = $s->fetchrow_array;
# set these if null...refresh because they might have entered the ASI before entering.
  $form->{'ClientASI_G2_1'} = $SSN if ( $form->{'ClientASI_G2_1'} eq '' );
  $form->{'ClientASI_G4_1'} = $ResAdmitDate if ( $form->{'ClientASI_G4_1'} eq '' );
  $form->{'ClientASI_G10_1'} = $Gend if ( $form->{'ClientASI_G10_1'} eq '' );
  $form->{'ClientASI_G16_1'} = $DOB if ( $form->{'ClientASI_G16_1'} eq '' );
  $form->{'ClientASI_G17_1'} = $Race if ( $form->{'ClientASI_G17_1'} eq '' );
  $form->{'ClientASI_G11_1'} = $StaffID if ( $form->{'ClientASI_G11_1'} eq '' );
#warn qq|$SSN,$ResAdmitDate,$Gend,$DOB,$Race,$StaffID\n|;
  $s->finish();
  return;
}
sub setAlert
{
  my ($self,$form,$text,$ForProvID) = @_;
#warn qq|setAlert: text=${text}, ${ForProvID}\n|;
  my $dbname = $form->{DBNAME};                 # name of this current database.
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  return(0) if ( $text eq '' );
  my $msg = $cdbh->quote($text);
  my $ProvID = $ForProvID ? $ForProvID : $form->{LOGINPROVID};
  my $s = $cdbh->prepare("insert into xAlert values (?,?,?,NULL)");
  $s->execute($dbname,$ProvID,$msg) || myDBI->dberror("FAILED: ${ProvID}: xAlert add message");
  $s->finish();
#warn qq|setAlert: text inserted\n|;
  return(1);
}
sub getAlert
{
  my ($self,$form,$ForProvID) = @_;
#warn qq|getAlert: ${ForProvID}\n|;
  my $dbname = $form->{DBNAME};                 # name of this current database.
  my $cdbh = myDBI->dbconnect('okmis_config');  # connect to the config database.
  my @text=(); my $cnt=0;
  my $ProvID = $ForProvID ? $ForProvID : $form->{LOGINPROVID};
  my $s = $cdbh->prepare("select Descr from xAlert where db='${dbname}' and ProvID='${ProvID}'");
  $s->execute() || myDBI->dberror("getAlert: select: ${dbname} ${ProvID}");
  while ( my ($Descr) = $s->fetchrow_array )
  { $cnt++; (my $msg = $Descr) =~ s/^'(.*)'$/$1/; push(@text,$msg); }
  $s->finish();
  if ( $cnt )
  {
#warn qq|getAlert: cnt=${cnt}, text=@text\n|;
    my $s = $cdbh->prepare("delete from xAlert where db='${dbname}' and ProvID='${ProvID}'");
    $s->execute() || myDBI->dberror("getAlert: delete: ${dbname} ${ProvID}");
    $s->finish();
  }
#warn qq|getAlert: text retrieved\n|;
  return(@text);
}
sub setAxis4
{
  my ($self,$form,$spc,$rDiag) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($Axis4,$delm) = ('','');
  $sxAxis4 = $dbh->prepare("select * from xAxis4 order by ID");
  $sxAxis4->execute() || myDBI->dberror("select xAxis4 error");
  while ( my $rxAxis4 = $sxAxis4->fetchrow_hashref )
  { 
    my $Descr = $rxAxis4->{'Descr'};                        # check field value
#warn qq|Descr=$Descr, value=$rDiag->{$Descr}\n|;
    if ( $rDiag->{$Descr} > 0 )                             # of incoming record set?
    { $Axis4 .= qq|${delm}$rxAxis4->{'Text'}|; $delm=$spc; } # return text.
  }
  $sxAxis4->finish();
  return($Axis4);
}
############################################################################
sub subchr
{
  my ($self,$in) = @_;
#warn qq|subchr: in=${in}\n|;
  my $out = $in;
  my $dlm = chr(253);
  $out =~ s/$dlm/ /g;            # this is our multi-value separator
  $out =~ s/\r//g;               # carriage return
  $out =~ s/\n/ /g;              # new line
  $out =~ s/\t/ /g;              # tab to space
  $out =~ s/
/ /g;              # new line
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�//g;
  $out =~ s/�/a/g;
  $out =~ s/�/e/g;
  $out =~ s;�;one-half;g;
#warn qq|subchr: out=${out}\n|;
  return($out);
}
sub subxml
{
  my ($self,$in) = @_;
#warn qq|subxml: in=${in}\n|;
  my $xml = $in;
  my $dlm = chr(253);
     $xml =~ s/$dlm/ /g;            # this is our multi-value separator
     $xml =~ s/&/&#38;/g;           # ampersand: FIRST so we don't change others!
     $xml =~ s/'/&#x27;/g;          # apostrophe: had to use hex for xml
     $xml =~ s/"/&#34;/g;           # double quotation: had to use dec for xml??
     $xml =~ s/</&#60;/g;           # less-than sign
     $xml =~ s/>/&#62;/g;           # greater-than sign
     $xml =~ s/\r//g;               # carriage return
     $xml =~ s/\n/ /g;              # new line
     $xml =~ s/\t/ /g;              # tab to space
     $xml =~ s/
/ /g;              # new line
     $xml =~ s/�/e/g;
     $xml =~ s;�;one-half;g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
     $xml =~ s/�//g;
#     $xml =~ s/&#8194;//g;         # HTML code for 'en space'
     $xml =~ s/�//g;
     $xml =~ s/�/a/g;
#     $xml =~ s/ > / greater /g;
#     $xml =~ s/ < / less /g;
#     $xml =~ s/fianc�/fiance/g;
#warn qq|subxml: xml=${xml}\n|;
  return($xml);
}
sub subCHAR
{
  my ($self,$in,$def) = @_;
#warn qq|subCHAR: in=${in}\n|;
  my $out = $in;
  my $dlm = chr(253);
     $out =~ s/$dlm/ /g;            # this is our multi-value separator
     $out =~ s/&/&#38;/g;           # ampersand: FIRST so we don't change others!
     $out =~ s/'/&#x27;/g;          # apostrophe: had to use hex for out
     $out =~ s/"/&#34;/g;           # double quotation: had to use dec for out??
     $out =~ s/</&#60;/g;           # less-than sign
     $out =~ s/>/&#62;/g;           # greater-than sign
     $out =~ s/\r//g;               # carriage return
     $out =~ s/\n/ /g;              # new line
     $out =~ s/\t/ /g;              # tab to space
     $out =~ s/
/ /g;              # new line
     $out =~ s/�/e/g;
     $out =~ s;�;one-half;g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�//g;
     $out =~ s/�/a/g;
#warn qq|subCHAR: out=${out}\n|;
  return($out);
}
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
sub SignTrPlan
{
  my ($self,$form,$TrPlanID) = @_;
  my $out = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|DBA: SignTrPlan: LOGINPROVID=$form->{LOGINPROVID}, TrPlanID=${TrPlanID}|;
  return() unless ( $TrPlanID );
  return() if ( $TrPlanID eq 'new' );
  my $sTest = $dbh->prepare("select * from ClientTrPlanS where TrPlanID=? and ProvID=?");
  $sTest->execute($TrPlanID,$form->{'LOGINPROVID'}) || myDBI->dberror("SignTrPlan: Test ${TrPlanID}/$form->{LOGINPROVID}");
  if ( my $rTest = $sTest->fetchrow_hashref )
  { $out .= qq|SKIPPED: Already Signed $form->{'LOGINPROVID'}/${TrPlanID}\n|; }
  else
  {
    my ($s, $m, $h, $day, $mon, $year) = localtime;
    my $curtime = sprintf('%02d:%02d:%02d', $h, $m, $s);
    my $r = ();
    $r->{ClientID} = $form->{'Client_ClientID'};
    $r->{TrPlanID} = $TrPlanID;
    $r->{CreateProvID} = $form->{'LOGINPROVID'};
    $r->{CreateDate} = $form->{TODAY};
    $r->{ChangeProvID} = $form->{'LOGINPROVID'};
    $r->{ProvID} = $form->{'LOGINPROVID'};
    $r->{SignDate} = $form->{'TODAY'};
    $r->{SignTime} = $curtime;
    my $qInsert = DBA->genInsert($form,'ClientTrPlanS',$r);
#warn qq|DBA: SignTrPlan: qInsert=$qInsert\n|;
    my $sInsert = $dbh->prepare($qInsert);
    $sInsert->execute() || myDBI->dberror($qInsert);
    $sInsert->finish();
    $out .= qq|SIGNED: ${TrPlanID} by $form->{'LOGINPROVID'}\n|;
  }
  $sTest->finish();
  return($out);
}
sub isTrPlanSigned
{
  my ($self,$form,$TrPlanID,$row,$links) = @_;
#foreach my $f ( sort keys %{$form} ) { warn "isTrPlanSigned: form-$f=$form->{$f}\n"; }
  return("** Remember to sign the Treatment Plan when complete.") if ( $TrPlanID eq 'new' );
  my $out = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from ClientTrPlanS left join Provider on Provider.ProvID=ClientTrPlanS.ProvID where ClientTrPlanS.TrPlanID=? and ClientTrPlanS.ProvID=?");
  $s->execute($TrPlanID,$form->{'LOGINPROVID'}) || myDBI->dberror("isTrPlanSigned: ${TrPlanID}/$form->{'LOGINPROVID'}");
  if ( my $r = $s->fetchrow_hashref )
  {
    my $SignDate = DBUtil->Date($r->{'SignDate'},'fmt','MM/DD/YYYY');
    my $SignTime = DBUtil->AMPM($r->{'SignTime'});
    my $when = $SignTime eq '' ? $SignDate : qq|${SignDate} @ ${SignTime}|;
    $out .= qq|** Treatment Plan Signed by you.|;
  }
  else
  {
    my $add = myConfig->cfgfile('add.png',1);
    $out .= qq|** Click below for<BR><DIV CLASS="heading" >$form->{'LOGINUSERNAME'}</DIV>to sign Treatment Plan **<BR>
      <A HREF="javascript:callAjax('ListClientTrPlanS','yes','ListClientTrPlanS','&${links}&row=${row}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="Sign Treatment Plan">Click here to Sign<IMG SRC="${add}" HEIGHT="20" WIDTH="20" ></A>
|;
  }
  $s->finish();
  my $html = qq|      <TD CLASS="colstr" WIDTH="25%" >${out}</TD>\n|;
  return($html);
}
sub listNoteTrPlan
{
  my ($self,$form,$TrPlanID) = @_;
#warn qq|\nlistNoteTrPlan: TrPlanID=${TrPlanID}\n|;
  return() unless ( $TrPlanID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientTrPlan = $dbh->prepare("select Locked from ClientTrPlan where ID=?");
  $sClientTrPlan->execute($TrPlanID) || myDBI->dberror("listNoteTrPlan: select ClientTrPlan ${TrPlanID}");
  my ($Locked) = $sClientTrPlan->fetchrow_array;
  $sClientTrPlan->finish();
  my $txt = $Locked ? 'LOCKED' : 'NOT LOCKED<BR>(have Primary Provider sign)';
  my $out = '';
  my $sClientNoteTrPlanPG = $dbh->prepare("select ClientNoteTrPlanPG.TrID, DATE_FORMAT(Treatment.ContLogDate,'%m/%d/%Y') as ContDate from ClientNoteTrPlanPG left join Treatment on Treatment.TrID=ClientNoteTrPlanPG.TrID left join ClientTrPlanPG on ClientTrPlanPG.ID=ClientNoteTrPlanPG.TrPlanPGID left join ClientTrPlan on ClientTrPlan.ID=ClientTrPlanPG.TrPlanID where ClientTrPlan.ID=? group by ClientNoteTrPlanPG.TrID");
  $sClientNoteTrPlanPG->execute($TrPlanID) || myDBI->dberror("listNoteTrPlan: select ClientNoteTrPlanPG ${TrPlanID}");
  while ( my ($TrID,$ContDate) = $sClientNoteTrPlanPG->fetchrow_array )
  { $out .= qq|${TrID} ${ContDate}<BR>|; $lock = $Locked; }
  $sClientNoteTrPlanPG->finish();
  my $html = qq|Treatment Plan ${txt}<BR>Notes with Problems/Goals checked<BR>TrID ContactDate<BR>${out}|;
  return($html);
}
sub allowDelTrPlanS
{
  my ($self,$form,$TrPlanSID,$row,$links) = @_;
  my $out = '';
  $out .= qq|
      <A HREF="javascript:callAjax('ListClientTrPlanS','delete','ListClientTrPlanS','&sid=${TrPlanSID}&${links}&row=${row}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="Click to delete"><IMG SRC="/img/delete.png" HEIGHT="20" WIDTH="20" ></A>
| if ( SysAccess->verify($form,'Privilege=Agent') );
  return($out);
}
## by TrPlanID or TrID, if TrID select the TrPlanID (TPID).
sub lockTrPlan
{
  my ($self,$form,$TrPlanID,$TrID) = @_;
#warn qq|\nlockTrPlan: TrPlanID=${TrPlanID}, TrID=${TrID}\n|;
  return() unless ( $TrPlanID || $TrID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $TPID = $TrPlanID;        # could change via TrID.

# if given TrID then find the Treatment Note TrPlanID...
  if ( $TrID )
  {
    my $sClientNoteTrPlanPG = $dbh->prepare("select ClientTrPlanPG.TrPlanID from ClientNoteTrPlanPG left join ClientTrPlanPG on ClientTrPlanPG.ID=ClientNoteTrPlanPG.TrPlanPGID where ClientNoteTrPlanPG.TrID=? group by ClientTrPlanPG.TrPlanID");
    $sClientNoteTrPlanPG->execute($TrID) || myDBI->dberror("lockTrPlan: select ClientNoteTrPlanPG ${TrID}");
    ($TPID) = $sClientNoteTrPlanPG->fetchrow_array;
    $sClientNoteTrPlanPG->finish();
  }

#warn qq|lockTrPlan: UNLOCK/LOCK TPID=${TPID}\n|;
# first unlock the Treatment Plan...
  $self->lockTrPlanID($form,0,$TPID);
# then lock the Treatment Plan...
  $self->lockTrPlanID($form,1,$TPID);

  return(1);
}
sub lockTrPlanID
{
  my ($self,$form,$flag,$TrPlanID) = @_;
#warn qq|\nlockTrPlan: flag=${flag}, TrPlanID=${TrPlanID}\n|;
  return() unless ( $TrPlanID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});

# ON LOCK, check that the Primary Provider has Signed the TrPlan...
  if ( $flag )
  {
    my $sTrPlanS = $dbh->prepare("select Client.ProvID,ClientTrPlanS.ProvID from ClientTrPlanS left join Client on Client.ClientID=ClientTrPlanS.ClientID where ClientTrPlanS.TrPlanID=? and Client.ProvID=ClientTrPlanS.ProvID");
    $sTrPlanS->execute($TrPlanID) || myDBI->dberror("lockTrPlan: ClientTrPlanS ${TrPlanID}");
    my $cnt = $sTrPlanS->rows;
#warn qq|lockTrPlan: cnt=$cnt, TrPlanID=${TrPlanID}\n|;
    $sTrPlanS->finish();
    return(1) unless ( $cnt );
  }

  my $sLockTP = $dbh->prepare("update ClientTrPlan set Locked=? where ID=?");
  my $sLockPG = $dbh->prepare("update ClientTrPlanPG set Locked=? where TrPlanID=?");
  my $sLockOBJ = $dbh->prepare("update ClientTrPlanOBJ set Locked=? where TrPlanPGID=?");
  my $sClientTrPlanPG = $dbh->prepare("select ID from ClientTrPlanPG where TrPlanID=?");
  $sClientTrPlanPG->execute($TrPlanID) || myDBI->dberror("lockTrPlanID: select ClientTrPlanPG ${TrPlanID}");
  while ( my ($TrPlanPGID) = $sClientTrPlanPG->fetchrow_array )
  {
#warn qq|lockTrPlan: OBJ: flag=${flag}, TrPlanID=${TrPlanID}, TrPlanPGID=${TrPlanPGID}\n|;
    $sLockOBJ->execute($flag,$TrPlanPGID) || myDBI->dberror("lockTrPlanID: LOCK TrPlanOBJ: ${TrPlanPGID}");
  }
#warn qq|lockTrPlan: PG: flag=${flag}, TrPlanID=${TrPlanID}\n|;
  $sLockPG->execute($flag,$TrPlanID) || myDBI->dberror("lockTrPlan: LOCK TrPlanPG: ${TrPlanID}");
#warn qq|lockTrPlan: flag=${flag}, TrPlanID=${TrPlanID}\n|;
  $sLockTP->execute($flag,$TrPlanID) || myDBI->dberror("lockTrPlan: LOCK TrPlan: ${TrPlanID}");

  $sClientTrPlanPG->finish();
  $sLockOBJ->finish();
  $sLockPG->finish();
  $sLockTP->finish();
  return(1);
}
sub listNoteProblems
{
  my ($self,$form,$UUID) = @_;
#warn qq|\nlistNoteProblems: UUID=${UUID}\n|;
  return() unless ( $UUID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out = '';
  my $sClientNoteProblems = $dbh->prepare("select ClientNoteProblems.TrID, DATE_FORMAT(Treatment.ContLogDate,'%m/%d/%Y') as ContDate from ClientNoteProblems inner join Treatment on Treatment.TrID=ClientNoteProblems.TrID inner join ClientProblems on ClientProblems.UUID=ClientNoteProblems.UUID and ClientNoteProblems.ClientID=ClientProblems.ClientID where ClientProblems.ID=? order by Treatment.ContLogDate");
  $sClientNoteProblems->execute($UUID) || myDBI->dberror("listNoteProblems: select ClientNoteProblems ${UUID}");
  while ( my ($TrID,$ContDate) = $sClientNoteProblems->fetchrow_array )
  { $out .= qq|${TrID} ${ContDate}<BR>|; $lock = $Locked; }
  $sClientNoteProblems->finish();
#warn qq|listNoteProblems: out=${out}\n|;
  my $html = qq|Problem ${txt}<BR>Notes with Problem checked<BR>TrID ContactDate<BR>${out}|;
#warn qq|listNoteProblems: html=${html}\n|;
  return($html);
}
sub listContractValues
{
  my ($self,$form,$rContracts) = @_;
#warn qq|\nlistContractValues: UUID=${UUID}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "listContractValues: form-$f=$form->{$f}\n"; }
#foreach my $f ( sort keys %{$rContracts} ) { warn "listContractValues: rContracts-$f=$rContracts->{$f}\n"; }
  $out .= qq|$rxInsurance->{Name} ($rxInsurance->{ID})\t$rxInsurance->{Descr}\t$rxInsurance->{PayID}\t$rxInsurance->{ClearingHouse}\t${remit}\t${help}\n|;
  my $setContract = $rContracts->{'setContract'} eq 'N' ? 'n/a' : $rContracts->{'setContract'} eq '1' ? 'yes' : 'no';
  my $setPA = $rContracts->{'setPA'} eq 'N' ? 'n/a' : $rContracts->{'setPA'} eq '1' ? 'yes' : 'no';
  my $setInsEFT = $rContracts->{'setInsEFT'} eq 'N' ? 'n/a' : $rContracts->{'setInsEFT'} eq '1' ? 'yes' : 'no';
  my $setBillEFT = $rContracts->{'setBillEFT'} eq 'N' ? 'n/a' : $rContracts->{'setBillEFT'} eq '1' ? 'yes' : 'no';
  my $remit = $rContracts->{'ClearingHouseRemit'} == 1 ? 'yes' : 'no';
  my $autoRec = $rContracts->{'AutoReconcile'} == 1 ? 'yes' : 'no';
  my $autoPay = $rContracts->{'AutoPay'} == 1 ? 'yes' : 'no';
  my $html = qq|Setup<BR>Contract: ${setContract}<BR>PA: ${setPA}<BR>EFT: ${setInsEFT}<BR>ERA: ${setBillEFT}<BR><BR>Description: $rContracts->{'Descr'}<BR>Payer ID: $rContracts->{'PayID'}<BR>ClearingHouse: $rContracts->{'ClearingHouse'}<BR>Remit: ${remit}<BR>Auto Reconcile: ${autoRec}<BR>Auto Pay: ${autoPay}|;
#warn qq|listContractValues: html=${html}\n|;
  return($html);
}
#############################################################################
sub getLogo
{
  my ($self,$form,$type,$id,$encode) = @_;
#warn qq|getLogo: type=$type, id=$id\n|;
  my $AgencyID = $id;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  if ( $type eq 'Client' )
  {
    my $sClient = $dbh->prepare("select * from Client where ClientID=?");
    $sClient->execute($id) || myDBI->dberror("getLogo: select Client ${id}");
    my $rClient = $sClient->fetchrow_hashref;
    $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
    $sClient->finish();
  }
  elsif ( $type eq 'Provider' || $type eq 'Clinic' )
  { $AgencyID = MgrTree->getAgency($form,$id); }
  my $sAgencyControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  $sAgencyControl->execute($AgencyID) || myDBI->dberror("getLogo: select ProviderControl ${AgencyID}");
  my $rAgencyControl = $sAgencyControl->fetchrow_hashref;
  $sAgencyControl->finish();
  return() if ( $rAgencyControl->{'LOGO'} eq '' );
  my $imgFile = $form->{'DOCROOT'}.$rAgencyControl->{'LOGO'};
  return('not found') unless ( -f "${imgFile}" );
  my $logo = DBA->getImage($imgFile,$encode);
  return($logo);
}
sub getImage
{
  my ($self,$imgFile,$flag) = @_;
#warn qq|getImage: imgFile=$imgFile, flag=$flag\n|;
  open IMAGE, "<${imgFile}" or die "Couldn't open file: $!";
  my $raw_string = do{ local $/ = undef; <IMAGE>; };
  my $encoded = $flag ? encode_base64( $raw_string ) : $raw_string;
  close(IMAGE);
  return($encoded);
}
sub setEDocTags
{ 
  my ($self,$form,$ProvID,$Tags) = @_;
  my @Tabs = ();
  my $table = $ProvID == 90 ? 'MISEDocs' : 'ProviderEDocs';
  my $dbh = $ProvID == 90
          ? myDBI->dbconnect('okmis_config')
          : myDBI->dbconnect($form->{'DBNAME'});
#warn qq|\nsetEDocTags: Tags=$Tags\n|;
  foreach my $Tag ( split(':',$Tags) )
  {
    #next if ( $Tag eq '' );  
    my $with = $Tag eq '' ? qq|and (${table}.Type='' or ${table}.Type is null)| : qq|and xEDocTags.Tag='${Tag}'|;
    my $s=$dbh->prepare("select ${table}.*, xEDocTags.Tag from ${table} left join okmis_config.xEDocTags on xEDocTags.ID=${table}.Type where ${table}.ProvID='${ProvID}' and ${table}.Public=1 ${with} order by ${table}.Title");
    my $header = $Tag eq '' ? 'No Tag' : $Tag;
    my $html = qq|
<TABLE CLASS="home" >
  <TR CLASS="home" ><TD CLASS="hdrtxt" >${header}</TD></TR>
|;
    $s->execute();
    my $cnt = $s->rows;
    while ( my $r = $s->fetchrow_hashref )
    {
#warn qq|$r->{'ID'}:\n|;
#warn qq|  Title=$r->{'Title'}\n|;
#warn qq|  Path=$r->{'Path'}\n|;
#warn qq|  Link=$r->{'Link'}\n|;
foreach my $f ( sort keys %{ $r } ) { warn qq|: r-$f=$r->{$f}\n|; }
      my ($path,$file) = $r->{'Path'} =~ /(.*\/)?(.+)/s;
      my $href = $r->{'Link'} eq ''
               ? $ProvID == 90 
                 ? qq|http://forms.okmis.com/${ProvID}/${Tag}:${file}|
                 : $r->{'Path'}
               : $r->{'Link'};
#warn qq|\nfilepath=$r->{'Path'}, p=$path, f=$file\n|;
#warn qq|NO TAG:  Path=$r->{'Path'}\nhref=${href}\n| if ( $Tag eq '' );
      my $textlink = $r->{'Title'} eq '' ? 'MISSING Title ID: '.$r->{'ID'} : $r->{'Title'};
      $html .= qq|
  <TR>
    <TD CLASS="port title" >
      <A HREF="javascript:ReportWindow('${href}','FormsWindow')" >${textlink}</A>
    </TD>
  </TR>
|;
  
    }
    $s->finish();
    $html .= qq|
</TABLE>
|;
    my $tabcontent = $Tag.chr(253).$html;
    push(@Tabs,$tabcontent);
  }
  my $out = gHTML->setTab('','.85em arial',@Tabs);
  return($out);
}
sub check90
{
  my ($self,$form) = @_;
  my $a = SysAccess->chkPriv($form,'ProviderEDocs');
  my $ok = $form->{Provider_ProvID} == 90 ? 0 : SysAccess->chkPriv($form,'ProviderEDocs') ? 1 : 0;
#warn qq| ProvID=$form->{Provider_ProvID}, ok=$ok, a=$a\n|;
  return($ok);
}
sub setProviderCDAparms
{
  my ($self,$form,$ProvID) = @_;
#warn qq|\nENTER setProviderCDAparms: ProvID=${ProvID}\n|;
  return() unless ( $ProvID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProviderCDAparms = $dbh->prepare("select * from ProviderCDAparms where ProvID=? order by Priority");
  $sProviderCDAparms->execute($ProvID) || myDBI->dberror("setProviderCDAparms: select ProviderCDAparms ${ProvID}");
  my $cnt = $sProviderCDAparms->rows;
  if ( $cnt == 0 )
  {
    my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
    my $s=$cdbh->prepare("select * from xCDAparms");
    $s->execute();
    while ( my $r = $s->fetchrow_hashref )
    {
      my $rProviderCDAparms = ();
      $rProviderCDAparms->{'CreateProvID'} = $form->{'LOGINPROVID'};
      $rProviderCDAparms->{'CreateDate'} = $form->{'TODAY'};
      $rProviderCDAparms->{'ChangeProvID'} = $form->{'LOGINPROVID'};
      $rProviderCDAparms->{'ProvID'} = $ProvID;
      $rProviderCDAparms->{'Descr'} = $r->{'Descr'};
      $rProviderCDAparms->{'Priority'} = $r->{'Priority'};
      $rProviderCDAparms->{'Visible'} = $r->{'Visible'};
      $rProviderCDAparms->{'Exclude'} = $r->{'Exclude'};
      $rProviderCDAparms->{'Locked'} = $r->{'Locked'};
      $rProviderCDAparms->{'Active'} = $r->{'Active'};
#foreach my $f ( sort keys %{$rProviderCDAparms} ) { warn "setProviderCDAparms: rProviderCDAparms-$f=$rProviderCDAparms->{$f}\n"; }
      my $UPDID = DBA->doUpdate($form,'ProviderCDAparms',$rProviderCDAparms,"ProvID='${ProvID}' and Descr='$rProviderCDAparms->{Descr}'");
    }
    $s->finish();
  }
  $sProviderCDAparms->finish();
  my $html = qq|${cnt} found.|;
#warn qq|setProviderCDAparms: html=${html}\n|;
  return($html);
}
sub listDeviceID
{
  my ($self,$form,$ID) = @_;
#warn qq|\nlistDeviceID: ID=${ID}\n|;
  return() unless ( $ID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientProcedures = $dbh->prepare("select * from ClientProcedures where ID=?");
  $sClientProcedures->execute($ID) || myDBI->dberror("listDeviceID: select ClientProcedures ${ID}");
  my $r = $sClientProcedures->fetchrow_hashref;
#foreach my $f ( sort keys %{$r} ) { warn "listDeviceID: r-$f=$r->{$f}\n"; }
  $sClientProcedures->finish();
  my $popup = qq|<TABLE>|;
  $popup .= qq|<TR><TD>error</TD><TD>$r->{'error'}</TD></TR>| if ( $r->{'error'} ne '' );
  $popup .= qq|<TR><TD>Device Identifier</TD><TD>$r->{'donation_id'}</TD></TR>|;
  $popup .= qq|<TR><TD>Issuing Agency</TD><TD>$r->{'issuing_agency'}</TD></TR>|;
  $popup .= qq|<TR><TD>LotBatch No</TD><TD>$r->{'lot_number'}</TD></TR>|;
  $popup .= qq|<TR><TD>serial_number</TD><TD>$r->{'serial_number'}</TD></TR>|;
  $popup .= qq|<TR><TD>Expiration Date</TD><TD>$r->{'expiration_date'}</TD></TR>|;
  $popup .= qq|<TR><TD>Manufactured Date</TD><TD>$r->{'manufacturing_date'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>Distinct Identification Code</TD><TD>WHAT VALUE $r->{''}</TD></TR>|;
  $popup .= qq|<TR><TD>GMDN PT Name</TD><TD>$r->{'gmdnPTName'}</TD></TR>|;
  $popup .= qq|<TR><TD>GMDN PT Definition</TD><TD>$r->{'gmdnPTDefinition'}</TD></TR>|;
  $popup .= qq|<TR><TD>Brand Name</TD><TD>$r->{'brandName'}</TD></TR>|;
  $popup .= qq|<TR><TD>Version or Model Number</TD><TD>$r->{'versionModelNumber'}</TD></TR>|;
  $popup .= qq|<TR><TD>Company Name</TD><TD>$r->{'companyName'}</TD></TR>|;
  $popup .= qq|<TR><TD>MRI Safety Information</TD><TD>$r->{'MRISafetyStatus'}</TD></TR>|;
  $popup .= qq|<TR><TD>Human Cell, Tissue or Cellular or Tissue-Based Product (HCT/P)</TD><TD>$r->{'deviceHCTP'}</TD></TR>|;
  $popup .= qq|<TR><TD>Device required to be labeled as containing natural rubber latex or dry natural rubber (21 CFR 801.437)</TD><TD>$r->{'labeledContainsNRL'}</TD></TR>|;
  $popup .= qq|<TR><TD>Device labeled as &quot;Not made with natural rubber latex&quot;</TD><TD>$r->{'labeledNoNRL'}</TD></TR>|;
  $popup .= qq|<TR><TD></TD><TD></TD></TR>|;
#not needed  $popup .= qq|<TR><TD>expiration_date_original</TD><TD>$r->{'expiration_date_original'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>expiration_date_original_format</TD><TD>$r->{'expiration_date_original_format'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>manufacturing_date_original</TD><TD>$r->{'manufacturing_date_original'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>manufacturing_date_original_format</TD><TD>$r->{'manufacturing_date_original_format'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>devicePublishDate</TD><TD>$r->{'devicePublishDate'}</TD></TR>|;
#not needed  $popup .= qq|<TR><TD>catalogNumber</TD><TD>$r->{'catalogNumber'}</TD></TR>|;
  $popup .= qq|</TABLE>|;
  $popup .= qq||;
  my $html = qq|<A HREF="javascript:void(0)" TITLE="${popup}" >$r->{di}</A>\n|;
  return($html);
}
sub genUUID
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select UUID()");
  $s->execute() || myDBI->dberror("genUUID: select");
  my ($UUID) = $s->fetchrow_array;
  $s->finish();
  return($UUID);
}
sub getPrAuthTrans
{
  my ($self,$form,$ClientID,$InsID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  return(21) if ( $ClientID eq 'new' );
  my $qPrev = qq|select * from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID |;
  if ( $InsID ) { $qPrev .= qq| left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ClientID='${ClientID}' and Insurance.InsID='${InsID}'|; } else { $qPrev .= qq| where ClientPrAuth.ClientID='${ClientID}'|; }
  $qPrev .= qq| order by ClientPrAuth.RecDOLC desc|;
  my $sPrev = $dbh->prepare($qPrev);
  $sPrev->execute || myDBI->dberror($qPrev);
  my $rPrev = $sPrev->fetchrow_hashref;
  $sPrev->finish();
  return($rPrev->{'TransType'} == 21 ? 23 : 42);
}
sub getPrAuthTransDT
{
  my ($self,$form,$ClientID,$StartDate) = @_;
  my ($TransDate,$TransTime) = ($StartDate,'09:00:00');
# default for setDefaults.
#warn "getPrAuthTransDT: BEGIN: ClientID=${ClientID}, TransDate=$TransDate, TransTime=$TransTime\n";
  return($TransDate,$TransTime) if ( $ClientID eq 'new' ); 

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  # First try to use Notes...
  my $qTreatment = qq|select * from Treatment where ClientID='${ClientID}' order by ContLogDate desc|;
  my $sTreatment = $dbh->prepare($qTreatment);
  $sTreatment->execute || myDBI->dberror($qTreatment);
  my $rTreatment = $sTreatment->fetchrow_hashref;
  my $cnt = $sTreatment->rows();
  $sTreatment->finish();
  if ( $cnt ) 
  {
    $TransDate = $rTreatment->{ContLogDate}; 
    $TransTime = $rTreatment->{ContLogBegTime};
#warn "getPrAuthTransDT: Treatment: ClientID=${ClientID}, TransDate=$TransDate, TransTime=$TransTime\n";
    return($TransDate,$TransTime); 
  }

  # Second try to use ClientPrAuthCDC...
  my $qClientPrAuthCDC = qq|select * from ClientPrAuthCDC where ClientID='${ClientID}' order by TransDate desc, TransTime desc|;
  my $sClientPrAuthCDC = $dbh->prepare($qClientPrAuthCDC);
  $sClientPrAuthCDC->execute || myDBI->dberror($qClientPrAuthCDC);
  my $rClientPrAuthCDC = $sClientPrAuthCDC->fetchrow_hashref;
  my $cnt = $sClientPrAuthCDC->rows();
  $sClientPrAuthCDC->finish();
  if ( $cnt ) 
  {
#warn "getPrAuthTransDT: ClientPrAuthCDC: ClientID=${ClientID}, TransDate=$rClientPrAuthCDC->{TransDate}, TransTime=$rClientPrAuthCDC->{TransTime}\n";
    $TransDate = $rClientPrAuthCDC->{TransDate};
    my ($hr,$min,$sec) = split(':',$rClientPrAuthCDC->{TransTime});
    $min++;      # make 1 moinute later than last CDC.
    $TransTime = $hr.':'.$min.':'.$sec;
#warn "getPrAuthTransDT: ClientPrAuthCDC: ClientID=${ClientID}, TransDate=$TransDate, TransTime=$TransTime\n";
    return($TransDate,$TransTime); 
  }

# Lastly try the Intake
  my $qClientIntake = qq|select * from ClientIntake where ClientID='${ClientID}'|;
  my $sClientIntake = $dbh->prepare($qClientIntake);
  $sClientIntake->execute || myDBI->dberror($qClientIntake);
  my $rClientIntake = $sClientIntake->fetchrow_hashref;
  if ( $rClientIntake->{IntDate} gt '2010-06-01' )
  { $TransDate = $rClientIntake->{IntDate}; $TransTime = $rClientIntake->{IntTime}; }
  $sClientIntake->finish();
#warn "getPrAuthTransDT: Intake: ClientID=${ClientID}, TransDate=$TransDate, TransTime=$TransTime\n";
  return($TransDate,$TransTime); 
}
sub setPrintClientIntake
{
  my ($self,$form,$ClientID,$ID,$display) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $where = $ClientID eq '' 
            ? qq|where ID='${ID}'|
            : qq|where ClientID='${ClientID}'|;
  my $sClientAdmit = $dbh->prepare("select * from ClientAdmit ${where} order by AdmitDate desc");
  $sClientAdmit->execute || myDBI->dberror("setPrintAdmit: select ClientAdmit: ${ID}");
  my $rClientAdmit = $sClientAdmit->fetchrow_hashref;
#warn qq|AdmitDate=$rClientAdmit->{'AdmitDate'}\n|;
  my $pgm = $rClientAdmit->{'AdmitDate'} gt '2017-01-01' || $rClientAdmit->{'AdmitDate'} eq ''
            ? '/cgi/bin/printClientAdmit.cgi'
            : '/cgi/bin/printClientAdmit.cgi';
  my $IDs = $ClientID eq '' 
            ? qq|IDs=${ID}|
            : qq|ClientID=${ClientID}|;
  if ( $display eq '' ) 
  { $display = DBUtil->Date($rClientAdmit->{'AdmitDate'},'fmt','MM/DD/YYYY'); }
  my $href = qq|<A HREF="javascript:ReportWindow('${pgm}?${IDs}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','print${ID}')" TITLE="click to print" >${display} <IMG ALT="print" SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  $sClientAdmit->finish();
  return($href); 
}
#############################################################################
1;
