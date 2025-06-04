#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBI;
use myForm;
use DBA;
use DBUtil;
use myHTML;
use graphs;
use utils;

############################################################################
my $form = myForm->new();
$form->{'method'} = 'BilledvsIncome';    # default graph
$form->{'daterange'} = 'lastmonth' if ( $form->{'daterange'} eq '' );
$form = DBUtil->setDates($form);

#foreach my $f ( sort keys %{$form} ) { warn "graphs.cgi: 1: form-$f=$form->{$f}\n"; }
#warn qq|graphs.cgi: s=$form->{'s'}\n|;
$form = utils->writesid( $form, $form->{'s'} );

#foreach my $f ( sort keys %{$form} ) { warn "graphs.cgi: 2: form-$f=$form->{$f}\n"; }
my $dbh    = myDBI->dbconnect( $form->{'DBNAME'} );
my $javaor = "||";

############################################################################
if ( $form->{LOGINPROVID} == 91 ) {
    open OUT, ">C:/xampp/htdocs/src/debug/graphs.out"
      or die "Couldn't open file: $!";
    foreach my $f ( sort keys %{$form} ) {
        print OUT "graphs.cgi: form-$f=$form->{$f}\n";
    }
    close(OUT);
}

# Static date variables...
my $fdow = DBUtil->Date( $form->{FromDate}, 'dow' );
my $fdayname =
  ( Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday )[$fdow];
my $tdow = DBUtil->Date( $form->{ToDate}, 'dow' );
my $tdayname =
  ( Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday )[$tdow];

my $addSelection =
  DBA->withClinicProvider( $form, 'and', 'Client.clinicClinicID',
    'Treatment.ProvID' );
my $ReportHeader = DBA->withSelectionHeader($form);
my $chartname    = 'bar_chart';
my $ChartStyle   = qq||;
my ( $xLabel, $xFormat ) = ( 'Clinics', ',.d0' );
my ( $yLabel, $yFormat ) = ( 'Population', ',.d0' );
############################################################################
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;
my $MENU = myHTML->getHTML( $form, 'graph.menu', 1 );
my $html = myHTML->new(
    $form,
    'Millennium Graphs',
    'CheckPopupWindow SetD3lib',
    'STYLE="background-color: white"'
  )
  . qq|
<SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"></SCRIPT>
  <LINK REL="stylesheet" TYPE="text/css" HREF="/cgi/jcal/calendar-forest.css" >
  <LINK REL="stylesheet" TYPE="text/css" HREF="/src/cgi/css/StyleYearMonth.css"> 
  <SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/Utils.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-en.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-setup.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/vDate.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/vNum.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/YearMonth.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" >
function validate(form)
{
//alert("validate: daterange="+form.daterange);
  if (typeof form.daterange != "undefined")
  { 
    var stat = vDates(form);
//alert("validate: stat="+stat);
    if ( !stat )
    { return stat; }
  }
  gather_Form('theoptions','reset');
  return true;
}
function vDates(form)
{
  if ( isEmpty(form.daterange) )
  {
    if ( isEmpty(form.FromDate) )
    {
      if ( isEmpty(form.ToDate) )
      { return vOK(form.FromDate,"Please select a radio date button!\\nor From/To Dates!"); }
      else
      { return vOK(form.FromDate,"Please enter From Date with To Date!"); }
    }
    else
    {
      if ( isEmpty(form.ToDate) )
      { return vOK(form.ToDate,"Please enter To Date with From Date!"); }
    }
  }
  return true;
}
function clrObj(Date,form,name)
{
  var Obj = form[name];
  for(var i = 0; i < Obj.length; i++) 
  { Obj[i].checked = false; }
  return vDate(Date); 
}
function execute_script(id)
{
//alert("git: id="+id);
  var scripts = document.getElementById(id).getElementsByTagName("script");
  for( var i=0; i<scripts.length; i++ )
  {
//alert("text: "+scripts[i].innerText);
      eval(scripts[i].innerText);
  }
}
function gather_Form(id,reset)
{
  var val = "";
//alert("gatherForm: id="+id+" reset="+reset);
  var obj = document.getElementById(id).elements;
  for(var i = 0; i < obj.length; i++)
  {
//alert("gatherForm: i="+i+" type="+obj[i].type+" name="+obj[i].name+" value="+obj[i].value);
    if( obj[i].type == "text"   ${javaor} obj[i].type == "textarea" 
     ${javaor} obj[i].type == "hidden" ${javaor} obj[i].type == "password" )
    { val += "&"+obj[i].name+"="+obj[i].value; }
    else if ( obj[i].type == "select-one" ${javaor} obj[i].type == "select-multiple" )
    {
      for(var j = 0; j < obj[i].options.length; j++)
      {
        var opt = obj[i].options[j];
        if ( opt.selected )
        { val += "&"+obj[i].name+"="+opt.value; }
      }
    }
    else if ( obj[i].type == "checkbox" )    
    { val += "&"+obj[i].name+"="+obj[i].value; }
    else if ( obj[i].type == "radio" )
    { 
      if ( obj[i].checked )
      { val += "&"+obj[i].name+"="+obj[i].value; }
    }
//  else // button/submit
//alert("gatherForm: val="+val);
  }
//alert("gatherForm: END: val="+val);
// null method call will use method from saved sesid
  callAjax('',reset,'grapharea',val,'graphs.pl');
}
</SCRIPT>
<P>
<P>
<TABLE CLASS="list fullsize" >
  <TR ><TD CLASS="hdrtxt header" COLSPAN="2" >Data Visualization</TD></TR>
  <TR >
    <TD CLASS="numcol" >${CloseButton}</TD>
  </TR>
