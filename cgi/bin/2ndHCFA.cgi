#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use myConfig;
use Cwd;
use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
if ( ! SysAccess->verify($form,'Privilege=BillingRemit') )
{ myDBI->error("BillingRemit Access / Not Found!"); }

$form = DBUtil->setDates($form);
my $fdow = DBUtil->Date($form->{FromDate},'dow');
my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
my $tdow = DBUtil->Date($form->{ToDate},'dow');
my $tdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$tdow];
my $DateRange = qq|from ${fdayname} $form->{FromDateD} - ${tdayname} $form->{ToDateD}|;

############################################################################
# 2ndHCFA.cgi does 1 Insurance type at a time.
##
my $sClientInsurance=$dbh->prepare("select * from Insurance where ClientID=? and InsID=? and Priority=?");
my $sInsurance=$dbh->prepare("select * from xInsurance where ID=?");
$sInsurance->execute($form->{'InsID'}) || myDBI->dberror("2ndHCFA: select xInsurance $form->{'InsID'}");
my $rInsurance = $sInsurance->fetchrow_hashref;
$s=$dbh->prepare("select * from xInsurance");
  $s->execute();
  while (my $r = $s->fetchrow_hashref) { $xInsurance{$r->{ID}} = $r; }
  $xInsurance{0}{ID} = 0;
  $xInsurance{0}{Name} = 'No Insurance';
  $xInsurance{0}{Descr} = 'none';
$s->finish();
my $SecondaryInsuranceID = '100';      # medicaid

my $html = $form->{'submit'} ? main->submit()
                             : main->list();
$sClientInsurance->finish();
$sInsurance->finish();
myDBI->cleanup();
print $html;
exit;

############################################################################
sub list()
{
#warn qq|2ndHCFA: doHTML\n|;
  my $Title = qq|$rInsurance->{Name} Billed and AmtDue Notes|;
  my $Hdr = qq|This screen selects notes for the client's secondary insurance payments for the primary insurance claims and generates the HCFA 1500 pdf. Check the box in the 'Due' column to select the note. When all notes are selected, hit the appropriate submit button for blank paper or pre-printed forms.<BR><U>For these notes the Primary insurance should have been used. And make sure that the Secondary Insurance for the Client has an EffDate before the PA of the Primary insurance.</U>|;
  my $html = myHTML->newHTML($form,'2nd HCFA','CheckPopupWindow noclock countdown_60') . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/serverREQ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form) { return(1); }
</SCRIPT>

<FORM NAME="HCFA" ACTION="/cgi/bin/2ndHCFA.cgi" METHOD="POST" >
<DIV CLASS="main header" >Generate 2nd HCFA</DIV>
<DIV CLASS="main heading" >${DateRange}</DIV>
<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="header" >${Title}</TD></TR>
  <TR ><TD CLASS="title" >${Hdr}</TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" >
    <TH ALIGN="left" >Client</TH>
    <TH ALIGN="left" >Name</TH>
    <TH ALIGN="left" >TrID</TH>
    <TH ALIGN="left" >Contact</TH>
    <TH ALIGN="left" >InProcess</TH>
    <TH ALIGN="left" >Reconciled</TH>
    <TH ALIGN="right" >Billed</TH>
    <TH ALIGN="right" >Paid</TH>
    <TH ALIGN="right" >Due</TH>
  </TR >
|; 

#============================================================================

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
    and xSC.InsID = '$form->{InsID}'
    ${ClinicSelection}
    ${DateSelection}
  order by Client.LName, Client.FName, Treatment.ContLogDate
