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
my $ID = $form->{'IDs'};   # DO WE NEED A LOOP?
my $table = $form->{'action'};
#foreach my $f ( sort keys %{$form} ) { warn "PrintPALines: form-$f=$form->{$f}\n"; }
my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $dbh = $form->dbconnect();
my @flds = ('PAgroup','LineNumber','BegDate','EndDate','Units','Cost','Status');
my @typs = ('text','integer','date','date','decimal','decimal','text');
my $out = qq|${DT}\nPrior Authorization Monthly Totals Listing\n|; foreach my $fld ( @flds ) { $out .= qq|${fld}\t|; } $out .= qq|\n|;
my $hdrline = 3;

my $where = qq|where PALines.PrAuthID='${ID}'|;
#my $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Client.ProvID','and');
$ProviderSelection .= qq| and Client.Active=1| if ( $form->{Active} );
############################################################################
my $select = qq|select PALines.* from PALines left join ClientPrAuth on ClientPrAuth.ID=PALines.PrAuthID left join Client on Client.ClientID=PALines.ClientID ${where} ${ProviderSelection} order by BegDate,EndDate|;
#warn qq|select=$select\n|;
my $s = $dbh->prepare($select);
$s->execute() || $form->dberror($select);
while (my $r = $s->fetchrow_hashref)
{
#foreach my $f ( sort keys %{$r} ) { warn ": r-$f=$r->{$f}\n"; }
  my $i = 0;
  foreach my $fld ( @flds )
  {
    my $val = $typs[$i] eq 'date'
            ? DBUtil->Date($r->{$fld},'fmt','MM/DD/YYYY')
            : $r->{$fld};
#warn qq|fld=${fld}, val=$r->{$fld}/${val}\n|;
    $out .= qq|${val}\t|; 
    $i++;
  }
  $out .= qq|\n|;
}
$s->finish();

$form->complete();
############################################################################
my $Name = qq|Prior Authorization Lines Report|;
print qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>${Name}</TITLE></HEAD>\n<BODY >|
    . gHTML->htmlReport($out,$hdrline) . qq|\n</BODY>\n</HTML>\n|;
exit;
############################################################################
