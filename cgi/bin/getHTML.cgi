#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use DBI;
use SysAccess;
use myForm;
use myDBI;
use myHTML;

############################################################################
# Parse the form contents and put fields into %form.                       #
#   also defines our global variables and puts them in %form.              #
############################################################################
my $form = myForm->new();

my $priv = 'hasClientAccess';
my $id = $form->{Client_ClientID};
my $c = 'C';
my $s = 'ClientPage.cgi';
if ( $form->{Provider_ProvID} ) 
{ $priv = 'hasProviderAccess'; $id = $form->{Provider_ProvID}; $c = 'P'; $s='ProviderPage.cgi'; }
$form->{MIS_Links} = qq|S:${s}:${c}:${id}|;    # this can go away if I put this code in mis.cgi.

if ( !SysAccess->verify($form,$priv,$id) ) { myDBI->error("Access denied! (getHTML)"); }

my $html = '';
$form->{MIS_Links} = qq|S:ProviderPage.cgi:P:$id|;
$code=SysAccess->verify($form,"Privilege=$form->{access}");
if ( SysAccess->verify($form,"Privilege=$form->{access}") )
{ $html = myHTML->getHTML($form,"$form->{view}.cgi"); }
else
{ $html = myHTML->getHTML($form,"$form->{view}.dis"); }
print $html;

############################################################################
myDBI->cleanup();
exit;
