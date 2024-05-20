#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use DBForm;
use DBA;
use myHTML;
use gXML;
use File::Copy;
use XML::LibXML;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
#warn "linkCCDA: IDs=$form->{'IDs'}, type=${type}\n";
#foreach my $f ( sort keys %{$form} ) { warn "linkCCDA: form-$f=$form->{$f}\n"; }
my $ClientID=$form->{'Client_ClientID'};
##
# prepare selects...
##
my $sPhiMailAttachments = $dbh->prepare("select * from PhiMailAttachments where ID=?");
$sPhiMailAttachments->execute($form->{'IDs'}) || $form->dberror("linkCCDA: select PhiMailAttachments");
my $html = '';
  my ($cnt,$list,$err) = (0,'','');
  my $rPhiMailAttachments = $sPhiMailAttachments->fetchrow_hashref;
  my $fromfile = qq|$form->{'DOCROOT'}$rPhiMailAttachments->{filename}|;
  my ($directory, $filename) = $fromfile =~ m/(.*\/)(.*)$/;
warn qq|begin: fromfile=${fromfile}\n|;
warn qq|begin: directory=${directory}\n|;
warn qq|begin: filename=${filename}\n|;
  if ( -f $fromfile )
  {
    if ( $form->{link} ) { $list = main->link($form,$ClientID,$rPhiMailAttachments); }
    else { $list = main->list($rPhiMailAttachments); }
  }
  else
  {
    if ( $fromfile eq '' )
    { $err = qq|File name is empty in link!|; $list = qq|Zero files to link, Aborted!|; }
    else
    { $err = qq|File NOT FOUND on disk!|; $list = qq|Aborted!|; }
  }
  my $html = main->html($filename,$list,$err);
