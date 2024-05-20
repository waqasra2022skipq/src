package QID_Measures;

use CGI::Carp qw(warningsToBrowser); 
use CGI::Carp qw(warningsToBrowser fatalsToBrowser); 

use DBI;
use myForm;
use myDBI;
use DBA;
use DBUtil;
use Time::Local;
my $DT = localtime();

our $dbh;
our $withSelection;
our $multidel = chr(253);

our %measures = (
  'IPOP' => { 'count' => 0, 'M' => 0, 'F' => 0, 'pop_id' => 'EB3E42F6-9774-4066-8CA8-4329C95E4541',

              'Ethnicity' => {'Hisp_Lati' => 0, 'Not_Hisp_Lati' => 0}, 
              
              'Race' => {'BLK_AFR_AME' => 0, 'WHITE' => 0, 'Asian' => 0, 'Americ_Indi' => 0, 'Native_Hawaiian' => 0, 'Other' => 0},

              'Payer' => {'Medicaid' => 0, 'Medicare' => 0, 'Private' => 0, 'Other' => 0}, 
            
            }, 
  'DENOM' => { 'count' => 0, 'M' => 0, 'F' => 0, 'pop_id' => '66167A47-3FD1-4E48-A51F-750ED6FF9147',
              'Ethnicity' => {'Hisp_Lati' => 0, 'Not_Hisp_Lati' => 0}, 
              
              'Race' => {'BLK_AFR_AME' => 0, 'WHITE' => 0, 'Asian' => 0, 'Americ_Indi' => 0, 'Native_Hawaiian' => 0, 'Other' => 0},

              'Payer' => {'Medicaid' => 0, 'Medicare' => 0, 'Private' => 0, 'Other' => 0}
  },
  'DENEX' => {'count' => 0, 'M' => 0, 'F' => 0, 'pop_id' => 'CD4A4AD6-3C0B-4D7B-9751-F1A9268DF402'},
  'DENEXCEP' => {'count' => 0, 'M' => 0, 'F' => 0, 'pop_id' => 'CD4A4AD6-3C0B-4D7B-9751-F1A9268DF402'},
  'NUMERATOR' => {'count' => 0, 'M' => 0, 'F' => 0, 'pop_id' => 'FDF9F696-67F2-4AE6-953C-5DDE27BB93E7',
              'Ethnicity' => {'Hisp_Lati' => 0, 'Not_Hisp_Lati' => 0}, 
              
              'Race' => {'BLK_AFR_AME' => 0, 'WHITE' => 0, 'Asian' => 0, 'Americ_Indi' => 0, 'Native_Hawaiian' => 0, 'Other' => 0},

              'Payer' => {'Medicaid' => 0, 'Medicare' => 0, 'Private' => 0, 'Other' => 0}
  },
);

sub getMeasures {
  my ($self,$form,$ProvID, $measure_id) = @_;
  $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $form = DBUtil->setDates($form);
  $withSelection = DBA->withSelection($form,'and','Client.clinicClinicID','Treatment.ProvID','Treatment.ClientID','Treatment.TrID');
  my %measures = {};
  if($measure_id eq '165') {
    %measures = $self->genMeasures165($form);
  } elsif($measure_id eq '117') {
    %measures = $self->genMeasures117($form);
  } elsif($measure_id eq '68') {
    %measures = $self->genMeasures68($form);
  } elsif($measure_id eq '69') {
    %measures = $self->genMeasures69($form);
  } elsif($measure_id eq '138') {
    %measures = $self->genMeasures138($form);
  } elsif($measure_id eq '2') {
    %measures = $self->genMeasures2($form);
  } elsif($measure_id eq '159') {
    %measures = $self->genMeasures159($form);
  } elsif($measure_id eq '161') {
    %measures = $self->genMeasures161($form);
  } elsif($measure_id eq '156') {
    %measures = $self->genMeasures156($form);
  } elsif($measure_id eq '149') {
    %measures = $self->genMeasures149($form);
  }

  return %measures;
}

sub genMeasures149 {
  my ($self,$form) = @_;

  my ($PFMET, $PFNOTMET, $PFMET_TWO, $PFNOTMET_TWO) = (0,0,0,0);

  $measures{'IPOP'}{'pop_id'} = "B131923B-75CF-4D85-B4C9-FD412CC0036D"; 
  $measures{'DENOM'}{'pop_id'} = "530B1477-EEA8-4383-AE24-06062643583B"; 
  $measures{'NUMERATOR'}{'pop_id'} = "FCA90502-9BED-48C7-B08F-F0719338ACCE"; 
  $measures{'NUMERATOR'}{'pop_id'} = "4BADB805-F737-4423-8DC3-DDDCF071244F"; 

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID     
        left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID    
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (
              xSC.SCNum IN ( '96116', '90791', '90792', '99304', '99305', '99306',
                '99318', '99316', '99315', '99310', '99307', '99308', '99309', '99324', '99325', '99326', '99327', '99328', '99334', '99335', '99336',
                '99337', '99341', '99342', '99343','99344', '99345', '99347', '99348', '99349', '99350', '90832', '90834', '90837', '97165', '97166', '97167', '97168', '99201', '99202', '99203', '99204', '99205',
                '99212', '99213', '99214', '99215', '99241', '99242', '99243', '99244', '99245' 
              ) 
        )
        AND (
          misICD10.ICD10 IN ('A52.17','F01.50', 'F01.51','F02.80','F02.81','F03.90','F03.91','F05','F06.8','G30.0','G30.1','G30.8','G30.9','G31.01','G31.09','G31.83')
          OR
          misICD10.SNOMEDID IN ('10349009', '10532003','111480006','12348006','14070001','15662003','191449005','191451009','191452002','191454001',
            '191455000','191457008','191458003','191459006','191461002','191463004','191464005','191465006','191466007','191493005','22381000119105',
            '230258005','230270009','230282000','230283005','230285003','230286002','230287006','230288001','230289009','25772007','26852004','278857002',
            '279982005','281004','31081000119101','312991009','32875003','371024007','371026009','416780008','420614009','421023003','421529006','425390006',
            '429458009','429998004','430771000124100','442344002','4817008','51928006','52448006','54502004','55009008','56267009','59651006','6475002',
            '65096006','66108005','698624003','698625002','698626001','698687007','698725008','698726009','698781002','702393003','702426001','702429008',
            '703544004','70936005','713488003','713844000','715737004','716667005','716994006','722977005','722978000','722979008','722980006','723123001',
            '723390000','724776007','724777003','724992007','725898002','733184002','733185001','733190003','733191004','733192006','733193001','733194007',
            '762350007','762351006','762707000','79341000119107','82959004','838276009','90099008','9345005',

          )

        )

        ${withSelection}

      group by Client.ClientID
  |;

  my $sExclude = $dbh->prepare("select Treatment.TrID
    from Treatment left join xSC on xSC.SCID=Treatment.SCID 
    where Treatment.ClientID=? 
    and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
    and xSC.SCNum = 'G9741' OR xSC.SCNum = 'G0034'"
  );


  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment 
     left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=?
       and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
       and xSC.SCNum IN ('G9367','G9368','M1209','M1210','G0032', 'G0033')"
    )
  ;

}

