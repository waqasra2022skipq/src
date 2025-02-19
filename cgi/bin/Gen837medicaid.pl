#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';

use CGI::Carp qw(fatalsToBrowser);
use Accounts;
use myConfig;
use Cwd;
use Time::Local;
use DateTime;

############################################################################
my $form = myForm->new();
my ( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst ) =
  localtime();

my $Y = $year + 1900;
my $M = $mon + 1;
$M = length($M) == 1 ? '0' . $M : $M;
my $D       = length($mday) == 1 ? '0' . $mday : $mday;
my $curdate = "${Y}-${M}-${D}";

# Get the last monday as we need to set Billings run last Monday to REBILL
my $LastMonday = DBUtil->Date( '', 0, 1 - $wday );

my $billDate = $LastMonday;

my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

unless ( SysAccess->chkPriv( $form, 'Agent' ) ) {
    myDBI->error("Access Denied! (List ${type} Electronic Files)");
}

############################################################################
# usage: command                    for all accounts
#    or: command mark               mark billing for weekly run
#    or: command acct1 acct2...     to run for 'acct1' 'acct2' ...
#    or: command mark acct1 acct2...to mark for 'acct1' 'acct2' ...
############################################################################
# get the command name...
my $BIN     = myConfig->cfg('BIN');
my $BILLDIR = myConfig->cfg('BILLDIR');

# remove the billing files from last week...
chdir($BILLDIR);
my @delfiles = glob("*.837 *.837.out *.837.txt");
print qq|\nRemoved OLD Billing files: | . @delfiles . qq|...\n|;
unlink(@delfiles);

my $dbname = $form->{'DBNAME'};
my $pwd    = cwd();
print qq|\n--------------------------------------\n|;
print
  qq|billdir: $BILLDIR billdate: $billDate database: ${dbname} pwd=${pwd}\n|;

my $sInsContracts = $dbh->prepare(
"select xInsurance.Descr from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID where Contracts.BillFlag=1 and Contracts.BillType='EL' and xInsurance.Descr='medicaid'  group by xInsurance.Descr"
);
$sInsContracts->execute();
while ( my $rInsContracts = $sInsContracts->fetchrow_hashref ) {
    print qq|\n    generate $rInsContracts->{Descr} '837'...\n|;
    system(
"${BIN}/gen837 DBNAME=${dbname}\\&InsDescr=$rInsContracts->{Descr}\\&BillDate=${billDate}\\&mlt=$form->{mlt}"
    );
}
$sInsContracts->finish();
myDBI->cleanup();

# print qq|\n\n=========Send Billing==============\n|;
# system("${BIN}/SendBilling");
print qq|\n\n======================================\n|;
print qq|Completed \n|;
exit;
############################################################################

