#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use CGI qw(:standard escape);
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use Inv;
use gHTML;

############################################################################
$form = DBForm->new();
$dbh  = $form->dbconnect();

my $BillingReportFlag = SysAccess->verify( $form, 'Privilege=BillingReports' );
my $qPrAuth =
qq|select ClientPrAuth.*,Client.FName,Client.LName,Client.DOB,Client.ProvID,Client.clinicClinicID,Insurance.InsID from ClientPrAuth left join Client on Client.ClientID=ClientPrAuth.ClientID left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ID=?|;
my $sPrAuth = $dbh->prepare($qPrAuth);
$sPrAuth->execute( $form->{IDs} ) || $form->dberror($qPrAuth);
if ( my $rPrAuth = $sPrAuth->fetchrow_hashref ) {
    unless ( SysAccess->hasClientAccess( $form, $rPrAuth->{ClientID} ) ) {
        $form->error("ClientPrAuth Access Page / Not Client");
    }

    my $InsDescr =
      DBA->getxref( $form, 'xInsurance', $rPrAuth->{InsID}, 'Name' );
    my $inv = Inv->InvPA( $form, $rPrAuth );
    $inv = $inv->InvNotes( $form, $rPrAuth->{ClientID}, $rPrAuth->{InsID} );
    my ( $cnt, $out, $hdrline ) = (
        0,
"$rPrAuth->{FName} $rPrAuth->{LName} ($rPrAuth->{ClientID}) - ${InsDescr}\n",
        1
    );
    foreach my $Dates ( @{ $inv->{PADates} } ) {
        $cnt++;
        my ( $BDate, $EDate ) = split( '/', $Dates );
        my $fBDate = DBUtil->Date( $BDate, 'fmt', 'MM/DD/YYYY' );
        my $fEDate = DBUtil->Date( $EDate, 'fmt', 'MM/DD/YYYY' );
        my $key    = "${fBDate}-${fEDate}";
        if ( $cnt == 1 ) {
            if ( $inv->{UnitsAuth} > 0 ) {
                $out .= qq|Authorized Codes\t \t \t \t \t \t \t \t \t \t \t \n|;
                $hdrline++;
                $out .=
qq|StartDate\tEndDate\tAuth\tUsed\tLeft\tPctLeft\tType\tServiceCode\tTrID\tContactDate\tUnits\tAmount\n|;
                $hdrline++;
                foreach $SCID ( keys %{ $inv->{PASCID} } ) {
                    my $UnitsAuth =
                      sprintf( "%.2f", $inv->{$SCID}->{UnitsAuth} );
                    my $UnitsUsed =
                      sprintf( "%.2f", $inv->{$SCID}->{UnitsUsed} );
                    my $UnitsLeft = sprintf( "%.2f",
                        $inv->{$SCID}->{UnitsAuth} -
                          $inv->{$SCID}->{UnitsUsed} );
                    my $PctUnits =
                      $UnitsAuth > 0
                      ? sprintf( "%.1f", ( ( $UnitsLeft / $UnitsAuth ) * 100 ) )
                      : '0.0';
                    $out .=
qq|$inv->{fPAEffDate}\t$inv->{fPAExpDate}\t${UnitsAuth}\t${UnitsUsed}\t${UnitsLeft}\t${PctUnits}\tAUTH\t$inv->{PASCID}->{$SCID}\t \t \t \t \n|;
                }
            }
            else {
                $out .=
qq|StartDate\tEndDate\tAuth\tUsed\tLeft\tPctLeft\tType\tServiceCode\tTrID\tContactDate\tUnits\tAmount\n|;
                $hdrline++;
            }
        }
        $out .= main->setInventory( $inv, $key );
    }
    my $html = gHTML->htmlReport( $out, $hdrline );
    print
qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>Prior Authorization</TITLE></HEAD>\n<BODY >\n|
      . $html
      . qq|\n</BODY>\n</HTML>\n|;
}
else { $form->error("ClientPrAuth Access Page / No PrAuth ID"); }