sub genMeasures156 {
   my ($self,$form) = @_;

  my ($PFMET, $PFNOTMET, $PFMET_TWO, $PFNOTMET_TWO) = (0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, '$form->{ToDate}') >= 65 )
        and (
              xSC.SCNum IN ( '92002', '92004', '92012', '92014', '99202', '99203',
                '99204', '99205', '99212', '99213', '99214', '99215', '99221', '99222', '99223', '99231', '99232', '99233', '99238', '99239', '99281',
                '99282', '99283', '99284', '99285', '99304', '99305', '99306', '99307', '99308', '99309', '99310', '99315', '99316', '99341', '99342',
                '99344', '99345', '99347', '99348', '99349', '99350', 'G0438', 'G0439'
              ) 
            OR xSC.SCNum LIKE '\%99387\%'  OR xSC.SCNum LIKE '\%99397\%'
        )

        ${withSelection}

      group by Client.ClientID
  |;


  my $sExclude = $dbh->prepare("select Treatment.TrID
    from Treatment left join xSC on xSC.SCID=Treatment.SCID 
    where Treatment.ClientID=? 
    and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
    and xSC.SCNum = 'G9741' OR xSC.SCNum = 'G0034'"
  );


  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment 
     left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=?
       and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
       and xSC.SCNum IN ('G9367','G9368','M1209','M1210','G0032', 'G0033')"
    )
  ;

  $measures{'IPOP'}{'pop_id'} = "064940DC-3F04-4B31-88CA-367BE20AC510"; 
  $measures{'DENOM'}{'pop_id'} = "CD3CCAD3-3E90-4094-9987-9A9D2A5D574D"; 
  $measures{'NUMERATOR'}{'pop_id'} = "E384D9B0-6AD6-45BC-B562-A57E46FC1E90"; 
  $measures{'DENEX'}{'pop_id'} = "CEC58D2D-4525-45B8-B320-FFB35B654DA8"; 

  $measures{'NUMERATOR_TWO'}{'pop_id'} = "5577FDAE-5153-4B75-9B85-59CEF09CFC82"; 

  $srecord = $dbh->prepare($qrecord);
  $srecord->execute();
  while (my $rrecord = $srecord->fetchrow_hashref)
  {
    my $ClientID =  $rrecord->{'ClientID'};

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $sExclude->execute($ClientID, $rrecord->{'ContLogDate'});
    $cnt = $sExclude->rows;
    if($cnt > 0) {
      $measures{'DENEX'}{'count'} += 1;
      $measures{'DENEX'}{$gender} += 1;   
      $measures{'DENEX'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'DENEX'}{'Race'}{$Race} += 1;
      $measures{'DENEX'}{'Payer'}{$Payer} += 1;
      
      next;
    }

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;

    $sNumertor->execute($ClientID);
    my $rNumertor = $sNumertor->fetchrow_hashref;

    if($rNumertor->{'SCNum'} == 'G9367' || $rNumertor->{'SCNum'} == 'G9368') {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;

      if($rNumertor->{'SCNum'} == 'G9367') {
        $PFMET++;
      }
      if($rNumertor->{'SCNum'} == 'G9368') {
        $PFNOTMET++;
      }

    }

    if($rNumertor->{'SCNum'} == 'G9367' || $rNumertor->{'SCNum'} == 'G9368') {
      $measures{'NUMERATOR_TWO'}{'count'} += 1;
      $measures{'NUMERATOR_TWO'}{$gender} += 1;   
      $measures{'NUMERATOR_TWO'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR_TWO'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR_TWO'}{'Payer'}{$Payer} += 1; 

      if($rNumertor->{'SCNum'} == 'M1209') {
        $PFMET_TWO++;
      } else {
        $PFNOTMET_TWO++;
      }
    }

  }

  $measures{'IPOP_TWO'} = $measures{'IPOP'};
  $measures{'DENOM_TWO'} = $measures{'DENOM'};
  $measures{'DENEX_TWO'} = $measures{'DENEX'};

  $measures{'IPOP_TWO'}{'pop_id'} = "5E28FE53-02D9-4A14-9721-74729FBF2F73"; 
  $measures{'DENOM_TWO'}{'pop_id'} = "5BE6C6E2-64FA-49D5-8D2E-B977E2AB62A7"; 
  $measures{'DENEX_TWO'}{'pop_id'} = "82D62AA5-015B-4256-AF2B-C43D52622EFB";

  if($PFMET eq '0' || $PFNOTMET eq '0') {
    my $rate_1 = 0;
  } else {
    my $rate_1 = $PFMET / ($PFMET + $PFNOTMET);
  }

  if($PFMET_TWO eq '0' || $PFNOTMET_TWO eq '0') {
    my $rate_2 = 0;
  } else {
    my $rate_2 = $PFMET_TWO / ($PFMET_TWO + $PFNOTMET_TWO);
  }


  $measures{'PFRATES'}{'RATE_1'} = $rate_1; 
  $measures{'PFRATES'}{'RATE_2'} = $rate_2; 

  return %measures;
}

