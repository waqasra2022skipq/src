#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;
use myHTML;
use uBill;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
my $InsID = $form->{'InsID'};
warn qq|\nENTER->Remit InsID=${InsID}\n|;

if ( ! SysAccess->verify($form,'Privilege=BillingRemit') )
{ myDBI->error("Remittance Access / Not Found!"); }

my $url = qq|/cgi/bin/mis.cgi?view=vInsID.cgi&title=Reconcile or Scholarship Notes&action=Remit&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}|;

############################################################################
# Remit.cgi does 1 Insurance type at a time.
my $sInsurance=$dbh->prepare("select * from xInsurance where ID=?");
$sInsurance->execute($InsID) || myDBI->dberror("Remit: select xInsurance ${InsID}");
my $rInsurance = $sInsurance->fetchrow_hashref;
my $Title = qq|$rInsurance->{Name} Billed NOT Reconciled or AmtDue Notes|;

my $html = $form->{'submit'} ? main->submit($InsID,$url)
         : $form->{'cancel'} ? qq|Location: ${url}\n\n|
                             : main->html($InsID);
$sInsurance->finish();

myDBI->cleanup();

print $html;
exit;

############################################################################
sub html()
{
  my ($self,$InsID) = @_;
#warn qq|Remit: doHTML\n|;
  my $FORMID = myDBI->getFORMID($form);
  my $Hdr = 'Please note: for each treatment note you may either; input reconciled amount, check scholarship, or select deny code. Priority is in that order as to which function is performed. A note may have to be denied before it can be rebilled.';
#  my $html =  myHTML->new($form,"Reconcile");
  my $html = myHTML->newHTML($form,'Reconcile','CheckPopupWindow noclock countdown_30') . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT type="text/javascript" SRC="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{   
  return vEntry("notnull",form.TheCheckNumber
                         ,form.TransDate
               );
}
</SCRIPT>

<FORM NAME="Reconcile" ACTION="/cgi/bin/Remit.cgi" METHOD="POST" >
<DIV CLASS="main header" >Reconcile or Scholarship Notes</DIV>
<TABLE CLASS="port" WIDTH="50%" >
  <TR ><TD CLASS="header" >${Title}</TD></TR>
  <TR WIDTH="50%" ><TD CLASS="title" >${Hdr}</TD></TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home strcol" >
  <TR >
    <TD CLASS="numcol" >Check # / Reference:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="TheCheckNumber" ONFOCUS="select()" SIZE=12 >
    </TD>
    <TD CLASS="numcol" >Transaction Date:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="TransDate" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE=12 >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR CLASS="port" >
    <TH ALIGN="left" >Client</TH>
    <TH ALIGN="left" >Name</TH>
    <TH ALIGN="left" >TrID</TH>
    <TH ALIGN="left" >Contact</TH>
    <TH ALIGN="left" >InProcess</TH>
    <TH ALIGN="left" >Reconciled</TH>
    <TH ALIGN="right" >AmtBilled</TH>
    <TH ALIGN="right" >AmtDue</TH>
    <TH ALIGN="left" >AmtPaid</TH>
    <TH ALIGN="center" >Scholarship</TH>
    <TH ALIGN="left" >Deny</TH>
  </TR >
|; 

  my $selDenCodes = DBA->selxTable($form,'xDenCodesTrans','','ID Descr');
  my $ForProvID = $form->{Provider} ? $form->{Provider} : $form->{LOGINPROVID};
  my $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Treatment.ClinicID');
  my $DateSelection = '';
  $DateSelection .= qq|and ContLogDate >= '$form->{FromDate}' | if ( $form->{FromDate} );
  $DateSelection .= qq|and ContLogDate <= '$form->{ToDate}' | if ( $form->{ToDate} );
  my $qNotes = qq|
select Treatment.*
      ,Provider.LName as PLName, Provider.FName as PFName
      ,Client.LName as CLName, Client.FName as CFName
      ,xSC.InsID
  from Treatment
  left join Provider on Provider.ProvID=Treatment.ProvID
  left join Client on Client.ClientID=Treatment.ClientID
  left join xSC on xSC.SCID=Treatment.SCID
  where Treatment.BillStatus>2 and Treatment.AmtDue > 0
    and xSC.InsID = '${InsID}'
    ${ClinicSelection}
    ${DateSelection}
  order by Client.LName, Client.FName, Treatment.ContLogDate