$sPhiMailAttachments->finish();
$form->complete();
print $html;
exit;
############################################################################
sub link
{
  my ($self,$form,$ClientID,$r) = @_;
  my $list = '';
#$list .= qq|form:<BR>|;
#foreach my $f ( sort keys %{$form} ) { $list .= qq|$f=$form->{$f}<BR>|; }
#$list .= qq|PhiMail:<BR>|;
#foreach my $f ( sort keys %{$r} ) { $list .= qq|$f=$r->{$f}<BR>|; }
  my $fromfile = qq|$form->{'DOCROOT'}$r->{filename}|;
  my ($directory, $filename) = $fromfile =~ m/(.*\/)(.*)$/;
warn qq|link: fromfile=${fromfile}\n|;
warn qq|link: directory=${directory}\n|;
warn qq|link: filename=${filename}\n|;
  my ($FName,$MName,$LName,$Gend,$DOB) = main->getInfo($fromfile);
  my $todir = qq|/Client/EDocs/${ClientID}|;
  my $topath = qq|$form->{DOCROOT}${todir}|;
  system("/bin/mkdir -pm 777 ${topath}");
  my $tofile = qq|${topath}/${filename}|;
  copy($fromfile,$tofile) or $list .= "<<< ERROR >>>: Copy ${fromfile} failed: $!<BR>";
  my $r = ();
  $r->{'ClientID'} = $ClientID;
  $r->{'Type'} = 41;                       # CCDA
  $r->{'Title'} = qq|Import CCDA file linked|;
  $r->{'Descr'} = qq|Import file: ${FName} ${MName} ${LName} ${Gend} ${DOB}|;
  $r->{'Path'} = qq|${todir}/${filename}|;
  $r->{'CreateProvID'} = $form->{'LOGINPROVID'};
  $r->{'CreateDate'} = $form->{'TODAY'};
  $NEWID = DBA->doUpdate($form,"ClientEDocs",$r,"ClientID='${ClientID}' and Path='$r->{htmfile}'");
  $list .= qq|Created Electronic Document for ClientID: ${ClientID}.<BR>|;
#warn qq|link: NEWID=${NEWID}\n|;
  return($list);
}
sub list
{
  my ($self,$r) = @_;
  my ($cnt,$list) = (0,'');
  my $fromfile = qq|$form->{'DOCROOT'}$r->{filename}|;
  my ($directory, $filename) = $fromfile =~ m/(.*\/)(.*)$/;
warn qq|list: fromfile=${fromfile}\n|;
warn qq|list: directory=${directory}\n|;
warn qq|list: filename=${filename}\n|;
  if ( -f $fromfile )
  {
    my ($FName,$MName,$LName,$Gend,$DOB) = main->getInfo($fromfile);
    $LName = $MName if ( $LName eq '' );
    my $sClient = $dbh->prepare("select * from Client where FName LIKE '%${FName}%' and LName LIKE '%${LName}%';");
warn qq|list: select * from Client where FName LIKE '%${FName}%' and LName LIKE '%${LName}%';|;
    $sClient->execute() || $form->dberror("linkCCDA: select Client");
    my $rows = $sClient->rows;
    $list = qq|${rows} Client(s) List for: ${FName} ${LName} ${Gender} ${DOB}<BR>|;
    while ( my $rClient = $sClient->fetchrow_hashref )
    {
      $cnt++;
      $list .= qq|$rClient->{'FName'} $rClient->{'LName'} $rClient->{'Gend'} $rClient->{'DOB'}
             <button CLASS="confirmLINK" MYTEXT="Are you sure you want to LINK this xml to this client?<BR>If so, then click the OK button below. If NOT, click the Cancel button below." HREF="/cgi/bin/mis.cgi?MIS_Action=linkCCDA.cgi&Client_ClientID=$rClient->{'ClientID'}&link=1&IDs=$form->{'IDs'}&mlt=$form->{'mlt'}" MYBUSY="Linking..." >Link</button> $rClient->{'ClientID'}<BR>|;
    }
    $sClient->finish();
  }
  else
  {
    if ( $fromfile eq '' )
    { $err = qq|fromfile name empty in link!|; $list = qq|Unable to search for client, Aborted!|; }
    else
    { $err = qq|fromfile NOT FOUND on disk!|; $list = qq|Aborted!|; }
  }
  return($list);
}
sub html
{
  my ($self,$filename,$list,$err) = @_;
  my $html = myHTML->newHTML($form,'Link CCDA','CheckPopupWindow noclock countdown_10') . qq|
<FORM ID="form" NAME="linkCCDA" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
  <TABLE CLASS="main" >
    <TR> <TD CLASS="hdrcol title" >Link CCDA</TD> </TR>
  </TABLE>
  <TABLE CLASS="home fullsize" >
    <TR>
      <TD CLASS="strcol" >
        Link: ${filename}<BR>
      </TD>
    </TR>
    <TR>
      <TD CLASS="strcol hotmsg" >
        ${list}
      </TD>
    </TR>
    <TR>
      <TD CLASS="strcol hotmsg" >
        ${err}<BR>
      </TD>
    </TR>
  </TABLE>
      
</TD> </TR> </TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
</FORM>
</BODY>
</HTML>
|;
  return($html);
}
sub getInfo
{
  my ($self,$filename) = @_;
  my $doc = '';
  #   load_xml: initializes the parser and parse_file()
warn "${filename}\n";
  eval { $doc = XML::LibXML->load_xml(location => $filename); };
  return('parse_error') if ( $@ );
  my $xml    = XML::LibXML::XPathContext->new;                # No argument here!
  $xml->registerNs('x', 'urn:hl7-org:v3');
  my ($longname,$othername) = ('','');
  for my $node ( $xml->findnodes('//x:patient/x:name', $doc) )
  {
    my $type = $xml->findvalue('@use', $node);            # Context specified as argument.
    for my $given ( $xml->findnodes('x:given', $node) )
    {
      if ( $type eq 'L' ) { $longname .= $given->to_literal.' '; }
      else                { $othername .= $given->to_literal.' '; }
    }
    for my $family ( $xml->findnodes('x:family', $node) )
    {
      if ( $type eq 'L' ) { $longname .= $family->to_literal.' '; }
      else                { $othername .= $family->to_literal.' '; }
    }
  }
  my $patientname = $longname eq '' ? $othername : $longname;
warn "$patientname\n";
  my ($fname,$mname,$lname) = split(' ',$patientname);
  $fname =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
warn "$fname\n";
  $mname =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
warn "$mname\n";
  $lname =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
warn "$lname\n";
  my $gender = $xml->findvalue('//x:patient/x:administrativeGenderCode/@code', $doc);
warn "$gender\n";
  my $dateofbirth = $xml->findvalue('//x:patient/x:birthTime/@value', $doc);
warn "$dateofbirth\n";
  my $descr = qq|${patientname} ${gender} ${dateofbirth}\n|; 
  return($fname,$mname,$lname,$gender,$dateofbirth);
}
############################################################################