sub genMeasures161 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
        left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID

      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, '$form->{ToDate}') >= 18 )
        and xSC.SCNum IN ( 
          '99281', '99282', '99283', '99284', '99285', '99201', '99202', '99203', '99204', '99205', '99212', 
          '99213', '99214', '99215', '99241', '99242', '99243', '99244', '99245', '90832', '90834', '90837', '90845',
          '98966', '98967', '98968', '99441', '99442', '99443', '90791', '90792'
        ) 

        and misICD10.ICD10 IN ('F32.0','F32.1', 'F32.2', 'F32.3','F32.89', 'F32.9', 'F33.0', 'F33.1', 'F33.2','F33.3', 'F33.9')

        ${withSelection}

      group by Client.ClientID
  |;


  my $sNumertor = $dbh->prepare("
    select 
      Treatment.TrID
    from Treatment 
      left join Client on Client.ClientID=Treatment.ClientID
      left join ClientInterventionsPerformed on ClientInterventionsPerformed.ClientID = Client.ClientID

    where Treatment.ClientID = ?
      AND Treatment.ContLogDate = ?
      AND (ClientInterventionsPerformed.Intervention = 'SNOMEDCT_225337009' and (ClientInterventionsPerformed.VisitDate >= '$form->{FromDate}' and ClientInterventionsPerformed.VisitDate<='$form->{ToDate}'))
      "
    )
  ;

  $measures{'IPOP'}{'pop_id'} = "DC8E1A1C-BD9E-4F8E-8584-388BECBEF0E8"; 
  $measures{'DENOM'}{'pop_id'} = "2B4E018E-7F6A-4C15-AD7B-AECABB45D4A7"; 
  $measures{'NUMERATOR'}{'pop_id'} = "D732F43D-14F0-44C4-B59E-EB48BA469080"; 

  $srecord = $dbh->prepare($qrecord);
  $srecord->execute();
  while (my $rrecord = $srecord->fetchrow_hashref)
  {
    my $ClientID =  $rrecord->{'ClientID'};

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;
    
    $sNumertor->execute($ClientID, $rrecord->{'ContLogDate'});

    if($sNumertor->rows > 0) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }


  }

  return %measures;
}

sub genMeasures159 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS, xSC.SCNum
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
        , ClientDischargeCDC.TransDate
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
        left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID
        left join ClientPHQ9 as CPHP9 on CPHP9.ClientID = Client.ClientID
        left join ClientTPHQ9 as CTPHP9 on CTPHP9.ClientID = Client.ClientID
        left join ClientDischargeCDC on ClientDischargeCDC.ClientID = Client.ClientID
 
      where Client.ClientID>100
        and (Treatment.ContLogDate >= '11/1/2021' and Treatment.ContLogDate<='10/31/2022')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, '10/31/2022') >= 12 )
        and (TIMESTAMPDIFF(YEAR, Client.DOB, '10/31/2022') <= 17)

        AND (xSC.SCNum IN ('90791', '90792', '90832',
              '90834', '90837', '99202', '99203', '99204', '99205', '99211', '99212', '99213', '99214', '99215', 'G0402', 'G0438',
              'G0439', '99421', '99422', '99423', '99441', '99442', '99443', '96156', '96158', '96159'
             )
          OR xSC.SCNum LIKE '99394%' OR xSC.SCNum LIKE '99384%' 
        )

        and misICD10.ICD10 IN ('F32.0','F32.1', 'F32.2', 'F32.3','F32.4', 'F32.5', 'F32.9','F33.0', 'F33.1', 'F33.2','F33.3', 'F33.40', 'F33.41', 'F33.42','F33.9', 'F34.1')
        and (
          (CPHP9.q1 + CPHP9.q2 + CPHP9.q3 + CPHP9.q4 + + CPHP9.q5 + CPHP9.q6 + CPHP9.q7 + CPHP9.q8 + CPHP9.q9 + CPHP9.q10) > 9 and (TIMESTAMPDIFF(DAY, CPHP9.TestDate, Treatment.ContLogDate) < 8 )
          OR            
          (CTPHP9.q1 + CTPHP9.q2 + CTPHP9.q3 + CTPHP9.q4 + + CTPHP9.q5 + CTPHP9.q6 + CTPHP9.q7 + CTPHP9.q8 + CTPHP9.q9 + CTPHP9.q10 + CTPHP9.q11 + CTPHP9.q12 + CTPHP9.q13) > 9 and (TIMESTAMPDIFF(DAY, CTPHP9.TestDate, Treatment.ContLogDate) < 8 )
        )


      ${withSelection}
      group by Client.LName,Client.FName,Client.ClientID
  |;

  my $sExclude = qq|
    select Treatment.TrID
    from Treatment 
    left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID    
    left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID    
    WHERE Treatment.ClientID=?
    Treatment.ContLogDate < ?
    AND (
      misICD10.ICD10 IN ('F30.10', 'F30.11', 'F30.12', 'F30.13', 'F30.2', 'F30.3', 'F30.4', 'F30.8', 'F30.9', 'F31.0', 'F31.10', 'F31.11',
        'F31.12', 'F31.13', 'F31.2', 'F31.30', 'F31.31', 'F31.32', 'F31.4', 'F31.5', 'F31.60', 'F31.61', 'F31.62', 'F31.63',
        'F31.64', 'F31.70', 'F31.71', 'F31.72', 'F31.73', 'F31.74', 'F31.75', 'F31.76', 'F31.77', 'F31.78', 'F31.81',
        'F31.89', 'F31.9'
      )

      OR misICD10.ICD10 IN ('F34.0', 'F60.3', 'F60.4', 'F68.10', 'F68.11', 'F68.12', 'F68.13' 'F30.12')
      
      OR misICD10.ICD10 IN ('F20.0', 'F20.1', 'F20.2', 'F20.3', 'F20.5', 'F20.81', 'F20.89', 'F20.9', 'F21', 'F23', 'F25.0', 'F25.1', 'F25.8', 'F25.9', 'F28', 'F29')

      OR misICD10.ICD10 IN ('F84.0', 'F84.3', 'F84.8', 'F84.9')

      OR (ClientDischargeCDC.TransType = '68' and (TIMESTAMPDIFF(MONTH, ClientDischargeCDC.TransDate, Treatment.ContLogDate) <= 14 )) -- Patients who died any time prior to the end of the measure assessment period 

      OR misICD10.ICD10 = 'Z51.5'

    )
  |;

  my $sNumertor = $dbh->prepare("
    select 
      Treatment.TrID, xSC.SCNum
    from Treatment 
      left join Client on Client.ClientID=Treatment.ClientID
      left join xSC on xSC.SCID=Treatment.SCID
      left join ClientPHQ9 as CPHP9 on CPHP9.ClientID = Client.ClientID
      left join ClientTPHQ9 as CTPHP9 on CTPHP9.ClientID = Client.ClientID

    where Treatment.ClientID=?
      and (TIMESTAMPDIFF(MONTH, ?, Treatment.ContLogDate) <= 14 )
      and xSC.SCNum IN ('M1019','M1020')
      and (
        (CPHP9.q1 + CPHP9.q2 + CPHP9.q3 + CPHP9.q4 + + CPHP9.q5 + CPHP9.q6 + CPHP9.q7 + CPHP9.q8 + CPHP9.q9 + CPHP9.q10) < 5 and (TIMESTAMPDIFF(DAY, CPHP9.TestDate, Treatment.ContLogDate) < 8 )
        OR            
        (CTPHP9.q1 + CTPHP9.q2 + CTPHP9.q3 + CTPHP9.q4 + + CTPHP9.q5 + CTPHP9.q6 + CTPHP9.q7 + CTPHP9.q8 + CTPHP9.q9 + CTPHP9.q10 + CTPHP9.q11 + CTPHP9.q12 + CTPHP9.q13) < 5 and (TIMESTAMPDIFF(DAY, CTPHP9.TestDate, Treatment.ContLogDate) < 8 )
      )
      "
    )
  ;

  $measures{'IPOP'}{'pop_id'} = "E9A0337E-6F37-434B-BA79-27A275C8AED2"; 
  $measures{'DENOM'}{'pop_id'} = "12EBE340-3CC4-4903-8C89-A64C1224E3C5"; 
  $measures{'NUMERATOR'}{'pop_id'} = "7783900A-FCDA-4105-ACA7-CE0A5B44D9B1"; 

  $srecord = $dbh->prepare($qrecord);
  $srecord->execute();
  while (my $rrecord = $srecord->fetchrow_hashref)
  {
    my $ClientID =  $rrecord->{'ClientID'};

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $sExclude->execute($ClientID, $rrecord->{'ContLogDate'});
    $cnt = $sExclude->rows;
    next if($cnt > 0);

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;

    $sNumertor->execute($ClientID, $rrecord->{'TransDate'});

    if($sNumertor->rows > 0) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }

  }

  return %measures;

}