</TABLE>
<FORM NAME="GRAPHS" METHOD="POST" >
<TABLE CLASS="fullsize" > <TR><TD>${MENU}</TD></TR> </TABLE>
</FORM>
|;

# create/finish the graph from data...
my $data  = main->default_graph( $form, $addSelection );
my $parms = ();
$parms->{'function'} = $chartname;
$parms->{'style'}    = $ChartStyle;
$parms->{'title'}    = qq|${ReportHeader} Billed vs Income by Month|;
$parms->{'subtitle'} =
qq|Notes for ServiceDate from ${fdayname} $form->{FromDateD} - ${tdayname} $form->{ToDateD}|;
$parms->{'xformat'} = $xFormat;
$parms->{'xlabel'}  = $xLabel;
$parms->{'yformat'} = $yFormat;
$parms->{'ylabel'}  = $yLabel;
$parms->{'height'}  = 500;
$parms->{'width'}   = 1000;

#print qq|parms: are...\n|;
#foreach my $f ( keys %{$parms} ) { print ": parms-$f=$parms->{$f}\n"; }
my $grapharea = graphs->d3_chart( $parms, $data );
$html .= qq|
<DIV ><INPUT TYPE="button" ONCLICK="printDiv('chart1');" VALUE="Print" /> </DIV>
<SPAN ID="grapharea" >
${grapharea}
</SPAN>

<SPAN ID="optionsarea" >
<FORM ID="theoptions" NAME="theoptions" METHOD="POST" > 
<INPUT TYPE="hidden" NAME="sesid" VALUE="$form->{'sesid'}" >
</FORM>
</SPAN>

</BODY>
</HTML>
|;
myDBI->cleanup();
print $html;
exit;
#############################################################################

#############################################################################
sub default_graph {
    my ( $self, $form, $addsel ) = @_;
    my $ForProvID =
      $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
    $chartname = 'bar_chart';
    $xLabel    = 'Billed vs Income';
    $yLabel    = 'Dollars';
    $yFormat   = ',.2f';
    my $s = qq|
select 'Amt' as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, SUM(Treatment.BilledAmt) as MyY1
, SUM(Treatment.IncAmt) as MyY2
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and |
      . DBA->withNoteAccess( $form, $ForProvID, 'Treatment' )
      . $unRec
      . $addsel . qq|
 group by MyKey, MyX |;

    if ( $form->{LOGINPROVID} == 91 ) {
        open OUT, ">>C:/xampp/htdocs/src/debug/graphs.out"
          or die "Couldn't open file: $!";
        print OUT qq|graphs.cgi: s=\n$s\n|;
        close(OUT);
    }
    my $dataset = ();
    $dataset = graphs->selData( $form, $s, $dataset, 'MyY1|BillAmt:MyY2|IncAmt',
        $chartname );
    my $data = graphs->setData($dataset);
    return ($data);
}
