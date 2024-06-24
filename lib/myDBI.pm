package myDBI;
use myConfig;
use DBI;
my $CONNECTIONS = ();
############################################################################
sub dbconnect               # this is the new dbh.
{
  my ($self,$dbname,$user,$pswd) = @_;

#warn qq|myDBI: ENTER: dbconnect: $dbname=${dbname}, user=${user}, pswd=${pswd}\n|;
#warn qq|CHECK CONNECTIONS 1: \n|;
#foreach my $f ( sort keys %{$CONNECTIONS} ) { foreach my $a ( sort keys %{$CONNECTIONS->{$f}} ) { warn qq|CONNECTIONS: $f-$a=$CONNECTIONS->{$f}->{$a}\n|; } }
  my $dbh;
  if ( $CONNECTIONS->{$dbname}->{'CONNECT'} )
  { 
$dbh = $CONNECTIONS->{$dbname}->{'HANDLE'};
#warn qq|myDBI: dbconnect: ALREADY GOT CONNECTION...\n|; 
  }
  else
  {
    my $u = $user eq '' ? myConfig->dbu($dbname) : $user;
    my $p = $pswd eq '' ? myConfig->dbp($dbname) : $pswd;
#warn qq|myDBI: dbconnect: RECONNECT: u=${u}, p=${p} db=${dbname}\n|; 
	  

    $dbh = DBI->connect("DBI:mysql:${dbname}",$u,$p, { mysql_enable_utf8mb4 => 1 }) || die myDBI->dberror("myDBI:dbconnect");

    $dbh->{RaiseError} = 1;
    $CONNECTIONS->{$dbname}->{CONNECT} = 1;
    $CONNECTIONS->{$dbname}->{HANDLE} = $dbh;
  }
#warn qq|CHECK CONNECTIONS 2: \n|;
#foreach my $f ( sort keys %{$CONNECTIONS} ) { foreach my $a ( sort keys %{$CONNECTIONS->{$f}} ) { warn qq|CONNECTIONS: $f-$a=$CONNECTIONS->{$f}->{$a}\n|; } }
  return($dbh);
}
sub cleanup 
{
  my ($self,$errmsg,$dbhandle) = @_;
#warn qq|myDBI: cleanup: errmsg=${errmsg}, dbhandle=${dbhandle}\n|;
  my $cnt = 0;
#warn qq|CHECK CONNECTIONS 1: \n|;
#foreach my $f ( sort keys %{$CONNECTIONS} ) { foreach my $a ( sort keys %{$CONNECTIONS->{$f}} ) { warn qq|CONNECTIONS: $f-$a=$CONNECTIONS->{$f}->{$a}\n|; } }
  foreach my $dbname ( sort keys %{$CONNECTIONS} )
  {
    $cnt++;
    my $dbh = $CONNECTIONS->{$dbname}->{HANDLE};
    $dbh->disconnect() if ( $dbh );
    delete $CONNECTIONS->{$dbname};
  }
  $cnt++ if ( $dbhandle );
  $dbhandle->disconnect() if ( $dbhandle );
  die "ERROR: $errmsg (myDBI::cleanup)\n" if ( $errmsg );
#warn qq|myDBI: cleanup: cnt=${cnt}\n|;
#warn qq|CHECK CONNECTIONS 2: \n|;
#foreach my $f ( sort keys %{$CONNECTIONS} ) { foreach my $a ( sort keys %{$CONNECTIONS->{$f}} ) { warn qq|CONNECTIONS: $f-$a=$CONNECTIONS->{$f}->{$a}\n|; } }
  return(1);
}
sub error 
{
  my ($self,$msg) = @_;
  my $form = $myForm::FORM;
  if ($ENV{HTTP_USER_AGENT}) 
  {
    $msg =~ s/\n/<BR>/g;
    print qq|Content-Type: text/html

<HTML>
<HEAD> <TITLE>${msg}</TITLE> </HEAD>

  <BODY BGCOLOR="black" LINK="white" VLINK="white" >
  <DIV ALIGN="center" >
  <FONT SIZE="+3" COLOR="red" ><B>Access Error</B></FONT>
  <P>
  <TABLE WIDTH="50%" BGCOLOR="red" BORDER="5" CELLSPACING="0" >
    <TR VALIGN="center" >
      <TD ALIGN="center" ><FONT SIZE="+2" ><B>${msg}</B></FONT></TD>
    </TR>
  </TABLE>
  <P>
  <TABLE WIDTH="50%" BORDER="0" CELLSPACING="0" >
    <TR VALIGN="center" >
      <FONT SIZE="+2" >
      <TD ALIGN="left" ><A HREF="$form->{HTTPSERVER}" TARGET="_top" >Home</A></TD>
      <TD ALIGN="right" ><A HREF="/cgi/bin/mis.cgi?misPOP=1&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}" TARGET="_top" >Back</A>
      </FONT>
    </TR>
  </TABLE>
  </BODY>
</HTML>
|;
  }
  else
  {
    if ($form->{error_function}) 
    { &{ $form->{error_function} }($msg); } 
  }

  my $LOGDIR = myConfig->cfg('LOGDIR');
  open AERR, ">>${LOGDIR}/access_errors" or warn "Can't open errors file ($!).";
  $now = localtime();
  print AERR qq|\n$form->{LOGINUSERNAME}: ${msg} @ $now\n|;
  foreach my $f ( sort keys %{$form} ) { print AERR "$f=$form->{$f}\n"; }
  close(AERR);
  myDBI->cleanup($msg);
  exit;
}
sub dberror 
{
  my ($self,$msg) = @_;
  myDBI->error("$msg\n".$DBI::errstr);
}
############################################################################
sub getFORMID()
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|insert into FormID (Page) values('MIS')|;
  my $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  my $NewID =  $s->{mysql_insertid};
  if($NewID % 3000 == 0)
  {
    $q = qq|delete from FormID where ID < ${NewID}|;
    $s = $dbh->prepare($q);
    $s->execute || $self->dberror($q);
  }
  $s->finish();