sub genMeasures2 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, '$form->{ToDate}') >= 12 )
        AND Treatment.POS != '12'
        and (
              xSC.SCNum IN ( '59400', '59510', '59610', '59618', '90791', '90792', '90832', '90834', '90837', '92625', '96105', 
                '96112', '96116', '96125', '96136', '96138', '96156', '96158', '97161', '97162', '97163', '97164', '97165', 
                '97166', '97167', '98966', '98967', '98968', '99078', '99202', '99203', '99204', '99205', '99212', '99213', '99214', 
                '99215', '99304', '99305', '99306', '99307', '99308', '99309', '99310', '99315', '99316', '99341', '99342', '99344', 
                '99345', '99347', '99348', '99349', '99350',   '99424', '99441', '99442', '99443', '99483', 
                '99484', '99491', '99492', '99493', 'G0101', 'G0402', 'G0438', 'G0439', 'G0444'
              ) 
            OR xSC.SCNum LIKE '\%99384\%' OR xSC.SCNum LIKE '\%99385\%' OR xSC.SCNum LIKE '\%99386\%' OR xSC.SCNum LIKE '\%99387\%' OR xSC.SCNum LIKE '\%99394\%'
            OR xSC.SCNum LIKE '\%99395\%' OR xSC.SCNum LIKE '\%99396\%' OR xSC.SCNum LIKE '\%99397\%'
            OR xSC.SCNum LIKE '\%99402\%' OR xSC.SCNum LIKE '\%99403\%' OR xSC.SCNum LIKE '\%96110\%'
        )

        ${withSelection}

      group by Client.ClientID
  |;

  my $sExclude = $dbh->prepare("select Treatment.TrID
    from Treatment left join xSC on xSC.SCID=Treatment.SCID 
    where Treatment.ClientID=? 
    AND Treatment.ContLogDate = ?
    and xSC.SCNum = 'G9717'"
  );


  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment 
     left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=?
       and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
       and xSC.SCNum IN ('G8431','G8510','G8433','G8432','G8511')"
    )
  ;

  $measures{'IPOP'}{'pop_id'} = "908AE77A-2E96-4BBA-89C1-8974F28F7DF1"; 
  $measures{'DENOM'}{'pop_id'} = "4A8586D1-0CD3-43CA-BFB3-A7089E65EA16"; 
  $measures{'NUMERATOR'}{'pop_id'} = "55EAE4F4-F97D-4574-9AA6-66E92D210465"; 
  $measures{'DENEXCEP'}{'pop_id'} = "4DAA814C-005B-4B38-A9B4-980A0BE45EF3"; 

  $srecord = $dbh->prepare($qrecord);
  $srecord->execute();
  while (my $rrecord = $srecord->fetchrow_hashref)
  {
    my $ClientID =  $rrecord->{'ClientID'};

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $sExclude->execute($ClientID, $rrecord->{'ContLogDate'});
    $cnt = $sExclude->rows;
    next if($cnt > 0);

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;

    $sNumertor->execute($ClientID);

    if($sNumertor->rows > 0) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }
    while(my $row = $sNumertor->fetchrow_hashref) {
      if($row->{'SCNum'} eq 'G8433') {
        $measures{'DENEXCEP'}{'count'} += 1; 
        $measures{'DENEXCEP'}{$gender} += 1;
        $measures{'DENEXCEP'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'DENEXCEP'}{'Race'}{$Race} += 1;
        $measures{'DENEXCEP'}{'Payer'}{$Payer} += 1;  
      }
    }

  }

  return %measures;
}

