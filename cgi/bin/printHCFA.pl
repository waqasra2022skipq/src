#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use DBI;
use myForm;
use myDBI;
use DBUtil;
use DBA;
use cBill;
use myConfig;
use MgrTree;

use strict;
use PDFlib::PDFlib;

my $debug=0;
############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $cdbh = myDBI->dbconnect('okmis_config');
#$form->{'TrIDs'} = "136915 139970 139979 140240";
warn "\n\nprintHCFA: TrIDs=$form->{'TrIDs'}\n";
my $Secondary = $form->{'Secondary'};
my $HCFAtype = $form->{'HCFAtype'};
#foreach my $f ( sort keys %{$form} ) { warn "printHCFA: form-$f=$form->{$f}\n"; }

my $pagewidth = 684;
my $pageheight = 864;

my $searchpath = "../data";

my $qrcodeimage = ""; #"qrcode.png";

my $fontname= "Arial";
my $boldfontname = "Arial-BoldMT";
my $fontsize3xsmall = 5;
my $fontsizexxsmall = 6;
my $fontsizexsmall = 7;
my $fontsizesmall = 8;
my $fontsize = 9;
my $fontsizemid = 10;
my $fontsizelarge = 11;
my $fontsizemidlarge = 12;
my $fontsizexlarge = 13;
my $fontsizexxlarge = 15;
my $basefontoptions = "fontname=" . $fontname . " fontsize=" . $fontsize . " embedding encoding=unicode";
my $baseboldfontoptions = "fontname=" . $boldfontname . " fontsize=" . $fontsize . " embedding encoding=unicode";
my $basexxsmallfontoptions = $basefontoptions . " fontsize=" . $fontsizexxsmall;
my $basexxsmallfontoptions_i = $basexxsmallfontoptions . " italicangle=-10";
my $baseboldxxsmallfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizexxsmall;
my $basexsmallfontoptions = $basefontoptions . " fontsize=" . $fontsizexsmall;
my $baseboldxsmallfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizexsmall;
my $basemidfontoptions = $basefontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions_u = $baseboldmidfontoptions . " underline=true underlineposition=-15% underlinewidth=1.0";
my $baselargefontoptions = $basefontoptions . " fontsize=" . $fontsizelarge;
my $basemidlargefontoptions = $basefontoptions . " fontsize=" . $fontsizemidlarge;
my $baseboldlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions_u = $baseboldfontoptions . " fontsize=" . $fontsizelarge . " underline=true underlineposition=-15% underlinewidth=0.03";
my $baseboldlargefontoptions_ui = $baseboldlargefontoptions_u . " fontstyle=italic";
my $basesmallfontoptions = $basefontoptions . " fontsize=" . $fontsizesmall;
my $baseboldsmallfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizesmall;
my $basexlargefontoptions = $basefontoptions . " fontsize=" . $fontsizexlarge;

my $marginleft = 60.2;
my $formwidth = 569;

my $linewidth1 = 1.9;
my $linewidth2 = 0.7;
my $linewidth3 = 0.5;
my $linewidth4 = 0.2;

############################################################################
##
# prepare selects...
##
my $qNotes = qq|
  select Treatment.*
        ,Provider.LName as ProvLName, Provider.FName as ProvFName
        ,Client.LName as ClientLName, Client.FName as ClientFName
    from Treatment
      left join Client on Treatment.ClientID=Client.ClientID
      left join Provider on Treatment.ProvID=Provider.ProvID
    where Treatment.TrID=?
|;
my $sNotes = $dbh->prepare($qNotes);
# Other select statements needed.
my $q= qq|
select Contracts.RefID, Contracts.PIN, Contracts.Taxonomy
      ,Contracts.InsID, Contracts.TaxID, Contracts.UseAgency
      ,xInsurance.Descr
      ,ProviderControl.NPI, Provider.ProvID, Provider.Name, Provider.Addr1, Provider.Addr2
      ,Provider.City, Provider.ST, Provider.Zip, Provider.WkPh
  from Contracts
    left join xInsurance on xInsurance.ID=Contracts.InsID
    left join Provider on Provider.ProvID=Contracts.ProvID
    left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID
  where xInsurance.ID=?
    and Provider.ProvID=?
  order by xInsurance.Descr, Provider.Name
|;
my $sClinics = $dbh->prepare($q);
my $sProvider = $dbh->prepare("select Provider.*,ProviderControl.NPI from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?");
my $sCredentials = $dbh->prepare("
select Credentials.RefID, Credentials.PIN, Credentials.Taxonomy,Credentials.DesigProvID, xCredentials.Abbr
  from Credentials
    left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID
  where Credentials.InsID=? and Credentials.ProvID=?
  order by Credentials.Rank
");
my $sProviderLicenses = $dbh->prepare("
select * from ProviderLicenses
  where ProvID=? and State='OK'
    and LicEffDate<=curdate() and (curdate()<=LicExpDate or LicExpDate is NULL)
");
my $sxInsurance = $dbh->prepare("select * from xInsurance where ID=?");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sClientReferrals = $dbh->prepare("select * from ClientReferrals where ClientID=?");
my $sClientRelations = $dbh->prepare("select * from ClientRelations where ClientID=?");
# Insurance for Note...
my $qInsurance1 = qq|
select Insurance.InsNumID from Insurance
    left join Treatment on Treatment.TrID=?
    left join xSC on xSC.SCID=Treatment.SCID
  where Insurance.ClientID=? and Insurance.InsID=xSC.InsID
    and Insurance.InsNumEffDate<=?
    and (?<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL)
|;
my $sInsurance1 = $dbh->prepare($qInsurance1);
my $qInsurance2 = qq|
select InsNumID from Insurance
  where Insurance.ClientID=?
    and Insurance.InsNumEffDate<=? 
    and (?<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL)
|;
my $sInsurance2 = $dbh->prepare($qInsurance2);
my $qReqIns = qq|
select * from Insurance
  left join Guarantor on Insurance.InsNumID=Guarantor.InsuranceID
  where Insurance.InsNumID=?
|;
my $sReqIns = $dbh->prepare($qReqIns);
# Other Insurance...
my $qOthIns = qq|
select * from Insurance
  left join Guarantor on Insurance.InsNumID=Guarantor.InsuranceID
  where Insurance.ClientID=?
    and Insurance.Priority=?
    and Insurance.InsNumEffDate<=? 
    and (?<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL)
  order by Insurance.InsNumEffDate desc
|;
my $sOthIns = $dbh->prepare($qOthIns);
my $sPrAuth = $dbh->prepare("select ID from ClientPrAuth where ClientPrAuth.ClientID=? and ClientPrAuth.InsuranceID=? and ? between ClientPrAuth.EffDate and ClientPrAuth.ExpDate");
my $sPA = $dbh->prepare("select ClientPrAuth.PAnumber,ClientPrAuth.EffDate,ClientPrAuth.ExpDate,PDDiag.Axis1ACode,PDDiag.Axis1BCode,PDDiag.Axis1CCode from ClientPrAuth left join PDDiag on PDDiag.PrAuthID=ClientPrAuth.ID where ClientPrAuth.ID=?");
my $sClientProblems=$dbh->prepare("select ClientProblems.UUID,ClientProblems.Priority,misICD10.ICD10 from ClientProblems left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID where ClientID=? order by ClientProblems.Priority");
my $sClientNoteProblems=$dbh->prepare("select ClientNoteProblems.UUID,ClientNoteProblems.Priority,misICD10.ICD10 from ClientNoteProblems left join okmis_config.misICD10 on misICD10.ID=ClientNoteProblems.UUID where TrID=? and UUID=?");

############################################################################
# MAIN
# first grab all the Notes...
#  and put in the global array to sort...
my @TrIDs = ();
my %Claims = ();
my %HCFAs = ();
my $rNotes;
foreach my $TrID ( split(' ',$form->{TrIDs}) )
{ 

  push(@TrIDs, $TrID);
#warn qq|READ: TrID=$TrID\n|;
  $sNotes->execute($TrID);
  $rNotes = $sNotes->fetchrow_hashref;
  my $ClinicID = $rNotes->{ClinicID};             # use the ClinicID in the note.
  my $ProviderKey = "$rNotes->{ProvLName}_$rNotes->{ProvFName}_$rNotes->{ProvID}";
  my $ClientKey = "$rNotes->{ClientLName}_$rNotes->{ClientFName}_$rNotes->{ClientID}";
# sort by the Prior Authorization info for the Contact Date.
#warn qq|TrID=$TrID, ClientID=$rNotes->{ClientID}, ContLogDate=$rNotes->{ContLogDate}\n|;
  $sInsurance1->execute($TrID,$rNotes->{ClientID},$rNotes->{ContLogDate},$rNotes->{ContLogDate});
  my ($InsuranceID) = $sInsurance1->fetchrow_array;
#warn qq|pass1: InsuranceID=$InsuranceID\n|;
  if ( $InsuranceID eq '' )
  {
    $sInsurance2->execute($rNotes->{ClientID},$rNotes->{ContLogDate},$rNotes->{ContLogDate});
    ($InsuranceID) = $sInsurance2->fetchrow_array;
#warn qq|pass2: InsuranceID=$InsuranceID\n|;
  }
  $sPrAuth->execute($rNotes->{ClientID},$InsuranceID,$rNotes->{ContLogDate});
  my ($PrAuthID) = $sPrAuth->fetchrow_array;
  my $ICD9 = $rNotes->{'ContLogDate'} lt '2015-10-01' ? 1 : 0;
  my $InsPAID = "${ClinicID}_${InsuranceID}_${PrAuthID}_${ICD9}_";
  my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_$rNotes->{'Mod4'}|;
  warn qq|1: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID\n| if ( $debug );
  warn qq|1: NoteStr=$NoteStr\n| if ( $debug );
  $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID} = $NoteStr;
  if ( $rNotes->{'SCID2'} ne '' )
  {
    my $TrID2 = $TrID.'.2';
    my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID2'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_|;
    warn qq|2: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID2\n| if ( $debug );
    warn qq|2: NoteStr=$NoteStr\n| if ( $debug );
    $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID2} = $NoteStr;
  }
  if ( $rNotes->{'SCID3'} ne '' )
  {
    my $TrID3 = $TrID.'.3';
    my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID3'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_|;
    warn qq|3: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID3\n| if ( $debug );
    warn qq|3: NoteStr=$NoteStr\n| if ( $debug );
    $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID3} = $NoteStr;
  }
  if ( $rNotes->{'SCID4'} ne '' )
  {
    my $TrID4 = $TrID.'.4';
    my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID4'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_|;
    warn qq|3: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID4\n| if ( $debug );
    warn qq|3: NoteStr=$NoteStr\n| if ( $debug );
    $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID4} = $NoteStr;
  }
  if ( $rNotes->{'SCID5'} ne '' )
  {
    my $TrID5 = $TrID.'.5';
    my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID5'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_|;
    warn qq|3: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID5\n| if ( $debug );
    warn qq|3: NoteStr=$NoteStr\n| if ( $debug );
    $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID5} = $NoteStr;
  }
  if ( $rNotes->{'SCID6'} ne '' )
  {
    my $TrID6 = $TrID.'.6';
    my $NoteStr = qq|$rNotes->{'TrID'}_$rNotes->{'ContLogDate'}_$rNotes->{'ContLogBegTime'}_$rNotes->{'ContLogEndTime'}_$rNotes->{'SCID6'}_$rNotes->{'BillDate'}_$rNotes->{'POS'}_$rNotes->{'Units'}_|;
    warn qq|3: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID, TrID=$TrID6\n| if ( $debug );
    warn qq|3: NoteStr=$NoteStr\n| if ( $debug );
    $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrID6} = $NoteStr;
  }

}
my $TotalServices = 0;
my $TotalBalance = 0;
# How to output with (warn) and still get pdf?
warn "Generating HCFA Forms\n";
############################################################################
#                                     # HCFAType =Black, =Red
#                                     #  cannot print multiple Types on 1 run
#                                     #  because of the different pdfs for each Type

# first divide int ONLY 6 claims per page...
foreach my $ProviderKey ( sort keys %Claims )
{ 
  foreach my $ClientKey ( sort keys %{ $Claims{$ProviderKey} } )
  { 
    foreach my $InsPAID ( sort keys %{ $Claims{$ProviderKey}{$ClientKey} } )
    {
      my ($cnt,$len) = (0,1);
      foreach my $TrIDidx ( sort keys %{ $Claims{$ProviderKey}{$ClientKey}{$InsPAID} } )
      {
        $cnt++;
        my $InsPAKey = $InsPAID . 'x' x $len;
        $HCFAs{$ProviderKey}{$ClientKey}{$InsPAKey}{$TrIDidx} = 
          $Claims{$ProviderKey}{$ClientKey}{$InsPAID}{$TrIDidx};
        $len++ if ( $cnt % 6 == 0 );
warn qq|setHCFAs: ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAKey=$InsPAKey, TrIDidx=$TrIDidx\n| if ( $debug );
warn qq|setHCFAs: $HCFAs{$ProviderKey}{$ClientKey}{$InsPAKey}{$TrIDidx}\n| if ( $debug );
      }
    }
  }
}

############################################################################
my $filename = '/tmp/'.$form->{'LOGINID'}.'_'.DBUtil->genToken().'_'.DBUtil->Date('','stamp').'.pdf';
my $outfile = $form->{'file'} eq ''                # create and print pdf else just create.
              ? $form->{'DOCROOT'}.$filename
              : $form->{'file'};
#$outfile = 'kls.pdf';

