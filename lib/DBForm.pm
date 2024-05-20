package DBForm;
use CGI qw(:standard escape);
use login;
use myConfig;
use myTables;
use myForm;
use myDBI;
use MgrTree;
use SysAccess;
use DBUtil;
use DBA;
use gHTML;
use PostUpd;
use PopUp;
use CDC;
use Cwd;
use NewCrop;
use uCalc;
use uHTML;
my $DEBUG=0;
############################################################################
sub new 
{
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my $InString = shift;
  my $self = {};
  bless $self, $class;
warn qq|DBForm: new: WARN-DBFORM\n| if ( $DEBUG );
  ##
  # parse is a routine that can be called separate.
  ##
  $self = $self->parse($InString);
  ##
  # get the login information and set the Access
  ##
#warn qq|ENTER new: dbhname=$dbhname\n|;
#warn qq|WATCHLOGIN: USER=$self->{user}, $self->{pass}\n|;
  $self = login->chkLogin($self);
#warn qq|4. LOGINID=$self->{LOGINID}\n|;
#warn qq|4. LOGINPROVID=$self->{LOGINPROVID}\n|;
#warn qq|4. mlt=$self->{mlt}\n|;
#warn qq|4. Browser=$self->{Browser}\n|;
  $self->setUserLogin();
#warn qq|4. LOGINNAME=$self->{LOGINNAME}\n|;
#warn qq|4. LOGINUSERNAME=$self->{LOGINUSERNAME}\n|;
#warn qq|4. LOGINACLID=$self->{LOGINACLID}\n|;
#warn qq|4. LOGINTYPE=$self->{LOGINTYPE}\n|;
#warn qq|4. LOGINEMAIL=$self->{LOGINEMAIL}\n|;
#warn qq|4. LOGINAGENCY=$self->{LOGINAGENCY}\n|;
  $self->saveHIST();
  ####################################
  # Now test for a data template file.
  # this file is used to pass data from one session to the next.
  ####################################
# test only  $self->{FORMID} = "12132";
#warn qq|\n\nnew CHECK skip:\n|;
#foreach my $f ( sort keys %{$skip} ) { warn qq|DBForm: new skip: $f=$skip->{$f}\n|; }
  $self->TMPread($skip);
  $self->pushLINK($self->{pushID}) if ( $self->{pushID} );
  $self->saveLINK('DBForm',"$ENV{SCRIPT_NAME}?$ENV{QUERY_STRING}");
#foreach my $f ( sort keys %{$self} ) { warn qq|self: $f=$self->{$f}\n|; }
#foreach my $f ( sort keys %ENV ) { warn qq|ENV: $f=$ENV{$f}\n|; }
#warn qq|DBForm: DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\n|;
  return($self);
}
############################################################################
sub parse 
{
  my $proto = shift;
  my $class = ref($proto) || $proto;
  my $InString = shift;
  my $self = {};
  bless $self, $class;

warn qq|DBForm: parse: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|DBForm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, InString=$InString\n|;
#warn qq|DBForm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, CONTENT_LENGTH=$ENV{CONTENT_LENGTH}\n|;
#foreach my $f ( sort keys %ENV ) { warn qq|parse: ENV: $f=$ENV{$f}\n|; }
#warn qq|DBForm: DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\n|;
  my ($query_string, @key_value_pairs, $key_value);
  my ($key_string, $key, $value);
  if ( $InString )
  { $query_string = $InString; } 
  elsif ( $ARGV[0] ) 
  { $query_string = join(' ',@ARGV); }
  elsif ( $ENV{'REQUEST_METHOD'} eq 'POST' )
  { read (STDIN, $query_string, $ENV{'CONTENT_LENGTH'}); }
  elsif ( $ENV{'REQUEST_METHOD'} eq 'GET' )
  { $query_string = $ENV{'QUERY_STRING'}; } 

  ####################################
  # Loop thru all the incoming parameters.
  ####################################
  my %skip = ();
#foreach my $f ( sort keys %{$skip} ) { warn qq|DBForm: parse skip: $f=$skip->{$f}\n|; }
  $self->{query} = $query_string;
#warn qq|DBForm.pm-parse: REQUEST_METHOD=$ENV{REQUEST_METHOD}, query=$self->{query}\n|;
  @key_value_pairs = split(/&/, $query_string);
  foreach $key_value (@key_value_pairs)
  {
#warn qq|\nparse: key_value=${key_value}\n|;
    ($key_string, $value) = split(/=/, $key_value);
    $key_string = $self->unescape($key_string);
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
      $value = $self->unescape($value);
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
      if ( exists($self->{$key}) )
      { $self->{$key} .= chr(253) . $value; }
      else
      { $self->{$key} = $value; }
      $skip->{$key} = 1;
#warn qq|DBForm parse: skip-$key=$skip->{$key}\n|;
#warn qq|DBForm parse: $key=$self->{$key}\n|;
    }
  }
  $self->{'TODAY'} = DBUtil->Date();              # save date.
  my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime();
  my $hrs = length($hrs) == 2 ? $hrs : '0'.$hrs;
  my $min = length($min) == 2 ? $min : '0'.$min;
  my $sec = length($sec) == 2 ? $sec : '0'.$sec;
  $self->{'NOW'} = "${hrs}:${min}:${sec}";        # save time.
  $self->{LOGINID} = $ENV{HTTP_USER_AGENT} ? $self->{user} : getpwuid($>);
  $self->getRoot();                       # set the root directory.
