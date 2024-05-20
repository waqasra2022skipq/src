package gQRDAIIIXML;

use CGI::Carp qw(warningsToBrowser); 
use CGI::Carp qw(warningsToBrowser fatalsToBrowser); 

use DBI;
use DBForm;
use myDBI;
use DBA;
use DBUtil;
use XML::LibXSLT;
use XML::LibXML;
use QID_Measures;
use MgrTree;
binmode STDOUT, ":utf8";
my $debug = 1;
#############################################################################
# local gXML variable: access with $gXML::varname
#############################################################################

our $TOP_MEASUREID;
# input xml, output qrda (text)
sub styleQRDA
{
  my ($self,$form,$xmlfile) = @_;
  # first read and parse the file
  my $xmlpath = $form->{'DOCROOT'}.$xmlfile;
  my $docfile = '';
  # load_xml: initializes the parser and parse_file()
  eval { $docfile = XML::LibXML->load_xml(location => $xmlpath); };
  return('parse_error') if ( $@ );

  # initialize XSLT processor and read stylesheet
  my $xslt = XML::LibXSLT->new( );
  my $QRDAxsl = $form->{'DOCROOT'}.myConfig->cfgfile("QRDAIII_INDIV.xsl",1);
  my $stylesheet_qrda = $xslt->parse_stylesheet_file( $QRDAxsl );
  # next the generate/transform the QRDA file...
  my $qrdatrans = $stylesheet_qrda->transform( $docfile );
  my $qrdaout = $stylesheet_qrda->output_string( $qrdatrans );
  return($qrdaout);
}

sub setXML
{ 
  my ($self,$form,$ProvID,$TrID,$BDate,$EDate,$MEASUREID) = @_;

  $TOP_MEASUREID = $MEASUREID;
  warn qq|ProvID=${ProvID}\n| if ( $debug );
  warn qq|TrID=${TrID}\n| if ( $debug );
  warn qq|BDate=${BDate}\n| if ( $debug );
  warn qq|EDate=${EDate}\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

  $sProvider->execute($ProvID) || $form->dberror("setXML: select Provider ${ProvID}");
  my $rNoteProvider = $sProvider->fetchrow_hashref;
  
  my %measures = QID_Measures->getMeasures($form, $ProvID, $MEASUREID);


  # print qq|Content-type: text/html\n\n|;


  # foreach my $person (keys %measures) {
  #   print "<div>Person: $person\n";
  #   foreach my $attribute (keys %{$measures{$person}}) {
  #     print "<p>$attribute: $measures{$person}{$attribute}</p>";
  #   }
  #   print "</div>";
  # }
  # die();


  (my $today = $form->{'TODAY'}) =~ s/-//g;
  (my $now = substr($form->{'NOW'},0,5)) =~ s/://g;
  my $DOCID = $today.$now.'_'.DBUtil->genToken();
  my $DOCTYPE = 'QRDA';
  my $HEADER = qq|<QRDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <documentGeneratedDatetime>${today}${now}</documentGeneratedDatetime>
  <CQMNumber>$MEASUREID</CQMNumber>|;
  my $DOCCLOSE = qq|\n</${DOCTYPE}>|;

  # KLS documentGeneratedDatetime OK?

  my $ehrid = '78A150ED-B890-49dc-B716-5EC0027B3982';    # KLS ??
  my $xml = qq|${HEADER}
  <DocumentID>${DOCID}</DocumentID>
  <EHRName>Millennium Information Services</EHRName>
  <EHRID>${ehrid}</EHRID>|;

  $xml .= $self->setQRDA($form,$rNoteProvider,$BDate,$EDate, %measures);


  $xml .= $DOCCLOSE;
  $xml =~ s{$/$/}{$/}gs;            # remove blanks lines.

  my $str = '';
  foreach my $line ( split(/\n/,$xml) ) { $str .= $line . "\n" unless ( $line =~ m/></ ); }
  $xml = $str;
  return($xml);
}

