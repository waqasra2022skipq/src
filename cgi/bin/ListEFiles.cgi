#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use myHTML;
use File::stat;

############################################################################
my $form = DBForm->new();
unless ( SysAccess->chkPriv($form,'Agent') )
{ $form->error("Access Denied! (List Electronic Files)"); }

############################################################################
my $dbh = $form->dbconnect();
my $CloseButton = qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;
my $UploadButton = qq|       <INPUT TYPE="submit" ONMOUSEOVER="window.status='upload button'; return true;" ONMOUSEOUT="window.status=''" NAME="view=ERAUpload.cgi&pushID=$form->{LINKID}" VALUE="upload" >|;

my $html = myHTML->new($form) . qq|
<P>
<P>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="hdrtxt header" >$form->{type} available files<BR>${CloseButton}</TD>
  </TR>
</TABLE>
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
| 
. main->gen837()
. main->gen835()
. qq|
</BODY>
</HTML>
|;

$form->complete();
print $html;
exit;
############################################################################
sub gen837
{
  my ($self) = @_;
  my $dir = qq|/Provider/EFiles/837|;
  my $out = qq|
<TABLE CLASS="home" >
  <TR > <TD CLASS="hdrtxt title" COLSPAN="5" >837 available files.</TD> </TR>
  <TR >
    <TD CLASS="hdrtxt" >type</TD>
    <TD CLASS="hdrtxt" >insurance</TD>
    <TD CLASS="hdrtxt" >date time</TD>
    <TD CLASS="hdrtxt" >count</TD>
    <TD CLASS="hdrtxt" >download</TD>
  </TR>
|;
foreach my $file  ( main->getFiles("$form->{'DOCROOT'}${dir}/*") )
{
  my ($type,$count,$dt,$sfx) = split('\.',$file);
  my $dat = substr($dt,4,2).'/'.substr($dt,6,2).'/'.substr($dt,0,4);
  my $tim = substr($dt,8,2).':'.substr($dt,10,2);
  $out .= qq|
  <TR >
    <TD CLASS="hdrcol" >${sfx}</TD>
    <TD CLASS="hdrcol" >${type}</TD>
    <TD CLASS="hdrcol" >${dat} ${tim}</TD>
    <TD CLASS="hdrcol" >${count}</TD>
    <TD CLASS="hdrcol" ><A HREF="${dir}/${file}" download >click here</A></TD>
  </TR>
|;
}
  $out .= qq|</TABLE>
<P>
|;
  return($out);
}
sub gen835
{
  my ($self) = @_;
  my $dir = qq|/Provider/EFiles/835|;
  my $path = $form->{'DOCROOT'}.$dir;
  my $out = qq|
<FORM NAME="ListEFiles" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="home" >
  <TR > <TD CLASS="hdrtxt title" COLSPAN="5" >835 available files. ${UploadButton}</TD> </TR>
  <TR >
    <TD CLASS="hdrtxt" >file</TD>
    <TD CLASS="hdrtxt" >date time</TD>
    <TD CLASS="hdrtxt" >download</TD>
  </TR>
|;
# out.0.500000008.835.151230055550.rsp
foreach my $file  ( main->getFiles("$path/*") )
{
#warn qq|file=$file\n|;
  my $timeobj = stat("$path/$file");
  my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime($timeobj->mtime);
  $year += 1900; $month += 1;
  $dat = $month.'/'.$day.'/'.$year.' '.$hrs.':'.$min.':'.$sec;
  $out .= qq|
  <TR >
    <TD CLASS="hdrcol" >${file}</TD>
    <TD CLASS="hdrcol" >${dat}</TD>
    <TD CLASS="hdrcol" ><A HREF="${dir}/${file}" download >click here</A></TD>
  </TR>
|;
}
  $out .= qq|</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>
<P>
|;
  return($out);
}
sub getFiles()
{
  my ($self,$Dir) = @_;

#warn qq|Dir=$Dir\n|;
  my @TmpFiles = glob($Dir);
  my @Files = ();
  foreach my $filepath ( @TmpFiles )
  {
    my ($path,$file) = $filepath =~ /(.*\/)?(.+)/s;
#warn qq|\nfilepath=$filepath\n|;
#warn qq|p=$path, f=$file\n|;
    my $dir = (split('/',$path))[-1];
#warn qq|d=$dir\n|;
    my($filename,$filesuffix) = $file =~ m/(.*)\.(.*)$/;
#warn qq|filename=$filename, filesuffix=$filesuffix\n|;
    push(@Files,$file);
  }
  return(@Files);
}
#####################################################################
