package myPDF;
use myForm;
use MgrTree;
############################################################################
sub setAgency
{
  my ($self,$p,$page,$ClinicID) = @_;
  my $form = $myForm::FORM;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $AgencyID = MgrTree->getAgency($form,$ClinicID);
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($AgencyID) || myDBI->dberror("setAgency: select Provider ${AgencyID}");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = $rAgency->{'Name'};
  my $AgencyAddr = $rAgency->{'Addr1'} . ', ';
  $AgencyAddr .= $rAgency->{'Addr2'} . ', ' if ( $rAgency->{'Addr2'} );
  my $AgencyCSZ .= $rAgency->{'City'} . ', ' . $rAgency->{'ST'} . '  ' . $rAgency->{'Zip'};
  my $AgencyPh = 'Office: ' . $rAgency->{'WkPh'} . '  Fax: ' . $rAgency->{'Fax'};
  my $optlist = "encoding=winansi embedding";
  my $str = qq|${AgencyName}\n${AgencyAddr}\n${AgencyCSZ}\n${AgencyPh}|;
  if ($p->fill_textblock($page, 'agencyinfo', $str, $optlist) == -1)
  { printf("Warning: %s\n", $p->get_errmsg()); }
  $sProvider->finish();
  return();
}
sub setConf
{
  my ($self,$p,$page) = @_;
  my $conf = qq|Confidentiality of drug/alcohol abuse records is protected by Federal Law. Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.|;
  my $optlist = "encoding=winansi embedding";
  if ($p->fill_textblock($page, 'myFooter', $conf, $optlist) == -1)
  { printf("Warning: %s\n", $p->get_errmsg()); }
  return();
}
############################################################################
1;
