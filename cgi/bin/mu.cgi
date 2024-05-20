#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use login;
use DBA;
use myHTML;
use DBUtil;
use gXML;
use XML::Simple;
#use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
#foreach my $f ( sort keys %{$form} ) { warn "mu: form-$f=$form->{$f}\n"; }
my $cdbh = $form->connectdb('okmis_config');
my $target = $form->{'target'};
my $value = $form->{'value'};
my $size = $form->{multiple} > 1 ? qq|SIZE="$form->{multiple}"| : '';
my $multiple = $form->{multiple} > 1 ? qq|MULTIPLE| : '';
my $SELVALUES = ();
#warn qq|popup: method=$form->{method}\n|;
#warn qq|popup: target=$form->{target} / ${target}\n|;
#warn qq|popup: value=$form->{value} / ${value}\n|;
#warn qq|popup: size=$form->{multiple} / ${size}\n|;
#warn qq|popup: multiple=${multiple}\n|;

my ($html,$out) = ('','');
if ( $form->{method} eq 'searchClient' ) { $html = main->searchClient(); }
elsif ( $form->{method} eq 'setClientDetails' ) { $html = main->setClientDetails($form); }
else { $html = main->wrapper(); }
#warn qq|mu: html=${html}\n|;
print $html;
$cdbh->disconnect();
$form->complete();
exit;

############################################################################

