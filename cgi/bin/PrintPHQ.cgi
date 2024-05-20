#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $cdbh = myDBI->dbconnect('okmis_config');
my $table = $form->{'action'};
my $page = $form->{'page'};
#warn "PrintPHQ: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
my $sPHQ = $dbh->prepare("select * from ${table} where ID=?");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sxTables = $cdbh->prepare("select xTables.theTable,xTableFields.* from xTables left join xTableFields on xTableFields.TableID=xTables.ID where xTables.theTable=? and xTableFields.theField=?");

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
#warn "PrintPHQ: table=${table}, page=${page}, ID=${ID}\n";
  $sPHQ->execute($ID) || myDBI->dberror("PrintPHQ: select ${table} ${ID}");
  while ( my $rPHQ = $sPHQ->fetchrow_hashref )
  { 
    $sClient->execute($rPHQ->{'ClientID'}) || myDBI->dberror("select Client: $rPHQ->{'ClientID'}");
    my $rClient = $sClient->fetchrow_hashref;
    $xdp .= main->printPHQ($rPHQ,$rClient); 
  }
}
my $pdfpath = myConfig->cfg('FormsPrintURL')."/Print${table}${page}_Rev2.pdf";
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
  open XML, ">/home/okmis/mis/src/debug/PrintPHQ.out" or die "Couldn't open file: $!";
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

$sPHQ->finish();
$sClient->finish();
$sProvider->finish();
$sxTables->finish();

myDBI->cleanup();

exit;