eval {

    # create a new PDFlib object 
    my $p = new PDFlib::PDFlib;

    $p->set_option("SearchPath={{" . $searchpath . "}}");

    # This mean we don't have to check error return values, but will
    # get an exception in case of runtime problems.
    
    $p->set_option("errorpolicy=exception");

    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    $p->begin_document($outfile, "");

    $p->set_info("Title", "HCFA Form");

    main->printHCFA($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}

$sNotes->finish();
$sClinics->finish();
$sProvider->finish();
$sCredentials->finish();
$sProviderLicenses->finish();
$sxInsurance->finish();
$sClient->finish();
$sClientReferrals->finish();
$sClientRelations->finish();
$sInsurance1->finish();
$sInsurance2->finish();
$sReqIns->finish();
$sOthIns->finish();
$sPrAuth->finish();
$sPA->finish();
$sClientProblems->finish();
$sClientNoteProblems->finish();

myDBI->cleanup();
if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;

############################################################################
sub printHCFA {
    my ($self, $p) = @_;

    foreach my $ProviderKey ( sort keys %HCFAs )
    { 
        foreach my $ClientKey ( sort keys %{ $HCFAs{$ProviderKey} } )
        { 
            foreach my $InsPAID ( sort keys %{ $HCFAs{$ProviderKey}{$ClientKey} } )
            {

                $p->begin_page_ext($pagewidth, $pageheight, "topdown");

                main->createClaimForm($p);
                main->createFormLavels($p);
                main->createFormContent($p, $ProviderKey, $ClientKey, $InsPAID);

                $p->end_page_ext("");

            }
        }
    }
    $TotalServices = sprintf("%.2f", $TotalServices);
    $TotalBalance = sprintf("%.2f", $TotalBalance);

}

sub createFormContent {
    my ($self, $p, $ProviderKey, $ClientKey, $InsPAID) = @_;
# get the Client info.
warn "  printHCFA:\n" if ( $debug );
warn qq|ProviderKey=$ProviderKey, ClientKey=$ClientKey, InsPAID=$InsPAID\n| if ( $debug );
  my ($ProvLName, $ProvFName, $ProvID) = $ProviderKey =~ /(.*)_(.*)_(\d*)/;
  my ($ClientLName, $ClientFName, $ClientID) = $ClientKey =~ /(.*)_(.*)_(\d*)/;
  my ($ClinicID, $InsuranceID, $PrAuthID, $ICD9, $Group) = $InsPAID =~ /(\d*)_(\d*)_(\d*)_(\d*)_(\d*)/;
warn "ClinicID=$ClinicID, InsuranceID=$InsuranceID, PrAuthID=$PrAuthID, ICD9=$ICD9, Group=$Group\n" if ( $debug );
#foreach $TrIDidx ( sort keys %{ $HCFAs{$ProviderKey}{$ClientKey}{$InsPAID} } ) { warn qq|is: $ProviderKey,$ClientKey,$InsPAID,$TrIDidx\n|; }
  $sClient->execute($ClientID);
  my $rClient = $sClient->fetchrow_hashref;
  $sClientReferrals->execute($ClientID);
  my $rClientReferrals = $sClientReferrals->fetchrow_hashref;
  $sClientRelations->execute($ClientID);
  my $rClientRelations = $sClientRelations->fetchrow_hashref;
# get the PrAuth/Diagnostic info.
  $sPA->execute($PrAuthID);
  my $rPA = $sPA->fetchrow_hashref;
  my $EffDate = $rPA->{'EffDate'};   # use the EffDate of PA to get OthIns
#foreach my $f ( sort keys %{$rPA} ) { warn ": rPA-$f=$rPA->{$f}\n"; }
  my @Problems = ();
  my @NoteProblems = ();
  $sClientProblems->execute($ClientID) || myDBI->dberror("select ClientProblems ${ClientID}");
warn qq| ICD9 CHECK: ICD9=${ICD9}\n| if ( $debug );
  while ( my $rClientProblems = $sClientProblems->fetchrow_hashref )
  { 
    my $ICD10 = $rClientProblems->{'ICD10'};
warn qq|BEFORE: ICD10=${ICD10}\n| if ( $debug );
    $ICD10 =~ s/\.//g;                          # trim period .
    next unless ( $ICD10 =~ /^F/ );             # skip non-MH Diagnosis

    # reset ICD10 to ICD9? ## remove?? this is for ContactDate before 10/1/2015.
    if ( $ICD9 )
    { $ICD10 = main->convertICD9($ICD10,$rClientProblems->{'UUID'}); }
warn qq| AFTER: ICD10=${ICD10}\n| if ( $debug );
    my $ICDdot = substr($ICD10,0,3).'.'.substr($ICD10,3);
    push(@Problems,$ICDdot); 
    push(@NoteProblems,$rClientProblems->{'UUID'}); 
warn "ClientID=$ClientID, icddot=$ICDdot, ICD9=$ICD9\n" if ( $debug );
  }
# Get the right Insurance info.
warn "ClientID=$ClientID, InsuranceID=$InsuranceID\n" if ( $debug );
  $sReqIns->execute($InsuranceID);
  my $rReqIns = $sReqIns->fetchrow_hashref;
warn "InsuranceID=$InsuranceID, ReqInsuranceID=$rReqIns->{'InsNumID'}\n" if ( $debug );
#foreach my $f ( sort keys %{$rReqIns} ) { warn ": rReqIns-$f=$rReqIns->{$f}\n"; }
  my $OtherPriority = $rReqIns->{Priority} == 1 ? 2 : 1;
warn "ClientID=$ClientID, OtherPriority=$OtherPriority, Eff=${EffDate}\n" if ( $debug );
  $sOthIns->execute($ClientID,$OtherPriority,$EffDate,$EffDate);
  my $rOthIns = $sOthIns->fetchrow_hashref;
#foreach my $f ( sort keys %{$rOthIns} ) { warn ": rOthIns-$f=$rOthIns->{$f}\n"; }
if ( $Secondary )     # switch and print Secondary Insurance.
{ $rReqIns = $rOthIns; $rOthIns = (); }
  my $InsID = $rReqIns->{'InsID'};
warn "rxInsurance: InsID=$InsID\n" if ( $debug );
  $sxInsurance->execute($InsID);
  my $rxInsurance = $sxInsurance->fetchrow_hashref;
warn "Secondary=$Secondary, OtherPriority=$OtherPriority, Name=$rReqIns->{'Name'}\n" if ( $debug );
#foreach my $f ( sort keys %{$rxInsurance} ) { warn ": rxInsurance-$f=$rxInsurance->{$f}\n"; }
warn "InsID=$InsID, ClinicID=$ClinicID\n" if ( $debug );
  $sClinics->execute($InsID,$ClinicID);
  my $rClinics = $sClinics->fetchrow_hashref;
#foreach my $f ( sort keys %{$rClincis} ) { warn ": rClincis-$f=$rClincis->{$f}\n"; }
  my ($rProvider,$rCredentials,$rProviderLicenses) = ('','','');
  if ( $rReqIns->{DesigProvID} eq '' )
  {
    $sProvider->execute($ProvID);
    $rProvider = $sProvider->fetchrow_hashref;
warn qq|NOT DesigProvID: InsID=$InsID, ProvID=$ProvID\n| if ( $debug );
    $sCredentials->execute($InsID,$ProvID);
    $rCredentials = $sCredentials->fetchrow_hashref;
    $sProviderLicenses->execute($ProvID);
    $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  }
  else
  {
    $sProvider->execute($rReqIns->{DesigProvID});
    $rProvider = $sProvider->fetchrow_hashref;
warn qq|DesigProvID: InsID=$InsID, DesigProvID=$rReqIns->{DesigProvID}\n| if ( $debug );
    $sCredentials->execute($InsID,$rReqIns->{DesigProvID});
    $rCredentials = $sCredentials->fetchrow_hashref;
    $sProviderLicenses->execute($rReqIns->{DesigProvID});
    $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
warn qq|DesigProvID: CredentialsPIN=$rCredentials->{PIN}, ProviderLicensesID=$rProviderLicenses->{ID}\n| if ( $debug );
  }
  my $ProvNPI = $rProvider->{NPI};
  my $ProvRID = $rCredentials->{RefID};
  my $ProvPIN = $rCredentials->{PIN};
#warn qq|NPIs: ProvRID=$ProvRID, ProvPIN=$ProvPIN, ProvNPI=$ProvNPI\n| if ( $debug );

# Insurance information.
  my $InsDescr = $rxInsurance->{'Descr'};
  my $insurancename = $rxInsurance->{'Name'};
  my $insurancestreet1 = $rxInsurance->{'Addr1'};
  my $insurancestreet2 = $rxInsurance->{'Addr2'};
  my $insurancecityzip = "$rxInsurance->{'City'} $rxInsurance->{'ST'}  $rxInsurance->{'Zip'}";
  if ( $insurancestreet1 eq '' )    # move lines up 1...
  {
    $insurancestreet1 = $insurancestreet2;
    $insurancestreet2 = $insurancecityzip;
    $insurancecityzip = '';
  }
  if ( $insurancestreet2 eq '' )    # move lines up 1...
  {
    $insurancestreet2 = $insurancecityzip;
    $insurancecityzip = '';
  }
warn "Ins: $insurancename, $InsDescr\n" if ( $debug );

# Box 1.
  my ($medicare,$medicaid,$tricare,$champva,$groupins,$feca,$otherins) = (0,0,0,0,0,0,0);
  if ( $InsDescr =~ /medicare/i ) { $medicare = 1; }
  elsif ( $InsDescr =~ /railroad/i ) { $medicare = 1; }
  elsif ( $InsDescr =~ /medicaid/i ) { $medicaid = 1; }
  elsif ( $InsDescr =~ /ibh/i ) { $medicaid = 1; }
  elsif ( $InsDescr =~ /tricare/i ) { $tricare = 1; }
  elsif ( $InsDescr =~ /champus/i ) { $champva = 1; }
  elsif ( $InsDescr =~ /bcbsok/i ) { $groupins = 1; }
  elsif ( $InsDescr =~ /feca/i ) { $feca = 1; }
  else { $otherins = 1; }
# Box 1a.
  #fix my $insid = $rReqIns->{'InsIDNum'};
  (my $insid = $rReqIns->{'InsIDNum'}) =~ s/^\s*(.*?)\s*$/$1/g;
  $insid = substr($insid,0,29);
# Box 2. Patient information (Boxes 2-6)
  #fix my $PatientName = "$rClient->{'LName'}, $rClient->{'FName'} $rClient->{'MName'}";
  my $PatientName = qq|$rClient->{'LName'}, $rClient->{'FName'}|;
  $PatientName .= qq|, $rClient->{'MName'}| if ( $rClient->{'MName'} ne '' );
  $PatientName =~ s/^\s*(.*?)\s*$/$1/g;
  $PatientName = substr($PatientName,0,28);
# Box 3.
  my ($PatientDOBY, $PatientDOBM, $PatientDOBD) = split('-',$rClient->{DOB});
  my $PatientGend = $rClient->{'Gend'};
  my ($psexm,$psexf) = (0,0);
  if ( $PatientGend eq 'M' ) { $psexm = 1; }
  elsif ( $PatientGend eq 'F' ) { $psexf = 1; }
# Box 4.
  #fix my $cm = $rReqIns->{'LName'} eq '' ? '' : ',';
  #fix my $insname = "$rReqIns->{'LName'}${cm} $rReqIns->{'FName'} $rReqIns->{'MName'}";
  my $insname = qq|$rReqIns->{'LName'}, $rReqIns->{'FName'}|;
  $insname .= qq|, $rReqIns->{'MName'}| if ( $rReqIns->{'MName'} ne '' );
  $insname =~ s/^\s*(.*?)\s*$/$1/g;
  $insname = substr($insname,0,29);
# Box 5.
  my $PatientAddr = qq|$rClient->{'Addr1'} $rClient->{'Addr2'}|;
  $PatientAddr =~ s/[^a-zA-Z0-9\s]+//g;             # eliminate all chars but these
  $PatientAddr =~ s/^\s*(.*?)\s*$/$1/g;             # eliminate before/after spaces
  $PatientAddr = substr($PatientAddr,0,28);         # limit to 'n' characters
  my $PatientCity = $rClient->{'City'};
  $PatientCity = substr($PatientCity,0,24);         # limit to 'n' characters
  my $PatientST = $rClient->{'ST'};
  $PatientST = substr($PatientST,0,3);              # limit to 'n' characters
  (my $PatientZip = $rClient->{'Zip'}) =~ s/[- ]//g;
  $PatientZip = substr($PatientZip,0,12);           # limit to 'n' characters
  my $Phone = $rClient->{'HmPh'} ne '' ? $rClient->{'HmPh'}
            : $rClient->{'MobPh'} ne '' ? $rClient->{'MobPh'}
            : $rClient->{'WkPh'};
  my ($AC,$PH) = split('-',$Phone,2);
  $AC = substr($AC,0,3);                            # limit to 'n' characters
  $PH = substr($PH,0,10);                           # limit to 'n' characters
  my $PatientHmPh = qq|${AC} ${PH}|;
# Box 6.
  my ($pself,$pspouse,$pchild,$pother) = (0,0,0,0); # see below...could change
  my $PatientRel = $rReqIns->{'ClientRel'};         #   if NO Guarantor
# Box 7. Guarantor information.
  my $InsuredAddr = qq|$rReqIns->{'Addr1'} $rReqIns->{'Addr2'}|;
  $InsuredAddr =~ s/[^a-zA-Z0-9\s]+//g;             # eliminate all chars but these
  $InsuredAddr =~ s/^\s*(.*?)\s*$/$1/g;             # eliminate before/after spaces
  $InsuredAddr = substr($InsuredAddr,0,28);         # limit to 'n' characters
  my $InsuredCity = $rReqIns->{'City'};
  $InsuredCity = substr($InsuredCity,0,24);         # limit to 'n' characters
  my $InsuredST = $rReqIns->{'ST'};
  $InsuredST = substr($InsuredST,0,3);              # limit to 'n' characters
  (my $InsuredZip = $rReqIns->{'Zip'}) =~ s/[- ]//g;
  $InsuredZip = substr($InsuredZip,0,12);           # limit to 'n' characters
  my $Phone = $rReqIns->{'HmPh'} ne '' ? $rReqIns->{'HmPh'}
            : $rReqIns->{'MobPh'} ne '' ? $rReqIns->{'MobPh'}
            : $rReqIns->{'WkPh'};
  my ($AC,$PH) = split('-',$Phone,2);
  $AC = substr($AC,0,3);                            # limit to 'n' characters
  $PH = substr($PH,0,10);                           # limit to 'n' characters
  my $InsuredHmPh = qq|${AC} ${PH}|;
# Box 8.
  my $reserved3 = ''; 
# Box 9.  Other (secondary) Insurance info with Guarantor.
  #fix my $OtherGrpNum = $rOthIns->{'GrpNum'} ? $rOthIns->{'GrpNum'} : 'None';
  (my $OtherGrpNum = $rOthIns->{'GrpNum'}) =~ s/[- ]//g;
  $OtherGrpNum = substr($OtherGrpNum,0,28);         # limit to 'n' characters
  my $reserved1 = ''; 
  my $reserved2 = ''; 
  #fix my $OtherName = "$rOthIns->{LName}, $rOthIns->{FName} $rOthIns->{MName}";
  my $OtherName = qq|$rOthIns->{'LName'}, $rOthIns->{'FName'}|;
  $OtherName .= qq|, $rOthIns->{'MName'}| if ( $rOthIns->{'MName'} ne '' );
  $OtherName =~ s/^\s*(.*?)\s*$/$1/g;
  $OtherName = substr($OtherName,0,28);             # limit to 'n' characters
  my $OtherPlanName = $rOthIns->{PlanName};
  $OtherPlanName = substr($OtherPlanName,0,28);     # limit to 'n' characters
  if ( $Secondary )     # Print 2nd HCFA
  {
    $OtherName = '';
    $OtherGrpNum = '';
    $OtherPlanName = '';
  }

# Box 10.
  my $Employment = 0;
  my $EmplStat = DBA->getxref($form,'xEmplStat',$rClient->{'EmplStat'},'Descr');
  my $EmplType = DBA->getxref($form,'xEmplType',$rClient->{'EmplType'},'Descr');
  if ( $EmplStat =~ /employed/i ) { $Employment = 1; }
  if ( $EmplStat =~ /employed/i && $EmplType =~ /student/i ) { $Employment = 1; } # part time student
  if ( $EmplStat !~ /employed/i && $EmplType =~ /student/i ) { $Employment = 0; } # full time student
  $Employment = 0;                       # per Dr. Hamil
  $Employment = $rClientReferrals->{'Employed'};                       # per Dr. Hamil
  my $AutoAccident = 0;
  my $AutoAccidentST = '';
  my $OtherAccident = 0;
  $AutoAccident = $rClientReferrals->{'AutoAccident'};                 # per Dr. Hamil
  $AutoAccidentST = $rClientReferrals->{'AutoAccidentST'};             # per Dr. Hamil
  $OtherAccident = $rClientReferrals->{'OtherAccident'};               # per Dr. Hamil
  my ($empyes,$empno) = (0,0);
  if ( $Employment ) { $empyes = 1; } else { $empno = 1; }
  my ($autoyes,$autono) = (0,0);
  if ( $AutoAccident ) { $autoyes = 1; } else { $autono = 1; }
  my $autostate = $AutoAccidentST;
  my ($otheryes,$otherno) = (0,0);
  if ( $OtherAccident ) { $otheryes = 1; } else { $otherno = 1; }
  my $claimcodes = ''; 
# Box 11.
  #fix my $InsuredGrpNum = $rReqIns->{'GrpNum'} ? $rReqIns->{'GrpNum'} : 'None';
warn qq|CHECK: InsuredGrpNum=$rReqIns->{'GrpNum'}\n| if ( $form->{LOGINPROVID} == 91 );
  (my $InsuredGrpNum = $rReqIns->{'GrpNum'}) =~ s/[- ]//g;
  $InsuredGrpNum = substr($InsuredGrpNum,0,29);         # limit to 'n' characters
warn qq|CHECK: InsuredGrpNum=$InsuredGrpNum\n| if ( $form->{LOGINPROVID} == 91 );
  my ($InsuredDOBY, $InsuredDOBM, $InsuredDOBD) = split('-',$rReqIns->{DOB});
  my $InsuredGend = $rReqIns->{Gend};
  if ( $rReqIns->{'GrtrID'} eq '' )     # No Guarantor
  {
    $PatientRel = 'I';                  # Self
    $insname = $PatientName;
    $InsuredAddr = $PatientAddr;
    $InsuredCity = $PatientCity;
    $InsuredST = $PatientST;
    $InsuredZip = $PatientZip;
    $InsuredHmPh = $PatientHmPh;
    ($InsuredDOBY, $InsuredDOBM, $InsuredDOBD) = ($PatientDOBY,$PatientDOBM,$PatientDOBD);
    $InsuredGend = $PatientGend;
  }
  if ( $PatientRel eq 'I' )                         { $pself = 1; }
  elsif ( $PatientRel eq 'H' || $PatientRel eq 'W' ){ $pspouse = 1; }
  elsif ( $PatientRel eq 'F' || $PatientRel eq 'M' ){ $pchild = 1; }
  else                                              { $pother = 1; }
  my ($inssexm,$inssexf) = (0,0);
  if ( $InsuredGend eq 'M' ) { $inssexm = 1; }
  elsif ( $InsuredGend eq 'F' ) { $inssexf = 1; }
  my $otherclaim = '';
  my $InsuredPlanName = $rReqIns->{PlanName} eq '' ? $insurancename : $rReqIns->{PlanName};
  $InsuredPlanName = substr($InsuredPlanName,0,29);         # limit to 'n' characters
  my $AnotherPlan = $OtherGrpNum eq '' ? 0 : 1;
  my ($anotheryes,$anotherno) = (0,0);
  if ( $AnotherPlan ) { $anotheryes = 1; } else { $anotherno = 1; }
# Box 12. Signature on file
  my $pdate = DBUtil->Date($form->{'TODAY'},'fmt','MM/DD/YY');
# Box 13. Signature on file
# Box 14.
  my ($lmpyy,$lmpmm,$lmpdd,$lmpqual) = ('','','','');
# Box 15.
  my ($otheryy,$othermm,$otherdd,$otherqual) = ('','','','');
# Box 16.
  my ($datepfromyy,$datepfrommm,$datepfromdd) = ('','','');
  my ($dateptoyy,$dateptomm,$dateptodd) = ('','','');
# Box 17.  # get the Referring Physician info.
# Wade said UPINs are obsolete. RefID,PIN from UPIN registry!!!
#   was coming from old x Physicians table.



# Change:START Added these lines

  my $rOrderingPhys = DBA->selxref($form,'xNPI','NPI',$rClientReferrals->{'OrderingRefPhysNPI'});

  # Change:END

  my $rRefPhys = DBA->selxref($form,'xNPI','NPI',$rClientReferrals->{'RefPhysNPI'});
  my $nameofrefa = '';   # DN=Referring, DK=Ordering, DQ=Supervising Provider
  my $nameofref = qq|$rRefPhys->{ProvFirstName} $rRefPhys->{ProvLastName} $rRefPhys->{ProvMiddleName}|;

  my $NPI_UPD = $rRefPhys->{'NPI'};

  if($rRefPhys->{'NPI'} ne '') {
    $nameofrefa = qq|DN|;
  }

  my $rProvInsCreds = '';
  if($rCredentials->{'DesigProvID'} ne '') {
    my $qProvInsCreds = qq|
    select Provider.*,LicType,LicNumber,NPI from Provider 
      left join ProviderLicenses on Provider.ProvID = ProviderLicenses.ProvID 
      left join ProviderControl on Provider.ProvID = ProviderControl.ProvID 
      WHERE Provider.ProvID = ?|;
    my $ProvInsCreds = $dbh->prepare($qProvInsCreds);
    $ProvInsCreds->execute($rCredentials->{'DesigProvID'});
    $rProvInsCreds = $ProvInsCreds->fetchrow_hashref;

    $nameofrefa = qq|DQ|;
    $NPI_UPD = $rProvInsCreds->{'NPI'};   
    my $mname = substr($rProvInsCreds->{'MName'},0,1);
    $nameofref = qq|$rProvInsCreds->{FName} $rProvInsCreds->{LName} $mname|;


    # if($rOrderingPhys->{'NPI'} eq $rProvInsCreds->{'NPI'}) {
    #   $nameofrefa = qq|DK|;
    # }

  }





  $nameofref = substr($nameofref,0,24);                      # limit to 'n' characters
  my $other17a = "";     # don't have "RefPhysRefID RefPhysPIN"
  my $other17b = $NPI_UPD;
# Box 18.
  my ($hospfromyy,$hospfrommm,$hospfromdd) = ('','','');
  my ($hosptoyy,$hosptomm,$hosptodd) = ('','','');
  my $Empty;
  my ($DY, $DM, $DD) = split('-',$Empty);
# Box 19.
  my $addclaim = '';
# Box 20.
  my $Lab = 0;
  my ($outsideyes,$outsideno) = (0,0);
  if ( $Lab ) { $outsideyes = 1; } else { $outsideno = 1; }
  my $outsidecharges = 0;
# Box 21.
  my $diagicd = '0';              # '9' ICD-9-CM or '0' ICD-10-CM – we use ICD10 only
  (my $diaga = $Problems[0]) =~ s/\.//g;;
  (my $diagb = $Problems[1]) =~ s/\.//g;;
  (my $diagc = $Problems[2]) =~ s/\.//g;;
  (my $diagd = $Problems[3]) =~ s/\.//g;;
  (my $diage = $Problems[4]) =~ s/\.//g;;
  (my $diagf = $Problems[5]) =~ s/\.//g;;
  (my $diagg = $Problems[6]) =~ s/\.//g;;
  (my $diagh = $Problems[7]) =~ s/\.//g;;
  (my $diagi = $Problems[8]) =~ s/\.//g;;
  (my $diagj = $Problems[9]) =~ s/\.//g;;
  (my $diagk = $Problems[10]) =~ s/\.//g;;
  (my $diagl = $Problems[11]) =~ s/\.//g;;
# Box 22.
  my ($resubcode,$resubnumber) = ('','');
  $resubcode = substr($resubcode,0,11);                 # limit to 'n' characters
  $resubnumber = substr($resubnumber,0,18);             # limit to 'n' characters
# Box 23.
  my $priorauth = $rPA->{'PAnumber'};
  $priorauth = substr($priorauth,0,29);                 # limit to 'n' characters
# Box 24.
# get the Treatment or Chart Notes info.
my @servicelines = ();
  my ($i,$TotalCharge,$TotalPaid) = (0,0,0);
  foreach my $TrIDidx ( sort keys %{ $HCFAs{$ProviderKey}{$ClientKey}{$InsPAID} } )
  { 
    $i++;
    my $NoteStr = $HCFAs{$ProviderKey}{$ClientKey}{$InsPAID}{$TrIDidx};
    my ($TrID,$ContDate,$BegTime,$EndTime,$SCID,$BillDate,$POS,$Units,$Mod4v) = $NoteStr =~ /(\d*)_(.*)_(.*)_(.*)_(\d*)_(.*)_(.*)_(.*)_(.*)/;
warn qq|i=$i, $ProviderKey,$ClientKey,$InsPAID,$TrIDidx\n| if ( $debug );
warn qq|i=$i, $NoteStr\n| if ( $debug );
warn qq|TrID=$TrID\n| if ( $debug );
warn qq|ContDate=$ContDate\n| if ( $debug );
warn qq|BegTime=$BegTime\n| if ( $debug );
warn qq|EndTime=$EndTime\n| if ( $debug );
warn qq|SCID=$SCID\n| if ( $debug );
warn qq|BillDate=$BillDate\n| if ( $debug );
warn qq|POS=$POS\n| if ( $debug );
warn qq|Units=$Units\n| if ( $debug );
    my $rxSC = cBill->getServiceCode($form,$SCID,$ContDate,$BegTime,$EndTime,$TrID,$BillDate);
    $TotalCharge += $rxSC->{BillAmt};
    my $AmtPaid = $rxSC->{RecAmt};
    $TotalPaid += $AmtPaid;
#   Box 24A.
    my ($ContY,$ContM,$ContD) = split('-',$ContDate);
    my $ContY2 = substr($ContY,2,2);
#   Box 24B.
##  Translate from Service Code / Client -> HCFA
    my $tPOS = DBA->getxref($form,'xPOS',$POS,'Federal');
#   Box 24D.
    my ($SCNum,$Mod1,$Mod2,$Mod3,$Mod4) = split(' ',$rxSC->{SCNum});
warn qq|my ($SCNum,$Mod1,$Mod2,$Mod3,$Mod4)\n| if ( $debug );
    if ( $Mod4v ne '' )
    {
      if ( $Mod1 eq '' ) { $Mod1 = $Mod4v; }
      elsif ( $Mod2 eq '' ) { $Mod2 = $Mod4v; }
      elsif ( $Mod3 eq '' ) { $Mod3 = $Mod4v; }
      elsif ( $Mod4 eq '' ) { $Mod4 = $Mod4v; }
    }
    my $rNoteTrans;
    $rNoteTrans->{SCNum} = $rNotes->{Mod4} eq '' ? $rxSC->{SCNum} : $rxSC->{SCNum}.' '.$rNotes->{Mod4};
#   Box 24E.  (based on above)
    my $AxisLabel = '';
    my $AxisLabeldel = '';      # changed from ',' to null below.
    $sClientNoteProblems->execute($TrID,$NoteProblems[0]) || myDBI->dberror("select ClientNoteProblems ${TrID}/$NoteProblems[0]");
    if ( my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref )
    { $AxisLabel .= 'A'; $AxisLabeldel = ''; } 
    $sClientNoteProblems->execute($TrID,$NoteProblems[1]) || myDBI->dberror("select ClientNoteProblems ${TrID}/$NoteProblems[1]");
    if ( my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref )
    { $AxisLabel .= $AxisLabeldel.'B'; $AxisLabeldel = ''; } 
    $sClientNoteProblems->execute($TrID,$NoteProblems[2]) || myDBI->dberror("select ClientNoteProblems ${TrID}/$NoteProblems[2]");
    if ( my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref )
    { $AxisLabel .= $AxisLabeldel.'C'; $AxisLabeldel = ''; } 
    $sClientNoteProblems->execute($TrID,$NoteProblems[3]) || myDBI->dberror("select ClientNoteProblems ${TrID}/$NoteProblems[3]");
    if ( my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref )
    { $AxisLabel .= $AxisLabeldel.'D'; $AxisLabeldel = ''; } 
#   Box 24F.
    my $ServiceRate = sprintf("%.2f", $rxSC->{ServiceRate});
    $ServiceRate =~ s/\./ /g;;
#   Box 24G. Units
    $Units =~ s/\.00//g;
#   Box 24I. ($ProvRID)
#   Box 24J. ($ProvPIN) ($ProvNPI)

    push(@servicelines, {
        item_info => "",
        mm_from => $ContM,
        dd_from => $ContD,
        yy_from => $ContY2,
        mm_to => $ContM,
        dd_to => $ContD,
        yy_to => $ContY2,
        place_b => $tPOS,
        emg_c => "",
        cpt_d => $SCNum,
        modifier_d1 => $Mod1,
        modifier_d2 => $Mod2,
        modifier_d3 => $Mod3,
        modifier_d4 => $Mod4,
        diag_e => $AxisLabel,
        charge_f => $ServiceRate,
        days_g => $Units,
        epsdt_h => "",
        family_h => "",
        qual_l => $ProvRID,
        id_l => $ProvPIN,
        npi_l => $ProvNPI
    });
    $TotalServices += $TotalCharge;
    $TotalBalance += $TotalPaid;
  }
# Box 25.
  #fix my $fedid = $rClinics->{TaxID};
  (my $fedid = $rClinics->{'TaxID'}) =~ s/[- ]//g;
  $fedid = substr($fedid,0,15);             # limit to 'n' characters
  my $fedssn = 0;
  my $fedein = 1;
# Box 26.
  my $paccount = $ClientID;
# Box 27.
  my $Box27 = 1;
  my $acceptyes = $Box27 ? 1 : 0;
  my $acceptno = !$Box27 ? 1 : 0;
# Box 28.
  my $totcharge = sprintf("%.2f",$TotalCharge);
  $totcharge =~ s/\./ /g;;
# Box 29.
  my $amntpaid = sprintf("%.2f",$TotalPaid);
  $amntpaid =~ s/\./ /g;;
# Box 30.
  my $rsvd30 = sprintf("%.2f",$TotalCharge-$TotalPaid);
  $rsvd30 =~ s/\./ /g;;
  $rsvd30 = '';                            # per Dr. Hamil
# Box 31.

  
  my $ProvName = qq|$rProvider->{FName} $rProvider->{LName}|;
  my $physigned = ${ProvName}.'  '.qq|$rProviderLicenses->{'LicType'} $rProviderLicenses->{'LicNumber'}|;


  if($rCredentials->{'DesigProvID'} ne '') {
    
    $ProvName = qq|$rProvInsCreds->{FName} $rProvInsCreds->{LName}|;
    $physigned = ${ProvName}.'  '.qq|$rProvInsCreds->{'LicType'} $rProvInsCreds->{'LicNumber'}|;
  
  }


  # render Provider replaced with Supervising Provider
  
  # not there anymore...
warn qq|LicType=$rProviderLicenses->{'LicType'}\n| if ( $debug );
warn qq|LicNumber=$rProviderLicenses->{'LicNumber'}\n| if ( $debug );
warn qq|Abbr=$rCredentials->{Abbr}\n| if ( $debug );
  my $phydate = DBUtil->Date($form->{'TODAY'},'fmt','MM/DD/YY');
# Box 32.  Service info: Service Facility or Client address or Clinic.
  my ($servicename,$serviceadd1,$serviceadd2,$servicecsz,$servicea,$serviceb)
   = ('','','','','','');
  my $rFac = DBA->selxref($form,'xNPI','NPI',$rClientRelations->{'FacIDNPI'});
  if ( $rFac->{'NPI'} ne '' )
  {
    $servicename = $rFac->{'ProvOrgName'};
    $serviceadd1 = qq|$rFac->{Addr1} $rFac->{Addr2}|;
    $serviceadd2 = qq|$rFac->{City} $rFac->{ST} $rFac->{Zip}|;
    $servicea = $rFac->{NPI};
    $serviceb = qq|$rClinics->{RefID} $rClinics->{PIN}|;
  } 
# per Dr. Hamil
#  elsif ( $InsDescr =~ /medicaid/i )   # just client address.
#  {
#    $servicename = qq|$rClient->{LName}, $rClient->{FName} $rClient->{MName}|;
#    $serviceadd1 = qq|$rClient->{Addr1} $rClient->{Addr2}|;
#    $serviceadd2 = qq|$rClient->{City} $rClient->{ST} $rClient->{Zip}|;
#  }
#  else
#  {
#    $servicename = $rClinics->{Name} ? $rClinics->{Name}
#                                     : "No ${insurancename} Contract for Clinic";
#    $serviceadd1 = qq|$rClinics->{Addr1} $rClinics->{Addr2}|;
#    $serviceadd2 = qq|$rClinics->{City} $rClinics->{ST} $rClinics->{Zip}|;
#  }
  $servicename =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $servicename =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $servicename = substr($servicename,0,26);             # limit to 'n' characters
  $serviceadd1 =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $serviceadd1 =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $serviceadd1 = substr($serviceadd1,0,26);             # limit to 'n' characters
  $serviceadd2 =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $serviceadd2 =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $serviceadd2 = substr($serviceadd2,0,26);             # limit to 'n' characters
  $serviceb = substr($serviceb,0,14);                   # limit to 'n' characters
# Box 33. Billing Provider / PayTo Provider is Clinic or Agency
  my ($billingname,$billingadd1,$billingadd2,$billingcsz,$billingphone,$billinga,$billingb)
   = ('','','','','','','');
  if ( $rClinics->{UseAgency} )
  {
    my $AgencyID = MgrTree->getManager($form,$ClinicID);
    $sProvider->execute($AgencyID);
    my $rBilling = $sProvider->fetchrow_hashref;
    $billingname = $rBilling->{'Name'};
    $billingadd1 = qq|$rBilling->{Addr1} $rBilling->{Addr2}|;
    $billingadd2 = qq|$rBilling->{City} $rBilling->{ST} $rBilling->{Zip}|;
    my ($AC,$PH) = split('-',$rBilling->{'WkPh'},2);
    $AC = substr($AC,0,3);                            # limit to 'n' characters
    $PH =~ s/[- ]//g;
    $PH = substr($PH,0,9);                            # limit to 'n' characters
    $billingphone = qq|${AC} ${PH}|;
    # always use Clinic for these
    $billinga = $rClinics->{NPI};
    $billingb = qq||;

  }
  else
  {
    $billingname = $rClinics->{Name} eq '' ? "No ${insurancename} Contract for Clinic"
                                           : $rClinics->{Name};
    $billingname = $rClinics->{'Name'};
    $billingadd1 = qq|$rClinics->{Addr1} $rClinics->{Addr2}|;
    $billingadd2 = qq|$rClinics->{City} $rClinics->{ST} $rClinics->{Zip}|;
    my ($AC,$PH) = split('-',$rClinics->{'WkPh'},2);
    $AC = substr($AC,0,3);                            # limit to 'n' characters
    $PH =~ s/[- ]//g;
    $PH = substr($PH,0,9);                            # limit to 'n' characters
    $billingphone = qq|${AC} ${PH}|;
    $billinga = $rClinics->{NPI};
    $billingb = qq||;

  }

  my $contInsId =$rClinics->{InsID};

  if( $contInsId eq '451' || $contInsId eq '452' || $contInsId eq '453') {
      $billingb = qq|$rClinics->{Taxonomy}|;
  }
  $billingname =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $billingname =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $billingname = substr($billingname,0,29);             # limit to 'n' characters
  $billingadd1 =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $billingadd1 =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $billingadd1 = substr($billingadd1,0,29);             # limit to 'n' characters
  $billingadd2 =~ s/[^a-zA-Z0-9\s]+//g;                 # eliminate all chars but these
  $billingadd2 =~ s/^\s*(.*?)\s*$/$1/g;                 # eliminate before/after spaces
  $billingadd2 = substr($billingadd2,0,29);             # limit to 'n' characters

##########################################
    my $name = $insurancename;
    my $address1 = $insurancestreet1;
    my $address2 = $insurancestreet2;
##
# Symbols
    my $medicare_1 = $medicare;
    my $medicaid_1 = $medicaid;
    my $tricare_1 = $tricare;
    my $champva_1 = $champva;
    my $group_1 = $groupins;
    my $feca_1 = $feca;
    my $other_1 = $otherins;
    my $m_3 = $psexm;
    my $f_3 = $psexf;
    my $self_6 = $pself;
    my $spouse_6 = $pspouse;
    my $child_6 = $pchild;
    my $other_6 = $pother;
    my $yes_10a = $empyes;
    my $no_10a = $empno;
    my $yes_10b = $autoyes;
    my $no_10b = $autono;
    my $yes_10c = $otheryes;
    my $no_10c = $otherno;
    my $m_11a = $inssexm;
    my $f_11a = $inssexf;
    my $yes_11d = $anotheryes;
    my $no_11d = $anotherno;
    my $yes_20 = $outsideyes;
    my $no_20 = $outsideno;
    my $ssn_25 = $fedssn;
    my $ein_25 = $fedein;
    my $yes_27 = $acceptyes;
    my $no_27 = $acceptno;
##
# Fields
    my $number_1a = $insid;
    my $fullname_2 = $PatientName;
    my $mm_3 = $PatientDOBM;
    my $dd_3 = $PatientDOBD;
    my $yy_3 = $PatientDOBY;
    my $fullname_4 = $insname;
    my $addr_5 = $PatientAddr;
    my $city_5 = $PatientCity;
    my $state_5 = $PatientST;
    my $zip_5 = $PatientZip;
    my ($area_5, $phone_5) = split(' ', "$PatientHmPh");
    my $addr_7 = $InsuredAddr;
    my $city_7 = $InsuredCity;
    my $state_7 = $InsuredST;
    my $zip_7 = $InsuredZip;
    my ($area_7, $phone_7) = split(' ', $InsuredHmPh);
    my $reserved_8 = $reserved3;
    my $fullname_9 = $OtherName;
    my $number_9a = $OtherGrpNum;
    my $reserved_9b = $reserved1;
    my $reserved_9c = $reserved2;
    my $name_9d = $OtherPlanName;
    my $state_10 = $autostate;
    my $codes_10d = $claimcodes;
    my $number_11 = $InsuredGrpNum;
    my $mm_11a = $InsuredDOBM;
    my $dd_11a = $InsuredDOBD;
    my $yy_11a = $InsuredDOBY;
    my ($qual_11b, $id_11b) = split(' ', $otherclaim);
    my $name_11c = $InsuredPlanName;
    my $signed_12 = "SOF";
    my $date_12 = $pdate;
    my $signed_13 = "SOF";
    my $mm_14 = $lmpmm;
    my $dd_14 = $lmpdd;
    my $yy_14 = $lmpyy;
    my $qual_14 = $lmpqual;
    my $qual_15 = $otherqual;
    my $mm_15 = $othermm;
    my $dd_15 = $otherdd;
    my $yy_15 = $otheryy;
    my $mm_from_16 = $datepfrommm;
    my $dd_from_16 = $datepfromdd;
    my $yy_from_16 = $datepfromyy;
    my $mm_to_16 = $dateptomm;
    my $dd_to_16 = $dateptodd;
    my $yy_to_16 = $dateptoyy;
    my $qual_17 = $nameofrefa;
    my $name_17 = $nameofref;
    my $qual_17a = "";
    my $number_17a = $other17a;
    my $npi_17b = $other17b;
    my $mm_from_18 = $hospfrommm;
    my $dd_from_18 = $hospfromdd;
    my $yy_from_18 = $hospfromyy;
    my $mm_to_18 = $hosptomm;
    my $dd_to_18 = $hosptodd;
    my $yy_to_18 = $hosptoyy;
    my $info_19 = $addclaim;
    my $charges_20 = $outsidecharges;
    my $qual_icd_21 = $diagicd;
    my $number_21a = $diaga;
    my $number_21b = $diagb;
    my $number_21c = $diagc;
    my $number_21d = $diagd;
    my $number_21e = $diage;
    my $number_21f = $diagf;
    my $number_21g = $diagg;
    my $number_21h = $diagh;
    my $number_21i = $diagi;
    my $number_21j = $diagj;
    my $number_21k = $diagk;
    my $number_21l = $diagl;
    my $code_22 = $resubcode;
    my $number_22 = $resubnumber;
    my $number_23 = $priorauth;
    my $number_25 = $fedid;
    my $number_26 = $paccount;
    my $charge_28 = $totcharge;
    my $amount_29 = $amntpaid;
    my $rsvd_30 = $rsvd30;
    my $signature_31 = $physigned;
    my $signed_31 = "SOF";
    my $date_31 = $phydate;
    my $info_32 = "$servicename\n$serviceadd1\n$serviceadd2\n$servicecsz";
    my $number_32a = $servicea;
    my $number_32b = $serviceb;
    my $info_33 = "$billingname\n$billingadd1\n$billingadd2\n$billingcsz";
    my ($area_33, $phone_33) = split(' ', $billingphone);
    my $number_33a = $billinga;
    my $number_33b = $billingb;

##

    my $adjustLeftMargin = 0;
    my $adjustTopMargin = 0;
    if ($HCFAtype eq "red"){
    	$adjustLeftMargin = 37;
	$adjustTopMargin = 32;
    }

    my @symbols = (
        [$medicare_1, 62.4 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$medicaid_1, 111.4 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$tricare_1, 161.6 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$champva_1, 226.6 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$group_1, 277.3 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$feca_1, 334.8 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$other_1, 378.2 - $adjustLeftMargin, 153 - $adjustTopMargin],
        [$m_3, 356.3 - $adjustLeftMargin, 176.9 - $adjustTopMargin],
        [$f_3, 392.2 - $adjustLeftMargin, 176.9 - $adjustTopMargin],
        [$self_6, 291.6 - $adjustLeftMargin, 201.6 - $adjustTopMargin],
        [$spouse_6, 328.1 - $adjustLeftMargin, 201.6 - $adjustTopMargin],
        [$child_6, 356.3 - $adjustLeftMargin, 201.6 - $adjustTopMargin],
        [$other_6, 392.5 - $adjustLeftMargin, 201.6 - $adjustTopMargin],
        [$yes_10a, 306.1 - $adjustLeftMargin, 297.6 - $adjustTopMargin],
        [$no_10a, 349.2 - $adjustLeftMargin, 297.6 - $adjustTopMargin],
        [$yes_10b, 306.1 - $adjustLeftMargin, 321.5 - $adjustTopMargin],
        [$no_10b, 349.2 - $adjustLeftMargin, 321.5 - $adjustTopMargin],
        [$yes_10c, 306.1 - $adjustLeftMargin, 345.1 - $adjustTopMargin],
        [$no_10c, 349.2 - $adjustLeftMargin, 345.1 - $adjustTopMargin],
        [$m_11a, 543.4 - $adjustLeftMargin, 297.1 - $adjustTopMargin],
        [$f_11a, 594 - $adjustLeftMargin, 297.1 - $adjustTopMargin],
        [$yes_11d, 428 - $adjustLeftMargin, 369.1 - $adjustTopMargin],
        [$no_11d, 464.7 - $adjustLeftMargin, 369.1 - $adjustTopMargin],
        [$yes_20, 428.6 - $adjustLeftMargin, 488.6 - $adjustTopMargin],
        [$no_20, 465 - $adjustLeftMargin, 488.6 - $adjustTopMargin],
        [$ssn_25, 177.4 - $adjustLeftMargin, 728.2 - $adjustTopMargin],
        [$ein_25, 191.9 - $adjustLeftMargin, 728.2 - $adjustTopMargin],
        [$yes_27, 328.4 - $adjustLeftMargin, 728.2 - $adjustTopMargin],
        [$no_27, 364.4 - $adjustLeftMargin, 728.2 - $adjustTopMargin],
    );


    my @textlines = (
        [$name, 341.8 - $adjustLeftMargin, 86.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$address1, 341.8 - $adjustLeftMargin, 98.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$address2, 341.8 - $adjustLeftMargin, 111.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$insurancecityzip, 341.8 - $adjustLeftMargin, 123.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_1a, 424.1 - $adjustLeftMargin, 153 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$fullname_2, 69.8 - $adjustLeftMargin, 175.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_3, 280.1 - $adjustLeftMargin, 177.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_3 , 301.7 - $adjustLeftMargin, 177.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_3 , 322.2 - $adjustLeftMargin, 177.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$fullname_4 , 420.8 - $adjustLeftMargin, 175.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$addr_5 , 69.8 - $adjustLeftMargin, 200.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$addr_7, 420.8 - $adjustLeftMargin, 200.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$city_5, 69.8 - $adjustLeftMargin, 223.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$state_5, 245.2 - $adjustLeftMargin, 223.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$city_7, 420.8 - $adjustLeftMargin, 223.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$state_7, 587.2 - $adjustLeftMargin, 223.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$zip_5, 69.8 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$area_5 , 173.5 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid position={center bottom}"],
        [$phone_5, 193 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$zip_7, 420.8 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$area_7, 533.5 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid position={center bottom}"],
        [$phone_7, 554 - $adjustLeftMargin, 249.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$fullname_9, 69.8 - $adjustLeftMargin, 271.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_9a, 69.8 - $adjustLeftMargin, 295.2 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$reserved_9b, 69.8 - $adjustLeftMargin, 320.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$reserved_9c, 69.8 - $adjustLeftMargin, 344.2 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$name_9d, 69.8 - $adjustLeftMargin, 367.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$state_10, 385.9 - $adjustLeftMargin, 321.5 - $adjustTopMargin, "fontsize=$fontsizemid position={center bottom}"],
        [$codes_10d, 276.5 - $adjustLeftMargin, 367.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_11, 423.7 - $adjustLeftMargin, 271.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_11a, 439.2 - $adjustLeftMargin, 298.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_11a, 461.2 - $adjustLeftMargin, 298.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_11a, 481.3 - $adjustLeftMargin, 298.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$qual_11b, 415.4 - $adjustLeftMargin, 320.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$id_11b, 435.6 - $adjustLeftMargin, 320.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$name_11c, 420.8 - $adjustLeftMargin, 344.2 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$signed_12, 99.4 - $adjustLeftMargin, 414.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$date_12, 316.4 - $adjustLeftMargin, 414.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$signed_13, 456.5 - $adjustLeftMargin, 414.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_14, 71.3 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_14, 94 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_14, 113.4 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$qual_14, 171 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$qual_15, 277.9 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_15, 322.2 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_15, 345.6 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_15, 365 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_from_16, 443.5 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_from_16, 466.9 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_from_16, 488.5 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_to_16, 545.4 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_to_16, 567.7 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_to_16, 586.8 - $adjustLeftMargin, 441.7 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$qual_17, 78.8 - $adjustLeftMargin, 463.3 - $adjustTopMargin, "fontsize=$fontsizemid position={right bottom}"],
        [$name_17, 83.2 - $adjustLeftMargin, 463.3 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$qual_17a, 270.7 - $adjustLeftMargin, 454 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_17a, 286.2 - $adjustLeftMargin, 454 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$npi_17b, 286.2 - $adjustLeftMargin, 465.5 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_from_18, 443.5 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_from_18, 466.9 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_from_18, 488.5 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$mm_to_18, 545.4 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$dd_to_18, 567.7 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$yy_to_18, 586.8 - $adjustLeftMargin, 464.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$info_19, 69.8 - $adjustLeftMargin, 488.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$charges_20, 561.2 - $adjustLeftMargin, 488.5 - $adjustTopMargin, "fontsize=$fontsizemid position={right bottom}"],
        [$qual_icd_21, 361.9 - $adjustLeftMargin, 502.6 - $adjustTopMargin, "fontsize=$fontsizemid position={center bottom}"],
        [$number_21a, 76.2 - $adjustLeftMargin, 513.6 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21b, 169.4 - $adjustLeftMargin, 513.6 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21c, 263.4 - $adjustLeftMargin, 513.6 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21d, 356.6 - $adjustLeftMargin, 514.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21e, 76.2 - $adjustLeftMargin, 525.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21f, 169.4 - $adjustLeftMargin, 525.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21g, 263.4 - $adjustLeftMargin, 525.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21h, 356.6 - $adjustLeftMargin, 526.1 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21i, 76.2 - $adjustLeftMargin, 537.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21j, 169.4 - $adjustLeftMargin, 537.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21k, 263.4 - $adjustLeftMargin, 537.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_21l, 356.6 - $adjustLeftMargin, 537.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$code_22, 423.8 - $adjustLeftMargin, 513.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_22, 498.5 - $adjustLeftMargin, 513.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_23, 423.8 - $adjustLeftMargin, 537.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_25, 69.8 - $adjustLeftMargin, 727.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_26, 226.1 - $adjustLeftMargin, 727.9 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$charge_28, 484.3 - $adjustLeftMargin, 727.9 - $adjustTopMargin, "fontsize=$fontsizemid position={right bottom}"],
        [$amount_29, 555.9 - $adjustLeftMargin, 727.9 - $adjustTopMargin, "fontsize=$fontsizemid position={right bottom}"],
        [$rsvd_30, 620.7 - $adjustLeftMargin, 727.9 - $adjustTopMargin, "fontsize=$fontsizemid position={right bottom}"],
        [$signed_31, 88.6 - $adjustLeftMargin, 789.8 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$date_31, 171 - $adjustLeftMargin, 781.6 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_32a, 228.6 - $adjustLeftMargin, 788.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_32b, 308.2 - $adjustLeftMargin, 788.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$area_33, 566.7 - $adjustLeftMargin, 741.2 - $adjustTopMargin, "fontsize=$fontsizemid position={center bottom}"],
        [$phone_33, 584.4 - $adjustLeftMargin, 741.2 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$number_33a, 423.7 - $adjustLeftMargin, 788.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
        # 33b Removed: changed
        [$number_33b, 503.3 - $adjustLeftMargin, 788.4 - $adjustTopMargin, "fontsize=$fontsizemid"],
    );
    for (my $i=0; $i <= $#servicelines; $i++) {
        push(@textlines, [$servicelines[$i]->{item_info}, 0 - $adjustLeftMargin, 572.9 - $adjustTopMargin + $i * 24, "fontsize=$fontsize"]);
        push(@textlines, [$servicelines[$i]->{mm_from}, 69.8 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{dd_from}, 90 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{yy_from}, 111.4 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{mm_to}, 133.4 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{dd_to}, 155 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{yy_to}, 176.9 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{place_b}, 199 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{emg_c}, 221 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{cpt_d}, 258.5 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{modifier_d1}, 299 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{modifier_d2}, 320.4 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{modifier_d3}, 342 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{modifier_d4}, 363.8 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{diag_e}, 391 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{charge_f}, 467.7 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={right bottom}"]);
        push(@textlines, [$servicelines[$i]->{days_g}, 489.8 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{epsdt_h}, 511.7 - $adjustLeftMargin, 572.9 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{family_h}, 511.7 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{qual_l}, 529.4 - $adjustLeftMargin, 572.9 - $adjustTopMargin + $i * 24, "fontsize=$fontsize position={center bottom}"]);
        push(@textlines, [$servicelines[$i]->{id_l}, 542.9 - $adjustLeftMargin, 572.9 - $adjustTopMargin + $i * 24, "fontsize=$fontsize"]);
        push(@textlines, [$servicelines[$i]->{npi_l}, 542.9 - $adjustLeftMargin, 585.1 - $adjustTopMargin + $i * 24, "fontsize=$fontsize"]);
    }

    my @textflows = (
        [$reserved_8, 276.5 - $adjustLeftMargin, 249.1 , 402.8, 210 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$signature_31, 69.8 - $adjustLeftMargin, 781.6 , 166.7, 757 - $adjustTopMargin, "fontsize=$fontsizemid"],
        [$info_32, 223.6 - $adjustLeftMargin, 777.3 - $adjustTopMargin, 402.8, 736.9 - $adjustTopMargin, "fontsize=$fontsize"],
        [$info_33, 418.3 - $adjustLeftMargin, 777.3 - $adjustTopMargin, 619.6, 736.9 - $adjustTopMargin, "fontsize=$fontsize"],
    );

    $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 1.0);

    main->renderTextLines($p, @textlines);
    main->renderSymbols($p, @symbols);
    main->renderTextFlowsContent($p, @textflows);
}
############################################################################
sub convertICD9
{
  my ($self,$ICD10,$UUID,$TrID) = @_;
## convert to ICD9 for now....
warn qq|convertICD9: ICD10=${ICD10}, UUID=${UUID}\n| if ( $debug );
  my ($ICD10,$rows,$ICD9) = main->findICD9($form,$UUID);
  $ICD9 =~ s/^\s*(.*?)\s*$/$1/g;             # trim leading/trailing spaces
  if ( $rows > 1 )
  {
    print qq|>>>ERROR: Check ClientProblems MULTIPLE: ${TrID} (${ICD10}:${rows}:${ICD9})\n|;
    my ($firstone,$rest) = split(' ',$ICD9,2);
    $ICD9 = $firstone;
  }
  return($ICD9);
}
sub findICD9
{
  my ($self,$form,$UUID) = @_;
  my %icd10to9 = (
    'F33.3' => '29634',
    'F34.1' => '3004',
    'F43.21' => '3090',
    'F63.81' => '31234',
    'H54.40' => '36960',
    'I50.9' => '4289',
    'J44.1' => '49322',
    'J45.20' => '49300',
    'R52' => '78096',
    'T14.91' => 'E9589',
    'F19.20' => '30460',
    'F90.9' => '31401',
    'I10' => '4019',
    'I11.9' => '40290',
    'J44.9' => '49320',
    'F10.10' => '30500',
    'L03.119' => '6827',
    'F05' => '2930',
    'F19.21' => '30463',
    'F32.3' => '29624',
    'F32.9' => '311',
    'F60.3' => '30183',
    'F84.0' => '29900',
    'F91.1' => '31281',
    'F91.2' => '31282',
    'F91.8' => '31289',
    'Z65.8' => 'V6289',
    'F10.20' => '30390',
    'F22' => '2970',
    'Z63.4' => 'V618',
    'F12.10' => '30520',
    'G47.30' => '78057',
    'F03.90' => '29420',
    'F14.23' => '30420',
    'F63.3' => '31239',
    'F64.1' => '30285',
    'F81.0' => '31500',
    'F81.81' => '3152',
    'F81.9' => '3159',
    'J45.21' => '49302',
    'K76.9' => '5739',
    'F11.20' => '30400',
    'F12.20' => '30430',
    'F13.20' => '30410',
    'F14.20' => '30420',
    'F15.20' => '30440',
    'F23' => '2988',
    'F48.9' => 'V409',
    'F11.10' => '30550',
    'F11.129' => '30550',
    'F13.10' => '30540',
    'F15.10' => '30570',
    'F16.10' => '30530',
    'F19.10' => '30580',
    'F93.8' => '31389',
    'F52.9' => '30270',
    'F84.5' => '29980',
    'B00.9' => '0549',
    'Z63.79' => 'V6149',
    'M19.90' => '71590',
    'Y07.499' => 'E9677',
    'Z71.1' => 'V7109',
    'Z03.89' => 'V7109',
    'Z04.9' => 'V7109',
    'Z63.8' => 'V6109',
    'Q05.9' => '74190',
    'F10.129' => '30500',
    'F14.10' => '30560',
    'M16.9' => '71595',
    'M15.9' => '71500',
    'M35.2' => '1361',
    'F10.229' => '30300',
    'H31.019' => '36332',
    'R46.89' => 'V4039', 
    'J45.40' => '49300', 
    'F60.4' => '30150',
    'F90.8' => '31401',
    'R68.89' => '78099',
    'H91.8X9' => '3888',
    'O90.6' => '64842',
    'Z87.09' => 'V1260',
    'Z63.32' => 'V6108',
    'F45.8' => '3068',
    'Z71.9' => 'V6540',
    'G12.29' => '33529',
    'Q74.2' => '75569',
    'T74.02XA' => '99552',
    'Z86.59' => 'V119',
    'F18.10' => '30590',
    'R99' => '7999',
    'G40.89' => '34580',
    'F48.8' => '30089',
    'T14.8' => '9599',
    'H90.5' => '38910',
    'E46' => '2639',
    'Z13.89' => 'V799',
    'F60.89' => '30184',
    'F50.8' => '30759',
    'F84.8' => '29980',
    'Z89.9' => 'V4970',
    'Z87.59' => 'V1329',
    'G40.109' => '34550',
    'R46.81' => 'V4039',
    'F94.8' => '30929'
  );
  my ($ICD10,$list) = ('','');
  my $sTest=$cdbh->prepare("select misICD10.ICD10,misICD10.sctName,misICD10.icdName,cmsI10gem.ICD9 from misICD10 left join okmis_config.cmsI10gem on cmsI10gem.ICD10=REPLACE(misICD10.ICD10,'.','') where misICD10.ID=?");
  $sTest->execute($UUID);
  my $rows = $sTest->rows;
  my $ICD10;
  while ( my $rTest = $sTest->fetchrow_hashref )
  { $ICD10 = $rTest->{'ICD10'}; $list .= qq|$rTest->{'ICD9'} |; }
warn qq|findICD9: ICD10=$ICD10, ICD9=$list\n| if ( $debug );
  $sTest->finish();
  if ( $rows > 1 && exists($icd10to9{$ICD10}) )
  { $rows = 1; $list = $icd10to9{$ICD10}; }
  if ( $ICD10 eq 'Z71.1' || $ICD10 eq 'Z03.89' || $ICD10 eq 'Z04.9' )
  { $rows = 1; $list = 'V7109'; }
warn qq|findICD9: ICD10=$ICD10, rows=$rows, list=$list\n| if ( $debug );
  return($ICD10,$rows,$list);
}
############################################################################

sub createClaimForm {
    my ($self, $p) = @_;
    
   # my $image = $p->load_image("auto", $qrcodeimage, "");
    # $p->fit_image($image, $marginleft - 2, 92.5, "boxsize={42 42} fitmethod=meet");
    # $p->close_image($image);

    if ($HCFAtype eq "red") {
        $p->setcolor("stroke", "cmyk", 0.0, 0.0, 0.0, 0.0);
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("stroke", "cmyk", 0, 0, 0, 1);
        $p->setcolor("fill", "cmyk", 0, 0, 0, 1);
    }
    

    $p->fit_textline("HEALTH INSURANCE CLAIM FORM", $marginleft + 0.4, 103.5, $baseboldlargefontoptions);
    $p->fit_textline("APPROVED BY NATIONAL UNIFORM CLAIM COMMITTEE (NUCC) 02/12", $marginleft + 0.8, 115.6, $basexxsmallfontoptions);

    $p->setlinewidth($linewidth4);
    $p->rect($marginleft + 0.9, 131.2, 7, 8.7);
    $p->rect($marginleft + 7.9, 131.2, 7, 8.7);
    $p->rect($marginleft + 14.9, 131.2, 7, 8.7);
    $p->stroke();
    $p->fit_textline("PICA", 83, 126.7, $basexxsmallfontoptions);

    $p->fit_textline("PICA", 590.9, 127.3, $basexxsmallfontoptions);
    $p->rect(607.7, 131.2, 7, 8.7);
    $p->rect(614.7, 131.2, 7, 8.7);
    $p->rect(621.7, 131.2, 7, 8.7);
    $p->stroke();
##
# Fill Rect
    if ($HCFAtype eq "red") {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("fill", "cmyk", 0.27, 0.19, 0.17, 0.01);
    }
    $p->rect(252.7, 455.5, 158.6, 12);
    $p->rect($marginleft, 575.5, $formwidth, 12.6);
    $p->rect($marginleft, 599.3, $formwidth, 12.3);
    $p->rect($marginleft, 623.1, $formwidth, 11.6);
    $p->rect($marginleft, 647.5, $formwidth, 12.5);
    $p->rect($marginleft, 671.1, $formwidth, 11.6);
    $p->rect($marginleft, 695, $formwidth, 12);
    $p->rect(227.5, 706.8, 8.7, 143.9);
    $p->rect(280, 706.8, 7.6, 143.9);
    $p->rect(406.7, 706.8, 8.5, 143.9);
    $p->rect(252.7, 455.5, 158.6, 12);
    $p->rect(300, 792.2, 111.3, 14.1);
    $p->rect(494.4, 792.2, 134.6, 14.1);
    $p->fill();
##

##
# Header line
    $p->setlinewidth($linewidth1);
    $p->moveto($marginleft, 132.2);
    $p->lineto($marginleft + $formwidth, 132.2);
    $p->stroke();
##

##
# Left Vertical Line
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 132.2 - $linewidth1 / 2);
    $p->lineto($marginleft, 792.2 + $linewidth1 / 2);
    $p->stroke();
##
# Numbers
    if ($HCFAtype eq "red") {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("fill", "cmyk", 0, 0, 0, 1);
    }
    $p->fit_textline("1", 55, 578.6, $basexlargefontoptions . " position={center bottom}");
    $p->fit_textline("2", 55, 603.4, $basexlargefontoptions . " position={center bottom}");
    $p->fit_textline("3", 55, 627.4, $basexlargefontoptions . " position={center bottom}");
    $p->fit_textline("4", 55, 651.1, $basexlargefontoptions . " position={center bottom}");
    $p->fit_textline("5", 55, 676.5, $basexlargefontoptions . " position={center bottom}");
    $p->fit_textline("6", 55, 700.2, $basexlargefontoptions . " position={center bottom}");
##
# Vertical Line 1
    $p->setlinewidth($linewidth3);
    $p->moveto(266.6, 157);
    $p->lineto(266.6, 372.5);
    $p->stroke();
##
# Vertical Line 2
    $p->setlinewidth($linewidth2);
    $p->moveto(411.3, 132.2);
    $p->lineto(411.3, 562.3);
    $p->stroke();
##
######## Section 1 Horizontal Lines
##
# Line 1
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 157);
    $p->lineto($marginleft + $formwidth, 157);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(295.3, 166.2);
    $p->lineto(295.3, 179.6);
    $p->moveto(317.6, 166.2);
    $p->lineto(317.6, 179.6);
    $p->stroke();
# Line 2
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 179.6);
    $p->lineto($marginleft + $formwidth, 179.6);
    $p->stroke();
##
# Line 3
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 204.5);
    $p->lineto($marginleft + $formwidth, 204.5);
    $p->stroke();
##
# Line 4
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 227.5);
    $p->lineto(266.6, 227.5);
    $p->moveto(411.3, 227.5);
    $p->lineto($marginleft + $formwidth, 227.5);
    $p->moveto(240, 204.5);
    $p->lineto(240, 227.5);
    $p->moveto(582, 204.5);
    $p->lineto(582, 227.5);
    $p->stroke();
##
# Line 5
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 253);
    $p->lineto($marginleft + $formwidth, 253);
    $p->moveto(153.6, 227.5);
    $p->lineto(153.6, 253);
    $p->moveto(504, 227.5);
    $p->lineto(504, 253);
    $p->stroke();