sub genMeasures138 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 18 )

        ${withSelection}

      group by Client.ClientID
  |;



  $qTwoEncounters = qq|
    SELECT COUNT(*) AS Treats FROM Treatment left join xSC on xSC.SCID=Treatment.SCID
      WHERE Treatment.ClientID = ? 
        AND ContLogDate >= '$form->{FromDate}' AND ContLogDate <= '$form->{ToDate}'
        AND xSC.SCNum IN (
          '90791', '90792', '90832', '90834', '90837', '90845', '92002', '92004', '92012', '92014', '92521', '92522', '92523', '92524', '92540', '92557', '92625', '96156',
          '96158', '97161', '97162', '97163', '97165', '97166', '97167', '97168', '97802', '97803', '97804', '99024', '99202', '99203',
          '99204', '99205', '99212', '99213', '99214', '99215', '99341', '99342', '99344', '99345', '99347', '99348', '99349', '99350',
          'G0270', 'G0271'
        )
  |;

  $qOneEncounters = qq|
    SELECT COUNT(*) AS Treats FROM Treatment left join xSC on xSC.SCID=Treatment.SCID
      WHERE Treatment.ClientID = ? 
        AND ContLogDate >= '$form->{FromDate}' AND ContLogDate <= '$form->{ToDate}'
        AND (
              xSC.SCNum LIKE '\%99385\%' OR xSC.SCNum LIKE '\%99386\%' OR xSC.SCNum LIKE '\%99387\%' OR xSC.SCNum LIKE '\%99395\%' OR xSC.SCNum LIKE '\%99396\%' OR xSC.SCNum LIKE '\%99397\%'
              OR xSC.SCNum LIKE '\%99401\%' OR xSC.SCNum LIKE '\%99402\%' OR xSC.SCNum LIKE '\%99403\%' OR xSC.SCNum LIKE '\%99404\%' OR xSC.SCNum LIKE '\%99411\%' OR xSC.SCNum LIKE '\%99412\%'
              OR xSC.SCNum LIKE '\%99429\%' OR xSC.SCNum = 'G0438' OR xSC.SCNum = 'G0439'
            )
  |;

  my $sExclude = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=? 
     AND Treatment.ContLogDate = ?
   and xSC.SCNum = 'M1159'");


  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=? 
       and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
       and xSC.SCNum IN ('G9902','G9903','G9906','G9908','G0030', '1036F', 'G0029', 'G9907')"
    )
  ;

  my $srecord = $dbh->prepare($qrecord);
  $srecord->execute();

  $measures{'IPOP'}{'pop_id'} = "908AE77A-2E96-4BBA-89C1-8974F28F7DF1"; 
  $measures{'DENOM'}{'pop_id'} = "4A8586D1-0CD3-43CA-BFB3-A7089E65EA16"; 
  $measures{'NUMERATOR'}{'pop_id'} = "55EAE4F4-F97D-4574-9AA6-66E92D210465"; 


  $measures{'DENOM_TWO'}{'pop_id'} = "21377D57-D5CC-4599-9DFE-2C989AFAAD1E"; 
  $measures{'NUMERATOR_TWO'}{'pop_id'} = "1434049B-C8C7-41F2-8454-212F248527E6"; 

  $measures{'NUMERATOR_THREE'}{'pop_id'} = "D72761CF-7D10-471A-A89C-461892FE8BD6"; 


  while (my $rrecord = $srecord->fetchrow_hashref)
  {
    my $ClientID =  $rrecord->{'ClientID'};

    $sTwoEncounters = $dbh->prepare($qTwoEncounters);
    $sOneEncounters = $dbh->prepare($qOneEncounters);

    $sTwoEncounters->execute($ClientID);
    $sOneEncounters->execute($ClientID);

    $rTwoEncounters = $sTwoEncounters->fetchrow_hashref;
    $rOneEncounters = $sOneEncounters->fetchrow_hashref;

    if($rTwoEncounters->{"Treats"} < 2 && $rOneEncounters->{"Treats"} < 1) {
      next;
    }

    my $gender = $rrecord->{'Gend'};

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;
    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $sExclude->execute($ClientID, $rrecord->{'ContLogDate'});
    $cnt = $sExclude->rows;
    next if($cnt > 0);

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;

    $sNumertor->execute($ClientID);

    if($sNumertor->rows > 0) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }
    while(my $row = $sNumertor->fetchrow_hashref) {


      if($row->{'SCNum'} eq 'G9902') {
        $measures{'DENOM_TWO'}{'count'} += 1;
        $measures{'DENOM_TWO'}{$gender} += 1;   
        $measures{'DENOM_TWO'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'DENOM_TWO'}{'Race'}{$Race} += 1;
        $measures{'DENOM_TWO'}{'Payer'}{$Payer} += 1; 
      }

      if($row->{'SCNum'} eq 'G9906' || $row->{'SCNum'} eq 'G9907' || $row->{'SCNum'} eq 'G9908') {
        $measures{'NUMERATOR_TWO'}{'count'} += 1;
        $measures{'NUMERATOR_TWO'}{$gender} += 1;   
        $measures{'NUMERATOR_TWO'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'NUMERATOR_TWO'}{'Race'}{$Race} += 1;
        $measures{'NUMERATOR_TWO'}{'Payer'}{$Payer} += 1; 
      }

      if($row->{'SCNum'} eq 'G0030' || $row->{'SCNum'} eq '1036F' || $row->{'SCNum'} eq 'G0029') {
        $measures{'NUMERATOR_THREE'}{'count'} += 1;
        $measures{'NUMERATOR_THREE'}{$gender} += 1;   
        $measures{'NUMERATOR_THREE'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'NUMERATOR_THREE'}{'Race'}{$Race} += 1;
        $measures{'NUMERATOR_THREE'}{'Payer'}{$Payer} += 1; 
      }
    }

  }

  $measures{'IPOP_TWO'} = $measures{'IPOP'};
  $measures{'IPOP_THREE'} = $measures{'IPOP'};

  $measures{'IPOP_TWO'}{'pop_id'} = "7C477BC5-C75B-4B7C-B061-A61CEC7E821B"; 
  $measures{'IPOP_THREE'}{'pop_id'} = "124F09CB-F6BB-4717-BC04-49E5C1CE52B2";

  $measures{'DENOM_THREE'} = $measures{'DENOM'};
  $measures{'DENOM_THREE'}{'pop_id'} = "1764C19B-A8EE-41A0-A384-93B5371CE650"; 

  return %measures;
}