sub setQRDA
{
  my ($self,$form,$rNoteProvider,$BDate,$EDate, %measures) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $NoteProvID = $rNoteProvider->{'ProvID'};
  warn qq|setQRDA: ProvID=${NoteProvID}\n| if ( $debug);

  my $out = '';

  $out .= $self->genProvider($form,$rNoteProvider);
  $out .= $self->genLegal($form,' ');
  $out .= $self->prepareMeasures($form,%measures);

  return($out);
}

sub prepareMeasures {
  my ($self,$form,%measures) = @_;

  
  my $ipop_measures = $self->prepare_ipop_measures(%measures);
  my $denom_measures = $self->prepare_denom_measures(%measures);
  my $numerator_measures = $self->prepare_numerator_measures(%measures);
  my $DENEXCEP_measures = $self->prepare_DENEXCEP_measures(%measures);


  my $ipop_two_measures;
  my $denom_two_measures;
  my $numerator_two_measures;

  my $ipop_three_measures;
  my $denom_three_measures;
  my $numerator_three_measures;
  my $numerator_three_measures;
  my $PFRATES;



  if($TOP_MEASUREID eq '138') {
    $ipop_two_measures = $self->prepare_ipop_two_measures(%measures);
    $denom_two_measures = $self->prepare_denom_two_measures(%measures);
    $numerator_two_measures = $self->prepare_numerator_two_measures(%measures);


    $ipop_three_measures = $self->prepare_ipop_three_measures(%measures);
    $denom_three_measures = $self->prepare_denom_three_measures(%measures);
    $numerator_three_measures = $self->prepare_numerator_three_measures(%measures);
  }

  if($TOP_MEASUREID eq '156') {
    $ipop_two_measures = $self->prepare_ipop_two_measures(%measures);
    $denom_two_measures = $self->prepare_denom_two_measures(%measures);
    $numerator_two_measures = $self->prepare_numerator_two_measures(%measures);

    $RATE_1 = $measures{'PFRATES'}{'RATE_1'}; 
    $RATE_2 = $measures{'PFRATES'}{'RATE_2'}; 
  }

  my $out = qq|
    <measures>
      
      ${ipop_measures}
      ${denom_measures}
      ${numerator_measures}
      ${DENEXCEP_measures}

      ${ipop_two_measures}
      ${denom_two_measures}
      ${numerator_two_measures}

      ${ipop_three_measures}
      ${denom_three_measures}
      ${numerator_three_measures}

      <PFRATES>
        <RATE_1>
          ${RATE_1}
        </RATE_1>
        <RATE_2>
          ${RATE_2}
        </RATE_2>
      </PFRATES>
    </measures>
  |;

  return($out);
}

sub prepare_ipop_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'IPOP'}{'pop_id'};


  my $IPOP_Count = $measures{'IPOP'}{'count'};

  my $IPOP_Count_M = $measures{'IPOP'}{'M'};
  my $IPOP_Count_F = $measures{'IPOP'}{'F'};

  my $Hisp_Lati = $measures{'IPOP'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'IPOP'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'IPOP'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'IPOP'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'IPOP'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'IPOP'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'IPOP'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'IPOP'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'IPOP'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'IPOP'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'IPOP'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'IPOP'}{'Payer'}{'Other'};

  my $out =qq|
    <IPOP>
      <count>${IPOP_Count}</count>
      <Gender>
        <male>${IPOP_Count_M}</male>
        <female>${IPOP_Count_F}</female>
      </Gender>
      <Ethnicity>
        <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
        <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
      </Ethnicity>
      <Race>
        <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
        <WHITE>${WHITE}</WHITE>
        <Asian>${Asian}</Asian>
        <Americ_Indi>${Americ_Indi}</Americ_Indi>
        <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
        <Other>${Other}</Other>
      </Race>
      <Payer>
        <Medicaid>${Medicaid}</Medicaid>
        <Medicare>${Medicare}</Medicare>
        <Private>${Private}</Private>
        <Payer_Other>${Payer_Other}</Payer_Other>
      </Payer>
      <pop_id>${pop_id}</pop_id>
    </IPOP>
  |;

  return($out);
}