##
# Line 6
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 275.4);
    $p->lineto(266.6, 275.4);
    $p->moveto(411.3, 276.2);
    $p->lineto($marginleft + $formwidth, 276.2);
    $p->stroke();
##
# Line 7
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 298.3);
    $p->lineto(266.6, 298.3);
    $p->moveto(411.3, 301.3);
    $p->lineto($marginleft + $formwidth, 301.3);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(454.2, 286.2);
    $p->lineto(454.2, 299.4);
    $p->moveto(475.4, 286.2);
    $p->lineto(475.4, 299.4);
    $p->stroke();
##
# Line 8
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 324.2);
    $p->lineto(266.6, 324.2);
    $p->moveto(411.3, 324);
    $p->lineto($marginleft + $formwidth, 324);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(428.8, 309.1);
    $p->lineto(428.8, 322.5);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth4);
    $p->moveto(375.5, 317.5);
    $p->lineto(375.5, 322.8);
    $p->moveto(375.5, 322.7);
    $p->lineto(396.3, 322.7);
    $p->moveto(396.3, 322.8);
    $p->lineto(396.3, 317.5);
    $p->stroke();
##
# Line 9
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 348.5);
    $p->lineto($marginleft + $formwidth, 348.5);
    $p->stroke();
##
# Line 10
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 372.5);
    $p->lineto($marginleft + $formwidth, 372.5);
    $p->moveto(96.3, 416.6);
    $p->lineto(276.5, 416.6);
    $p->moveto(312.4, 416.7);
    $p->lineto(411.3, 416.7);
    $p->moveto(452.7, 416.9);
    $p->lineto($marginleft + $formwidth, 416.9);
    $p->stroke();
