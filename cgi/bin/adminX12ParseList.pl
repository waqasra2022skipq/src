#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use myConfig;
use myHTML;
use File::stat;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $type = $form->{'type'};

unless ( SysAccess->chkPriv($form,'Agent') )
{ myDBI->error("Access Denied! (List ${type} Electronic Files)"); }


my $desc = qq|Select any files to see results|;


############################################################################
my $CloseButton = qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;


my $html = myHTML->newHTML($form,'Upload Panel','CheckPopupWindow noclock countdown_10') . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" src="/src/cgi/js/novalidate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" src="/src/cgi/js/tablesort.js"> </SCRIPT>
<LINK href="/src/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
<DIV CLASS="home title hdrcol" >
${desc}
</DIV>
<FORM NAME="adminFiles" ACTION="/src/cgi/bin/adminX12Parser.pl"  METHOD="POST" >
${UploadButton}
| 
. 
main->listFiles('271',"*.rsp")
.
qq||
. 
main->listFiles('835',"*.rsp")
.
qq||
. 
main->listFiles('837',"*.rsp")
.
qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>

</BODY>
</HTML>
|;

myDBI->cleanup();
print $html;
exit;



############################################################################
sub listFiles
{
  my ($self,$dir,$wildcards) = @_;

  my $typename = $dir eq '835' ? 'Remittances'
             : $dir eq '271' ? 'Eligibility'
  	     : $dir eq '837' ? 'Billing'
             : 'Unknown';

#warn qq|dir=${dir}\n|;
  my $ADMINDIR = myConfig->cfg('ADMINDIR');



  my ($adminpath, $admindir) = $ADMINDIR =~ m/(.*\/)(.*)$/;
#warn qq|ADMINDIR=${ADMINDIR}\n|;
#warn qq|adminpath=${adminpath}\n|;
#warn qq|admindir=${admindir}\n|;
  my $dirpath = qq|/${admindir}/${dir}|;


#warn qq|dirpath=${dirpath}\n|;
  my $html = '';

  foreach my $wildcard ( split(' ',$wildcards) )
  {
    my $count = 0;
    $html .= qq|
<P>
<TABLE CLASS="home" >
  <TR > <TD CLASS="hdrtxt title" COLSPAN="2" >${typename} ${wildcard} available files.</TD> </TR>
</TABLE>
<TABLE CLASS="chartsort table-autosort table-stripeclass:alternate">
<THEAD>
  <TR >
    <TH class="table-sortable:default" >file</TH>
    <TH >Action</TH>
    <TH >Download</TH>
  </TR>
</THEAD>
<TBODY>
|;
    foreach my $filepath  ( main->getFiles("${ADMINDIR}/${dir}/${wildcard}") )
    {
#warn qq|\nfilepath=$filepath\n|;
      $count++;
      my $even = int($count/2) == $count/2 ? '1' : '0';
      my $class = $even ? qq|CLASS="alternate"| : '';
      my ($path,$file) = $filepath =~ /(.*\/)?(.+)/s;
      my $fs = stat($filepath);
      $html .= qq|
  <TR ${class} >
    <TD >${file}</TD>
    <TD >
    
        <A HREF="javascript:ReportWindow('/cgi/bin/adminX12Parser.pl?filepath=$filepath&Type=$dir&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" src="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Read File</A>
    </TD>

    <TD >
        <A HREF="$filepath" download>Click Here</A>

    </TD>
  </TR>
|;
}
  my $result = $count ? '' : qq|<TR><TD CLASS="hdrcol" COLSPAN="2" >No files to list.</TD></TR>|;
  $html .= qq|${result}
</TBODY>
</TABLE>
<P>
|;
  }


  return($html);
}
sub getFiles()
{
  my ($self,$Dir) = @_;
#warn qq|Dir=$Dir\n|;
  my @TmpFiles = glob($Dir);
  my @Files = ();
  my @FilesByDate = ();
  foreach my $filepath ( @TmpFiles )
  { push(@Files,$filepath); }
  for my $file ( sort { my $a_stat = stat($a); my $b_stat = stat($b); $a_stat->ctime <=> $b_stat->ctime; }  @Files )
  { push(@FilesByDate,$file); }
  return(@FilesByDate);
}
#####################################################################