sub prepare_ipop_two_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'IPOP_TWO'}{'pop_id'};


  my $IPOP_TWO_Count = $measures{'IPOP_TWO'}{'count'};

  my $IPOP_TWO_Count_M = $measures{'IPOP_TWO'}{'M'};
  my $IPOP_TWO_Count_F = $measures{'IPOP_TWO'}{'F'};

  my $Hisp_Lati = $measures{'IPOP_TWO'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'IPOP_TWO'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'IPOP_TWO'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'IPOP_TWO'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'IPOP_TWO'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'IPOP_TWO'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'IPOP_TWO'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'IPOP_TWO'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'IPOP_TWO'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'IPOP_TWO'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'IPOP_TWO'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'IPOP_TWO'}{'Payer'}{'Other'};

  my $out =qq|
    <IPOP_TWO>
      <count>${IPOP_TWO_Count}</count>
      <Gender>
        <male>${IPOP_TWO_Count_M}</male>
        <female>${IPOP_TWO_Count_F}</female>
      </Gender>
      <Ethnicity>
        <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
        <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
      </Ethnicity>
      <Race>
        <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
        <WHITE>${WHITE}</WHITE>
        <Asian>${Asian}</Asian>
        <Americ_Indi>${Americ_Indi}</Americ_Indi>
        <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
        <Other>${Other}</Other>
      </Race>
      <Payer>
        <Medicaid>${Medicaid}</Medicaid>
        <Medicare>${Medicare}</Medicare>
        <Private>${Private}</Private>
        <Payer_Other>${Payer_Other}</Payer_Other>
      </Payer>
      <pop_id>${pop_id}</pop_id>
    </IPOP_TWO>
  |;

  return($out);
}

sub prepare_ipop_three_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'IPOP_THREE'}{'pop_id'};


  my $IPOP_THREE_Count = $measures{'IPOP_THREE'}{'count'};

  my $IPOP_THREE_Count_M = $measures{'IPOP_THREE'}{'M'};
  my $IPOP_THREE_Count_F = $measures{'IPOP_THREE'}{'F'};

  my $Hisp_Lati = $measures{'IPOP_THREE'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'IPOP_THREE'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'IPOP_THREE'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'IPOP_THREE'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'IPOP_THREE'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'IPOP_THREE'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'IPOP_THREE'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'IPOP_THREE'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'IPOP_THREE'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'IPOP_THREE'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'IPOP_THREE'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'IPOP_THREE'}{'Payer'}{'Other'};

  my $out =qq|
    <IPOP_THREE>
      <count>${IPOP_THREE_Count}</count>
      <Gender>
        <male>${IPOP_THREE_Count_M}</male>
        <female>${IPOP_THREE_Count_F}</female>
      </Gender>
      <Ethnicity>
        <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
        <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
      </Ethnicity>
      <Race>
        <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
        <WHITE>${WHITE}</WHITE>
        <Asian>${Asian}</Asian>
        <Americ_Indi>${Americ_Indi}</Americ_Indi>
        <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
        <Other>${Other}</Other>
      </Race>
      <Payer>
        <Medicaid>${Medicaid}</Medicaid>
        <Medicare>${Medicare}</Medicare>
        <Private>${Private}</Private>
        <Payer_Other>${Payer_Other}</Payer_Other>
      </Payer>
      <pop_id>${pop_id}</pop_id>
    </IPOP_THREE>
  |;

  return($out);
}