#warn qq|DBForm.pm-parse: return\n|;
  return($self);
}
############################################################################
sub unescape
{
  my ($self, $str) = @_;
warn qq|DBForm: unescape: WARN-DBFORM\n| if ( $DEBUG );
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
warn qq|DBForm: getRoot: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|ENTER set= DBNAME=$self->{DBNAME}, DOC_ROOT=$ENV{DOCUMENT_ROOT},$self->{DOCROOT}\n|;
#foreach my $f ( sort keys %{$self} ) { warn qq|getRoot: $f=$self->{$f}\n|; }
#foreach $var (sort keys %ENV) { warn "$var=$ENV{$var}=\n"; }
  if ( defined($ENV{DOCUMENT_ROOT}) )
  {
    $self->{DOCROOT} = $ENV{DOCUMENT_ROOT}; 
#warn qq|1: DOCROOT=$self->{DOCROOT}\n|;
    my ($parent,$dir) = $self->{DOCROOT} =~ m/(.*\/)(.*)$/;
    $self->{DOCPARENT} = $parent;
#warn qq|1: DOCPARENT=$self->{DOCPARENT}\n|;
    my ($p1,$p2,$p3,$p4,$p5,$p6) = split('/',$self->{'DOCROOT'});
#warn qq|1: 1=${p1}, 2=${p2}, 3=${p3}, 4=${p4}, 5=${p5}, 6=${p6}\n|;
    $self->{DBNAME} = $p3.'_'.$p5;
#warn qq|1: DBNAME=$self->{DBNAME}\n|;
  }
  elsif ( $self->{DBNAME} )     # assume it is /home.../www
  {
    my ($p1,$p2) = split('_',$self->{'DBNAME'});
#warn qq|2: 1=${p1}, 2=${p2}, 3=${p3}, 4=${p4}, 5=${p5}, 6=${p6}\n|;
    $self->{DOCROOT} = qq|/home/${p1}/www/${p2}|;
    $self->{DOCPARENT} = qq|/home/${p1}/www/|;
  }
  else
  { warn qq|NO DB GIVEN!\n|; $self->dberror('NO DB GIVEN!'); }
#warn qq|set= DOCROOT=$self->{DOCROOT}=\n|;
#warn qq|set= DBNAME=$self->{DBNAME}=\n|;
  $self->{DOCBIN} = $self->{DOCROOT} . "/cgi/bin";
#warn qq|set= DOCROOT=$self->{DOCROOT}=\n|;
#warn qq|set= DBNAME=$self->{DBNAME}=\n|;
  if ( $ENV{SERVER_NAME} eq '' )     # this is for non-http logins.
  {
    my ($p1,$p2) = split('_',$self->{'DBNAME'});
    $self->{'HTTPSERVER'} = 'https://' . $p2 . '.' . $p1 . '.com';
  }
  else { $self->{HTTPSERVER} = qq|https://$ENV{SERVER_NAME}|; }
  return $self;
}
sub setUserLogin 
{
  my ($self) = @_;
warn qq|DBForm: setUserLogin: WARN-DBFORM\n| if ( $DEBUG );
  #my $dbh = $self->dbconnect();
  my ($DB,$ID) = split(':',$self->{'USERLOGINID'});
#warn qq|\nsetUserLogin: DB=${DB}, ID=${ID}\n| if ( $self->{LOGINUSERID} == 91 );
#warn qq|\nsetUserLogin: DB=${DB}, ID=${ID}\n| if ( $DB eq 'okmis_demo' );
  my $dbh = myDBI->dbconnect($DB);
  my $qUser = $self->{'LOGINTYPE'} == 0
            ? qq|select * from Provider where ProvID=?|
            : qq|select * from Client where ClientID=?|;
  my $sUser = $dbh->prepare($qUser);
#warn qq|setUserLogin: qUser=${qUser}\n| if ( $self->{LOGINUSERID} == 91 );
#warn qq|setUserLogin: qUser=${qUser}, LOGINUSERID=$self->{LOGINUSERID}\n| if ( $DB eq 'okmis_demo' );
  $sUser->execute($self->{'LOGINUSERID'}) || $self->error("renewLogin: ${qUser} $self->{'LOGINUSERID'}");
#foreach my $f ( sort keys %{$self} ) { warn qq|setUserLogin: $f=$self->{$f}\n|; }
  if ( my $rUser = $sUser->fetchrow_hashref )
  {
#warn qq|setUserLogin: FOUND: FName=$rUser->{FName}\n| if ( $DB eq 'okmis_demo' );
    $self->{LOGINNAME} = $rUser->{'Name'};
    $self->{LOGINUSERNAME} = "$rUser->{'FName'} $rUser->{'LName'} $rUser->{'Suffix'}";
    $self->{LOGINACLID} = $rUser->{'ACLID'};
    $self->{LOGINUSERTYPE} = $rUser->{'Type'};
    $self->{LOGINEMAIL} = $rUser->{'Email'};
    $self->{LOGINAGENCY} = $self->{'LOGINTYPE'} == 0 ? MgrTree->getAgency($self,$self->{LOGINUSERID}) : '';
  }
#warn qq|setUserLogin: END: LOGINUSERNAME=$self->{LOGINUSERNAME}\n| if ( $DB eq 'okmis_demo' );
#  my $kls = myDBI->dbconnect($DB);
#  $sUser = $kls->prepare('select * from Provider where ProvID=?');
#  $sUser->execute('101') || $self->error("renewLogin: ${qUser} $self->{'LOGINUSERID'}");
#warn qq|LOOKAT: sUser\n|;
#my $rUser = $sUser->fetchrow_hashref;
#foreach my $f ( sort keys %{$rUser} ) { warn qq|setUserLogin: rUser: $f=$rUser->{$f}\n|; }
  $sUser->finish();
  #$dbh->disconnect();
  return($self);
}
sub setURL
{
  my ($self, $URL) = @_;

warn qq|DBForm: setURL: WARN-DBFORM\n| if ( $DEBUG );
  return('') if ( ${URL} eq '' );

  if ( $URL =~ /mlt=/ )
  {
    $URL .= '&' if ( $URL =~ /[&]/ );
    $URL =~ s/([?&])mlt=(.+?)([&])/$1mlt=$self->{mlt}$3/x;
  }
  elsif ( $URL =~ /[?]/ )
  { $URL .= qq|&mlt=$self->{mlt}|; }
  else
  { $URL .= qq|?mlt=$self->{mlt}|; }
  return($URL);
}
sub getIDX()
{
  my ($self,$Type) = @_;
warn qq|DBForm: getIDX: WARN-DBFORM\n| if ( $DEBUG );
  my $dbh = $self->connectdb('okmis_config');
  my $s = $dbh->prepare("insert into idxFILE values(NULL, '${Type}')");
  $s->execute || die "ERROR: insert into idxFILE!\n";
  my $NewID = $s->{mysql_insertid};
#warn qq|NewID=$NewID\n|;
  if($NewID % 30 == 0)
  { 
    $s = $dbh->prepare("delete from idxFILE where ID < ${NewID}");
    $s->execute || die "ERROR: delete from idxFILE";
  }
  $s->finish();
  #$dbh->disconnect();
#warn qq|NewID=$NewID\n|;
  return($NewID);
}
############################################################################
sub connectdb               # this is the new dbh.
{
  my ($self,$dbname,$user,$pswd) = @_;
warn qq|DBForm--: connectdb: WARN-DBFORM\n| if ( $DEBUG );
#my $kls = myConfig->dbp($dbname);
#warn qq|dbname=$dbname, kls=$kls\n|;
  $myForm::FORM = $self;
  my $dbh = myDBI->dbconnect($dbname);
  return($dbh);
}
sub dbconnect
{
  my ($self) = @_;
warn qq|DBForm--: dbconnect: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|DBForm: ENTER: dbconnect: DBNAME=$self->{DBNAME}, dbhname=${dbhname}, dbh=${dbh}\n|;
  $myForm::FORM = $self;
  my $dbh = myDBI->dbconnect($self->{'DBNAME'});
  return($dbh);
}
############################################################################
# SET UP THE HTML PAGE FROM A FORM TEMPLATE
#
# Arguments: $htmlname  --  file containing template, path in /html
#                           Example: "Treatment.html" 
#                                    meaning /html/Treatment.html
#            %FORM      --  Form variables associative array
#
# This routine sets up an html page.  It fills in the FORM/SCREEN with 
#   data read from the SQL database and returns the completed html page.
#
#   Five sub-routines are called to setup the html page.
#
#   1. call &Read_html($htmlname, $FORM)
#   READ THE HTML TEMPLATE FROM DISK
#   then
#     searches for prepare routines
#     and
#     searches for Tables identified as <<TABLE_FIELD_INDEX>>
#     These tables identified will be passed to the TBLread subroutine
#       to read the SQL database records for the Client or Provider which
#       was requested through the &FormGet 
#       and the key/value pair of
#       Client='ClientID' or Provider='ProvID' (for valid ClientID/ProvID)
#     The SQL tables are read once per session or update here and the
#     associative array %FORM is filled in with the SQL data.
#     when a Table is later updated it is closed logically.
#
#   2. call &SetDisplay_html($html, $FORM)
#   SET THE 'Display Only' VARIABLES.
#   These are variables identified as <<<VARIABLE>>> on the html page.
#   They are used for Text only display on the html page. They are not
#   used for any data input or updates to the SQL database 
#   but are for display only on the html page, such as LOGINUSERNAME.
#
#   3. call &SetFields_html($html, $FORM, \%FS)
#   SET THE HTML PAGE INPUT VARIABLES.
#   These are variables identified as <<VARIABLE>> on the html page.
#   They are substituted with the corresponding key/value from the 
#   associative arrays %FORM (SQL database), or %ENV (server environment)
#   Some examples of use in the html page are:
#     <INPUT TYPE="TEXT" NAME="Client_LName_1" VALUE="<<Client_LName_1>>" >
#     <TEXTAREA COLS=70 ROWS=5 WRAP="virtual" 
#      NAME="Treatment_Methods_1" ><<Treatment_Methods_1>></TEXTAREA> 
#     (watch out for TEXTAREA - don't use any spaces or it will add them
#      to the variable each time the page is re-displayed.)
#     <INPUT TYPE=hidden NAME="misLINKS" VALUE="<<misLINKS>>" >
#     <INPUT TYPE="checkbox" NAME="table_field_1" 
#      VALUE=1 <<table_field_1=1>> >
#     (substitutes 'CHECKED' if FORM{table_field_1}=1)
#     (checkboxes are always written to the data session template as =0)
#     <INPUT TYPE=radio NAME="ClientIntake_RaisedIn_1" 
#      VALUE=City <<ClientIntake_RaisedIn_1=City>> > City
#     <INPUT TYPE=radio NAME="ClientIntake_RaisedIn_1" 
#      VALUE=Country <<ClientIntake_RaisedIn_1=Country>> > Country
#     (substitutes 'CHECKED' if FORM{ClientIntake_RaisedIn_1}=Country)
#
#   the DATA SESSION TEMPLATE and CHECK BOXES:
#   If a field is on the html page then it is not set in the data session
#   template.  Only the $FORM values that are not on the html page and 
#   therefore not transmitted back to the server from the client are written
#   so that when the server does received the html page back from the 
#   client those 'saved' values can be read and included as part of the 
#   html page.  The only exception are check boxes because they only transmit
#   when checked, not when un-checked.  Therefore checkboxes are always
#   written to the data session template as '0' so if they are unchecked by
#   the client (meaning not sent back at all) then the template is read and
#   the check box is set to 0 or un-checked.
#
#   4. call FUNCTION( $FORM , $ARGS);
#      EXECUTES ANY FUNCTIONS WITHIN THE HTML PAGE.
#      A function is defined by surrounding [[]].
#      Any defined perl function can be called from within any html template by using this syntax.
#      The most common function called is the DBA->selxTable to setup a SELECT
#      list from the SQL database xfiles (cross-reference files).
#      An example to this type is:
#        <SELECT NAME="Client_ST_1
#          [[DBA->selxTable(%form+xState+<<Client_ST_1>>+Descr)]]
#        </SELECT> 
#
#   5. call DBForm->TMPwrite(skip);
#   WRITES OUT DATA SESSION TEMPLATE
#   The variables in the FORM associative array (SQL database read) are saved
#   in a session template to be used by other html pages if needed.  A random
#   'session id' number is generate once per session (or SQL update) and
#   tracked by a hidden variable within the html page ('SessionID').
#
# Returns: html page for output to client,
#
# Files Created: One session template containing FORM or SQL data not on html.
#
############################################################################
############################################################################
# READ THE HTML TEMPLATE FROM DISK along with the SQL data
#   This routine is called my mis.cgi.
# Arguments: $htmlname  --  name of html template on disk
#                           will be prefixed with 'DocRoot/html/'
#                           where DocRoot is sites' home directory
#
#   This routine does the actual read from disk of the html template,
#   then
#     searches for include files identified as ((filename))
#     and
#     searches for tables identified as 'TABLE_FIELD_INDEX'
#     These tables identified will be read from the database based on
#                                       'TABLE_ID'
#   The SQL tables are read once per session and the
#     associative array %self is filled in with the SQL data.
#     when a Table is later updated it is closed logically.
############################################################################
sub getHTML
{
  my ($self, $htmlname, $NoTMP) = @_;
warn qq|DBForm: getHTML: WARN-DBFORM\n| if ( $DEBUG );
warn qq|DBForm: getHTML: htmlname=${htmlname}, NoTMP=$NoTMP\n| if ( $DEBUG );
  ####################################
  # Open the html file and parse each line
  ####################################
  my $SRC = myConfig->cfg('SRC');
  my $htmlpathname = $SRC . "/html/" . $htmlname;
  if ( !open(TEMPLATE, $htmlpathname) ) 
  { $self->error("Can't open $htmlname ($!)."); }

  ####################################
  # MAIN loop goes through the html template we just opened
  #   $html is string returned.
  ####################################
  my $html = '';
  my $line = '';
  my $line_copy = '';
  while ($line = <TEMPLATE>) 
  {
    ####################################
    # 1st Search for Table Names 
    #   so we can read the records from the SQL database.
    #   and open all the tables.
    ####################################
    $line_copy = '';
    while ($line =~ /<<([^>]+)>>/) 
    {
      $whatmatch=$1;                          # what matched
      $prematch=$`;                           # before what matched
      $line = $';                             # now set to after what matched
      # put back what we found, we are only looking.
      $line_copy .= $prematch . '<<' . $whatmatch . '>>';
      my ($table, $field, $num) = $whatmatch =~ /<?(.+?)_(.+?)_(\d+)/;
      next if ( $table eq '' );
      if ( !$self->{"OPENTABLE:${table}"} ) { $self->TBLread($table); }
    }
    $html .= $line_copy . $line;
  }

  ####################################
  # next search for any prepare functions...
  ####################################
  $line = $html;
  $line_copy = '';
  while ( $line =~ /\[\[\[(.+?)\]\]\]/ ) 
  {
    $whatmatch=$1;                            # what matched
    $prematch=$`;                             # before what matched
    $line = $';                               # now set to after what matched
    $line_copy .= $prematch;                  # copy set to before what matched
    $line_copy .= $self->exFunc($whatmatch);  #   plus what the function returns
    ####################################
  }
  $html = $line_copy . $line;

  ####################################
  # SET THE 'Display Only' VARIABLES.
  # These are variables identified as <<<VARIABLE>>> on the html page.
  #   They are used for Text only display on the html page. They are not
  #   used for any data input or updates to the SQL database,
  #   but are for display only on the html page, such as LOGINUSERNAME.
  #   they ARE written to the TMPfile, unless skipped in the <<>> section.
  ####################################
  $line = $html;
  $line_copy = '';
  while ($line =~ /<<<([^>]+)>>>/) 
  {
    $whatmatch=$1;                            # what matched
    $prematch=$`;                             # before what matched
    $line = $';                               # now set to after what matched
    #   (check %self, then %ENV for match)
    if ( defined($self->{$whatmatch}) )
    { 
      ($text = $self->{$whatmatch}) =~ s/"/&quot;/g;
      $line_copy .= $prematch . $text;
    }
    elsif ( defined($ENV{$whatmatch}) )
    { 
      ($text = $ENV{$whatmatch}) =~ s/"/&quot;/g;
      $line_copy .= $prematch . $text;
    }
    else { $line_copy .= $prematch; }
  }
  $html = $line_copy . $line;

  ####################################
  # SET THE HTML PAGE INPUT VARIABLES.
  # These are variables identified as <<VARIABLE>> on the html page.
  #   They are substituted with the corresponding key/value from the 
  #   associative arrays %self (SQL database), or %ENV (server environment)
  # Anywhere in the html page <<...>> is found is checked for
  #   1. ... in the %self associative array
  #   2. ... in the %ENV associative array
  #   3. ... being some form of name=checkbox for INPUT TYPE=checkbox
  #   4. ... being some for of name=value for INPUT TYPE=radio
  # See above in &FormSet description for some examples.
  ####################################
  # Initialize our variables 
  ####################################
  my %skip = ();
  my %radio = ();
#warn qq|\n\ngetHTML CHECK skip:\n|;
#foreach my $f ( sort keys %{$skip} ) { warn qq|skip: $f=$skip->{$f}\n|; }

  ####################################
  # Search for variables in the current html
  #   these are FORM INPUT variables in html, 
  #   they DO NOT get written in data 'session' template.
  ####################################
  $line = $html;
  $line_copy = '';
  while ( $line =~ /<<([^>]+)>>/ ) 
  {
    $whatmatch=$1;                            # what matched
    $prematch=$`;                             # before what matched
    $line = $';                               # now set to after what matched
    ####################################
    # Check %self, then %ENV for match
    # FIELD_SET is set to know which fields are INPUT on the FORM
    #     or not session template fields
    #     and which fields are NOT sent by the form so must be
    #     read from the session template.
    #   CheckBoxes are always set as session template so if not
    #     transmitted by the form they will be set to 0
    #     from the session template
    ####################################
    if ( defined($self->{$whatmatch}) )
    {
      ($text = $self->{$whatmatch}) =~ s/"/&quot;/g;
      $line_copy .= $prematch . $text;
      $skip->{$whatmatch} = 1;
    }
    elsif ( defined($ENV{$whatmatch}) )
    { 
      ($text = $ENV{$whatmatch}) =~ s/"/&quot;/g;
      $line_copy .= $prematch . $text;
      $skip->{$whatmatch} = 1;
    }
    elsif ( $whatmatch =~ /(.+?)=checkbox/ )
    { 
      $line_copy .= $prematch;                # copy set to before what matched
      $line_copy .= "CHECKED" if ( $self->{$1} == 1 );
      $self->{$1} = 0;        # set to NOT CHECKED (1=CHECKED)
      $whatmatch = $1;
    }
    elsif ( $whatmatch =~ /(.+?)=(.*)=selectlist/ ) # selectlist, CANNOT use a NULL for match!
    { 
      $line_copy .= $prematch;                # copy set to before what matched
      $whatmatch = $1;
      if ( $self->{$1} eq $2 )
      { 
        $line_copy .= "SELECTED";
      }
    }
    elsif ( $whatmatch =~ /(.+?)=(.*)/ ) # radio button, CANNOT use a NULL for match!
    { 
      $line_copy .= $prematch;                # copy set to before what matched
      $whatmatch = $1;
      if ( $self->{$1} eq $2 && !$radio{$1} )
      { 
        $line_copy .= "CHECKED";
        $self->{$1} = '';      # set to NOT CHECKED (null)
        $radio{$1} = 1;
      }
    }
    else 
    { 
      $line_copy .= $prematch;                # copy set to before what matched
      $skip->{$whatmatch} = 1;
    }
  }
  $html = $line_copy . $line;

  ####################################
  # EXECUTES ANY FUNCTIONS WITHIN THE HTML PAGE.
  # first new: [[myHTML->rightpane(%form+search)]]
  ####################################
  $line = $html;
  $line_copy = '';
  while ( $line =~ /\[\[(.+?)\]\]/ ) 
  {
    $whatmatch=$1;
    $prematch=$`;
    $line = $';                               # now set to after what matched
    $line_copy .= $prematch;                  # copy set to before what matched
    $line_copy .= $self->exFunc($whatmatch);  #   plus what the function returns
  }
  $html = $line_copy . $line;
  close(TEMPLATE);

  ####################################
  # Convert any Tabs in html (<!--TAB:   )
  ####################################
  $html = gHTML->setTabs($self,$html);

  ####################################
  # Save / write out to TMP file 
  #   and add in hidden vars.
  ####################################
  my $hidden = $self->TMPwrite($skip) unless ( $NoTMP );
  $html =~ s|</LOADHIDDEN>|${hidden}|g;

  return($html);
}
############################################################################
sub TBLread
{
  my ($self,$inTable) = @_;
warn qq|DBForm: TBLread: WARN-DBFORM\n| if ( $DEBUG );
  return($self) if ( $self->{"OPENTABLE:${inTable}"} );
#warn qq|DBForm:BEGIN: TBLread: inTable=$inTable\n|;

  my $dbh = myDBI->dbconnect($self->{'DBNAME'});
# Recursion to get Header tables read too.
  my $hdrtable = myDBI->getTableConfig($inTable,'HEADERTABLE');
  if ( $hdrtable ) { $self->TBLread($hdrtable); }

  my $HDRID = myDBI->getTableConfig($hdrtable,'RECID');
  my $HDRIDval = $self->{"${hdrtable}_${HDRID}"};
  my $HDRIDval1 = $self->{"${hdrtable}_${HDRID}_1"};
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $IDval = $self->{"${inTable}_${ID}"};
  my $DETID = myDBI->getTableConfig($inTable,'DETAILID');
#warn qq|DBForm:BEGIN: TBLread: inTable=$inTable, ID=$ID, IDval=$IDval, DETID=$DETID\n|;
#warn qq|DBForm:BEGIN: TBLread: inTable=$inTable, hdrtable=$hdrtable, HDRIDval=$HDRIDval, HDRIDval1=$HDRIDval1\n|;
  if ( $IDval =~ /new/i )
  { $self->setDefaults($inTable,$ID); }
  elsif ($IDval ne '')
  { $self->TBLselect($inTable,$ID,$IDval); }
  elsif ( $HDRIDval =~ /new/i )
  { $self->{"${inTable}_${ID}"} = 'new'; $self->setDefaults($inTable,$ID); }
  ####################################
  # this will select multiple records if HEADERID is not null, ie with ClientID=357
  #   to set a new detail record set IDval='new', ie ClientPrAuth_ID='new'
  ####################################
  elsif ($HDRIDval ne '')
  { 
    $self->TBLselect($inTable,$DETID,$HDRIDval);
    $self->setDefaults($inTable,$ID) if ( $self->{"${inTable}_${ID}_1"} eq '' );
  }
  elsif ($HDRIDval1 ne '')
  { 
    $self->TBLselect($inTable,$DETID,$HDRIDval1);
    $self->setDefaults($inTable,$ID) if ( $self->{"${inTable}_${ID}_1"} eq '' );
  }
#foreach my $f ( sort keys %{$self} ) { warn qq|self: $f=$self->{$f}\n|; }

  if ( $inTable eq 'Treatment' )
  {
    $self->{'BeginTime'} = DBUtil->AMPM($self->{'Treatment_ContLogBegTime_1'});
    $self->{'EndTime'} = DBUtil->AMPM($self->{'Treatment_ContLogEndTime_1'});
  }
  elsif ( $inTable eq 'Insurance' )
  {
    $s=$dbh->prepare("select * from xInsurance where ID=?");
    $s->execute($self->{'Insurance_InsID_1'});
    my $r = $s->fetchrow_hashref;
    $self->{'INSURANCE_TAG'} = $r->{Descr};
    $s->finish();
  }
  elsif ( $inTable eq 'PrAuthRVU' )
  {
    # set the sub PANum (in PrAuthRVU) if not set from main PAnumber.
    $self->{'PrAuthRVU_PANum_1'} = $self->{'PrAuth_PAnumber_1'} if ( $self->{'PrAuthRVU_PANum_1'} eq '' );
    $self->{'PrAuthRVU_EffDate_1'} = $self->{'PrAuth_EffDate_1'};
    $self->{'PrAuthRVU_ExpDate_1'} = $self->{'PrAuth_ExpDate_1'};
  }

  DBA->locked($self,$inTable);
  ####################################
  # and tell everyone the table is open.
  ####################################
  $self->{"OPENTABLE:${inTable}"} = 1;
  if ( $self->{'OPENTABLES'} ) { $self->{'OPENTABLES'} .= ',' . ${inTable}; }
  else { $self->{'OPENTABLES'} = ${inTable}; }
  return($self);
}
############################################################################
# These defaults are for 'new' records which are skipped in difFields.
#   caution: defaults can affect the outcome when difFields is called on update.
############################################################################
sub setDefaults
{
  my $self = shift;
  my ($inTable,$ID) = @_;
warn qq|DBForm: setDefaults: WARN-DBFORM\n| if ( $DEBUG );
  my $dbh = $self->dbconnect();
#warn qq|DBForm:BEGIN:setDefaults: inTable=$inTable, ID=$ID\n|;
#foreach my $f ( sort keys %{$self} ) { warn qq|self: $f=$self->{$f}\n|; }

  if ( $inTable eq 'Provider' )
  {
    $self->{'Provider_Active_1'} = '1';
    $self->{'Provider_ST_1'} = 'OK';
    $self->{'Provider_Type_1'} = '4';                   # means Provider (Group=1,Agency=2,Clinic=3)
    $self->{'Provider_NoMail_1'} = 0;
  }
  elsif ( $inTable eq 'ProviderLicenses' )
  {
    $self->{'ProviderLicenses_State_1'} = 'OK';
  }
  elsif ( $inTable eq 'ProviderPrefs' )
  {
    $self->{'ProviderPrefs_TreeTabs_1'} = 0;
    $self->{'ProviderPrefs_ListClients_1'} = 0;
    $self->{'ProviderPrefs_MISEmails_1'} = 0;
  }
  elsif ( $inTable eq 'ProviderCreds' )
  {
    $self->{'ProviderCreds_License1ST_1'} = 'OK';
    $self->{'ProviderCreds_DEA1Type_1'} = 'DEA';
    $self->{'ProviderCreds_DEA2Type_1'} = 'DEA';
    $self->{'ProviderCreds_BNDDType_1'} = 'BNDD';
    $self->{'ProviderCreds_CDSType_1'} = 'CDS';
  }
  elsif ( $inTable eq 'ProviderPay' )
  {
    $self->{'ProviderPay_isMgr_1'} = '0';
  }
  elsif ( $inTable eq 'Credentials' )
  {
    $self->{'Credentials_Taxonomy_1'} ='101Y00000X';
  }
  elsif ( $inTable eq 'Client' )
  {
#warn qq|setDefaults: Client, ID=$self->{Client_ClientID_1}\n|;
    $self->{'Client_Active_1'} = '1';
    $self->{'Client_SSN_1'} = $self->{'SSN'};
    $self->{'Client_ST_1'} = 'OK';
    $self->{'Client_ProvID_1'} = $self->{'ProviderID'};
    $self->{'Client_clinicClinicID_1'} = MgrTree->getClinic($self,$self->{'LOGINPROVID'});
  }
  elsif ( $inTable eq 'ClientIntake' )
  {
    $self->{'ClientIntake_AbsentSchool_1'} = '0';       # 0 days
    $self->{'ClientIntake_SuspendedSchool_1'} = '0';    # 0 days
    $self->{'ClientIntake_AbsentDayCare_1'} = '0';      # 0 days
    $self->{'ClientIntake_SchoolLast3_1'} = '0';        # 0 = no
  }
  elsif ( $inTable eq 'ClientEmergency' )
  {
    # Do NOT Opt-Out of sending information if MMS, others Yes OptOut.
    my $OptOut = $self->{'DBNAME'} eq 'okmis_mms' ? 0 : 1;
    $self->{'ClientEmergency_MyHealth_1'} = $OptOut;
  }
  elsif ( $inTable eq 'Insurance' )
  {
    my $q = qq|select * from xInsurance where Descr LIKE '%medicaid%'|;
    my $s = $dbh->prepare($q);
    $s->execute || $self->dberror($q);
    if ( my $r = $s->fetchrow_hashref ) { $self->{'Insurance_InsID_1'} = $r->{ID}; }
    else { $self->{'Insurance_InsIDNum_1'} = $self->{'Client_SSN_1'}; }
    $self->{'Insurance_Priority_1'} = '1';
    $self->{'Insurance_InsNumEffDate_1'} = DBUtil->Date('today','fmt','YYYY-MM') . '-01';
    $self->{'Insurance_InsNumActive_1'} = '1';
    $self->{'Insurance_Deductible_1'} = '0';
    $self->{'Insurance_Copay_1'} = '0';
    $s->finish();
  }
  elsif ( $inTable eq 'ClientLegal' )
  {
    $self->{'ClientLegal_LegalStatus_1'} = '116';      # INFORMAL ADMISSION
  }
  elsif ( $inTable eq 'MedHx' )
  {
    $self->{'MedHx_AttSuicides_1'} = '0';               # 0 attempts
    $self->{'MedHx_FamilySuicideHx_1'} = '0';           # 0 = no
    $self->{'MedHx_Firearms_1'} = '0';                  # 0 = no
    $self->{'MedHx_RestrictivePlacement_1'} = '0';      # 0 days
    $self->{'MedHx_SelfHarm_1'} = '0';                  # 0 days
  }
  elsif ( $inTable eq 'ClientProblems' )
  {
    $self->{'ClientProblems_InitiatedDate_1'} = $self->{'TODAY'};
    $self->{'ClientProblems_Priority_1'} = 9999;
  }
  elsif ( $inTable eq 'ClientRelations' )
  {
    $self->{'ClientRelations_MarStat_1'} = 1;           # Never married
    $self->{'ClientRelations_ResNum_1'} = 0;
    $self->{'ClientRelations_HomelessLong_1'} = '0';    # 0 = no
    $self->{'ClientRelations_HomelessMany_1'} = '0';    # 0 = no
  }
  elsif ( $inTable eq 'ClientResources' )
  {
    $self->{'ClientResources_SelfHelp30_1'} = '0';      # 0 days
  }
  elsif ( $inTable eq 'ClientTrPlan' )
  {
    my $r = DBA->getLAST($self,'',$inTable,"where ClientTrPlan.ClientID='$self->{Client_ClientID_1}'"
                                          ,"order by ClientTrPlan.EffDate desc, ClientTrPlan.ExpDate desc");
    if ( $r )
    {
      $self->setTable($inTable,$r);
#warn qq|setDefaults: ClientTrPlan: delete ${inTable}_${ID}_1=$self->{"${inTable}_${ID}_1"}\n|;
      delete $self->{"${inTable}_${ID}_1"};
      delete $self->{"${inTable}_CreateDate_1"};
      delete $self->{"${inTable}_CreateProvID_1"};
      delete $self->{"${inTable}_ChangeDate_1"};
      $self->{'ClientTrPlan_ClSigDate_1'} = '';
      $self->{'ClientTrPlan_PGSigDate_1'} = '';
      $self->{'ClientTrPlan_PhSigDate_1'} = '';
    }
    else
    {
      my $q = qq|select S1,S2,S3,S4,L1,L2,L3,L4,Prefs from ClientSummary where ClientID='$self->{Client_ClientID_1}'|;
#warn qq|setDefaults: ClientTrPlan: ClientID=$self->{Client_ClientID_1}\n${q}\n|;
      my $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($S1,$S2,$S3,$S4,$L1,$L2,$L3,$L4,$Prefs) = $s->fetchrow_array;
      $self->{'ClientTrPlan_SA1_1'} = $S1;
      $self->{'ClientTrPlan_SA2_1'} = $S2;
      $self->{'ClientTrPlan_SA3_1'} = $S3;
      $self->{'ClientTrPlan_SA4_1'} = $S4;
      $self->{'ClientTrPlan_L1_1'} = $L1;
      $self->{'ClientTrPlan_L2_1'} = $L2;
      $self->{'ClientTrPlan_L3_1'} = $L3;
      $self->{'ClientTrPlan_L4_1'} = $L4;
      $self->{'ClientTrPlan_Preferences_1'} = $Prefs;
      $s->finish();
      my $q = qq|select Problem,Summary,Services,Referrals from ClientIntake where ClientID='$self->{Client_ClientID_1}'|;
#warn qq|setDefaults: ClientTrPlan: ClientID=$self->{Client_ClientID_1}\n${q}\n|;
      my $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($Problem,$Summary,$Services,$Referrals) = $s->fetchrow_array;
      $self->{'ClientTrPlan_Comments_1'} = $Problem;
      $self->{'ClientTrPlan_Summary_1'} = $Summary;
      $self->{'ClientTrPlan_Services_1'} = $Services;
      $self->{'ClientTrPlan_ReferralsNPI_1'} = $Referrals;
      $s->finish();
    }
    $self->{'ClientTrPlan_EffDate_1'} = DBUtil->Date();
    $self->{'ClientTrPlan_ExpDate_1'} = DBUtil->Date('',6,-1);
    $self->{'ClientTrPlan_Locked_1'} = 0;
    $self->{'ClientTrPlan_CopyID_1'} = $r->{$ID};
#warn qq|setDefault:  ${inTable}: CopyID=$r->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientTrPlanPG' )
  {
    my $s = $dbh->prepare("select CopyID from ClientTrPlan where ID='$self->{'ClientTrPlan_ID_1'}'");
    $s->execute() || $self->dberror("setDefault: select ClientTrPlan CopyID");
    my ($PrevID) = $s->fetchrow_array;
    $s->finish();
#warn qq|setDefault:  ${inTable}: PrevID=${PrevID}, TrPlanID=$self->{'ClientTrPlan_ID_1'}\n|;
    my $s = $dbh->prepare("select count(*) from ClientTrPlanPG where TrPlanID='$self->{'ClientTrPlan_ID_1'}'");
    $s->execute() || $self->dberror("setDefault: select ClientTrPlanPG count");
    my ($cnt) = $s->fetchrow_array;
    $s->finish();
#warn qq|setDefault:  ${inTable}: cnt=${cnt}\n|;
    my ($rLast,$i) = ('',0);
    my $s = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID='$PrevID'");
    $s->execute() || $self->dberror("setDefault: select CLientTrPlanPG ${PrevID}");
    while ( my $r = $s->fetchrow_hashref ) { $i++; $rLast = $r if ( $cnt < $i ); last if ( $i == $cnt+1 ); }
    $s->finish();
    $self->setTable($inTable,$rLast);
#warn qq|setDefault:  ${inTable}: i=${i}\n|;
    delete $self->{"${inTable}_${ID}_1"};
    delete $self->{"${inTable}_CreateDate_1"};
    delete $self->{"${inTable}_CreateProvID_1"};
    delete $self->{"${inTable}_ChangeDate_1"};
    delete $self->{"${inTable}_TrPlanID_1"};
    $self->{'ClientTrPlanPG_Priority_1'} = 9999;
    $self->{'ClientTrPlanPG_Locked_1'} = 0;
    $self->{'ClientTrPlanPG_CopyID_1'} = $rLast->{$ID};
#warn qq|setDefault:  ${inTable}: CopyID=$rLast->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientTrPlanOBJ' )
  {
    my $s = $dbh->prepare("select CopyID from ClientTrPlanPG where ID='$self->{'ClientTrPlanPG_ID_1'}'");
    $s->execute() || $self->dberror("setDefault: select ClientTrPlanPG CopyID");
    my ($PrevID) = $s->fetchrow_array;
    $s->finish();
#warn qq|setDefault:  ${inTable}: PrevID=${PrevID}, TrPlanPGID=$self->{'ClientTrPlanPG_ID_1'}\n|;
    my $s = $dbh->prepare("select count(*) from ClientTrPlanOBJ where TrPlanPGID='$self->{'ClientTrPlanPG_ID_1'}'");
    $s->execute() || $self->dberror("setDefault: select ClientTrPlanOBJ count");
    my ($cnt) = $s->fetchrow_array;
    $s->finish();
#warn qq|setDefault:  ${inTable}: cnt=${cnt}\n|;
    my ($rLast,$i) = ('',0);
    my $s = $dbh->prepare("select * from ClientTrPlanOBJ where TrPlanPGID='$PrevID' and ResolvedDate is null");
    $s->execute() || $self->dberror("setDefault: select CLientTrPlanOBJ ${PrevID}");
    while ( my $r = $s->fetchrow_hashref ) { $i++; $rLast = $r if ( $cnt < $i ); last if ( $i == $cnt+1 ); }
    $s->finish();
#warn qq|setDefault:  ${inTable}: i=${i}\n|;
    $self->setTable($inTable,$rLast);
    delete $self->{"${inTable}_${ID}_1"};
    delete $self->{"${inTable}_TrPlanPGID_1"};
    delete $self->{"${inTable}_CreateDate_1"};
    delete $self->{"${inTable}_CreateProvID_1"};
    delete $self->{"${inTable}_ChangeDate_1"};
    $self->{'ClientTrPlanOBJ_InitiatedDate_1'} = DBUtil->Date();
    $self->{'ClientTrPlanOBJ_TargetDate_1'} = DBUtil->Date('',6,-1);
    $self->{'ClientTrPlanOBJ_Priority_1'} = 9999;
    $self->{'ClientTrPlanOBJ_Locked_1'} = 0;
    $self->{'ClientTrPlanOBJ_CopyID_1'} = $rLast->{$ID};
#warn qq|setDefault:  ${inTable}: CopyID=$rLast->{$ID}\n|;
  }
  elsif ( $inTable eq 'ClientPrAuth' )
  {
    my $ClientID = $self->{'Client_ClientID_1'};
#warn qq|setDefault: ClientPrAuth: ClientID=${ClientID}\n|;
    $self->{'ClientPrAuth_Type_1'} = $ClientID eq 'new' ? 'RI' : 'RE';
    $self->{'ClientPrAuth_ReqType_1'} = DBA->setPrAuthReqType($self,$ClientID);
    my ($isAdult,$TL) = TLevel->getTreatmentLevel($self,$ClientID,'18');
    $self->{'ClientPrAuth_TL_1'} = $TL;

    my $TDate = $self->{'ClientPrAuthCDC_TransDate_1'};
    $self->{'ClientPrAuth_EffDate_1'} = $TDate;
    my $InsID = $self->{'Insurance_InsID_1'};
    $PAgroup = CDC->calcPG($self,$ClientID,$InsID);
    my ($months,$days) = DBA->calcLOS($self,$InsID,$PAgroup);
    $self->{'ClientPrAuth_PAgroup_1'} = $PAgroup;
    $self->{'ClientPrAuth_ExpDate_1'} = DBUtil->Date($TDate,$months,$days);
    $self->{'ClientPrAuth_LOS_1'} = $months;
  }
  elsif ( $inTable eq 'PDDiag' 
       || $inTable eq 'PDDom'
        )
  {
    my $r = DBA->getLAST($self,'',$inTable,"where ClientPrAuth.ClientID='$self->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    if ( $r )
    {
      $self->setTable($inTable,$r);
#warn qq|delete ${inTable}_${ID}_1=$self->{"${inTable}_${ID}_1"}\n|;
      delete $self->{"${inTable}_${ID}_1"};
      delete $self->{"${inTable}_RecDOLC_1"};
      if ( $inTable eq 'PDDiag' )
      {
        $self->{'PDDiag_Axis5Prev_1'} = $self->{'PDDiag_Axis5Curr_1'};
#warn qq|setDefault: PDDiag ${inTable}_Axis1ACode_1=$self->{"${inTable}_Axis1ACode_1"}\n|;
      }
    }
    if ( $inTable eq 'PDDiag' )
    {
      $self->{'PDDiag_Axis1ACode_1'} = 390;       # V71.09
      $self->{'PDDiag_Axis2ACode_1'} = 18;        # V71.09
      $self->{'PDDiag_Axis3Diag_1'} = 'none reported';
      $self->{'PDDiag_Axis1BCode_1'} = 390;       # V71.09
      $self->{'PDDiag_Axis2BCode_1'} = 18;        # V71.09
      ##problem with DMH $self->{'PDDiag_Axis1CCode_1'} = 390;       # V71.09
      $self->{'PDDiag_Axis4Level_1'} = '03';      # Moderate
      $self->{'PDDiag_Diag4Support_1'} = 0;       # NONE
      $self->{'PDDiag_Diag4Social_1'} = 0;        # NONE
      $self->{'PDDiag_Diag4Health_1'} = 0;        # NONE
      $self->{'PDDiag_Diag4Legal_1'} = 0;         # NONE
      $self->{'PDDiag_Diag4Education_1'} = 0;     # NONE
      $self->{'PDDiag_Diag4Occup_1'} = 0;         # NONE
      $self->{'PDDiag_Diag4House_1'} = 0;         # NONE
      $self->{'PDDiag_Diag4Econ_1'} = 0;          # NONE
      $self->{'PDDiag_Diag4Other_1'} = 0;         # NONE
      my $q = qq|select Axis5Curr,Axis5High from ClientSocial where ClientID='$self->{Client_ClientID}'|;
      my $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($Axis5Curr,$Axis5High) = $s->fetchrow_array;
      $self->{'PDDiag_Axis5Curr_1'} = $Axis5Curr;
      $self->{'PDDiag_Axis5High_1'} = $Axis5High;
      $s->finish();
#warn qq|setDefault: new PDDiag ${inTable}_Axis1ACode_1=$self->{"${inTable}_Axis1ACode_1"}\n|;
    }
  }
  elsif ( $inTable eq 'Appointments' )
  {
    $self->{'Appointments_ProvID_1'} = $self->{'LOGINPROVID'};
    $self->{'Appointments_ContactDate_1'} = DBUtil->Date();
    $self->{'Appointments_BeginTime_1'} = '09:00:00';
  }
  elsif ( $inTable eq 'Treatment' )
  {
    ####################################
    # Dont' allow updates of BillDate, COPLDate, RecDate, PaidDate, DenDate, DenCode
    #   leave them off any HTML page INPUT FORMs
    #   these are only updated in billing routines
    ####################################
    $self->{'Treatment_ChartEntryDate_1'} = DBUtil->Date();
    $self->{'Treatment_ClinicID_1'} = $self->{'Client_clinicClinicID_1'};
    $self->{'Treatment_ProvID_1'} = $self->{'LOGINPROVID'};
    $self->{'Treatment_EnteredBy_1'} = $self->{'LOGINPROVID'};
    $self->{'Treatment_POS_1'} = 3;                         # Place of Service = Doctor's Office
    $self->{'Treatment_BillStatus_1'} = 0;                  # Billed Status = new.
    $self->{'Treatment_StatusDate_1'} = $self->{TODAY};     # Billed Status = new date.
    $self->{'Treatment_RevStatus_1'} = 0;                   # ReviewedStatus = new.
    ####################################
#warn qq|Treatment: AppointmentID=$self->{'AppointmentID'}\n|;
#warn qq|Treatment: DupNote\n| if ( SysAccess->verify($self,'Privilege=DupNote') );
    if ( $self->{'AppointmentID'} )
    {
      $self->{'Treatment_ProvID_1'} = $self->{'AppointmentProvID'};
      $self->{'Treatment_ContLogDate_1'} = $self->{'AppointmentContactDate'};
      $self->{'Treatment_ContLogBegTime_1'} = $self->{'AppointmentBeginTime'};
    }
    elsif ( SysAccess->verify($self,'Privilege=DupNote') )
    {
      my $r = DBA->getLAST($self,'',$inTable,"where Treatment.ClientID='$self->{Client_ClientID_1}' and Treatment.ProvID='$self->{LOGINPROVID}' and Treatment.Type!=3","order by Treatment.ContLogDate desc");
      if ( $r )
      {
        #$self->{'Treatment_SCID_1'} = $r->{'SCID'};
        #$self->{'Treatment_ContLogBegTime_1'} = $r->{'ContLogBegTime'};
        #$self->{'Treatment_ContLogEndTime_1'} = $r->{'ContLogEndTime'};
        #$self->{'Treatment_POS_1'} = $r->{'POS'};
        $self->{'Treatment_ProbNum_1'} = $r->{'ProbNum'};
        $self->{'useTrID'} = $r->{'TrID'};
      }
    }
  }
  elsif ( $inTable eq 'ProgNotes' )
  {
#warn qq|ProgNotes: useTrID=$self->{'useTrID'}\n|;
    if ( $self->{'AppointmentID'} )
    {
      $self->{'ProgNotes_ProgEvidence_1'} = $self->{'AppointmentNotes'};
    }
    elsif ( $self->{'useTrID'} )
    {
      my $s = $dbh->prepare("select * from ProgNotes where NoteID='$self->{useTrID}'");
      $s->execute() || $self->dberror("setDef: useTrID=$self->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        $self->setTable($inTable,$r);
#warn qq|delete ${inTable}_${ID}_1=$self->{"${inTable}_${ID}_1"}\n|;
        delete $self->{"${inTable}_${ID}_1"};
        delete $self->{"${inTable}_GrpSize_1"};
        delete $self->{"${inTable}_RecDOLC_1"};
      }
      $s->finish();
    }
  }
  elsif ( $inTable eq 'PhysNotes' )
  {
#warn qq|PhysNotes: useTrID=$self->{'useTrID'}\n|;
    my $ClientID = $self->{'Client_ClientID_1'};
    my ($h,$w) = ('','');
    if ( $self->{'useTrID'} )    # get them from last note.
    {
      my $s = $dbh->prepare("select * from PhysNotes where NoteID='$self->{useTrID}'");
      $s->execute() || $self->dberror("setDef: useTrID=$self->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        $self->setTable($inTable,$r);
#warn qq|delete ${inTable}_${ID}_1=$self->{"${inTable}_${ID}_1"}\n|;
        delete $self->{"${inTable}_${ID}_1"};
        delete $self->{"${inTable}_RecDOLC_1"};
        $h = $r->{'Height'};
        $w = $r->{'Weight'};
#warn qq|useTrID: $self->{'useTrID'} h=${h}, w=${w}\n|;
      }
    }
    if ( $h eq '' || $w eq '' )       # get them from Intake
    {
#warn qq|are null: h=${h}, w=${w}\n|;
      my $s = $dbh->prepare("select * from Client where ClientID='${ClientID}'");
      $s->execute() || $self->dberror("setDef PhysNotes: ClientID=${ClientID}");
      my $r = $s->fetchrow_hashref;
      $h = $r->{'Height'} if ( $h eq '' );
      $w = $r->{'Weight'} if ( $w eq '' );
      $self->{'PhysNotes_Height_1'} = $h;
      $self->{'PhysNotes_Weight_1'} = $w;
      $s->finish();
    }
    (my $height = $h) =~ s/^\s*(.*?)\s*$/$1/g; $height =~ s/\'//; $height =~ s/\"//;
    my ($f,$i) = split(" ",$height);
    my $hi = ($f * 12) + $i;          # Height in inches.
#warn qq|PhysNotes: height=$h,$height,$f,$i,$hi; weight=$w\n|;
    $self->{'PhysNotes_BMI_1'} = $hi == 0 ? 0 : sprintf("%.2f",( $w / ( $hi * $hi ) ) * 703);
    my $r = DBA->getLAST($self,'','PDDiag',"where ClientPrAuth.ClientID='$self->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    $self->{'PhysNotes_Axis1ACode_1'} = $r->{'Axis1ACode'};
  }
  elsif ( $inTable eq 'ClientTherapyNotes' )
  {
#warn qq|ClientTherapyNotes: useTrID=$self->{'useTrID'}\n|;
    if ( $self->{'useTrID'} )
    {
      my $s = $dbh->prepare("select * from ClientTherapyNotes where NoteID='$self->{useTrID}'");
      $s->execute() || $self->dberror("setDef: useTrID=$self->{useTrID}");
      my $r = $s->fetchrow_hashref;
      if ( $r )
      {
        $self->setTable($inTable,$r);
#warn qq|delete ${inTable}_${ID}_1=$self->{"${inTable}_${ID}_1"}\n|;
        delete $self->{"${inTable}_${ID}_1"};
        delete $self->{"${inTable}_RecDOLC_1"};
      }
    }
  }
  elsif ( $inTable eq 'xSCRates' )
  {
    $self->{'xSCRates_RatePct_1'} = '1.00';
    $self->{'xSCRates_CommissionPct_1'} = '1.00';
    $self->{'xSCRates_RVUPct_1'} = '1.00';
  }
  elsif ( $inTable eq 'ClientDischarge' )
  {
    my $qClientIntake = qq|select * from ClientIntake where ClientID='$self->{Client_ClientID}'|;
    my $sClientIntake= $dbh->prepare($qClientIntake);
    $sClientIntake->execute() || $self->dberror($qClientIntake);
    my $rClientIntake = $sClientIntake->fetchrow_hashref;
    $self->{ClientDischarge_IntDate_1} = $rClientIntake->{IntDate};
    $self->{ClientDischarge_ServiceFocus_1} = $rClientIntake->{ServiceFocus};
    $self->{ClientDischarge_InitCond_1} = $rClientIntake->{Problem};
    $self->{ClientDischarge_IDNeeds_1} = DBA->getxref($self,'xProblems',$rClientIntake->{'Problem1'},'Descr');
    $self->{ClientDischarge_IDNeeds_1} .= "; ".DBA->getxref($self,'xProblems',$rClientIntake->{'Problem2'},'Descr') if ( $rClientIntake->{'Problem2'} ne '' );
    $self->{ClientDischarge_IDNeeds_1} .= "; ".DBA->getxref($self,'xProblems',$rClientIntake->{'Problem3'},'Descr') if ( $rClientIntake->{'Problem3'} ne '' );
    $sClientIntake->finish();
    my $rClientTrPlan = DBA->getLAST($self,'','ClientTrPlan',"where ClientTrPlan.ClientID='$self->{Client_ClientID_1}'","order by ClientTrPlan.EffDate desc, ClientTrPlan.ExpDate desc");
#warn qq|ClientID=$rClientTrPlan->{ClientID}, ID=$rClientTrPlan->{ID}\n|;
    $self->{'ClientDischarge_Needs_1'} = $rClientTrPlan->{'SA1'};
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA2'}| if ( $rClientTrPlan->{'SA2'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA3'}| if ( $rClientTrPlan->{'SA3'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'SA4'}| if ( $rClientTrPlan->{'SA4'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L1'}| if ( $rClientTrPlan->{'L1'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L2'}| if ( $rClientTrPlan->{'L2'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L3'}| if ( $rClientTrPlan->{'L3'} ne '' );
    $self->{'ClientDischarge_Needs_1'} .= qq|; $rClientTrPlan->{'L4'}| if ( $rClientTrPlan->{'L4'} ne '' );
    $self->{'ClientDischarge_DischargePlan_1'} = $rClientTrPlan->{'TransitionPlan'};
    my $sClientDevl= $dbh->prepare("select * from ClientDevl where ClientID=?");
    $sClientDevl->execute($self->{Client_ClientID}) 
         || $self->dberror("setDefault: ClientDischarge: select ClientDevl $self->{Client_ClientID}");
    my $rClientDevl = $sClientDevl->fetchrow_hashref;
    $self->{'ClientDischarge_Axis3ACode_1'} = $rClientDevl->{'Handicap1'};
    $self->{'ClientDischarge_Axis3BCode_1'} = $rClientDevl->{'Handicap2'};
    $self->{'ClientDischarge_Axis3CCode_1'} = $rClientDevl->{'Handicap3'};
    $self->{'ClientDischarge_Axis3DCode_1'} = $rClientDevl->{'Handicap4'};
    $sClientDevl->finish();
    my $sClientSocial= $dbh->prepare("select * from ClientSocial where ClientID=?");
    $sClientSocial->execute($self->{Client_ClientID}) 
         || $self->dberror("setDefault: ClientDischarge: select ClientSocial $self->{Client_ClientID}");
    my $rClientSocial = $sClientSocial->fetchrow_hashref;
    $self->{'ClientDischarge_Axis5Curr_1'} = $rClientSocial->{'Axis5Curr'};
    $sClientSocial->finish();
    my $rPDDom = DBA->getLAST($self,'','PDDom',"where ClientPrAuth.ClientID='$self->{Client_ClientID_1}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
    $self->{'ClientDischarge_Dom1Score_1'} = $rPDDom->{'Dom1Score'};
    $self->{'ClientDischarge_Dom2Score_1'} = $rPDDom->{'Dom2Score'};
    $self->{'ClientDischarge_Dom3Score_1'} = $rPDDom->{'Dom3Score'};
    $self->{'ClientDischarge_Dom4Score_1'} = $rPDDom->{'Dom4Score'};
    $self->{'ClientDischarge_Dom5Score_1'} = $rPDDom->{'Dom5Score'};
    $self->{'ClientDischarge_Dom6Score_1'} = $rPDDom->{'Dom6Score'};
    $self->{'ClientDischarge_Dom7Score_1'} = $rPDDom->{'Dom7Score'};
    $self->{'ClientDischarge_Dom8Score_1'} = $rPDDom->{'Dom8Score'};
    $self->{'ClientDischarge_Dom9Score_1'} = $rPDDom->{'Dom9Score'};
  }
  elsif ( $inTable eq 'SAbuse' )
  {
    $self->{'SAbuse_Freq_1'} = '1';
    $self->{'SAbuse_Priority_1'} = '9';
  }
  elsif ( $inTable eq 'ClientASI' )
  {
    my $ClientID = $self->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($self,$inTable,"G1=$ClientID","CreateDate desc");
      if ( $val )
      {
        $self->TBLselect($inTable,$ID,$val);
        delete $self->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $multidel = chr(253);
      my $q = qq|select SSN,Gend,DOB,SUBSTRING_INDEX(Race,'${multidel}',1) as Race from Client where ClientID='$ClientID'|;
      my $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($SSN,$Gend,$DOB,$Race) = $s->fetchrow_array;
      $self->{'ClientASI_G2_1'} = $SSN;
      $self->{'ClientASI_G10_1'} = $Gend;
      $self->{'ClientASI_G16_1'} = $DOB;
      $self->{'ClientASI_G17_1'} = $Race;

      $q = qq|select StaffID from ClientIntake where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($StaffID) = $s->fetchrow_array;
      $self->{'ClientASI_G11_1'} = $StaffID;

      $q = qq|select OnPP from ClientLegal where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($OnPP) = $s->fetchrow_array;
      $self->{'ClientASI_L2_1'} = $OnPP;

      $q = qq|select MonthsTechEd from ClientEducation where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($MonthsTechEd) = $s->fetchrow_array;
      $self->{'ClientASI_E2_1'} = $MonthsTechEd;

      $q = qq|select HospOverNight from ClientHealth where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($HospOverNight) = $s->fetchrow_array;
      $self->{'ClientASI_M1_1'} = $HospOverNight;

      $q = qq|select AlcoholDTs from MedHx where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($AlcoholDTs) = $s->fetchrow_array;
      $self->{'ClientASI_D17_1'} = $AlcoholDTs;

      $q = qq|select WhoSpendTime,SatSpendTime,NumCloseFriends from ClientSocial where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($WhoSpendTime,$SatSpendTime,$NumCloseFrieds) = $s->fetchrow_array;
      $self->{'ClientASI_F9_1'} = $WhoSpendTime;
      $self->{'ClientASI_F10_1'} = $SatSpendTime;
      $self->{'ClientASI_F11_1'} = $NumCloseFriends;

      $q = qq|select MarStatY,MarStatM,ResAdmitDate,FamUsualLivArr,SatUsualLivArr from ClientRelations where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($MarStatY,$MarStatM,$ResAdmitDate,$FamUsualLivArr,$SatUsualLivArr) = $s->fetchrow_array;
      $self->{'ClientASI_F2Y_1'} = $MarStatY;
      $self->{'ClientASI_F2M_1'} = $MarStatM;
      $self->{'ClientASI_F4_1'} = $FamUsualLivArr;
      $self->{'ClientASI_F6_1'} = $SatUsualLivArr;
      $self->{'ClientASI_G4_1'} = $ResAdmitDate;

      $q = qq|select ValidDL,AutoForUse,RegSupport,MajSupport from ClientResources where ClientID='$ClientID'|;
      $s = $dbh->prepare($q);
      $s->execute() || $self->dberror($q);
      my ($ValidDL,$AutoForUse,$RegSupport,$MajSupport) = $s->fetchrow_array;
      $self->{'ClientASI_E4_1'} = $ValidDL;
      $self->{'ClientASI_E5_1'} = $AutoForUse;
      $self->{'ClientASI_E8_1'} = $RegSupport;
      $self->{'ClientASI_E9_1'} = $MajSupport;

      $s->finish();
    }
  }
  elsif ( $inTable eq 'ClientTASI' )
  {
    my $ClientID = $self->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($self,$inTable,"ClientID=$ClientID","AdmDate desc");
##$val=0;   ## don't know why asked to turn this off, now turn back on 07/11/2016
      if ( $val )
      {
        $self->TBLselect($inTable,$ID,$val);
        delete $self->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $multidel = chr(253);
      my $q = qq|select Client.*,SUBSTRING_INDEX(Client.Race,'${multidel}',1) as Race,ClientSocial.ReligionName from Client left join ClientSocial on ClientSocial.ClientID=Client.ClientID where Client.ClientID=?|;
      my $s = $dbh->prepare($q);
      $s->execute($ClientID) || $self->dberror($q);
      my $r = $s->fetchrow_hashref;
      $self->{'ClientTASI_Name_1'} = qq|$r->{FName} $r->{LName}|;
      foreach my $f ( 'Addr1','Addr2','City','ST','Zip','DOB','Gend','Race' )
      { $self->{"ClientTASI_${f}_1"} = $r->{$f}; }
      $self->{'ClientTASI_AdmDate_1'} = $self->{TODAY};
      $self->{'ClientTASI_IntDate_1'} = $self->{TODAY};
      $self->{'ClientTASI_Class_1'} = 1;
      $self->{'ClientTASI_Contact_1'} = 1;
      $self->{'ClientTASI_StaffID_1'} = $r->{ProvID};
      $self->{'ClientTASI_Religion_1'} = $r->{ReligionName};
      $q = qq|select count(*) from ClientLegalHx where ClientID=? and OutCome='J'|;
      my $s = $dbh->prepare($q);
      $s->execute($ClientID) || $self->dberror($q);
      my ($Count) = $s->fetchrow_array;
      if ( $Count > 0 ) { $self->{'ClientTASI_ContEnvi_1'} = 'dc'; }
      $s->finish();
    }
  }
  elsif ( $inTable eq 'SOGS' || $inTable eq 'SOGSGSI' )
  {
    my $ClientID = $self->{'Client_ClientID'};
    unless ( $ClientID eq 'new' )
    {
      my $val = DBA->getLastID($self,$inTable,"ClientID=$ClientID","TransDate desc");
      if ( $val )
      {
        $self->TBLselect($inTable,$ID,$val);
        delete $self->{"${inTable}_${ID}_1"};
      }
      # refresh these from main tables on each new record.
      my $p = $inTable.'_ProvID_1';
      $self->{$p} = $self->{LOGINPROVID};
      my $d = $inTable.'_TransDate_1';
      $self->{$d} = $self->{TODAY};
    }
  }
  elsif ( $inTable eq 'Contracts' )
  {
    #$self->{'Contracts_InsID_1'} = '100';              # Medicaid
    $self->{'Contracts_BillFlag_1'} = '1';              # Yes, Bill
    $self->{'Contracts_AutoReconcile_1'} = '0';
    $self->{'Contracts_AutoPay_1'} = '0';
    #$self->{'Contracts_PIN_1'} = '';                   # get PIN
    #$self->{'Contracts_RefID_1'} = '1D';               # Medicaid Provider Number for PIN
    $self->{'Contracts_Taxonomy_1'} = '261QM0801X';     # Mental Health including Community
    $self->{'Contracts_ServMeasure_1'} = 'UN';          # Units
    $self->{'Contracts_BillType_1'} = 'EL';             # Electronic
    $self->{'Contracts_UseAgency_1'} = '0';             # Not Agency Address - Clinic Address (Zip+4)
    $self->{'Contracts_ContractType_1'} = '09';         # Other
    #$self->{'Contracts_ContractCode_1'} = '';          # get for DMH
    #$self->{'Contracts_SourceCode_1'} = '';            # get for DMH
    $self->{'Contracts_UseReferring_1'} = '0';          # No
    $self->{'Contracts_UseRendering_1'} = '0';          # No
    $self->{'Contracts_UseSFacility_1'} = '0';          # No
    $self->{'Contracts_setContract_1'} = '0';           # No
    $self->{'Contracts_setPA_1'} = '0';                 # No
    $self->{'Contracts_setInsEFT_1'} = '0';             # No
    $self->{'Contracts_setBillEFT_1'} = '0';            # No
  }
  elsif ( $inTable eq 'ClientPrAuthCDC' )
  {
    my $ClientID = $self->{'Client_ClientID_1'};
#warn qq|setDefaults: ClientPrAuthCDC: ClientID=${ClientID}\n|;
#foreach my $f ( sort keys %{$self} ) { warn qq|self: $f=$self->{$f}\n|; }
    my $TransType = DBA->getPrAuthTrans($self,$ClientID);
    my ($TransDate,$TransTime) = DBA->getPrAuthTransDT($self,$ClientID,$self->{TODAY});
    $self->{'ClientPrAuthCDC_TransType_1'} = $TransType;
    $self->{'ClientPrAuthCDC_TransDate_1'} = $TransDate;
    $self->{'ClientPrAuthCDC_TransTime_1'} = $TransTime;
    $self->{'ClientPrAuthCDC_Status_1'} = 'New';
    $self->{'ClientPrAuthCDC_StatusDate_1'} = DBUtil->Date();
#   repeat from setDefaults->ClientPrAuth...
    $self->{'ClientPrAuth_EffDate_1'} = $TransDate;
    my $InsID = $self->{'Insurance_InsID_1'};
    $PAgroup = CDC->calcPG($self,$ClientID,$InsID);
    my ($months,$days) = DBA->calcLOS($self,$InsID,$PAgroup);
    $self->{'ClientPrAuth_PAgroup_1'} = $PAgroup;
    $self->{'ClientPrAuth_ExpDate_1'} = DBUtil->Date($TDate,$months,$days);
    $self->{'ClientPrAuth_LOS_1'} = $months;
#my $kkk = CDC->required($self,$self->{'Insurance_InsID_1'});
#warn qq|setDefaults: InsID=${'InsID'}, required=${kkk}\n|;
    $self->{'ClientPrAuthCDC_CDCOK_1'} = $ClientID eq 'new' ? 1 : CDC->required($self,$InsID) ? 0 : 1;
  }
  elsif ( $inTable eq 'ClientDischargeCDC' )
  {
    my $ClientID = $self->{'Client_ClientID_1'};
#warn qq|setDefaults: ClientDischargeCDC: ClientID=${ClientID}\n|;
    # as of last note...
    my $qTreatment = qq|select * from Treatment where ClientID='$self->{Client_ClientID}' order by ContLogDate desc|;
    my $sTreatment = $dbh->prepare($qTreatment);
    $sTreatment->execute() || $self->dberror($qTreatment);
    my $rTreatment = $sTreatment->fetchrow_hashref;
    $sTreatment->finish();
    $self->{'ClientDischargeCDC_TransDate_1'} = $rTreatment->{'ContLogDate'};
    $self->{'ClientDischargeCDC_TransTime_1'} = $rTreatment->{'ContLogBegTime'};
    $self->{'ClientDischargeCDC_TransType_1'} = '60';     # Discharge - Complete
    $self->{'ClientDischargeCDC_Status_1'} = 'New';
    $self->{'ClientDischargeCDC_StatusDate_1'} = DBUtil->Date();
    $self->{'ClientDischargeCDC_CDCOK_1'} = 0;
  }

  ####################################
  # set these defaults.
  ####################################
  my $TableFieldDefs = DBA->getFieldDefs($self,$inTable);
  my $fld = 'ClientID'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) && $self->{$key} eq '' )
  { $self->{$key} = $self->{Client_ClientID}; }
  my $fld = 'CreateProvID'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) ) { $self->{$key} = $self->{LOGINPROVID}; }
  my $fld = 'CreateDate'; $key = $inTable . '_' . $fld . '_1';
  if ( exists($TableFieldDefs->{$fld}) ) { $self->{$key} = $self->{TODAY}; }
#foreach my $f ( sort keys %{$self} ) { warn qq|self: $f=$self->{$f}\n|; }
  return(1); 
}
sub TBLselect
{
  my $self = shift;
  my ($inTable, $id, $val, $inorder) = @_;
warn qq|DBForm: TBLselect: WARN-DBFORM\n| if ( $DEBUG );

  my $AccFunc = myDBI->getTableConfig($inTable,'ACCESS');
#warn "BEGIN: TBLselect: inTable=$inTable, id=$id, val=$val, AccFunc=$AccFunc\n";
  SysAccess->verify($self,$AccFunc) || $self->error("Access DENIED to ${inTable} (TBLselect)");

  my $dbh = $self->dbconnect;
  my $ID = myDBI->getTableConfig($inTable,'RECID');
  my $order = $inorder eq '' ? qq|order by ${ID} desc| : $inorder;
  my $q = qq|select * from ${inTable} where ${id}='${val}' $order|;
  my $s = $dbh->prepare($q);
#warn qq|TBLselect: q=$q\n|;
  $s->execute || $self->dberror($q);
  my $idx = 0;
  $self->{"${inTable}_${id}_1"} = ${val};
  while ( my $r = $s->fetchrow_hashref )
  { $idx++; 
#    map { $self->{"${inTable}_${_}_${idx}"} = $r->{${_}} } keys %$r;
    foreach my $f ( keys %{ $r } ) 
    { $key = ${inTable} . "_" . ${f} . "_" . ${idx};
#warn qq|TBLselect: $f=$r->{$f}\n|;
      $self->{$key} = $r->{$f};
      $self->{$key} = '' if ( $f =~ /date/i && $self->{$key} eq '0000-00-00' );
#warn qq|TBLselect: $key=$self->{$key}\n|;
    }
  }
  $s->finish();
  return($self);
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
  my ($self,$skip) = @_;

warn qq|DBForm: TMPread: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|\n\nTMPread: CHECK skip:\n|;
#foreach my $f ( sort keys %{$skip} ) { warn qq|skip: $f=$skip->{$f}\n|; }
  if ( exists($self->{'FORMID'}) )
  {
    my $pathname = $self->{DOCROOT} . '/tmp/' . $self->{LOGINID} . '_' . $self->{'FORMID'};
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
#warn qq|TMPread: CHECK skip-${key} IF :$skip->{$key}:\n|;
          $self->{$key} = $value if ( ! $skip->{$key} ); 
          $keyflag = 1; 
        }
        else { $value .= $_; }
      }
      close(TEMPLATE);
    }
  }
  return($self);
}
############################################################################
# WRITES OUT DATA SESSION TEMPLATE in /tmp/
# Arguments: $htmlname      --  name of html file
#            %skip          --  Flag field set so we don't write to template
# The variables in the self associative array (SQL database read) are saved
#   in a session template to be used by other html pages if needed.  A random
#   'session id' number is generate once per session (or SQL update) and
#   tracked by a hidden variable within the html page ('SessionID').
############################################################################
sub TMPwrite
{
  my ($self, $skip) = @_;

warn qq|DBForm: TMPwrite: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|\n\nTMPwrite CHECK skip:\n|;
#foreach my $f ( sort keys %{$skip} ) { warn qq|skip: $f=$skip->{$f}\n|; }

# Gen a NEW FORMID.
  my $FORMID = $self->getFORMID;
  $self->{'FORMID'} = $FORMID;
  my $hidden .= qq|<INPUT TYPE="hidden" NAME="FORMID" VALUE="${FORMID}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="mlt" VALUE="$self->{mlt}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="LINKID" VALUE="$self->{LINKID}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$self->{misLINKS}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="NONAVIGATION" VALUE="$self->{NONAVIGATION}">\n|;

  my $data_vars = qq|OPENTABLES\n$self->{'OPENTABLES'}\n<EOT>\n|;
  foreach my $t ( split(/,/,$self->{'OPENTABLES'}) )
  { $data_vars .= qq|OPENTABLE:${t}\n1\n<EOT>\n|; }

  foreach $key ( sort keys %{ $self } )
  { 
    if ( !defined($skip->{$key}) && $key =~ /(.+?)_(.+?)_(\d+)/ )
    {
      my $open = 'OPENTABLE:' . $1; 
      if ( $self->{$open} )
      { $data_vars .= qq|${key}\n$self->{$key}\n<EOT>\n|; }
    }
  }
  my $pathname = $self->{DOCROOT} . '/tmp/' . $self->{LOGINID} . '_' . $FORMID;
  if (!open(TEMPLATE, ">$pathname")) 
  { $self->error("Can't open $self->{'LOGINID'}_${FORMID} ($!)."); }
  print TEMPLATE $data_vars;
  close(TEMPLATE);

  return($hidden);
}

sub getFORMID()
{
  my $self = shift;
warn qq|DBForm: getFORMID: WARN-DBFORM\n| if ( $DEBUG );
  my $dbh = $self->dbconnect;
  my $q = qq|insert into FormID values(NULL, 'MIS')|;
  my $s = $dbh->prepare($q);
  $s->execute || $self->dberror($q);
  my $NewID = $s->{mysql_insertid};
  if($NewID % 3000 == 0)
  { $q = qq|delete from FormID where ID < ${NewID}|;
    $s = $dbh->prepare($q);
    $s->execute || $self->dberror($q);
  }
  $s->finish();
#  $NewID .= 'A';
  return($NewID);
}
sub setIDs
{
  my ($self,$table,$id) = @_;
warn qq|DBForm: setIDs: WARN-DBFORM\n| if ( $DEBUG );
  return('') if ( $table eq '' );
  return('') if ( $id eq '' );
#warn qq|DBForm:setIDs: table=$table, id=$id\n|;
  my $RECID = myDBI->getTableConfig($table,'RECID');
  my $q = qq|select * from ${table} where ${RECID}='${id}'|;
  my $s = $dbh->prepare($q);
  $s->execute() || $self->dberror($q);
  my $r = $s->fetchrow_hashref;
  $self->{"${table}_${RECID}"} = $r->{$RECID};
#warn qq|first: ${table}-${RECID}: $self->{"${table}_${RECID}"} = $r->{$RECID};\n|;
  my $DETID = myDBI->getTableConfig($table,'DETAILID');
#warn qq| next: DETID=${DETID}, VAL=$r->{$DETID}\n|;
  my $hdrtable = $table;           # find HeaderTable for Table
  while ( defined(myConfig->tbl($hdrtable,'HEADERTABLE')) )
  { 
    $hdrtable = myConfig->tbl($hdrtable,'HEADERTABLE');
    $RECID = myDBI->getTableConfig($hdrtable,'RECID');
#warn qq| next: hdrtable=${hdrtable}, RECID=${RECID}, VAL=$r->{$DETID}\n|;
    my $q = qq|select * from ${hdrtable} where ${RECID}='$r->{$DETID}'|;
    my $s = $dbh->prepare($q);
    $s->execute() || $self->dberror($q);
    $r = $s->fetchrow_hashref;
    $self->{"${hdrtable}_${RECID}"} = $r->{$RECID};
#warn qq| next: ${hdrtable}-${RECID}: $self->{"${hdrtable}_${RECID}"} = $r->{$RECID};\n|;
    $DETID = myDBI->getTableConfig($hdrtable,'DETAILID');
#warn qq| next: DETID=${DETID}, VAL=$r->{$DETID}\n|;
  }
  $s->finish();
  return($self);
}
sub setTable
{
  my ($self,$inTable,$record,$idx) = @_;
warn qq|DBForm: setTable: WARN-DBFORM\n| if ( $DEBUG );
  $i = $idx ? $idx : 1;
  foreach my $f ( keys %{ $record } ) 
  { 
    my $key = ${inTable} . "_" . ${f} . "_" . ${i};
    $self->{$key} = $record->{$f};
#warn qq|setTable: ${key}=$self->{$key}\n|;
  }
  return($self);
}
# execute function as redirect
sub exFunc
{
  my ($self,$string,$record) = @_;
warn qq|DBForm: exFunc: WARN-DBFORM\n| if ( $DEBUG );
warn qq|DBForm: exFunc: string=$string\n| if ( $DEBUG );
  ####################################
  #   parse out ...
  #     1: library/module name 
  #     2: function name 
  #     3: function arguments 
  #     4: value to return 
  ####################################
  my ($module_name, $rest) = split(/->/,$string);
  my ($function_name, $function_arguments) = split(/\(/,$rest,2);
  my ($function_arguments, $return_string) = split(/\)/,$function_arguments,2);

  ####################################
  #   neg means take the negative of function results.
  #   functions begin with a '!' (not)
  ####################################
  my $neg = 0;
  if ( substr($module_name,0,1) eq '!' )
  { $neg = 1; $module_name = substr($module_name,1); }

  ####################################
  #   acc means this is a possible access validation (ABORT).
  #   this is to check if user has access to html page.
  #   if module begins with a '*'
  #   the * in front of a module simply means this is an abort situation
  #     with the 'Access Denied' message if the client does not pass.
  ####################################
  my $acc = 0;
  if ( substr($module_name,0,1) eq '*' )
  { $acc = 1; $module_name = substr($module_name,1); }
  $module_name=$self if ( $module_name eq 'DBForm' );

  ####################################
  # create argument array.
  ####################################
  @function_args = ();
  foreach my $arg ( split(/\+/,$function_arguments) ) 
  {
    if ( $arg eq '%form' ) { push(@function_args,$self); }
    elsif ( $arg eq '%record' ) { push(@function_args,$record); }
    else { push(@function_args,$arg); }
  }

  ####################################
  #   add a null argument if nefuncval...
  #   allows for func;arg1,;lineofhtml (,; meaning null argument)
  ####################################
  push(@function_args,'') if (substr($function_arguments,-1) eq '+');

  ####################################
  # now execute the function found
  #   if this was an Access allowed function call (function begins with *)
  #     check for negative and returned value true
  #     or check for returned value false
  #     else we passed Access test.
  #   otherwise we will output or not output the line of html following function
  #     check for negative and returned value true
  #     or check for returned value false
  ####################################
#warn "SET FUNCTION: module_name=$module_name, function_arguments=$function_arguments\n";
  my $funcval = $module_name->$function_name(@function_args);
# 'return0' only needed if possible funcval can be 0 and is not a test (neg) so a 0 can be returned.
  my $rtnval = '';
#warn "SET FUNCTION: funcval=$funcval, return_string=$return_string, acc=$acc, neg=$neg\n";
#foreach my $arg ( @function_args ) { warn qq|function_args=${arg}\n|; }
#warn qq|SET FUNCTION: 1=|.$function_args[1].qq|\n|;
  (my $view = $self->{'view'}) =~ s/\.cgi//;
  if ( $acc && $neg && $funcval ) 
  { $self->error("Access Denied to Page<BR>(${view})<BR>($function_args[1])"); }
  elsif ( $acc && !$neg && !$funcval ) 
  { $self->error("Access Denied to Page<BR>(${view})<BR>($function_args[1])"); }
  elsif ( $acc )
  { $acc = 0; }                               # just to do nothing
  elsif ( $return_string eq 'return0' )       # this is needed incase funcval is 0 or ''
  { $rtnval = $funcval; }
  elsif ( $neg )
  { $rtnval = $return_string eq '' ? !$funcval : $return_string; }
  elsif ( !$neg && $funcval )                 # will return funcval or return_string, but not 0
  { $rtnval = $return_string eq '' ? $funcval : $return_string; }
#warn "SET FUNCTION: rtnval=$rtnval\n";
  return($rtnval);
}
############################################################################
# change all routines to call myDBI DIRECTLY...
sub error         # call myForm->
{ 
  my ($self,$msg) = @_; 
warn qq|DBForm--: error: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|CALLING myDBI-error\n|; 
  $myForm::FORM = $self;    # $form = $myForm::FORM inside dberror
  myDBI->error($msg); 
  return(1); 
}
sub dberror       # call myForm->
{ 
  my ($self,$msg) = @_; 
warn qq|DBForm--: dberror: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|CALLING myDBI-dberror\n|; 
  $myForm::FORM = $self;    # $form = $myForm::FORM inside dberror
  myDBI->dberror($msg); 
  return(1); 
}
sub complete      # call myForm->
{ 
  my ($self,$msg) = @_; 
warn qq|DBForm--: complete-cleanup: WARN-DBFORM\n| if ( $DEBUG );
#warn qq|CALLING myDBI-cleanup\n|; 
  myDBI->cleanup($msg,$dbh);           # dbh handle was set in sub dbconnect (not my)
  return(1); 
}
############################################################################
sub genLink       # call myForm->   can't elimnate till all call myForm->new()
{
  my ($self, $inTable, $view, $id) = @_;
warn qq|DBForm--: genLink: WARN-DBFORM\n| if ( $DEBUG );
warn qq|DBForm--: genLink: inTable=${inTable}, view=${view}, id=${id}\n| if ( $DEBUG );
foreach my $f ( sort keys %{$self} ) { warn qq|genLink self: $f=$self->{$f}\n|; }
  $myForm::FORM = $self;
  my $url = myForm->genLink($inTable,$view,$id);
  $self = $myForm::FORM;
  return($url);
}
#sub genLinkID     # skip myForm->
#{
#  my ($self, $table, $id) = @_;
#  return('') if ( $table eq '' );
#  my $url;
#warn qq|DBForm:genLinkID:BEGIN: table=$table, id=$id\n|;
#  my $ID = myDBI->getTableConfig($table,'RECID');
#  my $key = qq|${table}_${ID}|;
#  if ( $id eq '' )
#  {
#    my $fld = $self->{$key} eq '' ? "${table}_${ID}_1" : $key;
#    my $val = $self->{$fld} eq '' ? $self->genID($table) : $self->{$fld};
##    my $val = $self->{$fld};
#    $url = "${key}=${val}";
#  }
#  else { $url = "${key}=${id}"; }
#warn qq|DBForm:genLinkID:END: url=$url\n|;
#  return($url);
#}
#############################################################################
## this routine was created to make sure id is 'new' or some value.
# for use in going to next screen/record in series, w/o having the id yet.
## it will return first id found, if multiples, so not to be used where
##   multiple detail records exist for header record.
#############################################################################
#sub genID         # skip myForm->
#{
#  my ($self, $table) = @_;
#  my $dbh = $self->dbconnect;
#  my $HDRTABLE = myDBI->getTableConfig($table,'HEADERTABLE');
#  return('') if ( $table eq '' || $HDRTABLE eq '' );
#  my $HDRRECID = myDBI->getTableConfig($HDRTABLE,'RECID');
#  my $HDRIDVAL = $self->{"${HDRTABLE}_${HDRRECID}"};
#  my $DETID = myDBI->getTableConfig($table,'DETAILID');
#  my $RECID = myDBI->getTableConfig($table,'RECID');
#  my $q = qq|select ${RECID} from ${table} where ${DETID}='${HDRIDVAL}'|;
##warn qq|genID=$q\n|;
#  my $s = $dbh->prepare($q);
#  $s->execute() || $self->dberror($q);
#  my ($rtnid) = $s->fetchrow_array;
#  $s->finish();
#  return($rtnid eq '' ? 'new' : $rtnid);
#}
sub pushLINK      # call myForm->
{
  my ($self,$LINKID) = @_;
warn qq|DBForm--: pushLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my $url = myForm->pushLINK($LINKID);
  $self = $myForm::FORM;
  return();
}
sub popLINK       # call myForm->
{
  my ($self,$exe) = @_;
warn qq|DBForm--: popLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my $url = myForm->popLINK($exe);
  $self = $myForm::FORM;
  return($url);
}
# fwdTABLE is used when mis.cgi is called to have the next url to go to in Links.
sub saveLINK      # call myForm->
{
  my ($self, $pgm, $url) = @_;
warn qq|DBForm--: saveLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my $NewID = myForm->saveLINK($pgm,$url);
  $self = $myForm::FORM;
  return($NewID);
}
sub readLINK      # call myForm->
{
  my ($self,$id) = @_;
warn qq|DBForm--: readLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my ($ProvID,$pgm,$url,$browser,$ip) = myForm->readLINK($id);
  $self = $myForm::FORM;
  return($ProvID,$pgm,$url,$browser,$ip);
}
sub saveHIST      # call myForm->
{
  my ($self) = @_;
warn qq|DBForm--: saveHIST: WARN-DBFORM\n| if ( $DEBUG );
#foreach my $f ( sort keys %{$self} ) { warn qq|saveHIST self: $f=$self->{$f}\n|; }
  $myForm::FORM = $self;
  my $NewID = myForm->saveHIST();
  $self = $myForm::FORM;
  return($NewID);
}
sub updLINK       # call myForm->
{
  my ($self, $lid, $old, $new) = @_;
warn qq|DBForm--: updLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my ($ProvID,$pgm,$url,$browser,$ip) = myForm->updLINK($lid,$old,$new);
  $self = $myForm::FORM;
  return($ProvID,$pgm,$url,$browser,$ip);
}
sub genLINK       # call myForm->
{
  my ($self, $pgm) = @_;
warn qq|DBForm--: genLINK: WARN-DBFORM\n| if ( $DEBUG );
  $myForm::FORM = $self;
  my $url = myForm->genLINK($pgm);
  $self = $myForm::FORM;
  return($url);
}
############################################################################
1;
