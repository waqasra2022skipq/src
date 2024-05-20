#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use DBA;
use Time::Local;
$DT = localtime();
############################################################################
$form = DBForm->new();
my $CDCID = $form->{'IDs'};   # DO WE NEED A LOOP?
my $table = $form->{'action'};
#foreach my $f ( sort keys %{$form} ) { warn "PrintCDCLog: form-$f=$form->{$f}\n"; }
my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $dbh = $form->dbconnect();
my $out = qq|${DT}\nLogged activity.\nType\tTransType\tTransDate\tTransTime\tStatus\tStatusDate\tCDCKey\tReason\tFail\tLastUpdatedDateTime\txml\n|;
my $hdrline = 3;

my $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID');
$ClinicSelection .= qq| and Client.Active=1| if ( $form->{Active} );
############################################################################
my $select = qq|select ${table}CDCSent.* from ${table}CDCSent left join ${table}CDC on ${table}CDC.ID=${table}CDCSent.${table}CDCID left join Client on Client.ClientID=${table}CDCSent.ClientID where ${table}CDC.${table}ID=${CDCID} ${ClinicSelection} order by ${table}CDCSent.ChangeDate|;
#warn qq|select=$select\n|;
my $s = $dbh->prepare($select);
$s->execute() || $form->dberror($select);
while (my $r = $s->fetchrow_hashref)
{
#foreach my $f ( sort keys %{$r} ) { warn ": r-$f=$r->{$f}\n"; }
  $r->{Reason} =~ s/\n//sg;
  $xml = $r->{xmlstring} eq '' ? 'no' : 'yes';
  $out .= qq|Logged|;
  $out .= qq|\t$r->{TransType}|;
  $out .= qq|\t$r->{TransDate}|;
  $out .= qq|\t$r->{TransTime}|;
  $out .= qq|\t$r->{Status}|;
  $out .= qq|\t$r->{StatusDate}|;
  $out .= qq|\t$r->{CDCKey}|;
  $out .= qq|\t$r->{Reason}|;
  $out .= qq|\t|.DBA->subxml($r->{Fail});
  $out .= qq|\t$r->{ChangeDate}|;
  $out .= qq|\t${xml}|;
  $out .= qq|\n|;
}
$s->finish();

$form->complete();
############################################################################
my $Name = qq|Logged activity report|;
print qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>${Name}</TITLE></HEAD>\n<BODY >|
    . gHTML->htmlReport($out,$hdrline) . qq|\n</BODY>\n</HTML>\n|;
exit;
############################################################################