sub prepare_denom_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'DENOM'}{'pop_id'};


  my $DENOM_Count = $measures{'DENOM'}{'count'};

  my $DENOM_Count_M = $measures{'DENOM'}{'M'};
  my $DENOM_Count_F = $measures{'DENOM'}{'F'};

  my $Hisp_Lati = $measures{'DENOM'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'DENOM'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'DENOM'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'DENOM'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'DENOM'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'DENOM'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'DENOM'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'DENOM'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'DENOM'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'DENOM'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'DENOM'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'DENOM'}{'Payer'}{'Other'};

  my $out =qq|
      <DENOM>
        <count>${DENOM_Count}</count>
        <Gender>
          <male>${DENOM_Count_M}</male>
          <female>${DENOM_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </DENOM>
  |;

  return($out);
}

sub prepare_numerator_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'NUMERATOR'}{'pop_id'};

  my $NUMERATOR_Count = $measures{'NUMERATOR'}{'count'};

  my $NUMERATOR_Count_M = $measures{'NUMERATOR'}{'M'};
  my $NUMERATOR_Count_F = $measures{'NUMERATOR'}{'F'};

  my $Hisp_Lati = $measures{'NUMERATOR'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'NUMERATOR'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'NUMERATOR'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'NUMERATOR'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'NUMERATOR'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'NUMERATOR'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'NUMERATOR'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'NUMERATOR'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'NUMERATOR'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'NUMERATOR'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'NUMERATOR'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'NUMERATOR'}{'Payer'}{'Other'};

  my $out =qq|
      <NUMERATOR>
        <count>${NUMERATOR_Count}</count>
        <Gender>
          <male>${NUMERATOR_Count_M}</male>
          <female>${NUMERATOR_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </NUMERATOR>
  |;

  return($out);
}

sub prepare_denom_two_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'DENOM_TWO'}{'pop_id'};

  my $DENOM_TWO_Count = $measures{'DENOM_TWO'}{'count'};

  my $DENOM_TWO_Count_M = $measures{'DENOM_TWO'}{'M'};
  my $DENOM_TWO_Count_F = $measures{'DENOM_TWO'}{'F'};

  my $Hisp_Lati = $measures{'DENOM_TWO'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'DENOM_TWO'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'DENOM_TWO'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'DENOM_TWO'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'DENOM_TWO'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'DENOM_TWO'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'DENOM_TWO'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'DENOM_TWO'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'DENOM_TWO'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'DENOM_TWO'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'DENOM_TWO'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'DENOM_TWO'}{'Payer'}{'Other'};

  my $out =qq|
      <DENOM_TWO>
        <count>${DENOM_TWO_Count}</count>
        <Gender>
          <male>${DENOM_TWO_Count_M}</male>
          <female>${DENOM_TWO_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </DENOM_TWO>
  |;

  return($out);
}

sub prepare_numerator_two_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'NUMERATOR_TWO'}{'pop_id'};

  my $NUMERATOR_TWO_Count = $measures{'NUMERATOR_TWO'}{'count'};

  my $NUMERATOR_TWO_Count_M = $measures{'NUMERATOR_TWO'}{'M'};
  my $NUMERATOR_TWO_Count_F = $measures{'NUMERATOR_TWO'}{'F'};

  my $Hisp_Lati = $measures{'NUMERATOR_TWO'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'NUMERATOR_TWO'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'NUMERATOR_TWO'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'NUMERATOR_TWO'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'NUMERATOR_TWO'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'NUMERATOR_TWO'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'NUMERATOR_TWO'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'NUMERATOR_TWO'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'NUMERATOR_TWO'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'NUMERATOR_TWO'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'NUMERATOR_TWO'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'NUMERATOR_TWO'}{'Payer'}{'Other'};

  my $out =qq|
      <NUMERATOR_TWO>
        <count>${NUMERATOR_TWO_Count}</count>
        <Gender>
          <male>${NUMERATOR_TWO_Count_M}</male>
          <female>${NUMERATOR_TWO_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </NUMERATOR_TWO>
  |;

  return($out);
}

