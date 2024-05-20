#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use DBForm;
use DBA;
use myHTML;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
warn "valCCDA: IDs=$form->{'IDs'}, type=${type}\n";
##
# prepare selects...
##
my $sPhiMailAttachments = $dbh->prepare("select * from PhiMailAttachments where ID=?");
$sPhiMailAttachments->execute($form->{'IDs'}) || $form->dberror("valCCDA: select PhiMailAttachments");
my $rPhiMailAttachments = $sPhiMailAttachments->fetchrow_hashref;
warn "$form->{DOCROOT}/$rPhiMailAttachments->{filename}\n";
if ( -f "$form->{DOCROOT}/$rPhiMailAttachments->{filename}" )
{ warn qq|EXISTS\n|; }
else
{ warn qq|NOT FOUND\n|; }
my $file = qq|$form->{DOCROOT}$rPhiMailAttachments->{filename}|;
my ($directory, $filename) = $file =~ m/(.*\/)(.*)$/;
my $url = qq|-X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F ccdaFile=\@${file} -F validationObjective=NegativeTesting_CarePlan -F referenceFileName=NT_CP_Sample4_r21_v4.xml https://ttpds.sitenv.org:8443/referenceccdaservice/|;
warn qq|curl $url\n|;
my ($cnt,$err) = (0,'');
my $jsonData = `curl $url 2>/tmp/kls`;
if ( $jsonData eq '' )
{ $err .= qq|jsonData IS NULL!\n|; }
else
{
  my $json = JSON->new->allow_nonref;
  $rJSON = $json->decode( $jsonData );
foreach my $f ( sort keys %{$rJSON} ) { warn "rJSON: $f=$rJSON->{$f}\n"; }
#foreach my $f ( sort keys %{$rJSON->{resultsMetaData}} ) { warn "rJSON-resultsMetaData: $f=$rJSON->{resultsMetaData}->{$f}\n"; }
# resultsMetaData
#  ccdaDocumentType=NegativeTesting_CarePlan
#  ccdaFileContents=<?xml version="1.0"?>\r
#  ccdaFileName=ccdaFile
#  resultMetaData=ARRAY(0x2867a10)
#   my @resultMetaData = @{ $rJSON->{resultsMetaData}->{'resultMetaData'} };
#     foreach my $f ( @resultMetaData ) { $a->{'count'}, $a->{'type'} }
#     ie: count=0 and type=C-CDA MDHT Conformance Error
#  serviceError=0
#  serviceErrorMessage=
  $err .= $rJSON->{'resultsMetaData'}->{'serviceErrorMessage'} if ( $rJSON->{'resultsMetaData'}->{'serviceError'} == 1 );
  my @ccdaValidationResults = @{ $rJSON->{'ccdaValidationResults'} };
# ccdaValidationResults: i.e.:
#  actualCode=
#  actualCodeSystem=
#  actualCodeSystemName=
#  actualDisplayName=
#  dataTypeSchemaError=0
#  description=Consol Allergy Problem Act SHALL contain exactly one [1..1] code (CONF:NEW) code /@code SHALL="CONC" ...
#  documentLineNumber=879
#  igissue=1
#  muissue=0
#  schemaError=0
#  type=C-CDA MDHT Conformance Error
#  validatorConfiguredXpath=
#  xPath=/ClinicalDocument/component/structuredBody/component/section/entry[2]/act/code
#  actualCode=
#  actualCodeSystem=
#  actualCodeSystemName=
#  actualDisplayName=
#  dataTypeSchemaError=0
#  description=Consol Allergy Problem Act SHALL contain exactly one [1..1] code (CONF:NEW) code /@code SHALL="CONC" ...
#  documentLineNumber=1039
#  igissue=1
#  muissue=0
#  schemaError=0
#  type=C-CDA MDHT Conformance Error
#  validatorConfiguredXpath=
#  xPath=/ClinicalDocument/component/structuredBody/component/section/entry[3]/act/code
  foreach my $f ( @ccdaValidationResults )
  {
    if ($f->{"type"} eq "C-CDA MDHT Conformance Error" or $f->{"type"} eq "ONC 2015 S&amp;CC Vocabulary Validation Conformance Error")
    {
      $cnt++;
      $err .= $f->{'description'}."<BR>";
      $err .= $f->{'xPath'}." at line ".$f->{'documentLineNumber'}."<BR><BR>";
    }
  }
}
my $html = myHTML->newHTML($form,'Validate CCDA','CheckPopupWindow noclock countdown_1') . qq|
<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Validate CCDA</TD> </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      Validate: ${filename}<BR>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol hotmsg" >
      Total Conformance Errors: ${cnt}<BR>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol hotmsg" >
      ${err}<BR>
    </TD>
  </TR>
</TABLE>
  
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;
$sPhiMailAttachments->finish();
$form->complete();
print $html;
exit;
############################################################################
