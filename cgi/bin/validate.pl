#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use login;
use DBA;
use DBUtil;
use gHTML;
############################################################################
my $form = DBForm->parse();
my ( $err, $warn, $msg, $out, $xml ) = ( '', '', '', '', '' );

#foreach my $f ( sort keys %{$form} ) { warn "validate: form-$f=$form->{$f}\n"; }
if ( $form->{method} eq 'vInsID' ) {
    my $target      = $form->{'target'};
    my $value       = $form->{'value'};
    my $InsID       = $value;
    my $DesigProvID = $form->{'d'};
    if ( $target eq 'DesigProvID' ) {
        $InsID       = $form->{'i'};
        $DesigProvID = $value;
    }
    my $dbh = $form->dbconnect();
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("validate: InsID: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;

    #warn qq|validate: Descr=$rxInsurance->{'Descr'}\n|;
    if ( $DesigProvID eq '' ) { $warn = ''; }
    else {
        if    ( $rxInsurance->{'Descr'} =~ /bcbsok/i )      { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /choice/i )      { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /firsthealth/i ) { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /medicaid/i )    { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /medicare/i )    { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /pacificare/i )  { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /railroad/i )    { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /selectcare/i )  { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /tricare/i )     { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /uhc/i )         { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /BCBSofAR/i )    { $warn = ''; }
        elsif ( $rxInsurance->{'Descr'} =~ /aetna/i )       { $warn = ''; }
        else {
            $warn =
qq|Used only for BCBS,Medicare/Railroad,TriCare and other Insurances!|;
            $msg = qq|<![CDATA[<FONT COLOR="red">${warn}</FONT>]]>|;
            $out .= qq|
  <command method="setvalue">
    <target>DesigProvID</target>
    <value></value>
  </command>
|;
        }
    }
    $sxInsurance->finish();
    my $id = 'msgDesigProvID';    # SPAN msg
    $out .= main->iwarn( $warn, $msg, $id );
}
elsif ( $form->{method} eq 'vInsNum' ) {
    my $target = $form->{'target'};
    ( my $InsNum = $form->{'value'} ) =~
      s/^\s*(.*?)\s*$/$1/g;       # trim both leading/trailing
    my $InsID = $form->{'i'};

    #warn qq|validate: InsNum: InsID=$InsID, InsNum=$InsNum\n|;
    my $dbh = $form->dbconnect();
    my $sxInsurance =
      $dbh->prepare("select * from xInsurance where ID='${InsID}'");
    $sxInsurance->execute()
      || $form->dberror("validate: InsNum: select xInsurance (${InsID})");
    my $rxInsurance = $sxInsurance->fetchrow_hashref;

    #warn qq|validate: Descr=$rxInsurance->{'Descr'}\n|;
    if    ( $InsNum eq '' ) { $err = "InsNum cannot be NULL! "; }
    elsif ( $rxInsurance->{'Descr'} =~ /medicaid/i
        && ( $InsNum !~ /^B\d{8}$/ && $InsNum !~ /^\d{9}$/ ) )
    {
        $err = qq|InsNum MUST BE 9 digits or B followed by 8 digits!|;
    }
    elsif (
        $rxInsurance->{'Descr'} =~ /medicare/i
        && ( $InsNum !~
/\b[1-9][AC-HJKMNP-RT-Yac-hjkmnp-rt-y][AC-HJKMNP-RT-Yac-hjkmnp-rt-y0-9][0-9]-?[AC-HJKMNP-RT-Yac-hjkmnp-rt-y][AC-HJKMNP-RT-Yac-hjkmnp-rt-y0-9][0-9]-?[AC-HJKMNP-RT-Yac-hjkmnp-rt-y]{2}\d{2}\b/
        )
      )
    {
        $err =
qq|Insurance Number NOT IN Medicare Beneficiary Identifier (MBI) Format!|;
    }
    $sxInsurance->finish();
    my $id = 'msgInsIDNum';    # SPAN msg
    $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>${target}</target>
    <value>${InsNum}</value>
  </command>
  <command method="setcontent">
    <target>${id}</target>
    <content></content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
}
elsif ( $form->{method} eq 'calcPG' ) {
    my $target    = $form->{'target'};
    my $value     = $form->{'value'};
    my $ClientID  = $form->{'c'};
    my $InsID     = $form->{'i'};
    my $PrAuthID  = $form->{'p'};
    my $TransType = $target eq 'TransType' ? $value : $form->{'t'};
    my $PAgroup   = '';
    if ( CDC->required( $form, $InsID ) ) {
        $PAgroup =
          $target eq 'TransType' && $value == 21
          ? 'PG038'
          : CDC->calcPG( $form, $ClientID, $InsID, $PrAuthID, $TransType );
    }
    my ( $months, $days ) = DBA->calcLOS( $form, $InsID, $PAgroup );
    my $EffDate = $target eq 'TransType' ? $form->{'d'} : $value;
    my $ExpDate = DBUtil->Date( $EffDate, $months, $days );

#warn qq|target=$target,d=$form->{'d'},value=$value,EffDate=$EffDate,ExpDate=$ExpDate\n|;
#warn qq|PAgroup=$PAgroup,value=$value,months=$months,days=$days,ExpDate=$ExpDate\n|;
    my $id = '';    # SPAN msg
    $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>ClientPrAuth_PAgroup_1</target>
    <value>${PAgroup}</value>
  </command>
  <command method="setvalue">
    <target>ClientPrAuth_ExpDate_1</target>
    <value>${ExpDate}</value>
  </command>
  <command method="setvalue">
    <target>ClientPrAuth_LOS_1</target>
    <value>${months}</value>
  </command>
  <command method="setcontent">
    <target>ClientPrAuth_PAgroup_1_display</target>
    <content>${PAgroup}</content>
  </command>
  <command method="setcontent">
    <target>ClientPrAuth_ExpDate_1_display</target>
    <content>${ExpDate}</content>
  </command>
  <command method="setcontent">
    <target>ClientPrAuth_LOS_1_display</target>
    <content>${months} months</content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
}
elsif ( $form->{method} eq 'vUpload' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};
    my $ProvID = $form->{'p'};
    my $id     = '';                  # SPAN msg
    my ( $directory, $filename ) = $value =~ m/(.*\/)(.*)$/;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>ProviderEDocs_Path_1_display</target>
    <content>${filename}</content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
}
elsif ( $form->{method} eq 'calcBMI' ) {
    my $value  = $form->{'value'};
    my $target = $form->{'target'};
    my $hf     = $target eq 'HeightFeet'   ? $value : $form->{'hf'};
    my $hi     = $target eq 'HeightInches' ? $value : $form->{'hi'};
    my $weight = $target eq 'Weight'       ? $value : $form->{'w'};
    my $id     = 'Client_BMI';         # SPAN msg
    my $height = ( $hf * 12 ) + $hi;
    my $bmi    = 0;
    if   ( $height > 0 ) { $bmi = ( $weight / ( $height * $height ) ) * 703; }
    else                 { $msg = 'Need Height'; }
    $bmi = sprintf( "%.2f", $bmi );
    my $heightcm = $height * 2.54;
    my $weightkg = $weight * 0.45359237;
    my $bsa      = 0.007184 * $weightkg * $heightcm;
    $bsa = sprintf( "%.2f", $bsa );

    #warn qq|validate: weight=${weight}, height=${height}, bmi=${bmi}\n|;
    $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>ClientVitalSigns_BMI_1</target>
    <value>${bmi}</value>
  </command>
  <command method="setcontent">
    <target>Client_BSA</target>
    <content>${bsa}</content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
}
elsif ( $form->{method} eq 'HL7Report' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};
    my $rpt =
      qq|Tag\tConceptCode\tConceptName\tValueSetOID\tCodeSystemOID\tp\n|;
    my $dbh   = $form->connectdb('okmis_config');
    my $where = $value eq '' ? '' : "where Tag='${value}'";

    #warn "select * from xHL7 ${where}";
    my $sxHL7 = $dbh->prepare("select * from xHL7 ${where}");
    $sxHL7->execute() || $form->dberror("HL7 select: ${where}");
    while ( my $r = $sxHL7->fetchrow_hashref ) {

        #warn qq|r: $r->{ConceptCode}\n|;
        $rpt .=
qq|$r->{Tag}\t$r->{ConceptCode}\t$r->{ConceptName}\t$r->{ValueSetOID}\t$r->{CodeSystemOID}\t$r->{Popup}\n|;
    }
    $sxHL7->finish();
    $dbh->disconnect();

    #warn qq|rpt: $rpt\n|;
    my $text = gHTML->htmlReport( $rpt, 1 );

    #warn qq|text: $text\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>HL7Tag_display</target>
    <content><![CDATA[${text}]]></content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
}
$xml = qq|<response>\n${out}</response>|;
$form->complete();

#warn qq|validate: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;
exit;
############################################################################
############################################################################
sub imsg {
    my ( $self, $msg, $id ) = @_;
    return ('') if ( $msg eq '' );
    my $out = qq|
  <command method="setcontent">
    <target>${id}</target>
    <content>${msg}</content>
  </command>
|;
    return ($out);
}

sub iwarn {
    my ( $self, $warn, $msg, $id ) = @_;
    return ('') if ( $warn eq '' );
    my $out = qq|
  <command method="alert">
    <message>${warn}</message>
  </command>
|;
    $out .= main->imsg( $msg, $id ) if ( $id ne '' );
    return ($out);
}

sub ierr {
    my ( $self, $target, $err, $msg, $id ) = @_;
    my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
    $out .= main->imsg( $msg, $id ) if ( $id ne '' );
    return ($out);
}
############################################################################