############################################################################
sub ierr
{
  my ($self,$target,$err) = @_;
#warn qq|ierr: target=$target\n|;
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
  return($out);
}
sub selmatch
{
  my ($self,$form,$dbh,$sql,$value,$ID,@Text) = @_;
#foreach my $id ( @Text ) { warn qq|selmatch: Textid=${id}\n|; }
#warn qq|selmatch: sql=$sql\n|;
  return('<OPTION SELECTED VALUE="">unselected') if ( $value eq '' );
  my $out = qq|<OPTION VALUE="">unselected\n|;
  my $s = $dbh->prepare($sql);
  foreach my $id ( split(chr(253),$value) )
  {
#warn qq|selmatch: id=$id\n|;
    $s->execute($id) || $form->dberror($sql);
    if ( my $r = $s->fetchrow_hashref )
    {
#foreach my $f ( sort keys %{$r} ) { warn ": r-$f=$r->{$f}\n"; }
      $SELVALUES->{$r->{$ID}} = 1;             # globally marked.
      $out .= qq|<OPTION SELECTED VALUE="$r->{$ID}">|;
      $out .= main->seltext($r,@Text);
      $out .= "\n";
    }
  }
  $s->finish();
  return($out);
}
sub seloptions
{
  my ($self,$form,$dbh,$sql,$str,$ID,@Text) = @_;
  return() if ( $str eq '' );
  my $out = '';
#warn qq|seloptions: sql=$sql\n|;
  my $s = $dbh->prepare($sql);
  $s->execute() || $form->dberror($sql);
  while ( my $r = $s->fetchrow_hashref )
  { 
#warn qq|seloptions: ID=$r->{$ID}= \n|;
    next if ( $SELVALUES->{$r->{$ID}} );      # globally marked.
    $out .= qq|<OPTION VALUE="$r->{$ID}">|;
    $out .= main->seltext($r,@Text);
  }
  $s->finish();
  return($out);
}
sub seltext
{
  my ($self,$r,@Text) = @_;
  my $out = '';
# not sure what $last is for? but if first $r val is null then rest of $out is null
  my $last = 'notonfirst';  
  foreach my $fld ( @Text )
  {
#warn qq|last=${last}\nfld=${fld}=$r->{$fld}= \n|;
    if ( $fld eq ':' ) { $out .= qq|${fld} |; }
    elsif ( $fld eq '[' ) { $out .= qq| ${fld}|; }
    elsif ( $fld eq ']' ) { $out .= qq|${fld}|; }
    elsif ( $last eq '' ) { null; }
    elsif ( $fld eq ';' ) { $out .= qq|${fld} |; }
    elsif ( $fld eq ',' ) { $out .= qq|${fld} |; }
    else { $out .= $r->{$fld}; $last = $r->{$fld}; }
#warn qq|last=${last}\nout=${out}= \n|;
  }
  $out .= "\n";
#warn qq|done: out=${out}= \n|;
  return($out);
}
sub searchClient
{
  my ($self) = @_;
  (my $pattern = $form->{'pattern'}) =~ s/"//g;
  my $FOR = qq| and ( LName LIKE "%${pattern}%" or FName LIKE "%${pattern}" )| if ( $pattern ne '' );
  (my $dpattern = $form->{'dob'}) =~ s/"//g;
  my $DOB = qq| and DOB = "${dpattern}" | if ( $dpattern ne '' );
#warn qq|For=${FOR}\n|;
#warn qq|DOB=${DOB}\n|;
  @Display = ('LName',',','FName',',','Addr1',',','City',',','ST','[','DOB',']');
  my $opts = main->selmatch($form,$dbh,"select * from Client where ClientID=?",$value,'ClientID',@Display);
  my $q = qq|select * from Client where ClientID is not null ${FOR} ${DOB} order by LName, FName|;
#warn qq|q=$q\n|;
  my $chk = $pattern.$dpattern;
  $opts .= main->seloptions($form,$dbh,$q,$chk,'ClientID',@Display);
  my $list = qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
#warn qq|list=$list\n|;
  $out = $err eq '' ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
| : main->ierr($target,$err);
  my $html =  qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>\n${out}</response>
|;
  return($html);
}
sub setClientDetails
{
  my ($self,$form) = @_;
  my $xml = qq|<?xml version="1.0" encoding="utf-8"?>\n|;
  my $dbh = $form->dbconnect();
##
# we ONLY select 1 Note to get the last visit for the xml
#  since we setXML by TrID.
##
  my $sTreatment = $dbh->prepare("select * from Treatment where ClientID=? order by ContLogDate desc");
  my ($where,$join) = ('','');
  foreach my $id ( split(',',$form->{'IDs'}) ) { $where .= qq| ${join} ClientID=${id}|; $join='or'; }
#warn qq|setClientDetails: IDs=$form->{IDs}\n|;
#warn qq|setClientDetails:\nwhere=${where}\n|;
  my $sClient = $dbh->prepare("select * from Client where ${where} order by LName, FName");
  $sClient->execute();
  while ( my $rClient = $sClient->fetchrow_hashref )
  {
#warn qq|setClientDetails: ClientID=$rClient->{ClientID}\n|;
    $sTreatment->execute($rClient->{'ClientID'});
# ONLY 1 note...
    if ( my $rTreatment = $sTreatment->fetchrow_hashref )
    { $xml .= gXML->setXML($form,$rTreatment->{ProvID},$rClient->{ClientID},$rTreatment->{TrID},'','','CCDA nonulls'); }
    else { $xml .= '<Data>No Note Found!</Data>'; }
  }
#warn qq|xml=$xml\n|;
  $out = $err eq '' ? qq|
  <command method="setvalue">
    <target>showDetails</target>
    <value><![CDATA[${xml}]]></value>
  </command>
| : main->ierr($target,$err);
  my $html =  qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>\n${out}</response>
|;
  return($html);
}
sub wrapper
{
  my ($self) = @_;
  my $html = myHTML->newHTML($form,'Rollup CCDA','CheckPopupWindow noclock countdown_1') . qq|
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/pickDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function setURL(fieldname)
{
  //var obj = document.getElementById("MU").elements;
  var opts = [];
  var obj = document.MU.ClientID.options;
  for(var i = 0; i < obj.length; i++)
  { 
//alert('value='+obj[i].value); 
//alert('selected='+obj[i].selected); 
    if ( obj[i].selected )
    { opts.push(obj[i].value); }
  }
  opts.join(',');
//alert("opts="+opts);
  var url = '&IDs='+opts+'&mlt=$form->{mlt}';
//alert(url);
  callAjax('setClientDetails',this.value,'showDetails',url,'mu.cgi');
}
function validate(form)
{
  return true;
}
  \$.datepicker.setDefaults({ dateFormat: 'yy-mm-dd' });
  \$( function() { \$( "#datepicker1" ).datepicker(); } );
  \$( function() { \$( "#datepicker2" ).datepicker(); } );
</SCRIPT>

<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Rollup CCDA</TD> </TR>
</TABLE>
<FORM NAME="MU" ACTION="/cgi/bin/rest.cgi" METHOD="POST" >
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      Name <INPUT TYPE="text" NAME="CLIENTNAME" PLACEHOLDER="Name" >
      Date of Birth <INPUT TYPE="text" ID="datepicker1" NAME="DOB" VALUE="" PLACEHOLDER="yyyy-mm-dd" ></p>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BUTTON TYPE="button" ONCLICK="callAjax('searchClient',this.value,'selClient','&multiple=10&name=ClientID&pattern='+document.MU.CLIENTNAME.value+'&dob='+document.MU.DOB.value+'&mlt=$form->{mlt}','mu.cgi');" >Search</BUTTON>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Patients
      <SPAN ID="selClient"></SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <SELECT NAME="STATS" >,
        <OPTION VALUE="Demographics">Demographics
        <OPTION VALUE="Vitals">Vitals
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BUTTON TYPE="button" ONCLICK="setURL('ClientID');" >Get Patient Details</BUTTON>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Details
      <TEXTAREA NAME="showDetails" ID="showDetails" COLS="120" ROWS="22" WRAP="virtual" ONFOCUS="select()" >
      </TEXTAREA>
    </TD>
  </TR>
</TABLE>
  
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}">
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.MU.elements[0].focus();
callAjax('searchClient','','selClient','&multiple=10','mu.cgi');
</SCRIPT>
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;
  return($html);
}
#      <TEXTAREA NAME="showDetails" ID="showDetails" COLS="120" ROWS="22" WRAP="virtual" ONFOCUS="select()" >
#      </TEXTAREA>
############################################################################
