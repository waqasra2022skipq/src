#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use myConfig;
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $IDs  = $form->{'IDs'};

#warn "PrintClientASI: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
$sClientASI = $dbh->prepare("select * from ClientASI where ID=?");
$sClient    = $dbh->prepare("select * from Client where ClientID=?");
$sProvider  = $dbh->prepare("select * from Provider where ProvID=?");

############################################################################
my $xdp = qq|<?xml version="1.0" encoding="UTF-8" ?> 
<?xfa generator="XFA2_0" APIVersion="2.2.4333.0" ?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/" >
<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" >
<xfa:data>
<topmostSubform>
|;
foreach my $ID ( split( ' ', $IDs ) ) {

    #warn "PrintClientASI: ID=${ID}\n";
    $sClientASI->execute($ID) || myDBI->dberror("select ClientASI ${ID}");
    while ( my $rClientASI = $sClientASI->fetchrow_hashref ) {
        $sClient->execute( $rClientASI->{'G1'} )
          || myDBI->dberror("select Client: $rClientASI->{'G1'}");
        my $rClient = $sClient->fetchrow_hashref;
        $xdp .= main->printClientASI( $rClientASI, $rClient );
    }
}
my $pdfpath = myConfig->cfg('FormsPrintURL') . "/PrintClientASI_Rev2.pdf";

#warn qq|pdfpath=$pdfpath\n|;
$xdp .= qq|
</topmostSubform>
</xfa:data>
</xfa:datasets>
<pdf href="${pdfpath}" xmlns="http://ns.adobe.com/xdp/pdf/" />
</xdp:xdp>
|;
if ( $form->{file} ) {
    open OUT, ">$form->{file}" || die "Couldn't open '$form->{file}' file: $!";
    print OUT ${xdp};
    close(OUT);
}
else { print qq|Content-Type: application/vnd.adobe.xdp+xml\n\n${xdp}|; }
$sClientASI->finish();
$sClient->finish();
$sProvider->finish();
myDBI->cleanup();
exit;

############################################################################
sub printClientASI {
    my ( $self, $rClientASI, $rClient ) = @_;
##
    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rClient->{'clinicClinicID'} );
    $sProvider->execute($AgencyID)
      || myDBI->dberror("printClientASI: select Provider $AgencyID");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = DBA->subxml( $rAgency->{Name} );
    my $AgencyAddr = $rAgency->{Addr1} . ', ';
    $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
    $AgencyAddr .=
      $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
    my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
##
    my $clientname = qq|$rClient->{'FName'} $rClient->{'LName'}|;
    my $addr1      = $rClient->{'Addr1'};
    my $addr2      = $rClient->{'Addr2'};
    my $csz = qq|$rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
    if ( $addr2 eq '' ) { $addr2 = $csz; $csz = ''; }
##
    $rClientASI->{'DCOM'} = DBA->subxml( $rClientASI->{'DCOM'} );
    $rClientASI->{'ECOM'} = DBA->subxml( $rClientASI->{'ECOM'} );
    $rClientASI->{'FCOM'} = DBA->subxml( $rClientASI->{'FCOM'} );
    $rClientASI->{'GCOM'} = DBA->subxml( $rClientASI->{'GCOM'} );
    $rClientASI->{'HCOM'} = DBA->subxml( $rClientASI->{'HCOM'} );
    $rClientASI->{'LCOM'} = DBA->subxml( $rClientASI->{'LCOM'} );
    $rClientASI->{'MCOM'} = DBA->subxml( $rClientASI->{'MCOM'} );
    $rClientASI->{'PCOM'} = DBA->subxml( $rClientASI->{'PCOM'} );
    $rClientASI->{'E3T'}  = DBA->subxml( $rClientASI->{'E3T'} );
    $rClientASI->{'E7T'}  = DBA->subxml( $rClientASI->{'E7T'} );
    $rClientASI->{'F23T'} = DBA->subxml( $rClientASI->{'F23T'} );
    $rClientASI->{'G19T'} = DBA->subxml( $rClientASI->{'G19T'} );
    $rClientASI->{'G21T'} = DBA->subxml( $rClientASI->{'G21T'} );
    $rClientASI->{'G22T'} = DBA->subxml( $rClientASI->{'G22T'} );
    $rClientASI->{'G23T'} = DBA->subxml( $rClientASI->{'G23T'} );
    $rClientASI->{'G24T'} = DBA->subxml( $rClientASI->{'G24T'} );
    $rClientASI->{'G25T'} = DBA->subxml( $rClientASI->{'G25T'} );
    $rClientASI->{'G26T'} = DBA->subxml( $rClientASI->{'G26T'} );
    $rClientASI->{'G27T'} = DBA->subxml( $rClientASI->{'G27T'} );
    $rClientASI->{'G29T'} = DBA->subxml( $rClientASI->{'G29T'} );
    $rClientASI->{'L16T'} = DBA->subxml( $rClientASI->{'L16T'} );
    $rClientASI->{'G2'}   = substr( $rClientASI->{'G2'}, 7, 4 );
    $rClientASI->{'G4'} = DBUtil->Date( $rClientASI->{'G4'}, 'fmt', 'MMDDYY' );
    $rClientASI->{'G5'} = DBUtil->Date( $rClientASI->{'G5'}, 'fmt', 'MMDDYY' );
    $rClientASI->{'G16'} =
      DBUtil->Date( $rClientASI->{'G16'}, 'fmt', 'MMDDYY' );
    my $out = '';

    foreach my $f ( sort keys %{$rClientASI} ) {

        #warn qq|PrintClientASI: rClientASI-$f=$rClientASI->{$f}\n|;
        #next if ( $f =~ /COM/ );
        #next if ( $f =~ /T$/ );
        #next if ( $f =~ /^SP/ );
        $out .= qq|    <${f}>$rClientASI->{$f}</${f}>\n|;
    }
    my $html = qq|
  <Record>
    <Agency>$rClientASI->{AgencySite}</Agency> 
    <clientname>${clientname}</clientname> 
    <addr1>${addr1}</addr1> 
    <addr2>${addr2}</addr2> 
    <csz>${csz}</csz> 
${out}
  </Record>
|;
    return ($html);
}
############################################################################
