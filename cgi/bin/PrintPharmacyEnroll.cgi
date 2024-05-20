#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use DBForm;
use DBA;
use MgrTree;
use DBUtil;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
my $cdbh = $form->connectdb('okmis_config');
my $table = $form->{'action'};
#warn "PrintPharmacyEnroll: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
$sClient = $dbh->prepare("select * from Client where ClientID=?");
$sInsurance = $dbh->prepare("select Insurance.*,xInsurance.Name from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where ClientID=? and Priority=1 order by InsNumEffDate desc");
$sProvider = $dbh->prepare("select * from Provider where ProvID=?");

############################################################################
my $xdp = qq|<?xml version="1.0" encoding="UTF-8" ?> 
<?xfa generator="XFA2_0" APIVersion="2.2.4333.0" ?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/" >
<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" >
<xfa:data>
<topmostSubform>
|;
foreach my $ID ( split(' ',$form->{IDs}) )
{ 
#warn "PrintPharmacyEnroll: ID=${ID}\n";
  $sClient->execute($ID) || $form->dberror("PrintPharmacyEnroll: select Client ${ID}");
  while ( my $rClient = $sClient->fetchrow_hashref )
  { 
    $xdp .= main->printPharmacyEnroll($rClient); 
  }
}
my $pdfpath = myConfig->cfg('FormsPrintURL')."/PrintPharmacyEnroll_Rev2.pdf";
#warn qq|pdfpath=$pdfpath\n|;
$xdp .= qq|
</topmostSubform>
</xfa:data>
</xfa:datasets>
<pdf href="${pdfpath}" xmlns="http://ns.adobe.com/xdp/pdf/" />
</xdp:xdp>
|;
if ( $form->{LOGINPROVID} == 91 )
{
  open XML, ">/home/okmis/mis/src/debug/PrintPharmacyEnroll.out" or die "Couldn't open file: $!";
  print XML ${xdp};
  close(XML);
}
if ( $form->{file} )
{
  open OUT, ">$form->{file}" || die "Couldn't open '$form->{file}' file: $!"; 
  print OUT ${xdp};
  close(OUT);
}
else { print qq|Content-Type: application/vnd.adobe.xdp+xml\n\n${xdp}|; }
$sClient->finish();
$sInsurance->finish();
$sProvider->finish();
$cdbh->disconnect();
$form->complete();
exit;

############################################################################
sub printPharmacyEnroll
{
  my ($self,$rClient) = @_;
##
# Header info...
  my $AgencyID = MgrTree->getAgency($form,$rClient->{'clinicClinicID'});
  $sProvider->execute($AgencyID) || $form->dberror("printPharmacyEnroll: select Provider $AgencyID");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = DBA->subxml($rAgency->{Name});
  my $AgencyAddr = $rAgency->{Addr1} . ', ';
  $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
  $AgencyAddr .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPhFax = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
  my $reportInfo = '';                                 # right side of heading
  my $Title = '';
##
  $sProvider->execute($rClient->{'ProvID'}) || $form->dberror("printPharmacyEnroll: select PrimaryProvider $rClient->{'ProvID'}");
  my $rPrimaryProvider = $sProvider->fetchrow_hashref;
  my $primaryprovider = qq|$rPrimaryProvider->{'FName'} $rPrimaryProvider->{'LName'}|;
##
  $sProvider->execute($rClient->{'ProvID'}) || $form->dberror("printPharmacyEnroll: select Clinician $rClient->{'ProvID'}");
  my $rClinician = $sProvider->fetchrow_hashref;
  my $clinician = qq|$rClinician->{'FName'} $rClinician->{'LName'}|;
##
  $sInsurance->execute($rClient->{'ClientID'}) || $form->dberror("printPharmacyEnroll: select Insurance $rClient->{'ClientID'}");
  my $rInsurance = $sInsurance->fetchrow_hashref;
##
  my $today = DBUtil->Date($form->{TODAY},'fmt','MM/DD/YYYY');
##
  my $clientid = $rClient->{'ClientID'};
  my $clientname = qq|$rClient->{'FName'} $rClient->{'LName'}|;
  my $clientnameid = qq|$rClient->{'FName'} $rClient->{'LName'} / ${clientid}|;
  my $addr1 = $rClient->{'Addr1'};
  my $addr2 = $rClient->{'Addr2'};
  my $csz = qq|$rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
  if ( $addr2 eq '' ) { $addr2 = $csz; $csz = ''; }
  my $sex = $rClient->{'Gend'};
  my $clientdob = DBUtil->Date($rClient->{'DOB'},'fmt','MM/DD/YYYY');
  my $age = DBUtil->Date($rClient->{'DOB'},'age');
  my $insurance = $rInsurance->{'Name'};
  my $medid = $rInsurance->{'InsIDNum'};
  my $nameoncard = $clientname;
##
  my $xml = qq|
    <recordid>$rClient->{'ClientID'}</recordid>
    <companyLogo xfa:contentType="image/gif" xfa:transferEncoding="base64">
| . DBA->getLogo($form,'Client',$rClient->{ClientID},'base64') . qq|
    </companyLogo>
    <companyname>
      ${AgencyName}
      ${AgencyAddr}
      ${AgencyPhFax}
      ${Title}
    </companyname> 
    <reportInfo>${reportInfo}</reportInfo> 
    <footerLeft>${clientnameid}</footerLeft> 
    <footerRight>${DT}</footerRight> 
    <agencyname>${AgencyName}</agencyname> 
    <agencyaddr>${AgencyAddr}</agencyaddr> 
    <agencyphonefax>${AgencyPhFax}</agencyphonefax> 
    <primaryprovider>${primaryprovider}</primaryprovider> 
    <clinician>${clinician}</clinician> 
    <today>${today}</today> 
    <clientid>${clientid}</clientid> 
    <clientname>${clientname}</clientname> 
    <clientnameid>${clientnameid}</clientnameid> 
    <addr1>${addr1}</addr1> 
    <addr2>${addr2}</addr2> 
    <csz>${csz}</csz> 
    <sex>${sex}</sex> 
    <sex_F>${sex}</sex_F> 
    <sex_M>${sex}</sex_M> 
    <clientdob>${clientdob}</clientdob> 
    <age>${age}</age> 
    <insurance>${insurance}</insurance> 
    <nameoncard>${nameoncard}</nameoncard> 
    <medid>${medid}</medid> 
    <allergies>|.main->ptAllergies($rClient->{ClientID}).qq|</allergies>
|;
  return($xml);
}
sub ptAllergies
{
  my ($self,$ClientID) = @_;
  my $xml = '';
  my $sClientAllergies = $dbh->prepare("select * from ClientAllergies where ClientID=? and AID is not null");
  $sClientAllergies->execute($ClientID) || $form->dberror("select ClientAllergies ${ClientID}");
  while ( my $rClientAllergies = $sClientAllergies->fetchrow_hashref )
  {
    $xml .= DBA->getxref($form,'xAllergies',$rClientAllergies->{'AID'},'Descr') . ';';
  }
  $sClientAllergies->finish();
  return($xml);
}
############################################################################
