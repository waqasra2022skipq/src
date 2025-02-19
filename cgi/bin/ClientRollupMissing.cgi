#!/usr/bin/perl 
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use Rollup;
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn "ENTER ClientRollup: MIS_Action=$form->{'MIS_Action'}, fwdLINK=$form->{fwdLINK}\n";

if ( !$form->{Client_ClientID} ) {
    myDBI->error("Client Page / denied ClientID NULL");
}
if ( !SysAccess->verify( $form, 'hasClientAccess' ) ) {
    myDBI->error("Client Access Page / Not Client");
}
my $ClientID = $form->{Client_ClientID};
my $mlt      = $form->{mlt};
my $misLINKS = $form->{misLINKS};
my $Location =
qq|/cgi/bin/mis.cgi?view=ListClientEDocs.cgi&Client_ClientID=${ClientID}&mlt=${mlt}&misLINKS=$misLINKS\n\n|;

############################################################################
##
# make sure the directory exists
##
my $HomePath = qq|/Client/EDocs/${ClientID}|;
my $RootPath = $form->{DOCROOT} . ${HomePath};
system("/bin/mkdir -pm 777 ${RootPath}");

# ProgNotes all already getting rolled up at Notes so no need to do it separately

Rollup->edocs( $form, $ClientID, 'ClientPrAuthCDC' );

myDBI->cleanup();

print qq|Location: ${Location}\n\n|;
exit;
############################################################################