sub prepare_denom_three_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'DENOM_THREE'}{'pop_id'};


  my $DENOM_THREE_Count = $measures{'DENOM_THREE'}{'count'};

  my $DENOM_THREE_Count_M = $measures{'DENOM_THREE'}{'M'};
  my $DENOM_THREE_Count_F = $measures{'DENOM_THREE'}{'F'};

  my $Hisp_Lati = $measures{'DENOM_THREE'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'DENOM_THREE'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'DENOM_THREE'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'DENOM_THREE'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'DENOM_THREE'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'DENOM_THREE'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'DENOM_THREE'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'DENOM_THREE'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'DENOM_THREE'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'DENOM_THREE'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'DENOM_THREE'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'DENOM_THREE'}{'Payer'}{'Other'};

  my $out =qq|
      <DENOM_THREE>
        <count>${DENOM_THREE_Count}</count>
        <Gender>
          <male>${DENOM_THREE_Count_M}</male>
          <female>${DENOM_THREE_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </DENOM_THREE>
  |;

  return($out);
}

sub prepare_numerator_three_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'NUMERATOR_THREE'}{'pop_id'};

  my $NUMERATOR_THREE_Count = $measures{'NUMERATOR_THREE'}{'count'};

  my $NUMERATOR_THREE_Count_M = $measures{'NUMERATOR_THREE'}{'M'};
  my $NUMERATOR_THREE_Count_F = $measures{'NUMERATOR_THREE'}{'F'};

  my $Hisp_Lati = $measures{'NUMERATOR_THREE'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'NUMERATOR_THREE'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'NUMERATOR_THREE'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'NUMERATOR_THREE'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'NUMERATOR_THREE'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'NUMERATOR_THREE'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'NUMERATOR_THREE'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'NUMERATOR_THREE'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'NUMERATOR_THREE'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'NUMERATOR_THREE'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'NUMERATOR_THREE'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'NUMERATOR_THREE'}{'Payer'}{'Other'};

  my $out =qq|
      <NUMERATOR_THREE>
        <count>${NUMERATOR_THREE_Count}</count>
        <Gender>
          <male>${NUMERATOR_THREE_Count_M}</male>
          <female>${NUMERATOR_THREE_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </NUMERATOR_THREE>
  |;

  return($out);
}

sub prepare_DENEXCEP_measures {
  my ($self, %measures) = @_;

  my $pop_id = $measures{'DENEXCEP'}{'pop_id'};

  my $DENEXCEP_Count = $measures{'DENEXCEP'}{'count'};

  my $DENEXCEP_Count_M = $measures{'DENEXCEP'}{'M'};
  my $DENEXCEP_Count_F = $measures{'DENEXCEP'}{'F'};

  my $Hisp_Lati = $measures{'DENEXCEP'}{'Ethnicity'}{'Hisp_Lati'};
  my $Not_Hisp_Lati = $measures{'DENEXCEP'}{'Ethnicity'}{'Not_Hisp_Lati'};


  # Set up Race
  my $BLK_AFR_AME     = $measures{'DENEXCEP'}{'Race'}{'BLK_AFR_AME'};
  my $WHITE           = $measures{'DENEXCEP'}{'Race'}{'WHITE'};
  my $Asian           = $measures{'DENEXCEP'}{'Race'}{'Asian'};
  my $Americ_Indi     = $measures{'DENEXCEP'}{'Race'}{'Americ_Indi'};
  my $Native_Hawaiian = $measures{'DENEXCEP'}{'Race'}{'Native_Hawaiian'};
  my $Other           = $measures{'DENEXCEP'}{'Race'}{'Other'};

  # Set up Payer
  my $Medicaid    = $measures{'DENEXCEP'}{'Payer'}{'Medicaid'};
  my $Medicare    = $measures{'DENEXCEP'}{'Payer'}{'Medicare'};
  my $Private     = $measures{'DENEXCEP'}{'Payer'}{'Private'};
  my $Payer_Other = $measures{'DENEXCEP'}{'Payer'}{'Other'};

  my $out =qq|
      <DENEXCEP>
        <count>${DENEXCEP_Count}</count>
        <Gender>
          <male>${DENEXCEP_Count_M}</male>
          <female>${DENEXCEP_Count_F}</female>
        </Gender>
        <Ethnicity>
          <Hisp_Lati>${Hisp_Lati}</Hisp_Lati>
          <Not_Hisp_Lati>${Not_Hisp_Lati}</Not_Hisp_Lati>
        </Ethnicity>
        <Race>
          <BLK_AFR_AME>${BLK_AFR_AME}</BLK_AFR_AME>
          <WHITE>${WHITE}</WHITE>
          <Asian>${Asian}</Asian>
          <Americ_Indi>${Americ_Indi}</Americ_Indi>
          <Native_Hawaiian>${Native_Hawaiian}</Native_Hawaiian>
          <Other>${Other}</Other>
        </Race>
        <Payer>
          <Medicaid>${Medicaid}</Medicaid>
          <Medicare>${Medicare}</Medicare>
          <Private>${Private}</Private>
          <Payer_Other>${Payer_Other}</Payer_Other>
        </Payer>
        <pop_id>${pop_id}</pop_id>
      </DENEXCEP>
  |;

  return($out);
}