############################################################################
sub setInventory() {
    my ( $self, $inv, $CurPeriod ) = @_;
    my $out = '';

# now the current/monthly period of the PA...
#warn qq|setInventory: PPACnt=$inv->{PPACnt}, Status=$StatusColor, $StatusReason\n|;
    my ( $BDate, $EDate ) = split( '-', $CurPeriod );

#warn qq|setInventory: PrAuthID=$form->{IDs}, InsDescr=$inv->{InsDescr}, CurPeriod=$CurPeriod\n|;
#foreach my $f ( sort keys %{$inv->{$CurPeriod}} ) { warn "  main: inv-${CurPeriod}-${f} is $inv->{$CurPeriod}->{$f}\n"; }
    $UnitsAuth = sprintf( "%.2f", $inv->{$CurPeriod}->{UnitsAuth} );
    $UnitsUsed = sprintf( "%.2f", $inv->{$CurPeriod}->{UnitsUsed} );
    $UnitsLeft = sprintf( "%.2f",
        $inv->{$CurPeriod}->{UnitsAuth} - $inv->{$CurPeriod}->{UnitsUsed} );
    $PctUnits =
      $UnitsAuth > 0
      ? sprintf( "%.1f", ( ( $UnitsLeft / $UnitsAuth ) * 100 ) )
      : '0.0';
    $AmtAuth = sprintf( "%.2f", $inv->{$CurPeriod}->{AmtAuth} );
    $AmtUsed = sprintf( "%.2f", $inv->{$CurPeriod}->{AmtUsed} );
    $AmtLeft = sprintf( "%.2f",
        $inv->{$CurPeriod}->{AmtAuth} - $inv->{$CurPeriod}->{AmtUsed} );
    $PctAmt =
      $AmtAuth > 0
      ? sprintf( "%.1f", ( ( $AmtLeft / $AmtAuth ) * 100 ) )
      : '0.0';
    $out .= qq|${BDate}\t${EDate}\t|;

    if ( $UnitsAuth > 0 ) {
        $out .= qq|${UnitsAuth}\t${UnitsUsed}\t${UnitsLeft}\t${PctUnits}%|;
    }
    elsif ( $AmtLeft == 0 && $BillingReportFlag ) {
        $out .= qq|${AmtAuth}\t${AmtUsed}\t${AmtLeft}\t${PctAmt}%|;
    }
    elsif ( $AmtLeft == 0 ) { $out .= qq|\t\t\t${PctAmt}%|; }
    elsif ($BillingReportFlag) {
        $out .= qq|${AmtAuth}\t${AmtUsed}\t${AmtLeft}\t${PctAmt}%|;
    }
    else { $out .= qq|\t\t\t${PctAmt}%|; }
    $out .= qq|\t \t \t \t \t \t \n|;
    foreach my $SCID ( sort keys %{ $inv->{$CurPeriod}->{INPA} } ) {
        my $SCNum = DBA->getxref( $form, 'xSC', $SCID, 'SCNum' );
        $out .= qq|\t\t\t\t\t\tINPA\t${SCNum}\t|;
        my $tabs = "";
        foreach my $TrID ( sort keys %{ $inv->{$CurPeriod}->{$SCID} } ) {
            next if ( $TrID eq 'AMT' || $TrID eq 'LIST' || $TrID eq 'UNITS' );
            $out .=
qq|${tabs}${TrID}\t$inv->{$CurPeriod}->{$SCID}->{$TrID}->{ContDate}\t$inv->{$CurPeriod}->{$SCID}->{$TrID}->{Units}\t|;
            $out .=
              $BillingReportFlag
              ? qq|$inv->{$CurPeriod}->{$SCID}->{$TrID}->{Amt}\t|
              : " \t";
            $out .= qq|\n|;
            $tabs = "\t\t\t\t\t\t\t\t";
        }
    }
    foreach my $SCID ( sort keys %{ $inv->{$CurPeriod}->{NONPA} } ) {
        my $SCNum = DBA->getxref( $form, 'xSC', $SCID, 'SCNum' );
        $out .= qq|\t\t\t\t\t\tNONPA\t${SCNum}\t|;
        my $tabs = "";
        foreach my $TrID ( sort keys %{ $inv->{$CurPeriod}->{$SCID} } ) {
            next if ( $TrID eq 'AMT' || $TrID eq 'LIST' || $TrID eq 'UNITS' );
            $out .=
qq|${tabs}${TrID}\t$inv->{$CurPeriod}->{$SCID}->{$TrID}->{ContDate}\t$inv->{$CurPeriod}->{$SCID}->{$TrID}->{Units}\t|;
            $out .=
              $BillingReportFlag
              ? qq|$inv->{$CurPeriod}->{$SCID}->{$TrID}->{Amt}\t|
              : " \t";
            $out .= qq|\n|;
            $tabs = "\t\t\t\t\t\t\t\t";
        }
    }
    return ($out);
}
