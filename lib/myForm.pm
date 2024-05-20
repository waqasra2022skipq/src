package myForm;

use myLogin;
use myDBI;
our $FORM;
my $SKIP;
require(myConfig->cfg('CFG').'/scripts.cfg');
############################################################################
sub new 
{

  my ($self,$in_string) = @_;
#warn qq|myForm: ENTER: new:\n|;
  $FORM = {};
  ##
  # parse is a routine that can be called separate.
  ##

  myForm->parse($in_string);

# foreach my $f ( sort keys %{$FORM} ) { warn qq|1 FORM: $f=$FORM->{$f}\n|; }
  ##
  # get the login information and set the Access
  ##

  ###if access token in param that means it is coming from office 365
  if( exists $FORM->{'code'} && $FORM->{'code'} !~ /^\s*$/ ) {
    #Generate Signature
    use LWP::UserAgent;
    use JSON;

    my $obj_useragent = LWP::UserAgent->new();   
    $obj_useragent->agent('Mozilla/5.0 [en] (Win98; U)');
    $obj_useragent->protocols_allowed( [ 'http', 'https']);

    my $token_url = 'https://login.microsoftonline.com/b717b7ec-b71d-460b-9c8a-a1b4d05dbbfb/oauth2/v2.0/token';
    
    my $params = {
        "client_id" => '90499e5d-418e-4a90-81a0-946f54a25199',
        "code"  => $FORM->{'code'},
        "redirect_uri" => "https://mms.okmms.com/cgi/bin/mis.cgi",
        "grant_type" => "authorization_code",
        "client_secret" => "uq9uJk4..-vC3-W2~6Kv54NZAUFePTNXB~"
      };

    $obj_useragent->default_header("content_type" => "application/x-www-form-urlencoded");
    my $response = $obj_useragent->post( $token_url, $params );
   
    my $resp_content = $response->decoded_content;
    if ( $resp_content ) {
      my $token_data = undef;
      eval {
        $token_data = from_json( $resp_content );
      };
      if ( exists $token_data->{'access_token'} && $token_data->{'access_token'} !~ /^\s*$/ ) {
        $obj_useragent->default_header('graph' => 'graph.microsoft.com');
        $obj_useragent->default_header('Authorization' => 'Bearer '.$token_data->{'access_token'});
        my $sso_guest_profile_url = 'https://graph.microsoft.com/v1.0/me';
        my $resp_content = undef;
        eval {
            my $response = $obj_useragent->get( $sso_guest_profile_url );

            $resp_content = $response->content;
            if ( $resp_content ) {
              my $office_user_data = undef;
              eval {
                $office_user_data = from_json( $resp_content );
              };

              if ( exists $office_user_data->{'userPrincipalName'} && $office_user_data->{'userPrincipalName'} !~ /^\s*$/ ) {
                ###code here further
                $FORM->{user} = $office_user_data->{'userPrincipalName'};
                $FORM->{email} = $office_user_data->{'userPrincipalName'};
                $FORM->{office_365_login} = 1;
              }
            }
        };
      }
    }
  }

#warn qq|WATCHLOGIN: USER=$FORM->{user}, $FORM->{pass}\n|;
  myLogin->chkLogin();
#warn qq|4. LOGINID=$FORM->{LOGINID}\n|;
#warn qq|4. LOGINPROVID=$FORM->{LOGINPROVID}\n|;
#warn qq|4. mlt=$FORM->{mlt}\n|;
#warn qq|4. Browser=$FORM->{Browser}\n|;
#warn qq|myForm: new: call=setUserLogin\n|;
  myForm->setUserLogin();
#foreach my $f ( sort keys %{$FORM} ) { warn qq|2 FORM: $f=$FORM->{$f}\n|; }
#warn qq|4. LOGINNAME=$FORM->{LOGINNAME}\n|;
#warn qq|4. LOGINUSERNAME=$FORM->{LOGINUSERNAME}\n|;
#warn qq|4. LOGINACLID=$FORM->{LOGINACLID}\n|;
#warn qq|4. LOGINTYPE=$FORM->{LOGINTYPE}\n|;
#warn qq|4. LOGINEMAIL=$FORM->{LOGINEMAIL}\n|;
#warn qq|4. LOGINAGENCY=$FORM->{LOGINAGENCY}\n|;
  myForm->saveHIST();
  ####################################
  # Now test for a data template file.
  # this file is used to pass data from one session to the next.
  ####################################
# test only  $FORM->{FORMID} = "12132";
  myForm->pushLINK($FORM->{pushID}) if ( $FORM->{pushID} );
  myForm->saveLINK('myForm',"$ENV{SCRIPT_NAME}?$ENV{QUERY_STRING}");
  myForm->TMPread();                  # read in the saved dataform from TMP file
#foreach my $f ( sort keys %{$FORM} ) { warn qq|FORM: $f=$FORM->{$f}\n|; }
#warn qq|myForm: DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\n|;
  return($FORM);
}
############################################################################
sub parse 
{
  my ($self,$in_string) = @_;
  $FORM = {};
#warn qq|myForm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, in_string=$in_string\n|;
#warn qq|myForm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, CONTENT_LENGTH=$ENV{CONTENT_LENGTH}\n|;
#warn qq|myForm: DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\n|;
  my ($query_string, @key_value_pairs, $key_value);
  my ($key_string, $key, $value);
  if ( $in_string )
  { $query_string = $in_string; } 
  elsif ( $ARGV[0] ) 
  { $query_string = join(' ',@ARGV); }
  elsif ( $ENV{'REQUEST_METHOD'} eq 'POST' )
  { read (STDIN, $query_string, $ENV{'CONTENT_LENGTH'}); }
  elsif ( $ENV{'REQUEST_METHOD'} eq 'GET' )
  { $query_string = $ENV{'QUERY_STRING'}; } 

  ####################################
  # Loop thru all the incoming parameters.
  ####################################
  $SKIP = ();
  $FORM->{query} = $query_string;
#warn qq|myForm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, query=$FORM->{query}\n|;
  @key_value_pairs = split(/&/, $query_string);
  foreach $key_value (@key_value_pairs)
  {
#warn qq|\nparse: key_value=${key_value}\n|;
    ($key_string, $value) = split(/=/, $key_value);
    $key_string = myForm->unescape($key_string);
#warn qq|parse: key_string=${key_string}\n|;
#warn qq|parse: value=${value}\n|;
  ####################################
  #   split multiple key/value pairs in one name.
  #   these are separated by a backslash (\)
  ####################################
    my @keys = split(/&/,$key_string);
#warn qq|parse: keys=@keys\n|;
    foreach $key ( @keys )
    {
      # true if name has an equal sign, then we ignore value
      # and use key=value in name
      if ( $key =~ /(.+?)=(.*)/ ) { $key = $1; $value = $2; }
      $value = myForm->unescape($value);
#warn qq|parse: key=${key}, value=${value}\n|;
      # remove...
      # below, !-~ is a range which matches all characters between ! and ~.
      #  The range is set between ! and ~ because these are the first and last characters
      #  in the ASCII table (Alt+033 for ! and Alt+126 for ~ in Windows).
      #  As this range does not include whitespace, \s is separately included.
      #  \t simply represents a tab character.
      #  \s is similar to \t but the metacharacter \s is a shorthand for a whole
      #  character class that matches any whitespace character.
      #  This includes space, tab, newline and carriage return.
      #  \375 (octal 375) or decimal 253 is my placeholder for multi-valued arguments
      $value =~ s/[^!-~\s\375]//g;
#warn qq|parse: now value=${value}\n|;
      if ( exists($FORM->{$key}) )
      { $FORM->{$key} .= chr(253) . $value; }
      else
      { $FORM->{$key} = $value; }
      $SKIP->{$key} = 1;
#warn qq|parse: $key=$FORM->{$key}\n|;
    }
  }
  $FORM->{'TODAY'} = DBUtil->Date();              # save date.
  my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime();
  my $hrs = length($hrs) == 2 ? $hrs : '0'.$hrs;
  my $min = length($min) == 2 ? $min : '0'.$min;
  my $sec = length($sec) == 2 ? $sec : '0'.$sec;
  $FORM->{'NOW'} = "${hrs}:${min}:${sec}";        # save time.
  $FORM->{LOGINID} = $ENV{HTTP_USER_AGENT} ? $FORM->{user} : getpwuid($>);
  myForm->getRoot();                       # set the root directory.
#warn qq|myForm-parse: return\n|;
  return($FORM);
}
############################################################################
sub unescape
{
  my ($self,$str) = @_;
  $str =~ tr/+/ /;
  $str =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack ("C", hex($1))/eg;
  # seen used ...
#  $str =~ s/%([0-9a-fA-Z]{2})/pack("c",hex($1))/eg;
  $str;
}
############################################################################
# VERY IMPORTANT - decides which database to update
#   based upon the HTML DOCUMENT_ROOT variable
#   for instance, 
#   for home directory /home/okmis/www/dev
#    then the SQL database named 'okmis_dev' is updated
############################################################################
sub getRoot 
{
  my ($self) = @_;

# check for root directory
#warn qq|ENTER getRoot: DBNAME=$FORM->{DBNAME}, DOC_ROOT=$ENV{DOCUMENT_ROOT},$FORM->{DOCROOT}\n|;
#foreach my $f ( sort keys %{$FORM} ) { warn qq|getRoot: $f=$FORM->{$f}\n|; }
#foreach $var (sort keys %ENV) { warn "$var=$ENV{$var}=\n"; }
  if ( $FORM->{DBNAME} )     # assume it is /home.../www
  {
    my ($p1,$p2) = split('_',$FORM->{'DBNAME'});
#warn qq|2: 1=${p1}, 2=${p2}, 3=${p3}, 4=${p4}, 5=${p5}, 6=${p6}\n|;
    $FORM->{DOCROOT} = qq|/home/${p1}/www/${p2}|;
    $FORM->{DOCPARENT} = qq|/home/${p1}/www/|;
  }
  elsif ( defined($ENV{DOCUMENT_ROOT}) )
  {
    $FORM->{DOCROOT} = $ENV{DOCUMENT_ROOT}; 
#warn qq|1: DOCROOT=$FORM->{DOCROOT}\n|;
    my ($parent,$dir) = $FORM->{DOCROOT} =~ m/(.*\/)(.*)$/;
    $FORM->{DOCPARENT} = $parent;
#warn qq|1: DOCPARENT=$FORM->{DOCPARENT}\n|;
    my ($p1,$p2,$p3,$p4,$p5,$p6) = split('/',$FORM->{'DOCROOT'});
#warn qq|1: 1=${p1}, 2=${p2}, 3=${p3}, 4=${p4}, 5=${p5}, 6=${p6}\n|;
    $FORM->{DBNAME} = $p3.'_'.$p5;
#warn qq|1: DBNAME=$FORM->{DBNAME}\n|;
  }
  else
  { warn qq|NO DB GIVEN!\n|; myDBI->dberror('NO DB GIVEN!'); }
#warn qq|set= DOCROOT=$FORM->{DOCROOT}=\n|;
#warn qq|set= DBNAME=$FORM->{DBNAME}=\n|;
  $FORM->{DOCBIN} = $FORM->{DOCROOT} . "/cgi/bin";
#warn qq|set= DOCROOT=$FORM->{DOCROOT}=\n|;
#warn qq|set= DBNAME=$FORM->{DBNAME}=\n|;
  if ( $ENV{SERVER_NAME} eq '' )     # this is for non-http logins.
  {
    my ($p1,$p2) = split('_',$FORM->{'DBNAME'});
    $FORM->{'HTTPSERVER'} = 'https://' . $p2 . '.' . $p1 . '.com';
  }
  else { $FORM->{HTTPSERVER} = qq|https://$ENV{SERVER_NAME}|; }
  return($FORM);
}
sub setUserLogin 
{
  my ($self) = @_;
  my ($DB,$ID) = split(':',$FORM->{'USERLOGINID'});
#if ( $DB eq 'okmis_dev' ) { foreach my $f ( sort keys %{$FORM} ) { warn qq|setUserLogin FORM: $f=$FORM->{$f}\n|; } }
#warn qq|setUserLogin: DB=${DB}, ID=${ID}\n| if ( $FORM->{LOGINUSERID} == 91 );
#warn qq|setUserLogin: DB=${DB}, ID=${ID}\n| if ( $DB eq 'okmis_dev' );
  my $dbh = myDBI->dbconnect($DB);
#warn qq|setUserLogin: USERLOGINID=$FORM->{USERLOGINID}\n|;
#warn qq|setUserLogin: DB=${DB}\n|;
#warn qq|setUserLogin: ID=${ID}\n|;
#warn qq|setUserLogin: LOGINTYPE=$FORM->{LOGINTYPE}\n| if ( $DB eq 'okmis_dev' );
  my $qUser = $FORM->{'LOGINTYPE'} == 0
            ? qq|select * from Provider where ProvID=?|
            : qq|select * from Client where ClientID=?|;
  my $sUser = $dbh->prepare($qUser);
#warn qq|setUserLogin: qUser=${qUser}\n| if ( $FORM->{LOGINUSERID} == 91 );
#warn qq|setUserLogin: qUser=${qUser}, LOGINUSERID=$FORM->{LOGINUSERID}\n| if ( $DB eq 'okmis_dev' );
#warn qq|setUserLogin: LOGINUSERID=$FORM->{LOGINUSERID}\n| if ( $DB eq 'okmis_dev' );
  $sUser->execute($FORM->{'LOGINUSERID'}) || myDBI->error("renewLogin: ${qUser} $FORM->{'LOGINUSERID'}");
#if ( $DB eq 'okmis_dev' ) { foreach my $f ( sort keys %{$FORM} ) { warn qq|setUserLogin FORM: $f=$FORM->{$f}\n|; } }
  if ( my $rUser = $sUser->fetchrow_hashref )
  {
#warn qq|setUserLogin: FOUND: FName=$rUser->{FName}\n| if ( $DB eq 'okmis_dev' );
    $FORM->{LOGINNAME} = $rUser->{'Name'};
    $FORM->{LOGINUSERNAME} = "$rUser->{'FName'} $rUser->{'LName'} $rUser->{'Suffix'}";
    $FORM->{LOGINACLID} = $rUser->{'ACLID'};
    $FORM->{LOGINUSERTYPE} = $rUser->{'Type'};
    $FORM->{LOGINEMAIL} = $rUser->{'Email'};
    $FORM->{LOGINAGENCY} = $FORM->{'LOGINTYPE'} == 0 ? MgrTree->getAgency($FORM,$FORM->{LOGINUSERID}) : '';
  }
#if ( $DB eq 'okmis_dev' ) { foreach my $f ( sort keys %{$FORM} ) { warn qq|setUserLogin FORM: $f=$FORM->{$f}\n|; } }
  $sUser->finish();
  return($FORM);
}
############################################################################
sub saveHIST
{
  my ($self) = @_;
  return(0) unless ( $ENV{HTTP_USER_AGENT} );                 # don't save telnet sessions.
#foreach my $f ( sort keys %{$FORM} ) { warn qq|saveHIST FORM: $f=$FORM->{$f}\n|; }
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
  my $pgm = $ENV{SCRIPT_NAME};
  my ($pgmname) = $pgm =~ /([^\/]+)\z/;
  my $str = myForm->unescape($FORM->{query});
  my $url = qq|${pgm}?${str}|;
#warn qq|saveHIST: pgm=${pgm}, pgmname=${pgmname}\n|;
#warn qq|saveHIST: str=${str}\n|;
#warn qq|saveHIST: url=${url}\n|;
  return(0) if ( $url =~ /=new/ );                            # don't save inputs.
  my $Key;
  my $Value;
  my $rest;
  if ( $str =~ /MIS_Action=ManagerTree/i ) { return(); }       # catch on next one.
  elsif ( $str =~ /MIS_Action=ChartList/i ) { return(); }      # catch on next one.
  elsif ( $str =~ /MIS_Action=MgrTree/i ) { return(); }        # catch on next one.
  elsif ( $str =~ /MIS_Action=ClientList/i ) { return(); }     # catch on next one.
  elsif ( $str =~ /MIS_Action=ClientPage/i ) { return(); }     # catch on next one.
  elsif ( $str =~ /MIS_Action=LoginScreen/i ) { return(); }    # catch on next one.
  elsif ( $str =~ /misPOP=1/i ) { return(); }                  # catch on next one.
  elsif ( $str =~ /misPOP=2/i ) { return(); }                  # catch on next one.
  elsif ( $str =~ /logout=1/i ) { return(); }                  # ignore
  elsif ( $str =~ /UpdateTables=/i ) { return(); }             # ignore
  elsif ( $str =~ /view=\w+Inp\.cgi/ ) { return(); }           # ignore
  elsif ( $str =~ /view=\w+Inp2\.cgi/ ) { return(); }          # ignore
  elsif ( $str =~ /view=Surveys.cgi/i ) { return(); }          # ignore
  elsif ( $str =~ /view=vSSN.cgi/i ) { return(); }             # catch on next one.
  elsif ( $pgm =~ /vClient.cgi/i ) { return(); }               # catch on next one.
  elsif ( $pgm =~ /Search.cgi/i ) { return(); }                # catch on next one.
  elsif ( $pgmname =~ /^Print/i ) { return(); }                # ignore print window
  elsif ( $pgm =~ /CFSPrint.cgi/i ) { return(); }              # ignore print window
  elsif ( $pgm =~ /printInvoice.cgi/i ) { return(); }          # ignore print window
  elsif ( $pgm =~ /authPA.cgi/i ) { return(); }                # ignore 
  elsif ( $pgm =~ /DMHws.pl/i ) { return(); }                  # ignore 
  elsif ( $pgm =~ /DMHcm.pl/i ) { return(); }                  # ignore 
  elsif ( $pgm =~ /Remit.cgi/i ) { return(); }                 # ignore
  elsif ( $pgm =~ /Reconcile.cgi/i ) { return(); }             # ignore
  elsif ( $pgm =~ /UserReports.cgi/i ) { return(); }           # ignore
  elsif ( $pgm =~ /GenReport.cgi/i ) { return(); }             # ignore
  elsif ( $pgm =~ /PAPeriods.cgi/i ) { return(); }             # ignore
  elsif ( $pgm =~ /genHCFA.cgi/i ) { return(); }               # ignore
  elsif ( $pgm =~ /Upload.cgi/i ) { return(); }                # ignore
  elsif ( $pgm =~ /markPaid.cgi/i ) { return(); }              # ignore
  elsif ( $pgm =~ /TPPG.cgi/i ) { return(); }                  # ignore
  elsif ( $pgm =~ /NewCrop.cgi/i ) { return(); }               # ignore
  elsif ( $str =~ /MIS_Action=Note/i ) { return(); }           # ignore
  elsif ( $str =~ /view=ClientHealthHistory.cgi/i ) { return(); }  # ignore
  elsif ( $str =~ /MIS_Action=ListFacilities/i ) { $Key = 'List Facilities'; }
  elsif ( $str =~ /view=vInsID.cgi/i ) { $str = 'view=Reconcile/Scholarship'; }
  elsif ( $pgm =~ /ManagerTree/i ) { $Key = 'Manager Tree'; }
  elsif ( $pgm =~ /ProviderPage.cgi/i ) { $Key = 'Provider Page'; }
  elsif ( $pgm =~ /ProviderList.cgi/i ) { $Key = 'Provider List'; }
  elsif ( $pgm =~ /ProviderMail.cgi/i ) { $Key = 'Provider Mail'; }
  elsif ( $pgm =~ /Privileges.cgi/i ) { $Key = 'Provider Privileges'; }
  elsif ( $pgm =~ /ClientPage.cgi/i ) { $Key = 'Client Page'; }
  elsif ( $pgm =~ /ClientPage2.cgi/i ) { $Key = 'Client Page'; }
  elsif ( $pgm =~ /ClientList.cgi/i ) { $Key = 'Client List'; }
  elsif ( $pgm =~ /ChartList.cgi/i ) { $Key = 'Chart List'; }
  elsif ( $pgm =~ /ClientAccess.cgi/i ) { $Key = 'Client Access Control'; }
  elsif ( $pgm =~ /ClientReview.cgi/i ) { $Key = 'Client Review'; }
  elsif ( $pgm =~ /ListSurveys.cgi/i ) { $Key = 'List Surveys'; }
  elsif ( $pgm =~ /ListAppointments.cgi/i ) { $Key = 'List Appointments'; }
  elsif ( $pgm =~ /ListInsPaid.cgi/i ) { $Key = 'List Insurance Payments'; }
  elsif ( $pgm =~ /ListJournal.cgi/i ) { $Key = 'Client Journal'; }
  elsif ( $pgm =~ /TimeClock.cgi/i ) { $Key = 'Clock In/Out'; }
  elsif ( $pgm =~ /ListFiles.cgi/i ) { $Key = 'List Files'; }
  elsif ( $pgm =~ /ElecList.cgi/i ) { $Key = 'Electronic Files List'; }
  @keypairs = split(/&/,$str);
  foreach $keyvalue (@keypairs)
  {
    my ($key,$value) = split(/=/,$keyvalue);
#warn qq|saveHIST: loop: key=$key, value=$value\n|;
    if ( $key eq 'view' ) { ($Key,$rest) = split('\.',$value); }
    elsif ( $key eq 'Treatment_TrID' ) { $Value = $value; }
    elsif ( $key eq 'ForTrID' ) { $Value = $value; }
    elsif ( $key eq 'Provider_ProvID' ) { $Value = $value; }
    elsif ( $key eq 'ProvID' ) { $Value = $value; }
    elsif ( $key eq 'ProviderID' ) { $Value = $value; }
    elsif ( $key eq 'ForProvID' ) { $Value = $value; }
    elsif ( $key eq 'Client_ClientID' ) { $Value = $value; }
    elsif ( $key eq 'ClientID' ) { $Value = $value; }
    elsif ( $key eq 'SearchString' ) { $Value = $value; }
    elsif ( $key eq 'ClientPrAuth_ID' ) { $Value = $value; }
    elsif ( $key eq 'Type' ) { $Value = $value; }
    last if ( $Value ne '' );
#warn qq|saveHIST: loop: Key=$Key, Value=$Value\n|;
  }
#warn qq|saveHIST: last: Key=$Key, Value=$Value\n|;
  return() if ( $Key eq '' );                  # ignore-could be just call to mis.cgi
  return() if ( $Value eq '' );                # ignore-like parse cmd in bin/gp6
  my $Key = $Key eq '' ? 'NULL' : $dbh->quote($Key);
  my $Value = $Value eq '' ? 'NULL' : $dbh->quote($Value);
  my $URL = $url eq '' ? 'NULL' : $dbh->quote($url);
  my $Token = $FORM->{mlt} eq '' ? 'NULL' : $dbh->quote($FORM->{mlt});
  my $q = qq|insert into History (ProvID,Name,Descr,Link,Token) values ($FORM->{LOGINPROVID},${Key},${Value},$URL,$Token)|;
#warn qq|saveHIST: mlt=$FORM->{mlt}\nq=\n$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
 my $NewID = $s->{mysql_insertid};
  $s->finish();
  return(1);
}
############################################################################
# CHECK FOR DATA SESSION TEMPLATE FILE
# Test for a data template file.
#   If we saved one when the HTML page/form was created/set,
#   read it and set the FORM associative array to keep them
#   with us for the next HTML page/form or UPDATE.
############################################################################
sub TMPread
{ 
  my ($self) = @_;
#warn qq|\n\nTMPread: CHECK SKIP:\n|;
#foreach my $f ( sort keys %{$SKIP} ) { warn qq|SKIP: $f=$SKIP->{$f}\n|; }
#warn qq|TMPread: FORMID: $FORM->{'FORMID'}\n|;
  if ( exists($FORM->{'FORMID'}) )
  {
    my $pathname = $FORM->{'DOCROOT'}.'/tmp/'.$FORM->{'LOGINID'}.'_'.$FORM->{'FORMID'};
#warn qq|TMPread: pathname: ${pathname}\n|;
    if ( open(TEMPLATE, $pathname) ) 
    {
      my $keyflag=1;
      while ( <TEMPLATE> )
      { 
        if ( $keyflag ) 
        { chomp($_); $key = $_; $keyflag = 0; $value = ''; }
        elsif ( $_ eq "<EOT>\n" ) 
        { 
          chomp($value); 
          # if FORM value is NULL then assign what was in the template
          # if it was not NULL then it was read from GET or POST.
          # this applies mostly to radio buttons and fields in submit buttons
#warn qq|TMPread: CHECK SKIP-${key} IF :$SKIP->{$key}:\n|;
          $FORM->{$key} = $value if ( !$SKIP->{$key} ); 
          $keyflag = 1; 
        }
        else { $value .= $_; }
      }
      close(TEMPLATE);
    }
  }
  return(1);
}
# need to retire this and $PROGS
sub genLINK                                  # used in saveLINK and mis.cgi MIS_Action
{
  my ($self,$pgm) = @_;
#warn qq|BEGIN: genLINK: pgm=${pgm}\n|;
  return('') unless ( $pgm );
#foreach my $f ( sort keys %PROGS ) { warn qq|genLINK: PROGS: $f=$PROGS{$f}\n|; }
  my $url = $PROGS{$pgm}{PATH}; my $a = '?';
  foreach my $f ( sort keys %{ $PROGS{$pgm}{'ARGS'} } )
  { next if ( $FORM->{$f} eq '' ); $url .= qq|${a}${f}=$FORM->{$f}|; $a = '&'; }
#warn qq|END: genLINK: url=${url}\n|;
  return($url);
}
sub readLINK                                 # used by saveLINK and popLINK
{
  my ($self,$id) = @_;
#warn qq|BEGIN: readLINK: id=${id}\n|;
  return('') unless ( $id );
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
  $q = qq|select ProvID,pgm,url,browser,ip from Links where ID='$id'|;
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  my ($ProvID,$pgm,$url,$browser,$ip) = $s->fetchrow_array;
  $s->finish();
#warn qq|END: readLINK: ($ProvID,$pgm,$url,$browser,$ip)\n|;
  return($ProvID,$pgm,$url,$browser,$ip);
}
# fwdTABLE is used when mis.cgi is called to have the next url to go to in Links.
sub saveLINK                                 # save on login new()
{
  my ($self,$pgm,$url) = @_;
#warn qq|BEGIN: saveLINK: pgm=${pgm}, url=${url}\n|;
  return(0) unless $ENV{HTTP_USER_AGENT};                 # don't save telnet sessions.
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
  my $pgm = $pgm eq '' ? 'NULL' : $dbh->quote($pgm);
  my $browser = $ENV{HTTP_USER_AGENT} ? $ENV{HTTP_USER_AGENT} : 'Telnet Session';
  ($FORM->{browser},$rest) = split(/ /,$browser);
  my $q = qq|insert into Links (ProvID,pgm,url,browser,ip) values ($FORM->{LOGINPROVID},$pgm,?,'$FORM->{browser}','$ENV{REMOTE_ADDR}')|;
  my $s = $dbh->prepare($q);
  my $newurl = $url;
  if ( $url eq '/cgi/bin/mis.cgi?' )
  {
    my ($ProvID,$p,$u,$b,$i) = myForm->readLINK($FORM->{LINKID});
    my $flg = $FORM->{UpdateTables} ? 'UPDATETABLES' : 'SKIP';
    $newurl = "$flg=" . substr($u,9);
    if ( $FORM->{fwdTABLE} )                              # save and switch to fwdTABLE
    { 
      $s->execute($newurl) || myDBI->dberror($q);
      $newurl = substr($url,0,index($url,'?')) . '?'
              . myForm->genLink($FORM->{fwdTABLE},$FORM->{view}) . "&mlt=$FORM->{mlt}&misLINKS=$FORM->{misLINKS}";
    }
  }
  elsif ( $url =~ /^\/cgi\/bin\/.*\.cgi\?$/ )             # only matters for a POST.
  {
    my ($dir,$pgm) = $url =~ m/(.*\/)(.*)\?$/;
    $newurl = myForm->genLINK($pgm);
    $newurl = $newurl eq '' ? $url : $newurl;
  }
  $s->execute($newurl) || myDBI->dberror($q);
 my $NEWID = $s->{'mysql_insertid'};
#warn qq|END saveLINK: NEWID=$NEWID, LINKID=$FORM->{LINKID}\n|;
  $FORM->{updLINKIDnew} = $FORM->{LINKID};
  $FORM->{LINKID} = $NEWID;
  $s->finish();
  return($NEWID);
}
sub pushLINK                                 # push onto misLINKS at new screen if pushID [usually setto LINKID] (not inputs)
{
  my ($self,$LINKID) = @_;
#warn qq|pushLINK BEGIN: inLINKID=$LINKID, LINKID=$FORM->{LINKID}, misLINKS=$FORM->{misLINKS}\n|;
  my $lid = $LINKID ? $LINKID : $FORM->{LINKID};
  if ( $lid )
  {
    if ( $FORM->{misLINKS} eq '' )
    { $FORM->{misLINKS} = $lid; }
    else
    {
      my @links = split(';',$FORM->{misLINKS});
      my $link = pop(@links);            # takes the last element out of the array.
      $FORM->{misLINKS} .= ';' . $lid unless ( $lid == $link );   # don't add twice in a row.
    }
  }
#warn qq|pushLINK END: lid=$lid, LINKID=$FORM->{LINKID}, misLINKS=$FORM->{misLINKS}\n|;
  return();
}
sub popLINK                                  # popLINK on Updates (or misPOP=1)
{
  my ($self,$exe) = @_;
  my $cnt = $exe eq '' ? 1 : $exe;
#warn qq|popLINK BEGIN: cnt=$cnt, misLINKS=$FORM->{misLINKS}, fwdLINK=$FORM->{fwdLINK}\n|;
  my ($ProvID,$pgm,$url,$vars,$browser,$ip) = ('','','','','','');
  if ( $FORM->{fwdLINK} eq '' )              # fwdLINK takes precedence.
  {
    my @links = split(';',$FORM->{misLINKS});
    # takes the last element out of the array.
    my $link = pop(@links); $cnt--;
#warn qq|myForm\n      popLINK: link=$link\n|;
    while ( $cnt > 0 ) { $link = pop(@links); $cnt--; }
#warn qq|myForm\n      popLINK: link=$link\n|;
    $FORM->{misLINKS} = join(';',@links);
    ($ProvID,$pgm,$url,$browser,$ip) = myForm->readLINK($link);
  }
  else { $url = $FORM->{fwdLINK}; }          # fwdLINK set.
  $url = qq|/cgi/bin/mis.cgi?MIS_Action=ManagerTree&mlt=$FORM->{mlt}&default=mgrtree| if ( $url eq '' );
#warn qq|popLINK END: misLINKS=$FORM->{misLINKS}, url=\n$url\n|;
  return($url);
}
sub updLINK                                  # update saved LINKs on insert xSQL (ID=new)
{
  my ($self,$lid,$old,$new) = @_;
##warn qq|myForm: BEGIN: updLINK: lik=${lid}\n|;
  return('') unless ( $lid );
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
  $q = qq|select ProvID,pgm,url,browser,ip from Links where ID='$lid'|;
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  my ($ProvID,$pgm,$url,$browser,$ip) = $s->fetchrow_array;
  $url =~ s/${old}/${new}/;
  my $u = $url eq '' ? 'NULL' : $dbh->quote($url);
  $q = qq|update Links set url=$u where ID='$lid'|;
#warn qq|updLINK: q=\n${q}\n|;
  $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  $s->finish();
#warn qq|myForm: END: updLINK ($ProvID,$pgm,$url,$browser,$ip)\n|;
  return($ProvID,$pgm,$url,$browser,$ip);
}
sub genLink                                  # used to advance to next HTML; Intake,PrAuth,ASAM
{
  my ($self,$inTable,$view,$id) = @_;
  return('') if ( $inTable eq '' );
  my $url;             # id could be 'new', value, or from form.
#warn qq|myForm: BEGIN: genLink: inTable=$inTable, view=$view, id=$id\n|;
#foreach my $f ( sort keys %{$FORM} ) { warn qq|myForm: genLink: FORM: $f=$FORM->{$f}\n|; }
  $url = "view=$view&fwdTABLE=$inTable&" unless ( $view eq '' );
  $url .= myForm->genLinkID($inTable,$id);
  my $hdrtable = $inTable;
  while ( defined(myConfig->tbl($hdrtable,'HEADERTABLE')) )
  { 
    $hdrtable = myConfig->tbl($hdrtable,'HEADERTABLE');
    $url .= '&' . myForm->genLinkID($hdrtable);
  }
#warn qq|myForm: END: genLink: url=$url\n|;
  return($url);
}
sub genLinkID                                # used by genLink, create a url from table and id
{
  my ($self,$table,$id) = @_;
  return('') if ( $table eq '' );
  my $url;
#warn qq|myForm: BEGIN: genLinkID: table=$table, id=$id\n|;
#foreach my $f ( sort keys %{$FORM} ) { warn qq|myForm: genLinkID: FORM: $f=$FORM->{$f}\n|; }
  my $ID = myDBI->getTableConfig($table,'RECID');
  my $key = qq|${table}_${ID}|;
  if ( $id eq '' )
  {
    my $fld = $FORM->{$key} eq '' ? "${table}_${ID}_1" : $key;
    my $val = $FORM->{$fld} eq '' ? myForm->genID($table) : $FORM->{$fld};
    $url = "${key}=${val}";
  }
  else { $url = "${key}=${id}"; }
#warn qq|myForm: END: genLinkID: url=$url\n|;
  return($url);
}
############################################################################
# this routine was created to make sure id is 'new' or some value.
# for use in going to next screen/record in series, w/o having the id yet.
# it will return first id found, if multiples, so not to be used where
#   multiple detail records exist for header record.
############################################################################
sub genID                                    # used by genLinkID
{
  my ($self,$table) = @_;
#warn qq|myForm: BEGIN: genID: table=$table\n|;
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
  my $HDRTABLE = myDBI->getTableConfig($table,'HEADERTABLE');
  return('') if ( $table eq '' || $HDRTABLE eq '' );
  my $HDRRECID = myDBI->getTableConfig($HDRTABLE,'RECID');
  my $HDRIDVAL = $FORM->{"${HDRTABLE}_${HDRRECID}"};
  my $DETID = myDBI->getTableConfig($table,'DETAILID');
  my $RECID = myDBI->getTableConfig($table,'RECID');
  my $q = qq|select ${RECID} from ${table} where ${DETID}='${HDRIDVAL}'|;
#warn qq|UPDATE genID=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  my ($rtnid) = $s->fetchrow_array;
  $s->finish();
#warn qq|myForm: END: genID: rtnid=$rtnid\n|;
  return($rtnid eq '' ? 'new' : $rtnid);
}
############################################################################
sub TBLread
{
  my ($self,$inTable) = @_;
#warn qq|myForm: BEGIN: TBLread: inTable=$inTable\n|;
  return() if ( $FORM->{"OPENTABLE:${inTable}"} );
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});