|;
#warn qq|Remit: qNotes=\n$qNotes\n|;
  my $cnt = 0;
  $sNotes=$dbh->prepare($qNotes);
  $sNotes->execute();
  while (my $rNotes = $sNotes->fetchrow_hashref)
  {
    $cnt+=1;
    $even = int($cnt/2) == $cnt/2 ? '1' : '0';
    my $class = qq|CLASS=rptodd|;
    if ( $even ) { $class = qq|CLASS=rpteven|; }
#warn qq|cnt=$cnt, even=$even\n|;
#warn qq|TrID=$rNotes->{TrID}\n|;
#foreach my $f ( sort keys %{$rNotes} ) { warn qq|$f=$rNotes->{$f}\n|; }
    $html .= qq|
  <TR ${class} >
    <TD ALIGN="left" >$rNotes->{CLName} &nbsp;</TD>
    <TD ALIGN="left" >$rNotes->{CFName} &nbsp;</TD>
    <TD ALIGN="left" >$rNotes->{TrID} &nbsp;</TD>
    <TD ALIGN="left" >$rNotes->{ContLogDate} &nbsp;</TD>
    <TD ALIGN="left" >$rNotes->{CIPDate} &nbsp;</TD>
    <TD ALIGN="left" >$rNotes->{RecDate} &nbsp;</TD>
    <TD ALIGN="right" >$rNotes->{BilledAmt} &nbsp;</TD>
    <TD ALIGN="right" >$rNotes->{AmtDue} &nbsp;</TD>
    <TD ALIGN="left" >
      <INPUT TYPE=text NAME="AMT_$rNotes->{TrID}" VALUE="" ONFOCUS="select" ONCHANGE="return vNum(this,0,$rNotes->{AmtDue})" SIZE="10" >
    </TD>
    <TD ALIGN="center" >
      <INPUT TYPE="checkbox" NAME="SCH_$rNotes->{TrID}" VALUE="1" ONCLICK="form.AMT_$rNotes->{TrID}.value=''" >
    </TD>
    <TD ALIGN="left" >
      <SELECT NAME="DEN_$rNotes->{'TrID'}" >
        ${selDenCodes} 
      </SELECT> 
    </TD>
  </TR>
|;
  }
  $html .= qq|
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="site fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="cancel=1" VALUE="Cancel">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit=1" VALUE="Submit">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="InsID" VALUE="${InsID}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="${FORMID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >

</FORM>

<SCRIPT LANGUAGE="JavaScript">
document.Reconcile.elements[0].focus();
</SCRIPT>
|;
  $sNotes->finish();
  return($html);
}
############################################################################
sub submit()
{
  my ($self,$InsID,$url) = @_;
  # per Dr. Hamil goto insurance again.
  my $html = qq|Location: ${url}\n\n|;
  return($html) if ( DBA->updSQLdone($form) );

  myDBI->dberror("No Check Number!") if ( ! $form->{TheCheckNumber} );
  myDBI->dberror("No Transaction date!") if ( ! $form->{TransDate} );

#warn qq|Remit: submit\n|;
#warn qq|Remit: TheCheckNumber=$form->{TheCheckNumber}\n|;
#warn qq|Remit: TransDate=$form->{TransDate}\n|;

  my $sTreatment = $dbh->prepare("
select Treatment.ProvID, Treatment.ClientID, Treatment.TrID, Treatment.SCID, Treatment.Mod4
     , Treatment.ContLogDate, Treatment.Units, Treatment.BilledAmt, Treatment.AmtDue
     , xSC.InsID, xSC.SCNum
     , xInsurance.InsCode
  from Treatment
    left join xSC on xSC.SCID=Treatment.SCID
    left join xSCRates on xSCRates.SCID=xSC.SCID
    left join xInsurance on xInsurance.ID=xSC.InsID
  where TrID=?
    and xSCRates.EffDate <= Treatment.ContLogDate and (Treatment.ContLogDate <= xSCRates.ExpDate or xSCRates.ExpDate is null)
");
  foreach my $f ( sort keys %{$form} )
  { 
#warn qq|\nRemit: f=$f, form-$f=$form->{$f}\n|;
    my ($flag,$TrID) = split('_',$f);
    my ($PaidAmt,$DenCode,$SRC,$Code) = ($form->{$f},$form->{$f},'MR','MR');
    my $RecDate   = $form->{'TransDate'};
    my $StatusMsg = $form->{'StatusMsg'};                    # ADD to SCREEN.

#   reconcile, write-off or deny note...
    next if ( $f !~ /^AMT_/ && $f !~ /^SCH_/ && $f !~ /^DEN_/ );

#warn qq|Remit: PaidAmt=$PaidAmt, DenCode=$DenCode\n|; 
#warn qq|Remit: pass1: flag=$flag, TrID=$TrID\n|; 
    $sTreatment->execute($TrID) || myDBI->dberror("Remit: select Treatment ${TrID}");
    my $rTreatment = $sTreatment->fetchrow_hashref;
    my $AmtDue = $rTreatment->{'AmtDue'};

    next if ( $f =~ /^AMT_/ && $PaidAmt <= 0 );
    next if ( $f =~ /^DEN_/ && $DenCode eq '' );
    next if ( $f =~ /^SCH_/ && $AmtDue <= 0 );
warn qq|Remit: pass2: TrID=${TrID}, PaidAmt=${PaidAmt}, DenCode=${DenCode}\n|; 

# minimal settings postClaim: ClientID,ContDate,ServCode (TransID/ICN)
# add to uBill->selTrans that if TrID, look up note first by TrID (FindNote)
    my $r835 = ();
    $r835->{'TrID'}       = $TrID;                       # ok to set
    $r835->{'ClientID'}   = $rTreatment->{'ClientID'};
    $r835->{'ProvID'}     = $rTreatment->{'ProvID'};
    $r835->{'ContDate'}   = $rTreatment->{'ContLogDate'};
    $r835->{'ServCode'}   = $rTreatment->{'Mod4'} eq '' ? $rTreatment->{'SCNum'}
                          : $rTreatment->{'SCNum'}.' '.$rTreatment->{'Mod4'};
    $r835->{'RecDate'}    = $RecDate;
    $r835->{'RefID'}      = $form->{'TheCheckNumber'};
    $r835->{'InsCode'}    = $rTreatment->{'InsCode'};
#    $r835->{'Units'}      = $rTreatment->{'Units'};     # if needed.
#    $r835->{'ICN'}      = $ICN;                         # if needed.
#    $r835->{'PayerID'}      = $PayerID;                 # if needed.

    if ( $f =~ /^AMT_/ )
    {
      $SRC     = 'MR';
      $Code    = 'MR';
      $r835->{'PaidAmt'}    = $PaidAmt;
    }
#   writeoff the remainder of the note...
    elsif ( $f =~ /^SCH_/ )                              # checkbox only transmits if checked.
    {
      $SRC     = 'MR';
      $Code    = 'SR';
      $r835->{'PaidAmt'}    = $AmtDue;
      $r835->{'PaidDate'}   = $RecDate;                  # mark for Payroll exclusion.
    }
    elsif ( $f =~ /^DEN_/ )
    {
      $SRC     = 'MR';
      $Code    = 'MD';
      $r835->{'PaidAmt'} = 0;
      $r835->{'DenCode'} = $DenCode;
    }
    my ($trid,$scid,$code,$type) = uBill->postClaim($form,$r835,$SRC,$Code,$StatusMsg);
warn qq|Remit: TrID/trid=${TrID}/${trid}, scid=${scid}, code=${code}, type=${type}\n|;
    if ( $f =~ /^SCH_/ )                              # checkbox only transmits if checked.
    {
#warn qq|Remit: call fixBillDate: TrID=${TrID}, RecDate=${RecDate}\n|;
      # did we reconcile this note before it was even billed?
      uBill->fixBillDate($form,$TrID,$RecDate);
      # don't leave it unreviewed.
      uBill->fixRevDates($form,$TrID,3);
    }
  }
  $sTreatment->finish();

  return($html);
}
############################################################################