|;
warn qq|2ndHCFA: qNotes=\n$qNotes\n|;
  my $cnt = 0;
  my $ClinicID = '';
  $sNotes=$dbh->prepare($qNotes);
  $sNotes->execute();
  while (my $rNotes = $sNotes->fetchrow_hashref)
  {
    $ClientID = $rNotes->{ClientID};
    next unless ( main->check2nd($ClientID) );
    $cnt+=1;
    $ClinicID=$rNotes->{ClinicID};        # FOR NOW WE GET THE LAST CLINIC-NEEDS TO BE GIVEN
    $even = int($cnt/2) == $cnt/2 ? '1' : '0';
    my $class = qq|rptodd|;
    if ( $even ) { $class = qq|rpteven|; }
    $html .= qq|  <TR CLASS="${class}" >\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{CLName} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{CFName} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{TrID} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{ContLogDate} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{CIPDate} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rNotes->{RecDate} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="right" >$rNotes->{BilledAmt} &nbsp;</TD>\n|;
    my $PaidAmt = $rNotes->{'BilledAmt'} - $rNotes->{'AmtDue'};
    $html .= qq|    <TD ALIGN="right" >${PaidAmt} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="right" >\n|;
    $html .= qq|      <INPUT TYPE=checkbox NAME="2ND_$rNotes->{TrID}" VALUE=1 ONCLICK="form.AMT_$rNotes->{TrID}.value=''" >\n|;
    $html .= qq|      $rNotes->{AmtDue}\n|;
    $html .= qq|    </TD>\n|;
    $html .= qq|  </TR>\n|; 
  }
  $html .= qq|</TABLE>\n|;
  $html .= qq|
<HR WIDTH="90%" >
<TABLE WIDTH="90%" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR CLASS="site" >
    <TD ALIGN="center" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit=1&HCFAtype=Black" VALUE="Submit Blank paper forms">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit=1&HCFAtype=Red" VALUE="Submit Pre-Printed forms">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="InsID" VALUE="$form->{InsID}" >
<INPUT TYPE="hidden" NAME="ClinicID" VALUE="${ClinicID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>

<SCRIPT LANGUAGE="JavaScript">
document.HCFA.elements[0].focus();
</SCRIPT>
</BODY>
</HTML>
|;
  $sNotes->finish();
  return($html);
}

############################################################################
sub submit()
{
warn qq|2ndHCFA: submit\n|;
  chdir("$form->{DOCROOT}/reports3");
  my $Location = myForm->popLINK();
warn qq|2ndHCFA: Location: $Location\n|;
  my ($TrIDs,$cnt) = ('',0);
  foreach my $f ( sort keys %{$form} )
  { 
    if ( $f =~ /^2ND_/ )
    {
      my ($tag,$TrID) = split('_',$f);
      $TrIDs .= $TrID . ' ';
      $cnt++;
    }
  }
  my $stamp = DBUtil->Date('','stamp');
  my $token = DBUtil->genToken();
  my $file = qq|HCFA_2nd_$form->{ClinicID}_$form->{InsID}_$form->{TODAY}_${cnt}_${stamp}_${token}.pdf|;
warn qq|2ndHCFA: file: $file\n|;
warn qq|2ndHCFA: TrIDs: ${TrIDs}\n|;
### InsID DOES NOT MATTER...TEST WITHOUT IT...
  my $cmd = qq|/home/okmis/mis/src/cgi/bin/printHCFA.pl DBNAME=$form->{DBNAME}\\&Secondary=1\\&InsID=$form->{InsID}\\&HCFAtype=$form->{HCFAtype}\\&TrIDs=${TrIDs}\\&file=${file}\\&mlt=$form->{mlt}|;
warn qq|2ndHCFA: cmd: $cmd\n|;
  system($cmd);
  my $html = myHTML->newHTML($form,'2nd HCFA','CheckPopupWindow noclock countdown_2') . qq|
<HR WIDTH="90%" >
<DIV CLASS="title" >Reports Window</DIV>
<DIV CLASS="subtitle" >for $form->{LOGINNAME}</DIV>
<DIV ALIGN=center > 
  <P>Generated 2nd HCFA Adobe pdf</P>
  <P>${cnt} Notes generated, goto...</P>
  <P>Administration->Notes->HCFA 1500 Print (2nd section)</P>
</DIV>
<HR WIDTH="90%" >
</BODY>
</HTML>
|;
warn qq|2ndHCFA:\n$html\n|;
  return($html);
}
sub check2nd
{
  my ($self,$ClientID) = @_;
  $sClientInsurance->execute($ClientID,$SecondaryInsuranceID,2) || myDBI->dberror("2ndHCFA: select Insurance ${ClientID}");
  if ( my $rClientInsurance = $sClientInsurance->fetchrow_hashref )
  { return(1); }
  $sClientInsurance->execute($ClientID,$SecondaryInsuranceID,3) || myDBI->dberror("2ndHCFA: select Insurance ${ClientID}");
  if ( my $rClientInsurance = $sClientInsurance->fetchrow_hashref )
  { return(1); }
  return(0);
}
############################################################################
