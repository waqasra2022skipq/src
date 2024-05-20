#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});

unless ( SysAccess->chkPriv($form,'Agent') )
{ myDBI->error("Access Denied! (List ${type} Electronic Files)"); }

# Start out the display.
my $html = myHTML->newHTML($form,'Administration Panel','CheckPopupWindow noclock countdown_60') . qq|
<DIV ALIGN="center" > 

<DIV CLASS="port header hdrtxt" >Admin Panel</DIV>
<DIV CLASS="port heading hdrcol" >Used for administration of Millennium Information Services.</DIV>
<DIV CLASS="home title hdrcol" >Choose from the functions below.</DIV>
<TABLE CLASS="home fullsize" >
  <TR>
| . main->listTasks('837') . qq|
| . main->listTasks('835') . qq|
| . main->listTasks('271') . qq|
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
| . main->listTasks('Jobs') . qq|
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
  <TR>
| . main->RebillTask() . qq|
  </TR>
</TABLE>
|;

myDBI->cleanup();
print $html;
exit;
############################################################################
############################################################################
sub listTasks
{
  my ($self,$type) = @_;
  my $html = $type eq '837' ? main->list837()
             : $type eq '835' ? main->list835()
             : $type eq '271' ? main->list271()
             : $type eq 'Jobs' ? main->listJobs()
             : 'Unknown';
  return($html);
}
sub list837
{
  my ($self) = @_;
  my $html = '';
  $html .= qq|
    <TD WIDTH="34%" >

      <DIV CLASS="subtitle tophdr" >Billing</DIV>
      <DIV CLASS="subtitle strcol" >
        <A HREF="javascript:ReportWindow('/cgi/bin/adminGenerate.pl?type=837&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Generate',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Generate 837</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminFiles.pl?type=837&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Transfer',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Transfer files</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminLogs.pl?type=837&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Response & Log files</A>
      </DIV>

    </TD>
|;
  return($html);
}
#####################################################################
sub list835
{
  my ($self) = @_;
  my $html = '';
  $html .= qq|
    <TD WIDTH="33%" >

      <DIV CLASS="subtitle tophdr" >Remittances</DIV>
      <DIV CLASS="subtitle strcol" >
        <A HREF="javascript:ReportWindow('/cgi/bin/adminGenerate.pl?type=835&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Generate',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Instructions 835</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminFiles.pl?type=835&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Transfer',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Transfer files</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminLogs.pl?type=835&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Log files</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminJob.pl?type=835&job=process&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Process',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Process 835 Remittance Files</A>
      </DIV>

    </TD>
|;
  return($html);
}
#####################################################################
sub list271
{
  my ($self) = @_;
  my $html = '';
  $html .= qq|
    <TD WIDTH="33%" >

      <DIV CLASS="subtitle tophdr" >Eligibility</DIV>
      <DIV CLASS="subtitle strcol" >
        <A HREF="javascript:ReportWindow('/cgi/bin/adminGenerate.pl?type=271&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Generate',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Generate 270</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminFiles.pl?type=271&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Transfer',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Transfer files</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminLogs.pl?type=271&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Response & Log files</A>
        <BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminJob.pl?type=271&job=process&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Process',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Process 271 Eligibility Files</A>
      </DIV>

    </TD>
|;
  return($html);
}
sub listJobs
{
  my ($self) = @_;
  my $html = '';
  $html .= qq|
    <TD WIDTH="33%" >

      <DIV CLASS="subtitle tophdr" >Automatic Backgroups Job Logs</DIV>
      <DIV CLASS="subtitle strcol" >
        <A HREF="javascript:ReportWindow('/cgi/bin/adminLogs.pl?type=logs&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Log files</A>
<BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminJobACL.pl?type=271&job=process&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Process',800,1200)" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Run setACL (Update Manager Tree) </A>
<BR>
        <A HREF="javascript:ReportWindow('/cgi/bin/adminX12ParseList.pl?type=271_835_837&job=x12_parsing&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Logs',800,1200)" ><IMG ALT="edit" src="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" >Read 835/837/271 Response Files</A>
      
      </DIV>

    </TD>
|;
  return($html);
}
#####################################################################

sub RebillTask {
  my $html = '';
  $Rebill_Button = qq|<FONT COLOR="red"><A STYLE="background-color:white; padding:0.2em;" HREF="javascript:ReportWindow('/cgi/bin/runCMDBash.pl?AgencyID=&mlt=$form->{mlt}','adjNote')"  TITLE="Click here to change In Process notes to Rebill" >Rebill Notes</A></FONT>|;
  $Gen837_Button = qq|<FONT COLOR="red"><A STYLE="background-color:white; padding:0.2em;" id="gen837" HREF="javascript:ReportWindow('/cgi/bin/Gen837medicaid.pl?mlt=$form->{mlt}','adjNote')"  TITLE="Click here to Generate 837 files for last billing run" >Gen837 files</A></FONT>|;


  $html .= qq|
    <TD WIDTH="33%" >
      <DIV CLASS="subtitle tophdr" >Rebill Medicaid InProcess Notes</DIV>
      <DIV CLASS="subtitle strcol" >
      ${Rebill_Button}
      </DIV>
      <DIV CLASS="subtitle strcol" >
      ${Gen837_Button}
      </DIV>
    </TD>
  |;

  return($html);
}