sub genMeasures69 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS, xSC.SCNum
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
 
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 18 )
        and Treatment.Mod4 != 'GT'
        and Treatment.POS != '12'
        and (xSC.SCNum IN ( '90791', '90792', '90832', '90834', '90837', '96150', '96151', '96152', '97161', '97162', '97163',
                            '97165', '97166', '97167', '97802', '97803', '99201', '99202', '99203', '99204', '99205', '99212', 
                            '99213', '99214', '99215', '99236', '99304', '99305', '99306', '99307', '99308', '99309', '99310', 
                            '99315', '99316', '99318', '99324', '99325', '99326', '99327', '99328', '99334', '99335', '99336', 
                            '99337', '99339', '99340', '99401', '99402', 
                            'D7140', 'D7210', 'G0101', 'G0108', 'G0270', 'G0271', 'G0402', 'G0438', 'G0439', 'G0447', 'G0473'
                          ) 
              OR xSC.SCNum LIKE '\%99385\%' OR xSC.SCNum LIKE '\%99386\%' OR xSC.SCNum LIKE '\%99387\%' OR xSC.SCNum LIKE '\%99395\%' OR xSC.SCNum LIKE '\%99396\%' OR xSC.SCNum LIKE '\%99397\%'
            )

      ${withSelection}
      group by Client.LName,Client.FName,Client.ClientID
  |;

  my $sExclude = $dbh->prepare("select Treatment.TrID, xSC.SCNum
     from Treatment left join xSC on xSC.SCID=Treatment.SCID 
     where Treatment.ClientID=?
     AND Treatment.ContLogDate = ? 
   and xSC.SCNum IN ('G9996','G9997')");


  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum
                 from Treatment left join xSC on xSC.SCID=Treatment.SCID 
                 where Treatment.ClientID=? 
                   and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
                   and xSC.SCNum IN ('G8420','G8417','G8418','G2181','G9716', 'G8421', 'G8419')"
                )
  ;

  my $srecord = $dbh->prepare($qrecord);
  $srecord->execute();

  $measures{'IPOP'}{'pop_id'} = "ECEB0BD8-FF04-4ECE-8674-0AF4A3FB5CA9"; 
  $measures{'DENOM'}{'pop_id'} = "FAB66FEA-6008-423B-A3C2-FBE727361CC3"; 
  $measures{'NUMERATOR'}{'pop_id'} = "9B735D8D-3813-4887-A324-9F6B48BDC63C"; 
  $measures{'DENEXCEP'}{'pop_id'} = "19CB93F3-2532-4C7D-BC60-593589929D89"; 


  while (my $rrecord = $srecord->fetchrow_hashref)
  {

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    my $ClientID =  $rrecord->{'ClientID'};
    $sExclude->execute($ClientID, $rrecord->{'ContLogDate'});
    $cnt = $sExclude->rows;
    next if($cnt > 0);

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;

    $sNumertor->execute($ClientID);

    if($sNumertor->rows > 0) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }
    while(my $row = $sNumertor->fetchrow_hashref) {

      if($row->{'SCNum'} eq 'G2181' || $row->{'SCNum'} eq 'G9716') {
        $measures{'DENEXCEP'}{'count'} += 1; 
        $measures{'DENEXCEP'}{$gender} += 1;
        $measures{'DENEXCEP'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'DENEXCEP'}{'Race'}{$Race} += 1;
        $measures{'DENEXCEP'}{'Payer'}{$Payer} += 1;  
      }

    }

  }

  return %measures;
}

sub genMeasures68 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS, xSC.SCNum
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
 
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 18 )
        and (xSC.SCNum IN ( '59400', '59510', '59610', '59618', '90791', 
          '90792', '90832', '90834', '90837', '90839', '92002', '92004', '92012', '92014', '92507', '92508', '92526', '92537', '92538', '92540', 
          '92541', '92542', '92544', '92545', '92548', '92550', '92557', '92567', '92568', '92570', '92588', '92626', '96116', '96156', '96158', 
          '97129', '97161', '97162', '97163', '97164', '97165', '97166', '97167', '97168', '97802', '97803', '97804', '98960', '98961', '98962', 
          '99202', '99203', '99204', '99205', '99212', '99213', '99214', '99215', '99221', '99222', '99223', '99236', '99281', '99282', '99283', 
          '99284', '99285', '99304', '99305', '99306', '99307', '99308', '99309', '99310', '99315', '99316', '99341', '99342', '99344', '99345', 
          '99347', '99348', '99349', '99350', '99424', '99491', '99495', '99496', 
          'G0101', 'G0108', 'G0270', 'G0402', 'G0438', 'G0439'
        ) OR xSC.SCNum LIKE '\%99385\%' OR xSC.SCNum LIKE '\%99386\%' OR xSC.SCNum LIKE '\%99387\%' OR xSC.SCNum LIKE '\%99395\%' OR xSC.SCNum LIKE '\%99396\%' OR xSC.SCNum LIKE '\%99397\%')

      ${withSelection}
      group by Client.LName,Client.FName,Client.ClientID
  |;

  my $sNumertor = $dbh->prepare("select Treatment.TrID, xSC.SCNum from Treatment left join xSC on xSC.SCID=Treatment.SCID where Treatment.ClientID=? and xSC.SCNum IN ('G8427','G8428','G8430')");

  my $srecord = $dbh->prepare($qrecord);
  $srecord->execute();

  $measures{'IPOP'}{'pop_id'} = "972EBD00-B885-4E74-8033-B2F14671CCEF"; 
  $measures{'DENOM'}{'pop_id'} = "1959AB01-1DAF-4D59-94C9-D11DE2F515C9"; 
  $measures{'NUMERATOR'}{'pop_id'} = "5E7C9BEE-CC15-42B5-A34E-F8D813CD303E"; 


  while (my $rrecord = $srecord->fetchrow_hashref)
  {

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;


    my $ClientID =  $rrecord->{'ClientID'};

    $sNumertor->execute($ClientID);

    if(my $row = $sNumertor->fetchrow_hashref) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }

  }

  return %measures;
}

