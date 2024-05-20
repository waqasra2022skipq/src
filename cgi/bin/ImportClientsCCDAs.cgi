#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use DBA;
use myHTML;
use XML::LibXML;

#use strict;
#use warnings;
############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
my $Agent = SysAccess->verify($form,'Privilege=Agent');
if ( !$Agent ) { $form->error("Import CCDA Page / denied Access"); }

my $html = '';

if ( $form->{submit} ) { $html = main->submit(); }
else { $html = main->html(); }
#$sProvider->finish();
$form->complete();
print $html;
exit;
############################################################################
sub submit
{
  my ($list,$cnt) = ('',0);
  my $XMLfile = $form->{'DOCROOT'} . $form->{'file'};
  foreach my $rClient ( main->addClients($form,$XMLfile) )
  {
    $cnt++;
    $list .= qq|Client ${cnt}: [$rClient->{'ClientID'}] $rClient->{'FName'} $rClient->{'LName'}, $rClient->{'Addr1'}, $rClient->{'Addr2'}, $rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
  }

  my $html = myHTML->newHTML($form,'Add Client',"CheckPopupWindow noclock countdown_1") . qq|
<FORM NAME="submit" ACTION="/cgi/bin/ImportCCDA.cgi" METHOD="POST">
  <DIV CLASS="blackonwhite" >
    <DIV CLASS="blackonwhite txtleft" >
      <div data-role="header" >
        <DIV CLASS="txtheader" >Client Import Data</DIV>
        <DIV CLASS="txtheader" >ADDED</DIV>
      </div>
      <div data-role="main" class="ui-content">
        ${list}
      </div>
    </DIV>
    <DIV CLASS="blackonwhite txtright" >
      <INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >
    </DIV>
    <INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="${ClientID}" >
    <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  </DIV>
  </FORM>
      </TD>
    </TR>
  </TABLE>
</BODY>
</HTML>
|;
  return($html);
}
sub html
{
  my ($self) = @_;
my $out;
$out .= qq|\n<PRE>\n|;
$out .= qq|\n<DIV ALIGN="left">\n|;
foreach my $f ( sort keys %{ $form } ) { $out .= "form: $f=$form->{$f}\n"; }
$out .= qq|\n</DIV>\n|;
$out .= qq|\n</PRE>\n|;

#  my $INfile = $form->{'file'};
#  my $XMLfile = 'XML'.$INfile;
#  my $result = `php /home/okmis/mis/src/MU/parseCCDA.php ${INfile} > ${XMLfile} 2>${XMLfile}.err`;

  my ($list,$cnt) = ('',0);
  my $XMLfile = $form->{'DOCROOT'} . $form->{'file'};
  foreach my $rClient ( main->parseClients($form,$XMLfile) )
  {
    $cnt++;
    $list .= qq|Client ${cnt}: $rClient->{'FName'} $rClient->{'LName'}, $rClient->{'Addr1'}, $rClient->{'Addr2'}, $rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
  }

  my $html = myHTML->newHTML($form,'Import CCDA into MIS','CheckPopupWindow noclock countdown_1') . qq|
<FORM NAME="submit" ACTION="/cgi/bin/ImportCCDA.cgi" METHOD="POST">
  <DIV CLASS="blackonwhite" >
    <DIV CLASS="blackonwhite txtleft" >
      <div data-role="header" >
        <DIV CLASS="txtheader" >Client Import Data</DIV>
      </div>
      <div data-role="main" class="ui-content">
        ${list}
      </div>
    </DIV>
    <DIV CLASS="blackonwhite txtright" >
      Do you wish to import these client's?
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="Yes" >
      <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
    </DIV>
    <INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="${ClientID}" >
    <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
    <INPUT TYPE="hidden" NAME="file" VALUE="$form->{file}" >
  </DIV>
  </FORM>
      </TD>
    </TR>
  </TABLE>
</BODY>
</HTML>
|;
  return($html);
}
sub parseClients
{
  my ($self,$form,$XMLfile) = @_;
  my @list = ();
  if ( -f $XMLfile )
  {
    #my $dom = XML::LibXML->load_xml(location => $XMLfile, no_blanks => 1);
    my $dom = XML::LibXML->load_xml(location => $XMLfile);
    foreach my $demo ($dom->findnodes('/result/demo')) 
    {
      my $rClient = ();
      my $cnt = 0;
      foreach my $street ($demo->findnodes('./addr/street')) 
      {
        $cnt++;
        $rClient->{'Addr1'} = $street->findvalue('./node') if ( $cnt == 1 );
        $rClient->{'Addr2'} = $street->findvalue('./node') if ( $cnt == 2 );
      }
      $rClient->{'City'} = $demo->findvalue('./addr/city');
      $rClient->{'ST'} = $demo->findvalue('./addr/state');
      $rClient->{'FName'} = $demo->findvalue('./name/first');
      $rClient->{'LName'} = $demo->findvalue('./name/last');
      push(@list,$rClient);
    }
  }
  else { warn qq|\nfile: ${XMLfile} NOT FOUND!\n\n|; }
  return(@list);
}
sub addClients
{
  my ($self,$form,$XMLfile) = @_;
  $form->{'Provider_ProvID_1'} = $form->{'LOGINPROVID'};    # Primary Provider setDefaults
  my $uData = ();                                           # not used except for call to setDefaults
  my @list = ();
  if ( -f $XMLfile )
  {
    #my $dom = XML::LibXML->load_xml(location => $XMLfile, no_blanks => 1);
warn qq|addClients: XMLfile=${XMLfile}\n|;
    my $dom = XML::LibXML->load_xml(location => $XMLfile);
    foreach my $demo ($dom->findnodes('/result/demo')) 
    {
      my $rClient = ();
      my $cnt = 0;
      foreach my $street ($demo->findnodes('./addr/street')) 
      {
        $cnt++;
        $rClient->{'Addr1'} = $street->findvalue('./node') if ( $cnt == 1 );
        $rClient->{'Addr2'} = $street->findvalue('./node') if ( $cnt == 2 );
      }
      $rClient->{'City'} = $demo->findvalue('./addr/city');
      $rClient->{'ST'} = $demo->findvalue('./addr/state');
      $rClient->{'FName'} = $demo->findvalue('./name/first');
      $rClient->{'LName'} = $demo->findvalue('./name/last');
      DBA->setDefaults($form,'Client',$rClient,$uData);
foreach my $f ( sort keys %{ $rClient } ) { $out .= "rClient: $f=$rClient->{$f}\n"; }
      my $ClientID = main->insRecord($form,'Client',$rClient); 
      $rClient->{'ClientID'} = $ClientID;
      push(@list,$rClient);
    }
  }
  else { warn qq|\nfile: ${XMLfile} NOT FOUND!\n\n|; }
  return(@list);
}
sub insRecord
{
  my ($self,$form,$table,$record) = @_;
  my $dbh = $form->dbconnect();
  my $qInsert = DBA->genInsert($form,$table,$record);
warn qq|insRecord: qInsert=${qInsert}\n|;
  my $sInsert = $dbh->prepare($qInsert);
  $sInsert->execute() || $form->dberror("INSERT ERROR: ${table}: ${qInsert}");
  my $RTNID = $sInsert->{'mysql_insertid'};
  $sInsert->finish();
  return($RTNID);
}
############################################################################
#my $sClient = $dbh->prepare("select * from Client where Client.LName=?");
#$sClient->execute($rClient->{'LName'}) || $form->dberror("ImportCCDA: select Client $rClient->{LName}");
#my $rClient = $sClient->fetchrow_hashref;