##
########
##
# Mid line
    $p->setlinewidth($linewidth1);
    $p->moveto($marginleft, 420.2);
    $p->lineto($marginleft + $formwidth, 420.2);
    $p->stroke();
##
######## Section 2 Horizontal lines
##
    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(86.8, 430.4);
    $p->lineto(86.8, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(108.1, 430.4);
    $p->lineto(108.1, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(166, 429.3);
    $p->lineto(166, 442.3);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(252.7, 420.2);
    $p->lineto(252.7, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(273.6, 430.4);
    $p->lineto(273.6, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(299.3, 430.4);
    $p->lineto(299.3, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(339.4, 430.4);
    $p->lineto(339.4, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(360.5, 430.4);
    $p->lineto(360.5, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(459.1, 430.4);
    $p->lineto(459.1, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(482.9, 430.4);
    $p->lineto(482.9, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(561.1, 430.4);
    $p->lineto(561.1, 443.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(582, 430.4);
    $p->lineto(582, 443.5);
    $p->stroke();
# Line 1
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 443.5);
    $p->lineto($marginleft + $formwidth, 443.5);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(80.9, 453.9);
    $p->lineto(80.9, 467.1);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(253.2, 455.8);
    $p->lineto(410.7, 455.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(269, 443.5);
    $p->lineto(269, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(284.7, 443.5);
    $p->lineto(284.7, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(459.1, 454.4);
    $p->lineto(459.1, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(482.9, 454.4);
    $p->lineto(482.9, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(561.1, 454.4);
    $p->lineto(561.1, 467.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.1}");
    $p->setlinewidth($linewidth4);
    $p->moveto(582, 454.4);
    $p->lineto(582, 467.5);
    $p->stroke();
# Line 2
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 467.5);
    $p->lineto($marginleft + $formwidth, 467.5);
    $p->stroke();
##
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(494.7, 479.5);
    $p->lineto(494.7, 492);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(564, 479.5);
    $p->lineto(564, 492);
    $p->stroke();
# Line 3
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 492);
    $p->lineto($marginleft + $formwidth, 492);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(354.7, 492);
    $p->lineto(354.7, 505.4);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(368.5, 492);
    $p->lineto(368.5, 505.4);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(74, 509);
    $p->lineto(74, 515);
    $p->moveto(74, 514.8);
    $p->lineto(124.8, 514.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(167.2, 509.3);
    $p->lineto(167.2, 515.3);
    $p->moveto(167.2, 515.1);
    $p->lineto(218.3, 515.1);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(261.4, 508.8);
    $p->lineto(261.4, 514.8);
    $p->moveto(261.4, 514.6);
    $p->lineto(311.8, 514.6);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(354.7, 509.8);
    $p->lineto(354.7, 516);
    $p->moveto(354.7, 515.8);
    $p->lineto(406.1, 515.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(74, 520.3);
    $p->lineto(74, 526.6);
    $p->moveto(74, 526.4);
    $p->lineto(124.8, 526.4);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(167.2, 521.1);
    $p->lineto(167.2, 527.2);
    $p->moveto(167.2, 527);
    $p->lineto(218.3, 527);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(261.4, 521);
    $p->lineto(261.4, 527);
    $p->moveto(261.4, 526.8);
    $p->lineto(311.8, 526.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(354.7, 522.1);
    $p->lineto(354.7, 528.2);
    $p->moveto(354.7, 528);
    $p->lineto(406.1, 528);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(74, 532.8);
    $p->lineto(74, 538.8);
    $p->moveto(74, 538.6);
    $p->lineto(124.8, 538.6);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(167.2, 533.3);
    $p->lineto(167.2, 539.3);
    $p->moveto(167.2, 539.1);
    $p->lineto(218.3, 539.1);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(261.4, 532.8);
    $p->lineto(261.4, 538.8);
    $p->moveto(261.4, 538.6);
    $p->lineto(311.8, 538.6);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(354.7, 533.1);
    $p->lineto(354.7, 539.1);
    $p->moveto(354.7, 538.9);
    $p->lineto(406.1, 538.9);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(494, 503.5);
    $p->lineto(494, 515.8);
    $p->stroke();
# Line 4
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(411.3, 515.8);
    $p->lineto($marginleft + $formwidth, 515.8);
    $p->stroke();
##
# Line 5
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 540.5);
    $p->lineto(374.5, 540.5);
    $p->moveto(411.3, 540.5);
    $p->lineto($marginleft + $formwidth, 540.5);
    $p->stroke();
##
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(187, 540.5);
    $p->lineto(187, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(210, 540.5);
    $p->lineto(210, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(231.6, 540.5);
    $p->lineto(231.6, 569.1);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(284.2, 557.3);
    $p->lineto(284.2, 562.9);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(374.6, 540.3);
    $p->lineto(374.6, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(475, 540.3);
    $p->lineto(475, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(504.2, 540.3);
    $p->lineto(504.2, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(518.9, 540.3);
    $p->lineto(518.9, 706.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(540.2, 540.3);
    $p->lineto(540.2, 706.8);
    $p->stroke();
# Line 6
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 562.9);
    $p->lineto($marginleft + $formwidth, 562.9);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 574.5);
    $p->lineto(79.6, 587);
    $p->moveto(100.6, 574.5);
    $p->lineto(100.6, 587);
    $p->moveto(143.6, 574.5);
    $p->lineto(143.6, 587);
    $p->moveto(166.3, 574.5);
    $p->lineto(166.3, 587);
    $p->moveto(309.4, 574.5);
    $p->lineto(309.4, 587);
    $p->moveto(331, 574.5);
    $p->lineto(331, 587);
    $p->moveto(352.6, 574.5);
    $p->lineto(352.6, 587);
    $p->moveto(457, 574.5);
    $p->lineto(457, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 574.1);
    $p->lineto(122.6, 587);
    $p->moveto(231.6, 574.1);
    $p->lineto(231.6, 587);
    $p->moveto(284.1, 574.1);
    $p->lineto(284.1, 587);
    $p->moveto(411.4, 574.1);
    $p->lineto(411.4, 587);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 575);
    $p->lineto($marginleft + $formwidth, 575);
    $p->stroke();
# Line 7
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 587);
    $p->lineto($marginleft + $formwidth, 587);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 598.3);
    $p->lineto(79.6, 611.5);
    $p->moveto(100.6, 598.3);
    $p->lineto(100.6, 611.5);
    $p->moveto(143.6, 598.3);
    $p->lineto(143.6, 611.5);
    $p->moveto(166.3, 598.3);
    $p->lineto(166.3, 611.5);
    $p->moveto(309.4, 598.3);
    $p->lineto(309.4, 611.5);
    $p->moveto(331, 598.3);
    $p->lineto(331, 611.5);
    $p->moveto(352.6, 598.3);
    $p->lineto(352.6, 611.5);
    $p->moveto(457, 598.3);
    $p->lineto(457, 611.5);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 599.3);
    $p->lineto(122.6, 611.5);
    $p->moveto(187, 599.3);
    $p->lineto(187, 611.5);
    $p->moveto(210, 599.3);
    $p->lineto(210, 611.5);
    $p->moveto(231.6, 599.3);
    $p->lineto(231.6, 611.5);
    $p->moveto(284.1, 599.3);
    $p->lineto(284.1, 611.5);
    $p->moveto(374.6, 599.3);
    $p->lineto(374.6, 611.5);
    $p->moveto(411.4, 599.3);
    $p->lineto(411.4, 611.5);
    $p->moveto(475, 599.3);
    $p->lineto(475, 611.5);
    $p->moveto(504, 599.3);
    $p->lineto(504, 611.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 599.4);
    $p->lineto($marginleft + $formwidth, 599.4);
    $p->stroke();
# Line 8
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 611.5);
    $p->lineto($marginleft + $formwidth, 611.5);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 622.1);
    $p->lineto(79.6, 635);
    $p->moveto(100.6, 622.1);
    $p->lineto(100.6, 635);
    $p->moveto(143.6, 622.1);
    $p->lineto(143.6, 635);
    $p->moveto(166.3, 622.1);
    $p->lineto(166.3, 635);
    $p->moveto(309.4, 622.1);
    $p->lineto(309.4, 635);
    $p->moveto(331, 622.1);
    $p->lineto(331, 635);
    $p->moveto(352.6, 622.1);
    $p->lineto(352.6, 635);
    $p->moveto(457, 622.1);
    $p->lineto(457, 635);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 623.1);
    $p->lineto(122.6, 635);
    $p->moveto(187, 623.1);
    $p->lineto(187, 635);
    $p->moveto(210, 623.1);
    $p->lineto(210, 635);
    $p->moveto(231.6, 623.1);
    $p->lineto(231.6, 635);
    $p->moveto(284.1, 623.1);
    $p->lineto(284.1, 635);
    $p->moveto(374.6, 623.1);
    $p->lineto(374.6, 635);
    $p->moveto(411.4, 623.1);
    $p->lineto(411.4, 635);
    $p->moveto(475, 623.1);
    $p->lineto(475, 635);
    $p->moveto(504, 623.1);
    $p->lineto(504, 635);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 623);
    $p->lineto($marginleft + $formwidth, 623);
    $p->stroke();
# Line 9
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 635);
    $p->lineto($marginleft + $formwidth, 635);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 646.4);
    $p->lineto(79.6, 659.5);
    $p->moveto(100.6, 646.4);
    $p->lineto(100.6, 659.5);
    $p->moveto(143.6, 646.4);
    $p->lineto(143.6, 659.5);
    $p->moveto(166.3, 646.4);
    $p->lineto(166.3, 659.5);
    $p->moveto(309.4, 646.4);
    $p->lineto(309.4, 659.5);
    $p->moveto(331, 646.4);
    $p->lineto(331, 659.5);
    $p->moveto(352.6, 646.4);
    $p->lineto(352.6, 659.5);
    $p->moveto(457, 646.4);
    $p->lineto(457, 659.5);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 647.4);
    $p->lineto(122.6, 659.5);
    $p->moveto(187, 647.4);
    $p->lineto(187, 659.5);
    $p->moveto(210, 647.4);
    $p->lineto(210, 659.5);
    $p->moveto(231.6, 647.4);
    $p->lineto(231.6, 659.5);
    $p->moveto(284.1, 647.4);
    $p->lineto(284.1, 659.5);
    $p->moveto(374.6, 647.4);
    $p->lineto(374.6, 659.5);
    $p->moveto(411.4, 647.4);
    $p->lineto(411.4, 659.5);
    $p->moveto(475, 647.4);
    $p->lineto(475, 659.5);
    $p->moveto(504, 647.4);
    $p->lineto(504, 659.5);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 647.6);
    $p->lineto($marginleft + $formwidth, 647.6);
    $p->stroke();
# Line 10
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 659.5);
    $p->lineto($marginleft + $formwidth, 659.5);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 669.4);
    $p->lineto(79.6, 683);
    $p->moveto(100.6, 669.4);
    $p->lineto(100.6, 683);
    $p->moveto(143.6, 669.4);
    $p->lineto(143.6, 683);
    $p->moveto(166.3, 669.4);
    $p->lineto(166.3, 683);
    $p->moveto(309.4, 669.4);
    $p->lineto(309.4, 683);
    $p->moveto(331, 669.4);
    $p->lineto(331, 683);
    $p->moveto(352.6, 669.4);
    $p->lineto(352.6, 683);
    $p->moveto(457, 669.4);
    $p->lineto(457, 683);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 671);
    $p->lineto(122.6, 683);
    $p->moveto(187, 671);
    $p->lineto(187, 683);
    $p->moveto(210, 671);
    $p->lineto(210, 683);
    $p->moveto(231.6, 671);
    $p->lineto(231.6, 683);
    $p->moveto(284.1, 671);
    $p->lineto(284.1, 683);
    $p->moveto(374.6, 671);
    $p->lineto(374.6, 683);
    $p->moveto(411.4, 671);
    $p->lineto(411.4, 683);
    $p->moveto(475, 671);
    $p->lineto(475, 683);
    $p->moveto(504, 671);
    $p->lineto(504, 683);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 671);
    $p->lineto($marginleft + $formwidth, 671);
    $p->stroke();
# Line 11
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 683);
    $p->lineto($marginleft + $formwidth, 683);
    $p->stroke();
##
    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(79.6, 693.4);
    $p->lineto(79.6, 706.8);
    $p->moveto(100.6, 693.4);
    $p->lineto(100.6, 706.8);
    $p->moveto(143.6, 693.4);
    $p->lineto(143.6, 706.8);
    $p->moveto(166.3, 693.4);
    $p->lineto(166.3, 706.8);
    $p->moveto(309.4, 693.4);
    $p->lineto(309.4, 706.8);
    $p->moveto(331, 693.4);
    $p->lineto(331, 706.8);
    $p->moveto(352.6, 693.4);
    $p->lineto(352.6, 706.8);
    $p->moveto(457, 693.4);
    $p->lineto(457, 706.8);
    $p->stroke();

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(122.6, 695.2);
    $p->lineto(122.6, 706.8);
    $p->moveto(187, 695.2);
    $p->lineto(187, 706.8);
    $p->moveto(210, 695.2);
    $p->lineto(210, 706.8);
    $p->moveto(231.6, 695.2);
    $p->lineto(231.6, 706.8);
    $p->moveto(284.1, 695.2);
    $p->lineto(284.1, 706.8);
    $p->moveto(374.6, 695.2);
    $p->lineto(374.6, 706.8);
    $p->moveto(411.4, 695.2);
    $p->lineto(411.4, 706.8);
    $p->moveto(475, 695.2);
    $p->lineto(475, 706.8);
    $p->moveto(504, 695.2);
    $p->lineto(504, 706.8);
    $p->stroke();

    $p->set_graphics_option("dasharray={3 2.9}");
    $p->setlinewidth($linewidth4);
    $p->moveto(519.1, 695.2);
    $p->lineto($marginleft + $formwidth, 695.2);
    $p->stroke();
# Line 12
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 706.8);
    $p->lineto($marginleft + $formwidth, 706.8);
    $p->stroke();