sub genMeasures117 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS, xSC.SCNum
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
 
      where 
        Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 2 )
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) <= 3 )
        and xSC.SCNum IN ('99201', '99391', '99341', '99211', '99342', '99381', '98966')
      ${withSelection}
      group by Client.LName,Client.FName,Client.ClientID
  |;


  # Denom Exclusion

  my $sExclude = $dbh->prepare("select ClientProblems.UUID 
    from Client 
    left join ClientProblems on Client.ID=ClientProblems.ClientID 
    left join ClientEmergency on Client.ID=ClientEmergency.ClientID 
    left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID 
    where (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 2 ) 
    AND Treatment.ContLogDate = ?
    and misICD10.ICD10 IN ('D81.0','D81.1', 'D81.2', 'B20', 'K56.1', 'C90.0', 'C95.0', 'C95.90')
    or ClientEmergency.HospiceCheck = '1'
    "
  );

  my $srecord = $dbh->prepare($qrecord);
  $srecord->execute();

  $measures{'IPOP'}{'pop_id'} = "40CAFBE0-4A13-4D63-A2A8-49CFC65C726F"; 
  $measures{'DENOM'}{'pop_id'} = "DB248CBC-3C13-4C3E-A77C-447BF11FDECE"; 
  $measures{'NUMERATOR'}{'pop_id'} = "9F6EA4E8-5440-4EEF-8AA7-C99873F6814F"; 


  while (my $rrecord = $srecord->fetchrow_hashref)
  {

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;


    $sExclude->execute($rrecord->{'ClientID'}, $rrecord->{'ContLogDate'});
    $sExclude->fetchrow_hashref;
    my $cnt = $sExclude->rows;
    print qq|Exclude cnt=${cnt}\n| if ( $debug );
    next if ( $cnt );
 

    $measures{'DENOM'}{'count'} += 1;
    $measures{'DENOM'}{$gender} += 1;   
    $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'DENOM'}{'Race'}{$Race} += 1;
    $measures{'DENOM'}{'Payer'}{$Payer} += 1;


    my $ClientID =  $rrecord->{'ClientID'};

    my $checkDTap = $self->checkDTap($ClientID);
    my $checkIPV = $self->checkIPV($ClientID);
    my $checkMMR = $self->checkMMR($ClientID);

    my $checkHiB = $self->checkHiB($ClientID);

    my $checkpHipA = $self->checkpHipA($ClientID);
    my $checkpRotaVirus = $self->checkpRotaVirus($ClientID);
    my $checkpInfluenza = $self->checkpInfluenza($ClientID);
    my $checkPneumococcalVacc = $self->checkPneumococcalVacc($ClientID);
    my $checkvaricella = $self->checkvaricella($ClientID);
    my $checkHepB = $self->checkHepB($ClientID);

    if($checkDTap && $checkIPV && $checkMMR && $checkHiB && $checkHepB && $checkvaricella && $checkPneumococcalVacc && $checkpRotaVirus && $checkpInfluenza ) {
      $measures{'NUMERATOR'}{'count'} += 1; 
      $measures{'NUMERATOR'}{$gender} += 1;
      $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
      $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
    }

  }

  return %measures;

}


sub genMeasures165 {
  my ($self,$form) = @_;

  my ($Denominator, $total, $PFMET, $DNEXCEPTION, $PFNOTMET) = (0,0,0,0,0);

  my $qrecord = qq|
      select Treatment.TrID,Treatment.ContLogDate,Treatment.ClinicID, Treatment.POS, xSC.SCNum
        ,Client.LName,Client.FName,Client.ClientID
        ,Client.Gend, Client.Ethnicity ,Client.Race as ClientRace
        ,Clinic.Name as ClinicName
        ,xRaces.Descr as Race
        ,xInsurance.ID as InsID
 
      from Treatment 
        left join Client on Client.ClientID=Treatment.ClientID
        left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
        left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
        left join xSC on xSC.SCID=Treatment.SCID
        left join xInsurance on xInsurance.ID=xSC.InsID
        left join ClientNoteProblems on ClientNoteProblems.TrID=Treatment.TrID
 
      where Client.ClientID>100
        and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) >= 18 )
        and (TIMESTAMPDIFF(YEAR, Client.DOB, Treatment.ContLogDate) <= 85)
        AND (xSC.SCNum IN ('99202', '99203', '99204', '99205', '99212', '99213', '99214', '99215', '99341', '99342', '99344', '99345', '99347', '99348', '99349', '99350', 'G0438', 'G0439' )
          OR xSC.SCNum LIKE '99385%' OR xSC.SCNum LIKE '99386%' OR xSC.SCNum LIKE '99387%' OR xSC.SCNum LIKE '99395%' OR xSC.SCNum LIKE '99396%' OR xSC.SCNum LIKE '99397%'
          OR xSC.SCNum LIKE 'H0004 %' OR xSC.SCNum LIKE 'H0031%'
        )

      ${withSelection}
      group by Client.LName,Client.FName,Client.ClientID
  |;

  # and ClientNoteProblems.UUID LIKE '%\_I10'


  my $sGCode = $dbh->prepare("select Treatment.TrID, xSC.SCNum 
      from Treatment left join xSC on xSC.SCID=Treatment.SCID 
      where Treatment.ClientID=? 
      and (Treatment.ContLogDate >= '$form->{FromDate}' and Treatment.ContLogDate<='$form->{ToDate}')
      and xSC.SCNum IN ('G9740','G0031', 'G9231', 'G9910', 'G2115','G2116', 'G2118', 'G8754', 'G8755', 'G8756', 'G8752', 'G8753')"
  );



  my $srecord = $dbh->prepare($qrecord);
  $srecord->execute();


  while (my $rrecord = $srecord->fetchrow_hashref)
  {

    my $gender = $rrecord->{'Gend'};

    $measures{'IPOP'}{'count'} += 1; 
    $measures{'IPOP'}{$gender} += 1;

    my $Ethnicity = $self->getEthnicity($rrecord->{'Ethnicity'});
    my $Race = $self->getRace($rrecord->{'ClientRace'});
    my $Payer = $self->getPayer($rrecord->{'InsID'});

    $measures{'IPOP'}{'Ethnicity'}{$Ethnicity} += 1;
    $measures{'IPOP'}{'Race'}{$Race} += 1;
    $measures{'IPOP'}{'Payer'}{$Payer} += 1;

    my $update_denom = 1;

    $sGCode->execute($rrecord->{'ClientID'});
    while (my $rGCode = $sGCode->fetchrow_hashref) {
      my $update_numerator = 0;
      if($rGCode->{'SCNum'} == 'G8752' || $rGCode->{'SCNum'} == 'G8754' || $rGCode->{'SCNum'} == 'G8418') {
        $PFMET += 1;
        $update_numerator = 1; 
      }

      if($self->in_array($rGCode->{'SCNum'}, ('G9740', 'G0031', 'G9231', 'G9910', 'G2115', 'G2116', 'G2118'))) {
        $update_denom = 0;
      }

      if($self->in_array($rGCode->{'SCNum'}, ('G8755', 'G8753', 'G8756'))) {
        $PFNOTMET += 1; 
        $update_num = 1; 

      }

      if($update_numerator) {
        
        $measures{'NUMERATOR'}{'count'} += 1; 
        $measures{'NUMERATOR'}{$gender} += 1;
        $measures{'NUMERATOR'}{'Ethnicity'}{$Ethnicity} += 1;
        $measures{'NUMERATOR'}{'Race'}{$Race} += 1;
        $measures{'NUMERATOR'}{'Payer'}{$Payer} += 1;
      }

    }

    if($update_denom) {

      $measures{'DENOM'}{'count'} += 1;
      $measures{'DENOM'}{$gender} += 1;   
      $measures{'DENOM'}{'Ethnicity'}{$Ethnicity} += 1;
      $measures{'DENOM'}{'Race'}{$Race} += 1;
      $measures{'DENOM'}{'Payer'}{$Payer} += 1;
    }
  }


  return %measures;

}

