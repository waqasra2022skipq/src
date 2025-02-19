#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %{$form} ) { warn "fixNotes: form-$f=$form->{$f}\n"; }
if ( !SysAccess->chkPriv( $form, 'Agent' ) ) {
    myDBI->error("Fix Contractual Amounts / Access Denied!");
}

my $DT       = localtime;
my $RefID    = 'auto adjusted';
my $PaidDate = '2019-08-12';
( my $ICN = $PaidDate ) =~ s/-//g;
my $sPayDate = $dbh->prepare(
"update NoteTrans set PaidDate='${PaidDate}' where RefID='${RefID}' and PaidDate is null"
);
my $sTreatment = $dbh->prepare(
"select * from Treatment left join xSC on xSC.SCID = Treatment.SCID where xSC.InsID=212 and BillStatus=5 and AmtDue=?"
);

warn qq|fixNotes: database: $form->{'DBNAME'}\n|;
warn qq|fixNotes: start process ${DT}\n\n|;

##oldway, swap Amt,Code #my $noteCount = main->fixNotes('27.05','A2_16.75:253_.80');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('18.88','A2_10.05:253_.88:237_1.82');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('22.95','A2_16.75:253_.80');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('30.58','A2_22.31:253_1.07');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('34.68','A2_25.04:253_1.25');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('17.49','A2_8.51:253_.88:237_2.05');
##oldway, swap Amt,Code #my $noteCount = main->fixNotes('25.12','A2_35.69:253_1.16:237_3.50');

##my $noteCount = main->fixNotes('4.54','4.28_A2:0.26_253');
my $noteCount = main->fixNotes( '9.50',  '2.73_A2:0.18_253' );
my $noteCount = main->fixNotes( '10.05', '10.05_A2' );
my $noteCount = main->fixNotes( '10.96', '10.05_A2:0.91_253' );
my $noteCount = main->fixNotes( '12.09', '6.44_A2:0.56_253:1.17_237' );
my $noteCount = main->fixNotes( '12.75', '10.05_A2:0.88_253:1.82_237' );
my $noteCount = main->fixNotes( '12.90', '16.75_A2:0.80_253' );
my $noteCount = main->fixNotes( '13.38', '13.38_A2' );
my $noteCount = main->fixNotes( '14.59', '13.38_A2:1.21_253' );
my $noteCount = main->fixNotes( '14.78', '19.48_A2:0.98_253' );
my $noteCount = main->fixNotes( '16.51', '8.51_A2:0.90_253:0.92_237' );
my $noteCount = main->fixNotes( '16.75', '16.75_A2' );
my $noteCount = main->fixNotes( '16.97', '13.38_A2:1.16_253:2.43_237' );
my $noteCount = main->fixNotes( '17.09', '10.05_A2:0.91_253' );
my $noteCount = main->fixNotes( '17.55', '16.75_A2:0.80_253' );
my $noteCount = main->fixNotes( '18.78', '16.75_A2:0.80_253' );
my $noteCount = main->fixNotes( '19.48', '13.44_A2:2.25_253:0.48_237' );
my $noteCount = main->fixNotes( '20.46', '19.48_A2:0.98_253' );
my $noteCount = main->fixNotes( '22.31', '22.31_A2:' );
my $noteCount = main->fixNotes( '22.36', '10.05_A2:0.91_253' );
my $noteCount = main->fixNotes( '22.43', '1.90_A2:0.78_253' );
my $noteCount = main->fixNotes( '22.70', '8.51_A2:2.05_253:0.88_237' );
my $noteCount = main->fixNotes( '22.74', '13.28_A2:1.21_253' );
my $noteCount = main->fixNotes( '22.81', '14.01_A2:1.59_253:0.93_237' );
my $noteCount = main->fixNotes( '23.12', '11.23_A2:2.71_253:1.17_237' );
my $noteCount = main->fixNotes( '23.38', '22.31_A2:1.07_253' );
my $noteCount = main->fixNotes( '24.15', '10.05_A2:0.88_253:1.82_237' );
my $noteCount = main->fixNotes( '25.04', '25.04_A2' );
my $noteCount = main->fixNotes( '26.29', '25.04_A2:1.25_253' );
my $noteCount = main->fixNotes( '27.05', '19.48_A2:0.98_253' );
my $noteCount = main->fixNotes( '27.60', '16.75_A2:0.80_253' );
my $noteCount = main->fixNotes( '29.75', '13.38_A2:1.21_253' );
my $noteCount = main->fixNotes( '32.13', '13.38_A2:1.16_253:2.43_237' );
my $noteCount = main->fixNotes( '32.14', '20.91_A2:2.03_253:1.19_237' );
my $noteCount = main->fixNotes( '32.27', '8.51_A2:2.05_253:0.88_237' );
my $noteCount = main->fixNotes( '32.73', '19.48_A2:0.98_253' );
my $noteCount = main->fixNotes( '34.76', '118.23_23' );
my $noteCount = main->fixNotes( '35.12', '33.51_A2:1.61_253' );
my $noteCount = main->fixNotes( '36.77', '22.31_A2:1.07_253' );
my $noteCount = main->fixNotes( '38.40', '20.45_A2:1.78_253:3.71_237' );
my $noteCount = main->fixNotes( '41.90', '25.04_A2:1.25_253' );
my $noteCount = main->fixNotes( '44.64', '23.78_A2:2.06_253:4.32_237' );
my $noteCount = main->fixNotes( '45.93', '33.51_A2:1.61_253' );
my $noteCount = main->fixNotes( '46.92', '16.75_A2:0.80_253' );
my $noteCount = main->fixNotes( '50.03', '36.24_A2:1.79_253' );
my $noteCount = main->fixNotes( '51.02', '36.97_A2:1.82_253' );
my $noteCount = main->fixNotes( '55.23', '33.51_A2:1.61_253' );
my $noteCount = main->fixNotes( '60.36', '36.24_A2:1.79_253' );

$DT = localtime;
warn qq|fixNotes: processed complete ${DT}\n|;

# remove the 'ADJ' transactions from Payroll...
$sPayDate->execute();
$sPayDate->finish();
$sTreatment->finish();
myDBI->cleanup();
exit;
############################################################################
sub fixNotes {
    my ( $self, $ForAmtDue, $Trans ) = @_;
    my $cnt = 0;
    $sTreatment->execute($ForAmtDue);
    my $rows = $sTreatment->rows;
    warn qq|fixNotes: rows=${rows}, ForAmtDue=${ForAmtDue}\n|;
    while ( my $rTreatment = $sTreatment->fetchrow_hashref ) {
        $cnt++;
        my $TrID = $rTreatment->{'TrID'};

        #warn qq|fixNotes: TrID=${TrID}\n|;
        foreach my $tran ( split( ':', $Trans ) ) {
            my ( $Amount, $DenCode ) = split( '_', $tran, 2 );
            my $cmd =
qq|/var/www/okmis/src/cgi/bin/adjNote.pl DBNAME=$form->{DBNAME}\\&submit=1\\&TrID=${TrID}\\&PaidAmt=${Amount}\\&DenCode=${DenCode}\\&RefID=${RefID}\\&ICN=${ICN}\\&mlt=$form->{mlt}|;
            system($cmd);
        }
    }
    warn qq|fixNotes: processed ${cnt}\n\n|;
    return ($cnt);
}
############################################################################