# Recursion to get Header tables read too.
  my $hdrtable = myDBI->getTableConfig($inTable,'HEADERTABLE');
  if ( $hdrtable ) { myForm->TBLread($hdrtable); }

  my $HDRID = myDBI->getTableConfig($hdrtable,'RECID');
  my $HDRIDval = $FORM->{"${hdrtable}_${HDRID}"};
  my $HDRIDval1 = $FORM->{"${hdrtable}_${HDRID}_1"};
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $IDval = $FORM->{"${inTable}_${ID}"};
  my $DETID = myDBI->getTableConfig($inTable,'DETAILID');
#warn qq|myForm: BEGIN: TBLread: inTable=$inTable, ID=$ID, IDval=$IDval, DETID=$DETID\n|;
#warn qq|myForm: BEGIN: TBLread: inTable=$inTable, hdrtable=$hdrtable, HDRIDval=$HDRIDval, HDRIDval1=$HDRIDval1\n|;
  if ( $IDval =~ /new/i )
  {
#warn qq|INSIDE: IDval matches 'new': inTable=${inTable},ID=${ID}\n|;
    myForm->setDefaults($inTable,$ID); 
  }
  elsif ($IDval ne '')
  {
#warn qq|INSIDE: IDval ne '': inTable=${inTable},ID=${ID},IDval=${IDval}\n|; 
    myForm->TBLselect($inTable,$ID,$IDval); 
  }
  elsif ( $HDRIDval =~ /new/i )
  {
#warn qq|INSIDE: HDRIDval matches 'new': inTable=${inTable}_ID=${ID} set to 'new'\n|;
    $FORM->{"${inTable}_${ID}"} = 'new';
    myForm->setDefaults($inTable,$ID); 
  }
  ####################################
  # this will select multiple records if HEADERID is not null, ie with ClientID=357
  #   to set a new detail record set IDval='new', ie ClientPrAuth_ID='new'
  ####################################
  elsif ($HDRIDval ne '')
  { 
#warn qq|INSIDE: HDRIDval ne '': inTable=$inTable, DETID=$DETID, HDRIDval=$HDRIDval\n|;
    myForm->TBLselect($inTable,$DETID,$HDRIDval);
    myForm->setDefaults($inTable,$ID) if ( $FORM->{"${inTable}_${ID}_1"} eq '' );
  }
  elsif ($HDRIDval1 ne '')
  { 
#warn qq|INSIDE: HDRIDval1 ne '': inTable=$inTable, DETID=$DETID, HDRIDval=$HDRIDval\n|;
    myForm->TBLselect($inTable,$DETID,$HDRIDval1);
    myForm->setDefaults($inTable,$ID) if ( $FORM->{"${inTable}_${ID}_1"} eq '' );
  }