# This will return the Ethnicity that will upated for all population then
sub getEthnicity {
  my ($self,$Ethnicity_ID) = @_;
  my $Ethnicity = '';

  if($Ethnicity_ID eq '2135-2') {
    $Ethnicity = 'Hisp_Lati';
  }
  if($Ethnicity_ID eq '2186-5') {
    $Ethnicity = 'Not_Hisp_Lati';
  }

  return($Ethnicity);
}


# This will return the Payer that will upated for all population then
sub getPayer {
  my ($self,$InsID) = @_;
  my $Payer = '';

  if ($InsID eq '100') {
    $Payer = 'Medicaid';
    $measures{'IPOP'}{'Payer'}{'Medicaid'} += 1;
  } elsif ($InsID eq '212') {
    $Payer = 'Medicare';
  } elsif ($self->in_array($InsID, ('129', '178', '203', '284', '317', '348', '355', '386', '396', '397', '401', '422'))) {
    $Payer = 'Private';
  } else {
    $Payer = 'Other';
  }

  return($Payer)
}

# This will return the Race that will upated for all population then
sub getRace {
  my ($self,$Race_ID) = @_;

  my $Race = '';

  if ($Race_ID eq '2054-5') {
    $Race = 'BLK_AFR_AME';
  } elsif ($Race_ID eq '2106-3') {
    $Race = 'WHITE';
  } elsif ($Race_ID eq '2028-9') {
    $Race = 'Asian';
  } elsif ($Race_ID eq '1002-5') {
    $Race = 'Americ_Indi';
  } elsif ($Race_ID eq '2076-8') {
    $Race = 'Native_Hawaiian';
  } else {
    $Race = 'BLK_AFR_AME';
  }

  return($Race)
}


sub in_array {
  my ($self,$value, @array) = @_;

  foreach my $arr_val (@array) {
    if($value eq $arr_val) {
      return(1);
    }
  }
  return(0);
}

sub checkDTap {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.ID = '20'
      AND cv.ShotNum > 3
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}

sub checkIPV {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.Descr = 'IPV'
      AND cv.ShotNum > 2
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}

sub checkMMR {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND ((xv.Descr = 'MMR'
      AND cv.ShotNum > 0) or xv.Descr IN ('measles', 'Mumps', 'rubella', 'rubella/mumps'))
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}

sub checkHiB {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.Descr LIKE '\%Hib\%'
      AND cv.ShotNum > 2
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}


sub checkHepB {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.Descr LIKE '\%Hep B\%'
      AND cv.ShotNum > 2
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}

sub checkvaricella {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.Descr = 'varicella'
      AND cv.ShotNum > 0
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}

sub checkPneumococcalVacc {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.ID = '133'
      AND cv.ShotNum > 3
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);

}
sub checkpHipA {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.ID = '169'
      AND cv.ShotNum > 0
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);
}

sub checkpRotaVirus {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT xv.Descr, cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    JOIN okmis_config.xVaccines xv ON cv.CVX = xv.ID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND xv.ID = '119'
      AND cv.ShotNum > 3
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);
}

sub checkpInfluenza {
  my ($self, $ClientID) = @_;

  # Numertor

  my $sNumertor = $dbh->prepare("
    SELECT cv.ShotNum
    FROM Client c
    JOIN ClientVaccines cv ON c.ClientID = cv.ClientID
    WHERE
      c.ClientID = $ClientID
      AND (TIMESTAMPDIFF(DAY, c.DOB, cv.VisitDate) >= 42 )
      AND (cv.CVX = '88' OR cv.CVX = '149')
    "
  );

  $sNumertor->execute();
  my $cnt = $sNumertor->rows;

  return 1 if($cnt > 0);
  return(0);
}

#############################################################################
1;