#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use myHTML;
use SysAccess;

############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();

#foreach my $f ( sort keys %{$form} ) { warn "setPALines: form-$f=$form->{$f}\n"; }
if ( !SysAccess->chkPriv( $form, 'Agent' ) ) {
    $form->error("Reset Auth Lines / Access Denied!");
}
if ( $form->{'PrAuthID'} eq '' ) { $form->error("Reset Auth Lines / NO ID!"); }

my $PrAuthID = $form->{'PrAuthID'};
Inv->setPALines( $form, $PrAuthID );
my $html = myHTML->close();
$form->complete();
print $html;
exit;
############################################################################