##
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(216.5, 706.8);
    $p->lineto(216.5, 792.2);
    $p->moveto(322.1, 706.8);
    $p->lineto(322.1, 731.3);
    $p->moveto(411.4, 706.8);
    $p->lineto(411.4, 792.2);
    $p->moveto(492, 706.8);
    $p->lineto(492, 731.3);
    $p->moveto(560.5, 706.8);
    $p->lineto(560.5, 731.3);
    $p->stroke();

    $p->set_graphics_option("dasharray={3.6 1.2}");
    $p->setlinewidth($linewidth4);
    $p->moveto(472.3, 718.3);
    $p->lineto(472.3, 731.3);
    $p->moveto(543.8, 718.3);
    $p->lineto(543.8, 731.3);
    $p->moveto(608.6, 718.3);
    $p->lineto(608.6, 731.3);
    $p->stroke();
# Line 13
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft, 731.3);
    $p->lineto($marginleft + $formwidth, 731.3);
    $p->stroke();
##
########
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto(216.5, 778.1);
    $p->lineto($marginleft + $formwidth, 778.1);
    $p->moveto(300, 778.1);
    $p->lineto(300, 792.2);
    $p->moveto(494.3, 778.1);
    $p->lineto(494.3, 792.2);
    $p->stroke();

    if ($HCFAtype eq "red") {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("fill", "cmyk", 0.27, 0.19, 0.17, 0.01);
    }
    $p->fit_textline("NPI", 252.4, 789.6, $basefontoptions . " fontsize=14 fakebold=true");
    $p->fit_textline("NPI", 446.6, 789.6, $basefontoptions . " fontsize=14 fakebold=true");
