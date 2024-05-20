#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $link;
$q=qq|select ClientID from Client where SSN='$form->{SSN}'|;
$s=$dbh->prepare($q);
$s->execute() || myDBI->dberror($q);
if ( ($ClientID) = $s->fetchrow_array )
{ 
  # Redirect Header.
  $link = qq|Location: /cgi/bin/mis.cgi?MIS_Action=ClientPage&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
else
{ 
  if ( !SysAccess->verify($form,'Privilege=NewClient') )
  { myDBI->error("Client does not exist / NewClient"); }
  $form->{'Client_ClientID'} = 'new';
  $form->{view} = qq|NewClientIntake.cgi|;
  $link = myHTML->getHTML($form,$form->{view});
}
$s->finish();
myDBI->cleanup();
print $link;
exit;
############################################################################