############################################################################
sub printPHQ
{
  my ($self,$rPHQ,$rClient) = @_;
##
# Header info...
  my $AgencyID = MgrTree->getAgency($form,$rClient->{'clinicClinicID'});
  $sProvider->execute($AgencyID) || myDBI->dberror("printPHQ: select Provider $AgencyID");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = DBA->subxml($rAgency->{Name});
  my $AgencyAddr = $rAgency->{Addr1} . ', ';
  $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
  $AgencyAddr .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPhFax = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
  my $reportInfo = '';                                 # right side of heading
  my $Title = '';
##
  $sProvider->execute($rClient->{'ProvID'}) || myDBI->dberror("printPHQ: select PrimaryProvider $rClient->{'ProvID'}");
  my $rPrimaryProvider = $sProvider->fetchrow_hashref;
  my $primaryprovider = qq|$rPrimaryProvider->{'FName'} $rPrimaryProvider->{'LName'}|;
##
  $sProvider->execute($rPHQ->{'ProvID'}) || myDBI->dberror("printPHQ: select Clinician $rPHQ->{'ProvID'}");
  my $rClinician = $sProvider->fetchrow_hashref;
  my $clinician = qq|$rClinician->{'FName'} $rClinician->{'LName'}|;
##
  my $today = DBUtil->Date($form->{TODAY},'fmt','MM/DD/YYYY');
  my $testdate = DBUtil->Date($rPHQ->{TestDate},'fmt','MM/DD/YYYY');
##
  my $clientid = $rClient->{'ClientID'};
  my $clientname = qq|$rClient->{'FName'} $rClient->{'LName'}|;
  my $clientnameid = qq|$rClient->{'FName'} $rClient->{'LName'} / ${clientid}|;
  my $addr1 = $rClient->{'Addr1'};
  my $addr2 = $rClient->{'Addr2'};
  my $csz = qq|$rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
  if ( $addr2 eq '' ) { $addr2 = $csz; $csz = ''; }
  my $sex = $rClient->{'Gend'};
  my $age = DBUtil->Date($rClient->{'DOB'},'age');
##
  my $out = '';
  my $tALL = 0;
  my ($total,$t1,$t2,$t3) = (0,0,0,0);         # total = all t1=total all 1's, t2=total all 2's, t3=total all 3's values
  my ($t15,$t15_1,$t15_2) = (0,0,0);           # ClientPHQSADS [qA]
  my ($t7,$t7_1,$t7_2,$t7_3) = (0,0,0,0);      # ClientPHQSADS [qB]
  my ($t9,$t9_1,$t9_2,$t9_3) = (0,0,0,0);      # ClientPHQSADS [qD] & ClientPHQ9 [q10]
  my ($tINT,$tWM,$tD1,$tD2,$tD3,$tD4,$tD5,$tD6) = (0,0,0,0,0,0,0,0);              # ClientODAS,2017
  my ($tL1,$tL2,$tL3,$tL4,$tL5,$tL6) = (0,0,0,0,0,0);                             # ClientODAS,2017
  my ($sLINT,$tLWM,$tLD1,$tLD2,$tLD3,$tLD4,$tLD5,$tLD6) = (0,0,0,0,0,0,0,0);      # ClientODAS,2017
  my ($sIndicated,$sWMIndicated) = (0,0);                                         # ClientODAS,2017
  foreach my $f ( sort keys %{$rPHQ} )
  {
    $sxTables->execute($table,$f) || myDBI->dberror("printPHQ: select xTables ${table}/${f}");
    my $rxTables = $sxTables->fetchrow_hashref;
#foreach my $m ( sort keys %{$rxTables} ) { warn "${f}: rxTables-$m=$rxTables->{$m}\n"; }
    my $val = DBA->subxml($rPHQ->{$f});
    $out .= qq|    <${f}>${val}</${f}>\n|;
#   for check marks we get a range: 0-n; where the field Name: t(field)_n
#warn qq|${f}: theType=$rxTables->{'theType'}\n|;
    if ( $rxTables->{'theType'} =~ /radio/ )                # set check mark values
    {
      $out .= qq|    <${f}_${val}>${val}</${f}_${val}>\n|; 
      $t1 += 1 if ( $val == 1 );
      $t2 += 2 if ( $val == 2 );
      $t3 += 3 if ( $val == 3 );
      if ( $table eq 'ClientPHQSADS' && substr($f,0,2) eq 'qA' )
      {
        $t15_1 += 1 if ( $val == 1 );
        $t15_2 += 2 if ( $val == 2 );
      }
      elsif ( $table eq 'ClientPHQSADS' && substr($f,0,2) eq 'qB' )
      {
        $t7_1 += 1 if ( $val == 1 );
        $t7_2 += 2 if ( $val == 2 );
        $t7_3 += 3 if ( $val == 3 );
      }
      elsif ( $table eq 'ClientPHQSADS' && substr($f,0,2) eq 'qD' )
      {
        $t9_1 += 1 if ( $val == 1 );
        $t9_2 += 2 if ( $val == 2 );
        $t9_3 += 3 if ( $val == 3 );
      }
      elsif ( $table eq 'ClientPHQ9' && substr($f,0,3) ne 'q10' )
      {
        $t9_1 += 1 if ( $val == 1 );
        $t9_2 += 2 if ( $val == 2 );
        $t9_3 += 3 if ( $val == 3 );
      }
      elsif ( $table eq 'ClientPCL5' )
      { $out .= qq|    <${f}_N>${val}</${f}_N>\n|; }
      $tALL += $val;           # total all 'radio' values (could add for 'selectlist' if a digit?)
#     END radio IF
    }
#    else
#    { $out .= qq|    <${f}>${val}</${f}>\n|; }
    if ( $table eq 'ClientTCUDS' && $f eq 'q12b' )      # Other specify check mark
    { 
      $out .= $val eq '' ? qq|    <${f}_0>0</${f}_0>\n| : qq|    <${f}_1>1</${f}_1>\n|;
    }
    elsif ( $table eq 'ClientODAS' )
    {
      # Other specify check mark
      if ( $f eq 'D4Primary' || $f eq 'D4Secondary' || $f eq 'D4Tertiary' )
      { $out .= qq|    <${f}_${val}>${val}</${f}_${val}>\n|; }
      # totals...
      $tINT += $val if ( $f eq 'D1q1' || $f eq 'D1q2' );
      $tWM += $val if ( $f eq 'D1q3' || $f eq 'D1q4' || $f eq 'D1q5' || $f eq 'D1q6' );
      $tD1 = $tINT + $tWM;
#warn qq|f=$f: val=$val:\n tINT=$tINT, tWM=$tWM, tD1=$tD1\n|;
      $tD2 += $val if ( substr($f,0,3) eq 'D2q' && $f ne 'D2q8' );
      $tD3 += $val if ( substr($f,0,3) eq 'D3q' && $f ne 'D3q9' );
      $tD4 += $val if ( substr($f,0,3) eq 'D4q' );
      $tD5 += $val if ( substr($f,0,3) eq 'D5q' );
      $tD6 += $val if ( substr($f,0,3) eq 'D6q' );
#warn qq|f=$f: val=$val:\n tD1=$tD1, tD2=$tD2, tD3=$tD3\n tD4=$tD4, tD5=$tD5, tD6=$tD6\n|;
    }
    elsif ( $table eq 'ClientODAS2017' )
    {
      # Other specify check mark
      if ( $f eq 'D4Primary' || $f eq 'D4Secondary' || $f eq 'D4Tertiary' )
      { $out .= qq|    <${f}_${val}>${val}</${f}_${val}>\n|; }
      # totals...
      $tINT += $val if ( $f eq 'D1q1' || $f eq 'D1q2' );
      $tWM += $val if ( $f eq 'D1q3' || $f eq 'D1q4' || $f eq 'D1q5' || $f eq 'D1q6' || $f eq 'D1q7' );
      $tD1 = $tINT + $tWM;
#warn qq|f=$f: val=$val:\n tINT=$tINT, tWM=$tWM, tD1=$tD1\n|;
      $tD2 += $val if ( substr($f,0,3) eq 'D2q' );
      $tD3 += $val if ( substr($f,0,3) eq 'D3q' );
      $tD4 += $val if ( substr($f,0,3) eq 'D4q' );
      $tD5 += $val if ( substr($f,0,3) eq 'D5q' );
      $tD6 += $val if ( substr($f,0,3) eq 'D6q' );
#warn qq|f=$f: val=$val:\n tD1=$tD1, tD2=$tD2, tD3=$tD3\n tD4=$tD4, tD5=$tD5, tD6=$tD6\n|;
    }
  }
# Totals...
  $out .= qq|    <tALL>${tALL}</tALL>\n|;
  $total = $t1 + $t2 + $t3; 
  $out .= qq|    <t1>${t1}</t1>\n|;
  $out .= qq|    <t2>${t2}</t2>\n|;
  $out .= qq|    <t3>${t3}</t3>\n|;
  $out .= qq|    <total>${total}</total>\n|;
  if ( $table eq 'ClientPHQSADS' )
  {
    my $t15 = $t15_1 + $t15_2;
    $out .= qq|    <t15_1>${t15_1}</t15_1>\n|;
    $out .= qq|    <t15_2>${t15_2}</t15_2>\n|;
    $out .= qq|    <t15>${t15}</t15>\n|;
    my $t7 = $t7_1 + $t7_2 + $t7_3;
    $out .= qq|    <t7_1>${t7_1}</t7_1>\n|;
    $out .= qq|    <t7_2>${t7_2}</t7_2>\n|;
    $out .= qq|    <t7_3>${t7_3}</t7_3>\n|;
    $out .= qq|    <t7>${t7}</t7>\n|;
    my $t9 = $t9_1 + $t9_2 + $t9_3;
    $out .= qq|    <t9_1>${t9_1}</t9_1>\n|;
    $out .= qq|    <t9_2>${t9_2}</t9_2>\n|;
    $out .= qq|    <t9_3>${t9_3}</t9_3>\n|;
    $out .= qq|    <t9>${t9}</t9>\n|;
  }
  if ( $table eq 'ClientPHQ9' )
  {
    my $t9 = $t9_1 + $t9_2 + $t9_3;
    $out .= qq|    <t9_1>${t9_1}</t9_1>\n|;
    $out .= qq|    <t9_2>${t9_2}</t9_2>\n|;
    $out .= qq|    <t9_3>${t9_3}</t9_3>\n|;
    $out .= qq|    <t9>${t9}</t9>\n|;
  }
  if ( $table eq 'ClientPCL5' )
  {
    my $tB = $rPHQ->{'q1'} + $rPHQ->{'q2'} + $rPHQ->{'q3'} + $rPHQ->{'q4'} + $rPHQ->{'q5'};
    my $tC = $rPHQ->{'q6'} + $rPHQ->{'q7'};
    my $tD = $rPHQ->{'q8'} + $rPHQ->{'q9'} + $rPHQ->{'q10'} + $rPHQ->{'q11'} + $rPHQ->{'q12'} + $rPHQ->{'q13'} + $rPHQ->{'q14'};
    my $tE = $rPHQ->{'q15'} + $rPHQ->{'q16'} + $rPHQ->{'q17'} + $rPHQ->{'q18'} + $rPHQ->{'q19'} + $rPHQ->{'q20'};
    $out .= qq|    <tB>${tB}</tB>\n|;
    $out .= qq|    <tC>${tC}</tC>\n|;
    $out .= qq|    <tD>${tD}</tD>\n|;
    $out .= qq|    <tE>${tE}</tE>\n|;
    my $tBE = $tB + $tC + $tD + $tE;
    $out .= qq|    <tBE>${tBE}</tBE>\n|;
  }
  if ( $table eq 'ClientODAS' || $table eq 'ClientODAS2017' )
  {
    $out .= qq|    <tINT>${tINT}</tINT>\n|;
    $out .= qq|    <tWM>${tWM}</tWM>\n|;
    $out .= qq|    <tD1>${tD1}</tD1>\n|;
    $out .= qq|    <tD2>${tD2}</tD2>\n|;
    $out .= qq|    <tD3>${tD3}</tD3>\n|;
    $out .= qq|    <tD4>${tD4}</tD4>\n|;
    $out .= qq|    <tD5>${tD5}</tD5>\n|;
    $out .= qq|    <tD6>${tD6}</tD6>\n|;
# calculate the Service Levels ...
    $tLINT = $tINT == 0 ? 0 : $tINT <= 2 ? 1 : $tINT <= 4 ? 2 : $tINT <= 6 ? 3 : 4;
    $tLWM = $tWM == 0 ? 0 : $tWM <= 4 ? 1 : $tWM <= 8 ? 1 : $tWM <= 12 ? 3 : 4;
    $tL1 = $tLINT;      # same as L1 ACUTE INTOXICATION
    $tL2 = $tD2 == 0 ? 0 : $tD2 <= 7 ? 1 : $tD2 <= 14 ? 2 : $tD2 <= 21 ? 3 : 4;
    $tL3 = $tD3 == 0 ? 0 : $tD3 <= 8 ? 1 : $tD3 <= 16 ? 2 : $tD3 <= 24 ? 3 : 4;
    $tL4 = $tD4 == 0 ? 0 : $tD4 <= 6 ? 1 : $tD4 <= 12 ? 2 : $tD4 <= 18 ? 3 : 4;
    $tL5 = $tD5 == 0 ? 0 : $tD5 <= 10 ? 1 : $tD5 <= 20 ? 2 : $tD5 <= 30 ? 3 : 4;
    $tL6 = $tD6 == 0 ? 0 : $tD6 <= 9 ? 1 : $tD6 <= 18 ? 2 : $tD6 <= 27 ? 3 : 4;
    $out .= qq|    <tLINT>${tLINT}</tLINT>\n|;
    $out .= qq|    <tLWM>${tLWM}</tLWM>\n|;
    $out .= qq|    <tL1>${tL1}</tL1>\n|;
    $out .= qq|    <tL2>${tL2}</tL2>\n|;
    $out .= qq|    <tL3>${tL3}</tL3>\n|;
    $out .= qq|    <tL4>${tL4}</tL4>\n|;
    $out .= qq|    <tL5>${tL5}</tL5>\n|;
    $out .= qq|    <tL6>${tL6}</tL6>\n|;
# and calculate the Indicated Service Level ...
    $sIndicated = $tL1 == 0 
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 0 && $tL3 <= 1)
                  && ($tL5 >= 2 && $tL5 <= 4)
                  && ($tL6 >= 2 && $tL6 <= 3)
                  && ($tL4 >= 3 && $tL4 <= 3) ? '0.5'
                : ($tL1 >= 0 && $tL1 <= 1) || ($tL1 >= 2 && $tL1 <= 4 && $tWM == 1)
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 0 && $tL3 <= 1) || ($tL3 >= 2 && $tL3 <= 3 && $rPHQ->{'D3q9'} == 1)
                  && ($tL5 >= 0 && $tL5 <= 2)
                  && ($tL6 >= 0 && $tL6 <= 2)
                  && ($tL4 >= 0 && $tL4 <= 2) || 
                     ($tL4 >= 3 && $tL4 <= 4 && $tL1 >= 0 && $tL1 <= 1 && $tL2 >= 0 && $tL2 <= 1 && $tL3 >= 0 && $tL3 <= 1 && $tL5 >= 0 && $tL5 <= 1 && $tL6 >= 0 && $tL6 <= 1) ? '1'
                : ($tL1 >= 3 && $tL1 <= 4)
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 0 && $tL3 <= 1) || ($tL3 >= 2 && $tL3 <= 3 && $rPHQ->{'D3q9'} == 1)
                  && ($tL5 >= 2 && $tL5 <= 4)
                  && ($tL6 >= 0 && $tL6 <= 2)
                  && ($tL4 >= 0 && $tL4 <= 2) ? 'OTP1'
                : ($tL1 >= 0 && $tL1 <= 1) || ($tL1 >= 2 && $tL1 <= 4 && $tWM == 1)
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 0 && $tL3 <= 2)
                  && ($tL5 >= 2 && $tL5 <= 3)
                  && ($tL6 >= 2 && $tL6 <= 3)
                  && ($tL4 >= 2 && $tL4 <= 3) ? '2.1'
                : ($tL1 >= 0 && $tL1 <= 1) || ($tL1 >= 2 && $tL1 <= 4 && $tWM == 1)
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 0 && $tL3 <= 1) || ($tL3 >= 2 && $tL3 <= 3 && $rPHQ->{'D3q9'} == 1)
                  && ($tL5 >= 1 && $tL5 <= 3)
                  && ($tL6 >= 3 && $tL6 <= 4)
                  && ($tL4 >= 0 && $tL4 <= 3) ? '3.1'
                : ($tL1 >= 0 && $tL1 <= 1) || ($tL1 >= 2 && $tL1 <= 4 && $tWM == 1)
                  && ($tL2 >= 0 && $tL2 <= 1) || ($tL2 >= 2 && $tL2 <= 3 && $rPHQ->{'D2q8'} == 1)
                  && ($tL3 >= 3 && $tL3 <= 4) || (($tL3 >= 1 && $tL3 <= 2) && ($tL4 >= 3 && $tL4 <= 4))
                  && ($tL5 >= 3 && $tL5 <= 4)
                  && ($tL6 >= 3 && $tL6 <= 4)
                  && ($tL4 >= 3 && $tL4 <= 4) || (($tL4 >= 1 && $tL4 <= 2) && ($tL3 >= 3 && $tL3 <= 4)) ? '3.5'
                : '';
    $sWMIndicated = $tLWM == 2 ? '1 WM'
                  : $tLWM == 3 ? '3.2 WM'
                  : $tLWM == 4 ? '3.7 WM'
                  : 'none';
    $out .= qq|    <sIndicated>${sIndicated}</sIndicated>\n|;
    $out .= qq|    <sWMIndicated>${sWMIndicated}</sWMIndicated>\n|;
  }
# no logo on these forms...
#| . DBA->getLogo($form,'Client',$rClient->{ClientID},'base64') . qq|
  
  my $xml = qq|
    <recordid>$rPHQ->{'ID'}</recordid>
    <companyLogo xfa:contentType="image/gif" xfa:transferEncoding="base64">
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
    <testdate>${testdate}</testdate> 
    <testdate_pg2>${testdate}</testdate_pg2> 
    <testdate_pg3>${testdate}</testdate_pg3> 
    <today>${today}</today> 
    <clientid>${clientid}</clientid> 
    <clientname>${clientname}</clientname> 
    <clientname_pg2>${clientname}</clientname_pg2> 
    <clientname_pg3>${clientname}</clientname_pg3> 
    <clientnameid>${clientnameid}</clientnameid> 
    <clientnameid_pg2>${clientnameid}</clientnameid_pg2> 
    <addr1>${addr1}</addr1> 
    <addr2>${addr2}</addr2> 
    <csz>${csz}</csz> 
    <sex>${sex}</sex> 
    <sex_F>${sex}</sex_F> 
    <sex_M>${sex}</sex_M> 
    <age>${age}</age> 
${out}
|;
  return($xml);
}
############################################################################