##
# Footer line
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth1);
    $p->moveto($marginleft, 792.2);
    $p->lineto($marginleft + $formwidth, 792.2);
    $p->stroke();
##
    if ($HCFAtype eq "red") {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("fill", "cmyk", 0, 0, 0, 1);
    }
    $p->fit_textline("NUCC Instruction Manual available at: www.nucc.org", $marginleft + 0.2, 801.3, $basesmallfontoptions);
    $p->fit_textline("PLEASE PRINT OR TYPE", 290, 800.6, $baseboldsmallfontoptions . " italicangle=-10");
    $p->fit_textline("APPROVED OMB-0938-1197 FORM 1500 (02-12)", 450.2, 800.3, $basesmallfontoptions);
##
# Right Vertical Line
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft + $formwidth, 132.2 - $linewidth1 / 2);
    $p->lineto($marginleft + $formwidth, 792.2 + $linewidth1 / 2);
    $p->stroke();
##
    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth($linewidth3);
    $p->moveto($marginleft + $formwidth, 791.5);
    $p->lineto(638.2, 791.5);
    $p->moveto(633.6, 784.8);
    $p->lineto(633.6, 706.8);
    $p->moveto(634.3, 535.8);
    $p->lineto(634.3, 427.9);
    $p->moveto(629.3, 420);
    $p->lineto(638.4, 420);
    $p->moveto(633.9, 410.8);
    $p->lineto(633.9, 362.6);
    $p->moveto(634.1, 200);
    $p->lineto(634.1, 140.9);
    $p->moveto(630.4, 133.7);
    $p->lineto(639.4, 133.7);
    $p->moveto(634.1, 127.1);
    $p->lineto(634.1, 117);
    $p->moveto(633.8, 76.8);
    $p->lineto(633.8, 62.9);
    $p->stroke();

    $p->arc(625, 789.5, 8.5, 0, 40);
    $p->arc(633.5, 777.1, 6.4, 240, 300);
    $p->arc(642, 789.5, 8.5, 140, 180);
    $p->fill();

    $p->arc(642.7, 424.5, 8.5, 180, 220);
    $p->arc(634.2, 436.9, 6.4, 60, 120);
    $p->arc(625.7, 424.5, 8.5, 320, 360);
    $p->fill();

    $p->arc(625.3, 415.5, 8.5, 0, 40);
    $p->arc(633.8, 403.1, 6.4, 240, 300);
    $p->arc(642.3, 415.5, 8.5, 140, 180);
    $p->fill();

    $p->arc(642.7, 136.5, 8.5, 180, 220);
    $p->arc(634.2, 148.9, 6.4, 60, 120);
    $p->arc(625.7, 136.5, 8.5, 320, 360);
    $p->fill();

    $p->arc(625.6, 129.5, 8.5, 0, 40);
    $p->arc(634.1, 117.1, 6.4, 240, 300);
    $p->arc(642.6, 129.5, 8.5, 140, 180);
    $p->fill();

    $p->arc(642.3, 59.5, 8.5, 180, 220);
    $p->arc(633.8, 71.9, 6.4, 60, 120);
    $p->arc(625.3, 59.5, 8.5, 320, 360);
    $p->fill();

    if ($HCFAtype eq "red") {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 0.0);
    } else {
        $p->setcolor("fill", "cmyk", 0.0, 0.0, 0.0, 1.0);
    }
    
    $p->fit_textline("PHYSICIAN OR SUPPLIER INFORMATION", 631.4, 700.8, $baseboldsmallfontoptions . " orientate=west");
    $p->fit_textline("PATIENT AND INSURED INFORMATION", 631.3, 357.7, $baseboldsmallfontoptions . " orientate=west");
    $p->fit_textline("CARRIER", 630.8, 114.5, $baseboldsmallfontoptions . " orientate=west");

}

