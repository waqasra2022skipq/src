#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use login;
use DBA;
############################################################################
$form = DBForm->parse();

#warn qq|verify: type=$form->{'type'}, s=$form->{'s'}, a1=$form->{'a1'}, a2=$form->{'a2'}\n|;
my $dbh    = $form->dbconnect();
my $errmsg = '';
if ( $form->{type} eq 'InsID' ) {
    my $InsID       = $form->{'s'};
    my $DesigProvID = $form->{'a1'};
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("verify: InsID: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;
    warn qq|verify: Descr=$rxInsurance->{'Descr'}\n|;
    if ( $DesigProvID eq '' ) { $errmsg = ''; }
    else {
        if    ( $rxInsurance->{'Descr'} =~ /bcbsok/i )      { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /choice/i )      { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /firsthealth/i ) { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /medicaid/i )    { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /medicare/i )    { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /pacificare/i )  { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /railroad/i )    { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /selectcare/i )  { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /tricare/i )     { $errmsg = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /aetna/i )       { $errmsg = ''; }
        else {
            $errmsg =
qq|<FONT COLOR="red">Used only for BCBS,Medicare/Railroad,TriCare and other Insurances!</FONT>|;
        }
    }
}
elsif ( $form->{type} eq 'InsNum' ) {
    my $InsID = $form->{'a1'};
    ( my $InsNum = $form->{'s'} ) =~
      s/^\s*(.*?)\s*$/$1/g;    # trim both leading/trailing
    warn qq|verify: InsNum: InsID=$InsID, InsNum=$InsNum\n|;
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("verify: InsNum: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;
    warn qq|verify: Descr=$rxInsurance->{'Descr'}\n|;
    if    ( $InsNum eq '' ) { $errmsg = "InsNum cannot be NULL! "; }
    elsif ( $rxInsurance->{'Descr'} =~ /medicaid/i
        && ( $InsNum !~ /^B\d{8}$/ && $InsNum !~ /^\d{9}$/ ) )
    {
        $errmsg =
qq|<FONT COLOR="red">InsNum MUST BE 9 digits or B followed by 8 digits!</FONT>|;
    }
}
elsif ( $form->{type} eq 'DesigProv' ) {
    my $InsID = $form->{'a1'};
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("verify: DesigProv: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;

    #warn qq|verify: Descr=$rxInsurance->{'Descr'}\n|;
    if    ( $rxInsurance->{'Descr'} =~ /bcbsok/i )     { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /choice/i )     { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /medicaid/i )   { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /medicare/i )   { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /pacificare/i ) { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /railroad/i )   { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /selectcare/i ) { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /tricare/i )    { $errmsg = ''; }
    elsif ( $rxInsurance->{'Descr'} =~ /aetna/i )      { $errmsg = ''; }
    else {
        $errmsg =
qq|<FONT COLOR="red">Used only for BCBS,Medicare/Railroad,TriCare and other Insurances!</FONT>|;
    }
}
elsif ( $form->{type} eq 'LastSchoolName' ) {

    #warn qq|verify: s=$form->{'s'}, a1=$form->{'a1'}, a2=$form->{'a2'}\n|;
    my $DistID      = $form->{'a1'};   # or $form->['s'}, either one is the same
    my $SelectedIDs = $form->{'a2'};
    my $where =
      $DistID eq '' ? '' : "Active=1 and CountyDistrictCode='${DistID}'";

    #warn qq|verify: DistID=$DistID, SelectedIDs=$SelectedIDs\n|;
    $errmsg = qq|
  <SELECT ID="LastSchoolName" NAME="ClientIntake_LastSchoolName_1" >
  |
      . DBA->selxTable( $form, 'xSchoolSites', $SelectedIDs,
        'SchoolSite City State Zip CountyName CountyDistrictCode SiteCode',
        '', '', $where )
      . qq|
  </SELECT>
|;
}
elsif ( $form->{type} eq 'EFT' ) {
    my $InsID = $form->{'s'};
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("verify: InsID: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;
############################################################################
    my $files =
      qq|/var/www/okmis/www/forms/hesk_docs/Insurance_$rxInsurance->{Descr}_*|;
    my @Files = glob($files);
    foreach $path (@Files) {
        my ( $dir,      $fn )   = $path =~ /(.*\/)?(.+)/s;
        my ( $p1,       $p2 )   = $dir  =~ /(.*\/)?(.+)/s;
        my ( $filename, $sfx )  = split( '\.', $fn );
        my ( $Type,     $Link ) = split( '_',  $filename, 2 );
        $errmsg .=
qq|<BR><A HREF="javascript:ReportWindow(\'http://forms.okmis.com/${p2}${fn}\',\'$rxInsurance->{Descr}\')" >${Link}</A>|;
    }
    $errmsg .=
qq|<BR><A HREF="javascript:ReportWindow(\'$rxInsurance->{Help}\',\'HELP\')" >Additional Help</A>|
      if ( $rxInsurance->{Help} ne '' );
    $sxInsurance->finish();

    #warn qq|verify: InsID=$InsID, eft=$eft, era=$era\n|;
    #warn qq|verify: errmsg=${errmsg}\n|;
}

#warn qq|verify: errmsg=${errmsg}\n|;
print qq|Content-type: text/html

${errmsg}|;
############################################################################
exit;