sub genProvider
{
  my ($self,$form,$rProvider) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ProvID = $rProvider->{'ProvID'};
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=?");

  $sProviderControl->execute($ProvID) || $form->dberror("genProvider: select ProviderControl ${ProvID}");
  my $rProviderControl = $sProviderControl->fetchrow_hashref;
  $sProviderLicenses->execute($ProvID) || $form->dberror("genProvider: select ProviderLicenses ${ProvID}");
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;

  my $ClinicID = MgrTree->getClinic($form, $ProvID);

  $sProvider->execute($ClinicID) || $form->dberror("genProvider: select Clinic $ClinicID");
  my $rClinic = $sProvider->fetchrow_hashref;

  my $ClinicAddr = $rClinic->{'Addr1'};
  $ClinicAddr .= ', ' . $rClinic->{'Addr2'} if ( $rClinic->{'Addr2'} ne '' );
  my $ClinicPh = $rClinic->{'WkPh'} eq '' ? '' : 'tel: '.$rClinic->{'WkPh'};


  my $out = qq|
    <authorObj>
      <prefix>$rProvider->{'Prefix'}</prefix>
      <givenName>$rProvider->{'FName'}</givenName>
      <familyName>$rProvider->{'LName'}</familyName>
      <providerid>$rProvider->{'ProvID'}</providerid>
      <NPI>$rProviderControl->{NPI}</NPI>
    </authorObj>
    <custodianObj>
      <name>$rClinic->{'Name'}</name>
      <streetAddressLine>${ClinicAddr}</streetAddressLine>
      <city>$rClinic->{'City'}</city>
      <state>$rClinic->{'ST'}</state>
      <postalCode>$rClinic->{'Zip'}</postalCode>
      <country>US</country>
      <phone>${ClinicPh}</phone>
    </custodianObj>

  |;
  $sProvider->finish();
  $sProviderControl->finish();
  $sProviderLicenses->finish();
  return($out);
}

sub genLegal
{
  my ($self,$form,$spc) = @_;
  (my $today = $form->{'TODAY'}) =~ s/-//g;
  (my $now = substr($form->{'NOW'},0,5)) =~ s/://g;
  my $out = qq|
    ${spc}<legalObj>
    ${spc}  <time>${today}${now}</time>
    ${spc}  <streetAddressLine></streetAddressLine>
    ${spc}  <city></city>
    ${spc}  <state></state>
    ${spc}  <postalCode></postalCode>
    ${spc}  <country></country>
    ${spc}  <telecom></telecom>
    ${spc}  <assignedPerson_givenName></assignedPerson_givenName>
    ${spc}  <assignedPerson_familyName></assignedPerson_familyName>
    ${spc}  <representedOrganization_name></representedOrganization_name>
    ${spc}</legalObj>
  |;
  return($out);
}



#############################################################################
1;