sub createFormLavels {
    my ($self, $p) = @_;

    my @textlines = (
        ["1.", 62.5, 140],
        ["MEDICARE", 74.9, 140],
        ["MEDICAID", 124.6, 140],
        ["TRICARE", 175.6, 140],
        ["CHAMPVA", 239.4, 140],
        ["GROUP", 289.8, 140],
        ["HEALTH PLAN", 289.8, 145.4],
        ["FECA", 347.3, 140],
        ["BLK LUNG", 347.3, 145.4, "charspacing=-0.3"],
        ["OTHER", 390.2, 140, "charspacing=-0.3"],
        ["1a. INSURED'S I.D. NUMBER", 413.8, 139.8],
        ["(For Program in item 1)", 547.2, 140],
        ["(Medicare#)", 73.9, 151.1, "italicangle=-10"],
        ["(Medicaid#)", 123.3, 151.1, "italicangle=-10"],
        ["(ID#/DoD#)", 174.6, 151.1, "italicangle=-10"],
        ["(Member ID#)", 239.1, 151.1, "italicangle=-10 charspacing=-0.3"],
        ["(ID#)", 289.4, 151.1, "italicangle=-10"],
        ["(ID#)", 346.1, 151.1, "italicangle=-10"],
        ["(ID#)", 389.5, 151.1, "italicangle=-10"],
        ["2. PATIENT'S NAME (Last Name, First Name, Middle Initial)", 62.9, 163.6],
        ["3. PATIENT'S BIRTH DATE", 269.5, 163.6],
        ["SEX", 370.6, 164],
        ["4. INSURED'S NAME (Last Name, First Name, Middle Initial)", 414, 163.7],
        ["MM", 280.3, 168.5],
        ["DD", 303.9, 168.5],
        ["YY", 330.5, 168.5],
        ["M", 347, 175.2],
        ["F", 384.7, 175.2],
        ["5. PATIENT'S ADDRESS (No., Street)", 62.9, 186.3],
        ["6. PATIENT RELATIONSHIP TO INSURED", 270, 186.5],
        ["7. INSURED'S ADDRESS (No., Street)", 414.1, 186.3],
        ["Self", 278.1, 199.2],
        ["Spouse", 304.7, 199.2],
        ["Child", 340.1, 199.2],
        ["Other", 374.2, 199.2],
        ["CITY", 62.9, 211.2],
        ["STATE", 243.1, 211.2],
        ["8. RESERVED FOR NUCC USE", 269.9, 211.2],
        ["CITY", 414, 211.2],
        ["STATE", 584.9, 211.2],
        ["ZIP CODE", 62.9, 234.3],
        ["TELEPHONE (Include Area Code)", 156.7, 234.3],
        ["ZIP CODE", 414, 234.3],
        ["TELEPHONE (Include Area Code)", 506.9, 234.3],
        ["(", 159.9, 249.3, "fontsize=$fontsizemidlarge"],
        [")", 185, 249.3, "fontsize=$fontsizemidlarge"],
        ["(", 518.4, 249.3, "fontsize=$fontsizemidlarge"],
        [")", 545.3, 249.3, "fontsize=$fontsizemidlarge"],
        ["9. OTHER INSURED'S NAME (Last Name, First Name, Middle Initial)", 63.1, 259.4],
        ["10. IS PATIENT'S CONDITION RELATED TO:", 269.6, 259.5],
        ["11. INSURED'S POLICY GROUP OR FECA NUMBER", 414, 259.4],
        ["a. OTHER INSURED'S POLICY OR GROUP NUMBER", 63.1, 282.7],
        ["a. EMPLOYMENT? (Current or Previous)", 269.8, 282.6],
        ["YES", 318, 295.7],
        ["NO", 361.6, 295.7],
        ["a. INSURED'S DATE OF BIRTH", 414.2, 283.2],
        ["MM", 439.8, 288.6],
        ["DD", 462.1, 288.6],
        ["YY", 489.2, 288.6],
        ["SEX", 564.5, 283],
        ["M", 534.2, 294.2],
        ["F", 586.7, 294.2],
        ["b. RESERVED FOR NUCC USE", 63.1, 305.5],
        ["b. AUTO ACCIDENT?", 270, 306],
        ["PLACE (State)", 368.2, 309.5],
        ["YES", 318, 319.3],
        ["NO", 361.4, 319.1],
        ["b. OTHER CLAIM ID (Designated by NUCC)", 413.9, 307.9],
        ["c. RESERVED FOR NUCC USE", 63.1, 330.9],
        ["c. OTHER ACCIDENT?", 269.9, 331],
        ["YES", 318, 343],
        ["NO", 361.4, 342.9],
        ["c. INSURANCE PLAN NAME OR PROGRAM NAME", 413.9, 330.9],
        ["d. INSURANCE PLAN NAME OR PROGRAM NAME", 63.1, 355],
        ["10d. CLAIM CODES (Designated by NUCC)", 269.8, 355.2],
        ["d. IS THERE ANOTHER HEALTH BENEFIT PLAN?", 413.9, 355.2],
        ["YES", 439.5, 367.4],
        ["NO", 476.4, 367.4],
        ["If yes,", 501.8, 367.7, "italicangle=-10 fontname=$boldfontname encoding=unicode"],
        ["complete items 9, 9a, and 9d.", 520.4, 367.7],
        ["READ BACK OF FORM BEFORE COMPLETING & SIGNING THIS FORM", 133.9, 379, "fontname=$boldfontname encoding=unicode"],
        ["12.", 62.7, 385.4],
        ["13.", 413.6, 379.5],
        ["SIGNED", 72.7, 416],
        ["DATE", 295.7, 416],
        ["SIGNED", 428.6, 416.5],
        ["14. DATE OF CURRENT ILLNESS, INJURY, or PREGNANCY (LMP)", 63.4, 427.9],
        ["15. OTHER DATE", 255.4, 427.9],
        ["16. DATES PATIENT UNABLE TO WORK IN CURRENT OCCUPATION", 414, 427.9],
        ["MM", 72, 433],
        ["DD", 95.4, 433],
        ["YY", 122, 433],
        ["MM", 323.5, 433],
        ["DD", 346.8, 433],
        ["YY", 373.4, 433],
        ["MM", 445.2, 433],
        ["DD", 468.7, 433],
        ["YY", 496.7, 433],
        ["MM", 546, 433],
        ["DD", 569.5, 433],
        ["YY", 597.6, 433],
        ["QUAL.", 146.4, 440.2],
        ["QUAL.", 255.4, 437.7],
        ["FROM", 424.1, 439.6],
        ["TO", 531.8, 439.6],
        ["17. NAME OF REFERRING PROVIDER OR OTHER SOURCE", 63.4, 450.5],
        ["17a.", 256.2, 451.4],
        ["18. HOSPITALIZATION DATES RELATED TO CURRENT SERVICES", 414, 450.4],
        ["MM", 445.2, 455.5],
        ["DD", 468.6, 455.5],
        ["YY", 496.7, 455.5],
        ["MM", 546, 455.5],
        ["DD", 569.5, 455.5],
        ["YY", 597.6, 455.5],
        ["17b.", 256.2, 463.4],
        ["NPI", 272.2, 463.4],
        ["FROM", 424.1, 463.2],
        ["TO", 531.8, 463.2],
        ["19. ADDITIONAL CLAIM INFORMATION (Designated by NUCC)", 63.4, 474.5],
        ["20. OUTSIDE LAB?", 414, 474.5],
        ["\$ CHARGES", 530.6, 474.5],
        ["YES", 440.6, 487.5],
        ["NO", 477.6, 487.5],
        ["21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY Relate A-L to service line bellow (24E)", 63, 498.4],
        ["ICD Ind.", 330.8, 502.1],
        ["22. RESUBMISSION", 413.8, 498.8],
        ["CODE", 423.6, 504],
        ["ORIGINAL REF. NO.", 505.2, 504],
        ["A.", 65, 514.8],
        ["B.", 158.6, 515.3],
        ["C.", 251.8, 515],
        ["D.", 345.8, 515.8],
        ["E.", 65.5, 526.4],
        ["F.", 159, 527],
        ["G.", 251.8, 527],
        ["H", 345.8, 528],
        ["I.", 65.5, 537.9],
        ["J.", 158.6, 538.4],
        ["K.", 251.8, 538],
        ["L.", 345.8, 538.2],
        ["23. PRIOR AUTHORIZATION NUMBER", 414, 522.5],
        ["24.", 63, 547],
        ["A.", 74.4, 547],
        ["DATE(S) OF SERVICE", 94.5, 547],
        ["B.", 196.5, 547],
        ["C.", 218.4, 547],
        ["D. PROCEDURES, SERVICES, OR SUPPLIES", 235.9, 547],
        ["E.", 390.5, 547],
        ["F.", 441.1, 547],
        ["G.", 487, 547],
        ["H.", 509.5, 547],
        ["I.", 529.1, 547],
        ["J.", 583.1, 547],
        ["From", 85.9, 554],
        ["To", 150.7, 554],
        ["PLACE OF", 188.1, 554, "fontsize=5 charspacing=-0.5"],
        ["(Explain Unusual Circumstances)", 249.4, 554],
        ["DIAGNOSIS", 376.6, 554],
        ["DAYS", 483.6, 551.5, "fontsize=5"],
        ["OR", 486.2, 556.5, "fontsize=5"],
        ["UNITS", 483.1, 561.4, "fontsize=5"],
        ["EPSDT", 504.7, 551.5, "fontsize=5 charspacing=-0.7"],
        ["Family", 505.4, 556.5, "fontsize=5 charspacing=-0.5"],
        ["Plan", 506.8, 561.4, "fontsize=5"],
        ["ID.", 527.5, 554.3],
        ["QUAL.", 522.9, 561.4],
        ["RENDERING", 568.7, 554],
        ["MM", 64.5, 561.4],
        ["DD", 86.6, 561.4],
        ["YY", 107.8, 561.4],
        ["MM", 129.2, 561.4],
        ["DD", 149.4, 561.4],
        ["YY", 171.9, 561.4],
        ["SERVICE", 188.6, 561.4, "fontsize=5 charspacing=-0.4"],
        ["EMG", 214.4, 561.4],
        ["CPT/HCPCS", 238.8, 561.4],
        ["MODIFIER", 315.6, 561.4],
        ["POINTER", 379.7, 561.4],
        ["\$ CHARGES", 425.5, 561.4],
        ["PROVIDER ID. #", 563.9, 561.4],
        ["NPI", 524.6, 583.9],
        ["NPI", 524.6, 607.7],
        ["NPI", 524.6, 631.7],
        ["NPI", 524.6, 655.4],
        ["NPI", 524.6, 679.4],
        ["NPI", 524.6, 703.4],
        ["25. FEDERAL TAX I.D. NUMBER", 62.9, 714],
        ["SSN", 175.7, 714],
        ["EIN", 191.8, 714],
        ["26. PATIENT'S ACCOUNT NO.", 220.1, 714],
        ["27. ACCEPT ASSIGNMENT?", 325, 714],
        ["(For govt. claims, see back)", 334.6, 717.8, "fontsize=5"],
        ["28. TOTAL CHARGE", 414.2, 714],
        ["29. AMOUNT PAID", 494.4, 714],
        ["30. Rsvd for NUCC Use", 563.5, 714],
        ["YES", 340, 727],
        ["NO", 376.2, 727],
        ["\$", 417.4, 727],
        ["\$", 498.4, 727],
        ["31.", 63.1, 738],
        ["32. SERVICE FACILITY LOCATION INFORMATION", 220.2, 738],
        ["33. BILLING PROVIDER INFO & PH #", 414, 738],
        ["(", 552.1, 741, "fontsize=$fontsizemidlarge"],
        [")", 577, 741, "fontsize=$fontsizemidlarge"],
        ["SIGNED", 63.1, 789.8],
        ["DATE", 171.4, 789.8],
        ["a.", 220.2, 785.4],
        ["b.", 301, 785.4],
        ["a.", 415.1, 785.4],
        ["b.", 495.4, 785.4],
    );
    my @rectangles = (
        [$marginleft + 0.6, 155],
        [109.5, 155],
        [159.9, 155],
        [224.7, 155],
        [275.3, 155],
        [333, 155],
        [376.1, 155],
        [354.5, 178.3],
        [390.5, 178.3],
        [289.7, 203],
        [326.2, 203],
        [354.7, 203],
        [390.9, 203],
        [304.5, 299.1],
        [347.5, 299.1],
        [541.4, 298.7],
        [592.2, 298.7],
        [304.5, 322.8],
        [347.5, 322.8],
        [304.5, 346.4],
        [347.7, 346.4],
        [426.1, 370.4],
        [462.5, 370.4],
        [427, 490.5],
        [463.2, 490.5],
        [175.7, 729.8],
        [189.9, 729.8],
        [326.6, 729.8],
        [362.4, 729.8],
    );

    my @textflows = (
        ["PATIENT'S OR AUTHORIZED PERSON'S SIGNATURE I authorize the release of any medical or other information necessary to process this claim. I also request payment of government benefits either to myself or to the party who accepts assignment bellow.", 72.6, 399.8, 410, 379],
        ["INSURED'S OR AUTHORIZED PERSON'S SIGNATURE I authorize payment of medical benefits to the undersigned physician or supplier for services described bellow.", 423.6, 393.1, 616, 373],
        ["SIGNATURE OF PHYSICIAN OR SUPPLIER INCLUDING DEGREES OR CREDENTIALS\n" .
        "(I certify that the statements on the reverse apply to this bill and are made a part thereof.", 73, 759.1, 195, 731.6]
    );

    main->renderTextLines($p, @textlines);
    main->renderRectangles($p, @rectangles);
    my $isTemplate = 1;
    main->renderTextFlowsTemplate($p, @textflows);
}