#foreach my $f ( sort keys %{$FORM} ) { warn qq|FORM: $f=$FORM->{$f}\n|; }

  if ( $inTable eq 'Treatment' )
  {
    $FORM->{'BeginTime'} = DBUtil->AMPM($FORM->{'Treatment_ContLogBegTime_1'});
    $FORM->{'EndTime'} = DBUtil->AMPM($FORM->{'Treatment_ContLogEndTime_1'});
  }
  elsif ( $inTable eq 'Insurance' )
  {
    $s=$dbh->prepare("select * from xInsurance where ID=?");
    $s->execute($FORM->{'Insurance_InsID_1'});
    my $r = $s->fetchrow_hashref;
    $FORM->{'INSURANCE_TAG'} = $r->{Descr};
    $s->finish();
  }
  elsif ( $inTable eq 'PrAuthRVU' )
  {
    # set the PANum (in PrAuthRVU) if not set from main PAnumber.
    $FORM->{'PrAuthRVU_PANum_1'} = $FORM->{'PrAuth_PAnumber_1'} if ( $FORM->{'PrAuthRVU_PANum_1'} eq '' );
    $FORM->{'PrAuthRVU_EffDate_1'} = $FORM->{'PrAuth_EffDate_1'};
    $FORM->{'PrAuthRVU_ExpDate_1'} = $FORM->{'PrAuth_ExpDate_1'};
  }

  DBA->locked($FORM,$inTable);
  ####################################
  # and tell everyone the table is open.
  ####################################
  $FORM->{"OPENTABLE:${inTable}"} = 1;
  if ( $FORM->{'OPENTABLES'} ) { $FORM->{'OPENTABLES'} .= ',' . ${inTable}; }
  else { $FORM->{'OPENTABLES'} = ${inTable}; }
  return();
}
############################################################################
# These defaults are for 'new' records which are skipped in difFields.
#   caution: defaults can affect the outcome when difFields is called on update.
############################################################################
sub setDefaults
{
  my ($self,$inTable,$ID) = @_;
  my $dbh = myDBI->dbconnect($FORM->{'DBNAME'});
#warn qq|myForm: BEGIN: setDefaults: inTable=$inTable, ID=$ID\n|;
#foreach my $f ( sort keys %{$FORM} ) { warn qq|FORM: setDefaults: $f=$FORM->{$f}\n|; }

  if ( $inTable eq 'Provider' )
  {
    $FORM->{'Provider_Active_1'} = '1';
    $FORM->{'Provider_ST_1'} = 'OK';
    $FORM->{'Provider_Type_1'} = '4';                   # means Provider (Group=1,Agency=2,Clinic=3)
    $FORM->{'Provider_NoMail_1'} = 0;
  }
  elsif ( $inTable eq 'ProviderLicenses' )
  {
    $FORM->{'ProviderLicenses_State_1'} = 'OK';
  }
  elsif ( $inTable eq 'ProviderPrefs' )
  {
    $FORM->{'ProviderPrefs_TreeTabs_1'} = 0;
    $FORM->{'ProviderPrefs_ListClients_1'} = 0;
    $FORM->{'ProviderPrefs_MISEmails_1'} = 0;
  }
  elsif ( $inTable eq 'ProviderCreds' )
  {
    $FORM->{'ProviderCreds_License1ST_1'} = 'OK';
    $FORM->{'ProviderCreds_DEA1Type_1'} = 'DEA';
    $FORM->{'ProviderCreds_DEA2Type_1'} = 'DEA';
    $FORM->{'ProviderCreds_BNDDType_1'} = 'BNDD';
    $FORM->{'ProviderCreds_CDSType_1'} = 'CDS';
  }
  elsif ( $inTable eq 'ProviderPay' )
  {
    $FORM->{'ProviderPay_isMgr_1'} = '0';
  }
  elsif ( $inTable eq 'Credentials' )
  {
    $FORM->{'Credentials_Taxonomy_1'} ='101Y00000X';
  }
  elsif ( $inTable eq 'Client' )
  {
#warn qq|myForm: setDefaults: Client, ID=$FORM->{Client_ClientID_1}\n|;
    $FORM->{'Client_Active_1'} = '1';
    $FORM->{'Client_SSN_1'} = $FORM->{'SSN'};
    $FORM->{'Client_ST_1'} = 'OK';
    $FORM->{'Client_ProvID_1'} = $FORM->{'ProviderID'};
    $FORM->{'Client_clinicClinicID_1'} = MgrTree->getClinic($FORM,$FORM->{'LOGINPROVID'});
  }
  elsif ( $inTable eq 'ClientIntake' )
  {
    $FORM->{'ClientIntake_AbsentSchool_1'} = '0';       # 0 days
    $FORM->{'ClientIntake_SuspendedSchool_1'} = '0';    # 0 days
    $FORM->{'ClientIntake_AbsentDayCare_1'} = '0';      # 0 days
    $FORM->{'ClientIntake_SchoolLast3_1'} = '0';        # 0 = no
  }
  elsif ( $inTable eq 'ClientEmergency' )
  {
    # Do NOT Opt-Out of sending information if MMS, others Yes OptOut.
    my $OptOut = $FORM->{'DBNAME'} eq 'okmis_mms' ? 0 : 1;
    $FORM->{'ClientEmergency_MyHealth_1'} = $OptOut;
  }
  elsif ( $inTable eq 'Insurance' )
  {
    my $q = qq|select * from xInsurance where Descr LIKE '%medicaid%'|;
    my $s = $dbh->prepare($q);
    $s->execute || myDBI->dberror($q);
    if ( my $r = $s->fetchrow_hashref ) { $FORM->{'Insurance_InsID_1'} = $r->{ID}; }
    else { $FORM->{'Insurance_InsIDNum_1'} = $FORM->{'Client_SSN_1'}; }
    $FORM->{'Insurance_Priority_1'} = '1';
    $FORM->{'Insurance_InsNumEffDate_1'} = DBUtil->Date('today','fmt','YYYY-MM') . '-01';
    $FORM->{'Insurance_InsNumActive_1'} = '1';
    $FORM->{'Insurance_Deductible_1'} = '0';
    $FORM->{'Insurance_Copay_1'} = '0';
    $s->finish();
  }
  elsif ( $inTable eq 'ClientLegal' )
  {
    $FORM->{'ClientLegal_LegalStatus_1'} = '116';      # INFORMAL ADMISSION
  }
  elsif ( $inTable eq 'MedHx' )
  {
    $FORM->{'MedHx_AttSuicides_1'} = '0';               # 0 attempts
    $FORM->{'MedHx_FamilySuicideHx_1'} = '0';           # 0 = no
    $FORM->{'MedHx_Firearms_1'} = '0';                  # 0 = no
    $FORM->{'MedHx_RestrictivePlacement_1'} = '0';      # 0 days
    $FORM->{'MedHx_SelfHarm_1'} = '0';                  # 0 days
  }
  elsif ( $inTable eq 'ClientProblems' )
  {
    $FORM->{'ClientProblems_InitiatedDate_1'} = $FORM->{'TODAY'};
    $FORM->{'ClientProblems_Priority_1'} = 9999;
  }
  elsif ( $inTable eq 'ClientRelations' )
  {
    $FORM->{'ClientRelations_MarStat_1'} = 1;           # Never married
    $FORM->{'ClientRelations_ResNum_1'} = 0;
    $FORM->{'ClientRelations_HomelessLong_1'} = '0';    # 0 = no
    $FORM->{'ClientRelations_HomelessMany_1'} = '0';    # 0 = no
  }
  elsif ( $inTable eq 'ClientResources' )
  {
    $FORM->{'ClientResources_SelfHelp30_1'} = '0';      # 0 days
  }
  elsif ( $inTable eq 'ClientTrPlan' )
  {
    my $r = DBA->getLAST($FORM,'',$inTable,"where ClientTrPlan.ClientID='$FORM->{Client_ClientID_1}'"
                                          ,"order by ClientTrPlan.EffDate desc, ClientTrPlan.ExpDate desc");
    if ( $r )
    {
      myForm->setTable($inTable,$r);
#warn qq|myForm: setDefaults: ClientTrPlan: delete ${inTable}_${ID}_1=$FORM->{"${inTable}_${ID}_1"}\n|;
      delete $FORM->{"${inTable}_${ID}_1"};
      delete $FORM->{"${inTable}_CreateDate_1"};
      delete $FORM->{"${inTable}_CreateProvID_1"};
      delete $FORM->{"${inTable}_ChangeDate_1"};
      $FORM->{'ClientTrPlan_ClSigDate_1'} = '';
      $FORM->{'ClientTrPlan_PGSigDate_1'} = '';
      $FORM->{'ClientTrPlan_PhSigDate_1'} = '';
    }
    else
    {
      my $q = qq|select S1,S2,S3,S4,L1,L2,L3,L4,Prefs from ClientSummary where ClientID='$FORM->{Client_ClientID_1}'|;
#warn qq|myForm: setDefaults: ClientTrPlan: ClientID=$FORM->{Client_ClientID_1}\n${q}\n|;
      my $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($S1,$S2,$S3,$S4,$L1,$L2,$L3,$L4,$Prefs) = $s->fetchrow_array;
      $FORM->{'ClientTrPlan_SA1_1'} = $S1;
      $FORM->{'ClientTrPlan_SA2_1'} = $S2;
      $FORM->{'ClientTrPlan_SA3_1'} = $S3;
      $FORM->{'ClientTrPlan_SA4_1'} = $S4;
      $FORM->{'ClientTrPlan_L1_1'} = $L1;
      $FORM->{'ClientTrPlan_L2_1'} = $L2;
      $FORM->{'ClientTrPlan_L3_1'} = $L3;
      $FORM->{'ClientTrPlan_L4_1'} = $L4;
      $FORM->{'ClientTrPlan_Preferences_1'} = $Prefs;
      $s->finish();
      my $q = qq|select Problem,Summary,Services,Referrals from ClientIntake where ClientID='$FORM->{Client_ClientID_1}'|;
#warn qq|myForm: setDefaults: ClientTrPlan: ClientID=$FORM->{Client_ClientID_1}\n${q}\n|;
      my $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($Problem,$Summary,$Services,$Referrals) = $s->fetchrow_array;
      $FORM->{'ClientTrPlan_Comments_1'} = $Problem;
      $FORM->{'ClientTrPlan_Summary_1'} = $Summary;
      $FORM->{'ClientTrPlan_Services_1'} = $Services;
      $FORM->{'ClientTrPlan_ReferralsNPI_1'} = $Referrals;
      $s->finish();
    }
    $FORM->{'ClientTrPlan_EffDate_1'} = DBUtil->Date();
    $FORM->{'ClientTrPlan_ExpDate_1'} = DBUtil->Date('',6,-1);
    $FORM->{'ClientTrPlan_Locked_1'} = 0;
    $FORM->{'ClientTrPlan_CopyID_1'} = $r->{$ID};
#warn qq|myForm: setDefault:  ${inTable}: CopyID=$r->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientTrPlanPG' )
  {
    my $s = $dbh->prepare("select CopyID from ClientTrPlan where ID='$FORM->{'ClientTrPlan_ID_1'}'");
    $s->execute() || myDBI->dberror("setDefault: select ClientTrPlan CopyID");
    my ($PrevID) = $s->fetchrow_array;
    $s->finish();
#warn qq|myForm: setDefault:  ${inTable}: PrevID=${PrevID}, TrPlanID=$FORM->{'ClientTrPlan_ID_1'}\n|;
    my $s = $dbh->prepare("select count(*) from ClientTrPlanPG where TrPlanID='$FORM->{'ClientTrPlan_ID_1'}'");
    $s->execute() || myDBI->dberror("setDefault: select ClientTrPlanPG count");
    my ($cnt) = $s->fetchrow_array;
    $s->finish();
#warn qq|myForm: setDefault:  ${inTable}: cnt=${cnt}\n|;
    my ($rLast,$i) = ('',0);
    my $s = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID='$PrevID'");
    $s->execute() || myDBI->dberror("setDefault: select CLientTrPlanPG ${PrevID}");
    while ( my $r = $s->fetchrow_hashref ) { $i++; $rLast = $r if ( $cnt < $i ); last if ( $i == $cnt+1 ); }
    $s->finish();
    myForm->setTable($inTable,$rLast);
#warn qq|myForm: setDefault:  ${inTable}: i=${i}\n|;
    delete $FORM->{"${inTable}_${ID}_1"};
    delete $FORM->{"${inTable}_CreateDate_1"};
    delete $FORM->{"${inTable}_CreateProvID_1"};
    delete $FORM->{"${inTable}_ChangeDate_1"};
    delete $FORM->{"${inTable}_TrPlanID_1"};
    $FORM->{'ClientTrPlanPG_Priority_1'} = 9999;
    $FORM->{'ClientTrPlanPG_Locked_1'} = 0;
    $FORM->{'ClientTrPlanPG_CopyID_1'} = $rLast->{$ID};
#warn qq|myForm: setDefault:  ${inTable}: CopyID=$rLast->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientTrPlanOBJ' )
  {
    my $s = $dbh->prepare("select CopyID from ClientTrPlanPG where ID='$FORM->{'ClientTrPlanPG_ID_1'}'");
    $s->execute() || myDBI->dberror("setDefault: select ClientTrPlanPG CopyID");
    my ($PrevID) = $s->fetchrow_array;
    $s->finish();
#warn qq|myForm: setDefault:  ${inTable}: PrevID=${PrevID}, TrPlanPGID=$FORM->{'ClientTrPlanPG_ID_1'}\n|;
    my $s = $dbh->prepare("select count(*) from ClientTrPlanOBJ where TrPlanPGID='$FORM->{'ClientTrPlanPG_ID_1'}'");
    $s->execute() || myDBI->dberror("setDefault: select ClientTrPlanOBJ count");
    my ($cnt) = $s->fetchrow_array;
    $s->finish();
#warn qq|myForm: setDefault:  ${inTable}: cnt=${cnt}\n|;
    my ($rLast,$i) = ('',0);
    my $s = $dbh->prepare("select * from ClientTrPlanOBJ where TrPlanPGID='$PrevID' and ResolvedDate is null");
    $s->execute() || myDBI->dberror("setDefault: select CLientTrPlanOBJ ${PrevID}");
    while ( my $r = $s->fetchrow_hashref ) { $i++; $rLast = $r if ( $cnt < $i ); last if ( $i == $cnt+1 ); }
    $s->finish();
#warn qq|myForm: setDefault:  ${inTable}: i=${i}\n|;
    myForm->setTable($inTable,$rLast);
    delete $FORM->{"${inTable}_${ID}_1"};
    delete $FORM->{"${inTable}_TrPlanPGID_1"};
    delete $FORM->{"${inTable}_CreateDate_1"};
    delete $FORM->{"${inTable}_CreateProvID_1"};
    delete $FORM->{"${inTable}_ChangeDate_1"};
    $FORM->{'ClientTrPlanOBJ_InitiatedDate_1'} = DBUtil->Date();
    $FORM->{'ClientTrPlanOBJ_TargetDate_1'} = DBUtil->Date('',6,-1);
    $FORM->{'ClientTrPlanOBJ_Priority_1'} = 9999;
    $FORM->{'ClientTrPlanOBJ_Locked_1'} = 0;
    $FORM->{'ClientTrPlanOBJ_CopyID_1'} = $rLast->{$ID};
#warn qq|myForm: setDefault:  ${inTable}: CopyID=$rLast->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientPrAuth' )
  {
    my $ClientID = $FORM->{'Client_ClientID_1'};
#warn qq|myForm: setDefault: ClientPrAuth: ClientID=${ClientID}\n|;
    $FORM->{'ClientPrAuth_Type_1'} = $ClientID eq 'new' ? 'RI' : 'RE';
    $FORM->{'ClientPrAuth_ReqType_1'} = DBA->setPrAuthReqType($FORM,$ClientID);
    my ($isAdult,$TL) = TLevel->getTreatmentLevel($FORM,$ClientID,'18');
    $FORM->{'ClientPrAuth_TL_1'} = $TL;

    my $TDate = $FORM->{'ClientPrAuthCDC_TransDate_1'};
    $FORM->{'ClientPrAuth_EffDate_1'} = $TDate;
    my $InsID = $FORM->{'Insurance_InsID_1'};
    $PAgroup = CDC->calcPG($FORM,$ClientID,$InsID);
    my ($months,$days) = DBA->calcLOS($FORM,$InsID,$PAgroup);
    $FORM->{'ClientPrAuth_PAgroup_1'} = $PAgroup;
    $FORM->{'ClientPrAuth_ExpDate_1'} = DBUtil->Date($TDate,$months,$days);
    $FORM->{'ClientPrAuth_LOS_1'} = $months;
  }
  elsif ( $inTable eq 'PDDom' )
  {
    my $r = DBA->getLAST($FORM,'',$inTable,"where ClientPrAuth.ClientID='$FORM->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    if ( $r )
    {
      myForm->setTable($inTable,$r);
#warn qq|myForm: delete ${inTable}_${ID}_1=$FORM->{"${inTable}_${ID}_1"}\n|;
      delete $FORM->{"${inTable}_${ID}_1"};
      delete $FORM->{"${inTable}_RecDOLC_1"};
    }
  }
  elsif ( $inTable eq 'Appointments' )
  {
    $FORM->{'Appointments_ProvID_1'} = $FORM->{'LOGINPROVID'};
    $FORM->{'Appointments_ContactDate_1'} = DBUtil->Date();
    $FORM->{'Appointments_BeginTime_1'} = '09:00:00';
  }
  elsif ( $inTable eq 'Treatment' )
  {
    ####################################
    # Dont' allow updates of BillDate, COPLDate, RecDate, PaidDate, DenDate, DenCode
    #   leave them off any HTML page INPUT FORMs
    #   these are only updated in billing routines
    ####################################
    $FORM->{'Treatment_ChartEntryDate_1'} = DBUtil->Date();
    $FORM->{'Treatment_ClinicID_1'} = $FORM->{'Client_clinicClinicID_1'};
    $FORM->{'Treatment_ProvID_1'} = $FORM->{'LOGINPROVID'};
    $FORM->{'Treatment_EnteredBy_1'} = $FORM->{'LOGINPROVID'};
    $FORM->{'Treatment_POS_1'} = 3;                         # Place of Service = Doctor's Office
    $FORM->{'Treatment_BillStatus_1'} = 0;                  # Billed Status = new.
    $FORM->{'Treatment_StatusDate_1'} = $FORM->{TODAY};     # Billed Status = new date.
    $FORM->{'Treatment_RevStatus_1'} = 0;                   # ReviewedStatus = new.
    ####################################
#warn qq|myForm: setDefaults: Treatment: AppointmentID=$FORM->{'AppointmentID'}\n|;
#warn qq|myForm: setDefaults: Treatment: DupNote\n| if ( SysAccess->verify($FORM,'Privilege=DupNote') );
    if ( $FORM->{'AppointmentID'} )
    {
      $FORM->{'Treatment_ProvID_1'} = $FORM->{'AppointmentProvID'};
      $FORM->{'Treatment_ContLogDate_1'} = $FORM->{'AppointmentContactDate'};
      $FORM->{'Treatment_ContLogBegTime_1'} = $FORM->{'AppointmentBeginTime'};
    }
    elsif ( SysAccess->verify($FORM,'Privilege=DupNote') )
    {
      my $r = DBA->getLAST($FORM,'',$inTable,"where Treatment.ClientID='$FORM->{Client_ClientID_1}' and Treatment.ProvID='$FORM->{LOGINPROVID}' and Treatment.Type!=3","order by Treatment.ContLogDate desc");
      if ( $r )
      {
        #$FORM->{'Treatment_SCID_1'} = $r->{'SCID'};
        #$FORM->{'Treatment_ContLogBegTime_1'} = $r->{'ContLogBegTime'};
        #$FORM->{'Treatment_ContLogEndTime_1'} = $r->{'ContLogEndTime'};
        #$FORM->{'Treatment_POS_1'} = $r->{'POS'};
        $FORM->{'Treatment_ProbNum_1'} = $r->{'ProbNum'};
        $FORM->{'useTrID'} = $r->{'TrID'};
      }
    }
  }
  elsif ( $inTable eq 'ProgNotes' )
  {
#warn qq|myForm: setDefaults: ProgNotes: useTrID=$FORM->{'useTrID'}\n|;
    if ( $FORM->{'AppointmentID'} )
    {
      $FORM->{'ProgNotes_ProgEvidence_1'} = $FORM->{'AppointmentNotes'};
    }
    elsif ( $FORM->{'useTrID'} )
    {
      my $s = $dbh->prepare("select * from ProgNotes where NoteID='$FORM->{useTrID}'");
      $s->execute() || myDBI->dberror("setDef: useTrID=$FORM->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        myForm->setTable($inTable,$r);
#warn qq|myForm: setDefaults: delete ${inTable}_${ID}_1=$FORM->{"${inTable}_${ID}_1"}\n|;
        delete $FORM->{"${inTable}_${ID}_1"};
        delete $FORM->{"${inTable}_GrpSize_1"};
        delete $FORM->{"${inTable}_RecDOLC_1"};
      }
      $s->finish();
    }
  }
  elsif ( $inTable eq 'PhysNotes' )
  {
#warn qq|myForm: setDefaults: PhysNotes: useTrID=$FORM->{'useTrID'}\n|;
    my $ClientID = $FORM->{'Client_ClientID_1'};
    my ($h,$w) = ('','');
    if ( $FORM->{'useTrID'} )    # get them from last note.
    {
      my $s = $dbh->prepare("select * from PhysNotes where NoteID='$FORM->{useTrID}'");
      $s->execute() || myDBI->dberror("setDef: useTrID=$FORM->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        myForm->setTable($inTable,$r);
#warn qq|myForm: setDefaults: delete ${inTable}_${ID}_1=$FORM->{"${inTable}_${ID}_1"}\n|;
        delete $FORM->{"${inTable}_${ID}_1"};
        delete $FORM->{"${inTable}_RecDOLC_1"};
        $h = $r->{'Height'};
        $w = $r->{'Weight'};
#warn qq|myForm: setDefaults: useTrID: $FORM->{'useTrID'} h=${h}, w=${w}\n|;
      }
    }
    if ( $h eq '' || $w eq '' )       # get them from Intake
    {
#warn qq|myForm: setDefaults: are null: h=${h}, w=${w}\n|;
      my $s = $dbh->prepare("select * from Client where ClientID='${ClientID}'");
      $s->execute() || myDBI->dberror("setDef PhysNotes: ClientID=${ClientID}");
      my $r = $s->fetchrow_hashref;
      $h = $r->{'Height'} if ( $h eq '' );
      $w = $r->{'Weight'} if ( $w eq '' );
      $FORM->{'PhysNotes_Height_1'} = $h;
      $FORM->{'PhysNotes_Weight_1'} = $w;
      $s->finish();
    }
    (my $height = $h) =~ s/^\s*(.*?)\s*$/$1/g; $height =~ s/\'//; $height =~ s/\"//;
    my ($f,$i) = split(" ",$height);
    my $hi = ($f * 12) + $i;          # Height in inches.
#warn qq|myForm: setDefaults: PhysNotes: height=$h,$height,$f,$i,$hi; weight=$w\n|;
    $FORM->{'PhysNotes_BMI_1'} = $hi == 0 ? 0 : sprintf("%.2f",( $w / ( $hi * $hi ) ) * 703);
    my $r = DBA->getLAST($FORM,'','PDDiag',"where ClientPrAuth.ClientID='$FORM->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    $FORM->{'PhysNotes_Axis1ACode_1'} = $r->{'Axis1ACode'};
  }
  elsif ( $inTable eq 'ClientTherapyNotes' )
  {
#warn qq|myForm: setDefaults: ClientTherapyNotes: useTrID=$FORM->{'useTrID'}\n|;
    if ( $FORM->{'useTrID'} )
    {
      my $s = $dbh->prepare("select * from ClientTherapyNotes where NoteID='$FORM->{useTrID}'");
      $s->execute() || myDBI->dberror("setDef: useTrID=$FORM->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        myForm->setTable($inTable,$r);
#warn qq|myForm: setDefaults: delete ${inTable}_${ID}_1=$FORM->{"${inTable}_${ID}_1"}\n|;
        delete $FORM->{"${inTable}_${ID}_1"};
        delete $FORM->{"${inTable}_RecDOLC_1"};
      }
    }
  }
  elsif ( $inTable eq 'xSCRates' )
  {
    $FORM->{'xSCRates_RatePct_1'} = '1.00';
    $FORM->{'xSCRates_CommissionPct_1'} = '1.00';
    $FORM->{'xSCRates_RVUPct_1'} = '1.00';
  }
  elsif ( $inTable eq 'ClientDischarge' )
  {
    my $qClientIntake = qq|select * from ClientIntake where ClientID='$FORM->{Client_ClientID}'|;
    my $sClientIntake= $dbh->prepare($qClientIntake);
    $sClientIntake->execute() || myDBI->dberror($qClientIntake);
    my $rClientIntake = $sClientIntake->fetchrow_hashref;
    $FORM->{ClientDischarge_IntDate_1} = $rClientIntake->{IntDate};
    $FORM->{ClientDischarge_ServiceFocus_1} = $rClientIntake->{ServiceFocus};
    $FORM->{ClientDischarge_InitCond_1} = $rClientIntake->{Problem};
    $FORM->{ClientDischarge_IDNeeds_1} = DBA->getxref($FORM,'xProblems',$rClientIntake->{'Problem1'},'Descr');
    $FORM->{ClientDischarge_IDNeeds_1} .= "; ".DBA->getxref($FORM,'xProblems',$rClientIntake->{'Problem2'},'Descr') if ( $rClientIntake->{'Problem2'} ne '' );
    $FORM->{ClientDischarge_IDNeeds_1} .= "; ".DBA->getxref($FORM,'xProblems',$rClientIntake->{'Problem3'},'Descr') if ( $rClientIntake->{'Problem3'} ne '' );
    $sClientIntake->finish();
    my $rClientTrPlan = DBA->getLAST($FORM,'','ClientTrPlan',"where ClientTrPlan.ClientID='$FORM->{Client_ClientID_1}'","order by ClientTrPlan.EffDate desc, ClientTrPlan.ExpDate desc");
#warn qq|myForm: setDefaults: ClientID=$rClientTrPlan->{ClientID}, ID=$rClientTrPlan->{ID}\n|;
    $FORM->{'ClientDischarge_Needs_1'} = $rClientTrPlan->{'SA1'};
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA2'}| if ( $rClientTrPlan->{'SA2'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA3'}| if ( $rClientTrPlan->{'SA3'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA4'}| if ( $rClientTrPlan->{'SA4'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L1'}| if ( $rClientTrPlan->{'L1'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L2'}| if ( $rClientTrPlan->{'L2'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L3'}| if ( $rClientTrPlan->{'L3'} ne '' );
    $FORM->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L4'}| if ( $rClientTrPlan->{'L4'} ne '' );
    $FORM->{'ClientDischarge_DischargePlan_1'} = $rClientTrPlan->{'TransitionPlan'};
    my $sClientDevl= $dbh->prepare("select * from ClientDevl where ClientID=?");
    $sClientDevl->execute($FORM->{Client_ClientID}) 
         || myDBI->dberror("setDefault: ClientDischarge: select ClientDevl $FORM->{Client_ClientID}");
    my $rClientDevl = $sClientDevl->fetchrow_hashref;
    $FORM->{'ClientDischarge_Axis3ACode_1'} = $rClientDevl->{'Handicap1'};
    $FORM->{'ClientDischarge_Axis3BCode_1'} = $rClientDevl->{'Handicap2'};
    $FORM->{'ClientDischarge_Axis3CCode_1'} = $rClientDevl->{'Handicap3'};
    $FORM->{'ClientDischarge_Axis3DCode_1'} = $rClientDevl->{'Handicap4'};
    $sClientDevl->finish();
    my $sClientSocial= $dbh->prepare("select * from ClientSocial where ClientID=?");
    $sClientSocial->execute($FORM->{Client_ClientID}) 
         || myDBI->dberror("setDefault: ClientDischarge: select ClientSocial $FORM->{Client_ClientID}");
    my $rClientSocial = $sClientSocial->fetchrow_hashref;
    $FORM->{'ClientDischarge_Axis5Curr_1'} = $rClientSocial->{'Axis5Curr'};
    $sClientSocial->finish();
    my $rPDDom = DBA->getLAST($FORM,'','PDDom',"where ClientPrAuth.ClientID='$FORM->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    $FORM->{'ClientDischarge_Dom1Score_1'} = $rPDDom->{'Dom1Score'};
    $FORM->{'ClientDischarge_Dom2Score_1'} = $rPDDom->{'Dom2Score'};
    $FORM->{'ClientDischarge_Dom3Score_1'} = $rPDDom->{'Dom3Score'};
    $FORM->{'ClientDischarge_Dom4Score_1'} = $rPDDom->{'Dom4Score'};
    $FORM->{'ClientDischarge_Dom5Score_1'} = $rPDDom->{'Dom5Score'};
    $FORM->{'ClientDischarge_Dom6Score_1'} = $rPDDom->{'Dom6Score'};
    $FORM->{'ClientDischarge_Dom7Score_1'} = $rPDDom->{'Dom7Score'};
    $FORM->{'ClientDischarge_Dom8Score_1'} = $rPDDom->{'Dom8Score'};
    $FORM->{'ClientDischarge_Dom9Score_1'} = $rPDDom->{'Dom9Score'};
  }
  elsif ( $inTable eq 'SAbuse' )
  {
    $FORM->{'SAbuse_Freq_1'} = '1';
    $FORM->{'SAbuse_Priority_1'} = '9';
  }
  elsif ( $inTable eq 'ClientASI' )
  {
    my $ClientID = $FORM->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($FORM,$inTable,"G1=$ClientID","CreateDate desc");
      if ( $val )
      {
        myForm->TBLselect($inTable,$ID,$val);
        delete $FORM->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $multidel = chr(253);
      my $q = qq|select SSN,Gend,DOB,SUBSTRING_INDEX(Race,'${multidel}',1) as Race from Client where ClientID='$ClientID'|;
      utf8::upgrade($q); # UTF-8 fix for DBD::mysql

      my $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($SSN,$Gend,$DOB,$Race) = $s->fetchrow_array;
      $FORM->{'ClientASI_G2_1'} = $SSN;
      $FORM->{'ClientASI_G10_1'} = $Gend;
      $FORM->{'ClientASI_G16_1'} = $DOB;
      $FORM->{'ClientASI_G17_1'} = $Race;

      $q = qq|select StaffID from ClientIntake where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($StaffID) = $s->fetchrow_array;
      $FORM->{'ClientASI_G11_1'} = $StaffID;

      $q = qq|select OnPP from ClientLegal where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($OnPP) = $s->fetchrow_array;
      $FORM->{'ClientASI_L2_1'} = $OnPP;

      $q = qq|select MonthsTechEd from ClientEducation where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($MonthsTechEd) = $s->fetchrow_array;
      $FORM->{'ClientASI_E2_1'} = $MonthsTechEd;

      $q = qq|select HospOverNight from ClientHealth where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($HospOverNight) = $s->fetchrow_array;
      $FORM->{'ClientASI_M1_1'} = $HospOverNight;

      $q = qq|select AlcoholDTs from MedHx where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($AlcoholDTs) = $s->fetchrow_array;
      $FORM->{'ClientASI_D17_1'} = $AlcoholDTs;

      $q = qq|select WhoSpendTime,SatSpendTime,NumCloseFriends from ClientSocial where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($WhoSpendTime,$SatSpendTime,$NumCloseFrieds) = $s->fetchrow_array;
      $FORM->{'ClientASI_F9_1'} = $WhoSpendTime;
      $FORM->{'ClientASI_F10_1'} = $SatSpendTime;
      $FORM->{'ClientASI_F11_1'} = $NumCloseFriends;

      $q = qq|select MarStatY,MarStatM,ResAdmitDate,FamUsualLivArr,SatUsualLivArr from ClientRelations where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($MarStatY,$MarStatM,$ResAdmitDate,$FamUsualLivArr,$SatUsualLivArr) = $s->fetchrow_array;
      $FORM->{'ClientASI_F2Y_1'} = $MarStatY;
      $FORM->{'ClientASI_F2M_1'} = $MarStatM;
      $FORM->{'ClientASI_F4_1'} = $FamUsualLivArr;
      $FORM->{'ClientASI_F6_1'} = $SatUsualLivArr;
      $FORM->{'ClientASI_G4_1'} = $ResAdmitDate;

      $q = qq|select ValidDL,AutoForUse,RegSupport,MajSupport from ClientResources where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || myDBI->dberror($q);
      my ($ValidDL,$AutoForUse,$RegSupport,$MajSupport) = $s->fetchrow_array;
      $FORM->{'ClientASI_E4_1'} = $ValidDL;
      $FORM->{'ClientASI_E5_1'} = $AutoForUse;
      $FORM->{'ClientASI_E8_1'} = $RegSupport;
      $FORM->{'ClientASI_E9_1'} = $MajSupport;

      $s->finish();
    }
  }
  elsif ( $inTable eq 'ClientTASI' )
  {
    my $ClientID = $FORM->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($FORM,$inTable,"ClientID=$ClientID","AdmDate desc");
##$val=0;   ## don't know why asked to turn this off, now turn back on 07/11/2016
      if ( $val )
      {
        myForm->TBLselect($inTable,$ID,$val);
        delete $FORM->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $multidel = chr(253);
      my $q = qq|select Client.*,SUBSTRING_INDEX(Client.Race,'${multidel}',1) as Race,ClientSocial.ReligionName from Client left join ClientSocial on ClientSocial.ClientID=Client.ClientID where Client.ClientID=?|;
      my $s = $dbh->prepare($q);
      $s->execute($ClientID) || myDBI->dberror($q);
      my $r = $s->fetchrow_hashref;
      $FORM->{'ClientTASI_Name_1'} = qq|$r->{FName} $r->{LName}|;
      foreach my $f ( 'Addr1','Addr2','City','ST','Zip','DOB','Gend','Race' )
      { $FORM->{"ClientTASI_${f}_1"} = $r->{$f}; }
      $FORM->{'ClientTASI_AdmDate_1'} = $FORM->{TODAY};
      $FORM->{'ClientTASI_IntDate_1'} = $FORM->{TODAY};
      $FORM->{'ClientTASI_Class_1'} = 1;
      $FORM->{'ClientTASI_Contact_1'} = 1;
      $FORM->{'ClientTASI_StaffID_1'} = $r->{ProvID};
      $FORM->{'ClientTASI_Religion_1'} = $r->{ReligionName};
      $q = qq|select count(*) from ClientLegalHx where ClientID=? and OutCome='J'|;
      my $s = $dbh->prepare($q);
      $s->execute($ClientID) || myDBI->dberror($q);
      my ($Count) = $s->fetchrow_array;
      if ( $Count > 0 ) { $FORM->{'ClientTASI_ContEnvi_1'} = 'dc'; }
      $s->finish();
    }
  }
  elsif ( $inTable eq 'SOGS' || $inTable eq 'SOGSGSI' )
  {
    my $ClientID = $FORM->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($FORM,$inTable,"ClientID=$ClientID","TransDate desc");
      if ( $val )
      {
        myForm->TBLselect($inTable,$ID,$val);
        delete $FORM->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $p = $inTable.'_ProvID_1';
      $FORM->{$p} = $FORM->{LOGINPROVID};
      my $d = $inTable.'_TransDate_1';
      $FORM->{$d} = $FORM->{TODAY};
      $s->finish();
    }
  }
  elsif ( $inTable eq 'Contracts' )
  {
    #$FORM->{'Contracts_InsID_1'} = '100';              # Medicaid
    $FORM->{'Contracts_BillFlag_1'} = '1';              # Yes, Bill
    $FORM->{'Contracts_AutoReconcile_1'} = '0';
    $FORM->{'Contracts_AutoPay_1'} = '0';
    #$FORM->{'Contracts_PIN_1'} = '';                   # get PIN
    #$FORM->{'Contracts_RefID_1'} = '1D';               # Medicaid Provider Number for PIN
    $FORM->{'Contracts_Taxonomy_1'} = '261QM0801X';     # Mental Health including Community
    $FORM->{'Contracts_ServMeasure_1'} = 'UN';          # Units
    $FORM->{'Contracts_BillType_1'} = 'EL';             # Electronic
    $FORM->{'Contracts_UseAgency_1'} = '0';             # Not Agency Address - Clinic Address (Zip+4)
    $FORM->{'Contracts_ContractType_1'} = '09';         # Other
    #$FORM->{'Contracts_ContractCode_1'} = '';          # get for DMH
    #$FORM->{'Contracts_SourceCode_1'} = '';            # get for DMH
    $FORM->{'Contracts_UseReferring_1'} = '0';          # No
    $FORM->{'Contracts_UseRendering_1'} = '0';          # No
    $FORM->{'Contracts_UseSFacility_1'} = '0';          # No
    $FORM->{'Contracts_setContract_1'} = '0';           # No
    $FORM->{'Contracts_setPA_1'} = '0';                 # No
    $FORM->{'Contracts_setInsEFT_1'} = '0';             # No
    $FORM->{'Contracts_setBillEFT_1'} = '0';            # No
  }
  elsif ( $inTable eq 'ClientPrAuthCDC' )
  {
    my $ClientID = $FORM->{'Client_ClientID_1'};
#warn qq|myForm: setDefaults: ClientPrAuthCDC: ClientID=${ClientID}\n|;
#foreach my $f ( sort keys %{$FORM} ) { warn qq|FORM: $f=$FORM->{$f}\n|; }
    my $TransType = DBA->getPrAuthTrans($FORM,$ClientID);
    my ($TransDate,$TransTime) = DBA->getPrAuthTransDT($FORM,$ClientID,$FORM->{TODAY});
    $FORM->{'ClientPrAuthCDC_TransType_1'} = $TransType;
    $FORM->{'ClientPrAuthCDC_TransDate_1'} = $TransDate;
    $FORM->{'ClientPrAuthCDC_TransTime_1'} = $TransTime;
    $FORM->{'ClientPrAuthCDC_Status_1'} = 'New';
    $FORM->{'ClientPrAuthCDC_StatusDate_1'} = DBUtil->Date();
#   repeat from setDefaults->ClientPrAuth...
    $FORM->{'ClientPrAuth_EffDate_1'} = $TransDate;
    my $InsID = $FORM->{'Insurance_InsID_1'};
    $PAgroup = CDC->calcPG($FORM,$ClientID,$InsID);
    my ($months,$days) = DBA->calcLOS($FORM,$InsID,$PAgroup);
    $FORM->{'ClientPrAuth_PAgroup_1'} = $PAgroup;
    $FORM->{'ClientPrAuth_ExpDate_1'} = DBUtil->Date($TDate,$months,$days);
    $FORM->{'ClientPrAuth_LOS_1'} = $months;
#my $kkk = CDC->required($FORM,$FORM->{'Insurance_InsID_1'});
#warn qq|myForm: setDefaults: InsID=${'InsID'}, required=${kkk}\n|;
    $FORM->{'ClientPrAuthCDC_CDCOK_1'} = $ClientID eq 'new' ? 1 : CDC->required($FORM,$InsID) ? 0 : 1;
  }
  elsif ( $inTable eq 'ClientDischargeCDC' )
  {
    my $ClientID = $FORM->{'Client_ClientID_1'};
#warn qq|myForm: setDefaults: ClientDischargeCDC: ClientID=${ClientID}\n|;
    # as of last note...
    my $qTreatment = qq|select * from Treatment where ClientID='$FORM->{Client_ClientID}' order by ContLogDate desc|;
    my $sTreatment = $dbh->prepare($qTreatment);
    $sTreatment->execute() || myDBI->dberror($qTreatment);
    my $rTreatment = $sTreatment->fetchrow_hashref;
    $sTreatment->finish();
    $FORM->{'ClientDischargeCDC_TransDate_1'} = $rTreatment->{'ContLogDate'};
    $FORM->{'ClientDischargeCDC_TransTime_1'} = $rTreatment->{'ContLogBegTime'};
    $FORM->{'ClientDischargeCDC_TransType_1'} = '60';     # Discharge - Complete
    $FORM->{'ClientDischargeCDC_Status_1'} = 'New';
    $FORM->{'ClientDischargeCDC_StatusDate_1'} = DBUtil->Date();
    $FORM->{'ClientDischargeCDC_CDCOK_1'} = 0;
  }
  elsif ( $inTable eq 'ClientReferrals' )
  {
    $FORM->{'ClientReferrals_Employed_1'} = 0;
    $FORM->{'ClientReferrals_AutoAccident_1'} = 0;
    $FORM->{'ClientReferrals_AutoAccidentST_1'} = '';
    $FORM->{'ClientReferrals_OtherAccident_1'} = 0;
  }

  ####################################
  # set these defaults.
  ####################################
  my $TableFieldDefs = DBA->getFieldDefs($FORM,$inTable);
  my $fld = 'ClientID'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) && $FORM->{$key} eq '' )
  { $FORM->{$key} = $FORM->{Client_ClientID}; }
  my $fld = 'CreateProvID'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) ) { $FORM->{$key} = $FORM->{LOGINPROVID}; }
  my $fld = 'CreateDate'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) ) { $FORM->{$key} = $FORM->{TODAY}; }
#foreach my $f ( sort keys %{$FORM} ) { warn qq|FORM: $f=$FORM->{$f}\n|; }
  return(1); 
}
sub TBLselect
{
  my ($self,$inTable,$id,$val,$inorder) = @_;

  my $AccFunc = myDBI->getTableConfig($inTable,'ACCESS');
#warn "myForm: BEGIN: TBLselect: inTable=$inTable, id=$id, val=$val, AccFunc=$AccFunc\n";
  SysAccess->verify($FORM,$AccFunc) || myDBI->error("Access DENIED to ${inTable} (TBLselect)");

  my $DBCFGNAME = myDBI->getTableConfig($inTable,'DBCFGNAME');
  my $DBNAME = $DBCFGNAME eq '' ? $FORM->{'DBNAME'} : $DBCFGNAME;
#warn qq|TBLselect: inTable=$inTable, DBCFGNAME=${DBCFGNAME}, DBNAME=${DBNAME}\n|;
  my $dbh = myDBI->dbconnect($DBNAME);
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $order = $inorder eq '' ? qq|order by ${ID} desc| : $inorder;
  my $q = qq|select * from ${inTable} where ${id}='${val}' $order|;
  my $s = $dbh->prepare($q);
#warn qq|myForm: TBLselect: q=$q\n|;
  $s->execute || myDBI->dberror($q);
  my $idx = 0;
  $FORM->{"${inTable}_${id}_1"} = ${val};
  while ( my $r = $s->fetchrow_hashref )
  { $idx++; 
#    map { $FORM->{"${inTable}_${_}_${idx}"} = $r->{${_}} } keys %$r;
    foreach my $f ( keys %{ $r } ) 
    { $key = ${inTable} . "_" . ${f} . "_" . ${idx};
#warn qq|myForm: TBLselect: $f=$r->{$f}\n|;
      $FORM->{$key} = $r->{$f};
      $FORM->{$key} = '' if ( $f =~ /date/i && $FORM->{$key} eq '0000-00-00' );
#warn qq|myForm: TBLselect: $key=$FORM->{$key}\n|;
    }
  }
  $s->finish();
  return(1);
}
sub setTable
{
  my ($self,$inTable,$record,$idx) = @_;
  $i = $idx ? $idx : 1;
  foreach my $f ( keys %{ $record } )
  {
    my $key = ${inTable} . "_" . ${f} . "_" . ${i};
    $FORM->{$key} = $record->{$f};
#warn qq|setTable: ${key}=$FORM->{$key}\n|;
  }
  return(1);
}
############################################################################
1;