#  $NewID .= 'A';
  return($NewID);
}
sub getIDX()
{
  my ($self,$Type) = @_;
  my $cdbh = myDBI->dbconnect('okmis_config');
  my $s = $cdbh->prepare("insert into idxFILE values(NULL,'${Type}')");
  $s->execute || die "ERROR: insert into idxFILE!\n";
  my $NewID =  $s->{mysql_insertid};
  if($NewID % 30 == 0)
  { 
    $s = $cdbh->prepare("delete from idxFILE where ID < ${NewID}");
    $s->execute || die "ERROR: delete from idxFILE";
  }
  $s->finish();
#warn qq|NewID=$NewID\n|;
  return($NewID);
}
############################################################################
# WRITES OUT DATA SESSION TEMPLATE in /tmp/
# Arguments: $htmlname      --  name of html file
#            %skip          --  Flag field set so we don't write to template
# The variables in the self associative array (SQL database read) are saved
#   in a session template to be used by other html pages if needed.  A random
#   'session id' number is generate once per session (or SQL update) and
#   tracked by a hidden variable within the html page ('xxx').
############################################################################
sub TMPwrite
{
  my ($self,$form,$skip) = @_;
#warn qq|myDBI: ENTER: TMPwrite: skip=${skip}\n|;
# Gen a NEW FORMID.
  $form->{'FORMID'} = myDBI->getFORMID($form);
  my $hidden .= qq|<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{'FORMID'}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{'mlt'}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{'LINKID'}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{'misLINKS'}">\n|;
  $hidden .= qq|<INPUT TYPE="hidden" NAME="NONAVIGATION" VALUE="$form->{'NONAVIGATION'}">\n|;

  my $data_vars = qq|OPENTABLES\n$form->{'OPENTABLES'}\n<EOT>\n|;
  foreach my $t ( split(/,/,$form->{'OPENTABLES'}) )
  { $data_vars .= qq|OPENTABLE:${t}\n1\n<EOT>\n|; }

  foreach $key ( sort keys %{ $form } )
  { 
    if ( !defined($skip->{$key}) && $key =~ /(.+?)_(.+?)_(\d+)/ )
    {
      my $open = 'OPENTABLE:' . $1; 
      if ( $form->{$open} )
      { $data_vars .= qq|${key}\n$form->{$key}\n<EOT>\n|; }
    }
  }
  my $pathname = $form->{DOCROOT}.'/tmp/'.$form->{LOGINID}.'_'.$form->{'FORMID'};
  if (!open(TEMPLATE, ">$pathname")) 
  { myDBI->error("Can't open $form->{'LOGINID'}_$form->{'FORMID'} ($!)."); }
  print TEMPLATE $data_vars;
  close(TEMPLATE);
  return($hidden);
}
############################################################################
sub getTopTable
{
  my ($self,$inTable) = @_;
  my $hdrtable = $inTable;
  while ( defined(myConfig->tbl($hdrtable,'HEADERTABLE')) )
  { $hdrtable = myConfig->tbl($hdrtable,'HEADERTABLE'); }
  return($hdrtable);
}
sub getDetTables
{
  my ($self,$inTable) = @_;
  return(@{ myConfig->tbl($inTable,'DETAILTABLES') });
}
sub getTableLogFlag
{
  my ($self,$form,$inTable) = @_;
  return(0) if ( $form->{"NOLOG"} );              # did logging get turned off?
  return(0) if ( $form->{"${inTable}_NOLOG"} );   # did logging get turned off?
  my $flag = myConfig->tbl($inTable,'LOG') eq 'yes' ? 1 : myConfig->tbl($inTable,'LOG') == 1 ? 1 : 0;
  return($flag);
}
# return a generic variable from TABLES config
sub getTableConfig
{
  my ($self,$inTable,$Var) = @_;
  return(myConfig->tbl($inTable,$Var));
}
# execute function as redirect
sub exFunc
{
  my ($self,$form,$string,$record) = @_;
#warn qq|myDBI: exFunc: string=$string\n|;
#foreach my $f ( sort keys %{$form} ) { warn "myDBI: exFunc: form-$f=$form->{$f}\n"; }
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
  #$module_name=$form if ( $module_name eq 'DBForm' );
  #$module_name=$form if ( $module_name eq 'myForm' );

  ####################################
  # create argument array.
  ####################################
  @function_args = ();
  foreach my $arg ( split(/\+/,$function_arguments) ) 
  {
    if ( $arg eq '%form' ) { push(@function_args,$form); }
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
  (my $view = $form->{'view'}) =~ s/\.cgi//;
  if ( $acc && $neg && $funcval ) 
  { myDBI->error("Access Denied to Page<BR>(${view})<BR>($function_args[1])"); }
  elsif ( $acc && !$neg && !$funcval ) 
  { myDBI->error("Access Denied to Page<BR>(${view})<BR>($function_args[1])"); }
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
1;