sub renderTextLines {
    my ($self, $p, @textlines) = @_;

    for(my $i=0; $i <= $#textlines; $i++) {
        $p->fit_textline(
            $textlines[$i][0], $textlines[$i][1], $textlines[$i][2],
            $textlines[$i][3] ne '' ? $basexxsmallfontoptions . " $textlines[$i][3]" : $basexxsmallfontoptions
        );
    }
}

sub renderSymbols {
    my ($self, $p, @symbols) = @_;

    for(my $i=0; $i <= $#symbols; $i++) {
        if ($symbols[$i][0]) {
            $p->fit_textline(
                "X", $symbols[$i][1], $symbols[$i][2],
                "fontname={DejaVuSans} encoding=unicode fontsize=10 charref"
            );
        }
    }
}

sub renderRectangles {
    my ($self, $p, @rectangles) = @_;

    $p->setlinewidth($linewidth2);
    $p->set_graphics_option("dasharray=none");
    for(my $i=0; $i <= $#rectangles; $i++) {
        $p->rect($rectangles[$i][0], $rectangles[$i][1], 11, 11);
    }
    $p->stroke();
}

sub renderTextFlowsTemplate {
    my ($self, $p, @textflows) = @_;
    my $tf;

    for(my $i=0; $i <= $#textflows; $i++) {
        $tf = $p->create_textflow($textflows[$i][0],
            $basexxsmallfontoptions .
            " leading=110% fillcolor={cmyk " . ($HCFAtype eq "red" ? "0.0 0.0 0.0 0.0" : "0 0 0 1") . "}" .
            ($textflows[$i][5] ne '' ? " $textflows[$i][5]" : ""));
        $p->fit_textflow($tf, $textflows[$i][1], $textflows[$i][2],
                $textflows[$i][3], $textflows[$i][4], "verticalalign=top");
    }
}

sub renderTextFlowsContent {
    my ($self, $p, @textflows) = @_;
    my $tf;

    for(my $i=0; $i <= $#textflows; $i++) {
        $tf = $p->create_textflow($textflows[$i][0],
            $basexxsmallfontoptions .
            " leading=110% fillcolor={cmyk 0 0 0 1}" .
            ($textflows[$i][5] ne '' ? " $textflows[$i][5]" : ""));
        $p->fit_textflow($tf, $textflows[$i][1], $textflows[$i][2],
                $textflows[$i][3], $textflows[$i][4], "verticalalign=top");
    }
}
