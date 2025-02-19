#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use DBA;
use myHTML;
use Time::Local;
$DT = localtime();
############################################################################
my $form  = DBForm->new();
my $ID    = $form->{'IDs'};      # DO WE NEED A LOOP?
my $table = $form->{'action'};

#foreach my $f ( sort keys %{$form} ) { warn "show_log: form-$f=$form->{$f}\n"; }
my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $dbh       = $form->dbconnect();

my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

#my $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID');
#$ClinicSelection .= qq| and Client.Active=1| if ( $form->{Active} );
############################################################################
my ( $cnt, $reportlines ) = ( 0, '' );
my $prev = ();
my $select =
qq|select Log${table}.* from Log${table} where Log${table}.ID=${ID} order by Log${table}.ChangeDate|;

#warn qq|select=$select\n|;
my $s = $dbh->prepare($select);
$s->execute() || $form->dberror($select);
while ( my $current = $s->fetchrow_hashref ) {
    $cnt++;

    #warn qq|cnt=${cnt}, LogID=$current->{'LogID'}\n|;
    if ( $cnt == 1 ) { null; }
    else { $reportlines .= main->difFields( $form, $table, $current, $prev ); }
    $prev = $current;
}
$s->finish();
if ( $cnt > 0 ) {
    my $select =
qq|select ${table}.* from ${table} where ${table}.ID=${ID} order by ${table}.ChangeDate|;

    #warn qq|select=$select\n|;
    my $s = $dbh->prepare($select);
    $s->execute() || $form->dberror($select);
    if ( my $current = $s->fetchrow_hashref ) {
        $reportlines .= main->difFields( $form, $table, $current, $prev );
    }
    $s->finish();
}
$sProvider->finish();
$form->complete();
############################################################################
my $report =
qq|${DT}\nLogged activity count=${cnt}.\nType\tField\tFrom\tTo\tProvider\tDateTime\n${reportlines}|;

#print qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>${Name}</TITLE></HEAD>\n<BODY >|
#    . gHTML->htmlReport($html,$hdrline) . qq|\n</BODY>\n</HTML>\n|;
my $html = myHTML->newHTML(
    $form,
    'Logged activity report',
    'CheckPopupWindow noclock countdown_1'
  )
  . gHTML->htmlReport( $report, 3 )
  . qq|\n</BODY>\n</HTML>\n|;
print $html;
exit;
############################################################################
sub difFields {
    my ( $self, $form, $table, $cRecord, $pRecord ) = @_;
    my $out  = '';
    my @flds = ();
    foreach my $key ( sort keys %{$cRecord} ) {
        next                if ( $key eq 'LogID' );
        next                if ( $key eq 'CreateDate' );
        next                if ( $key eq 'CreateProvID' );
        next                if ( $key eq 'ChangeDate' );
        next                if ( $key eq 'ChangeProvID' );
        next                if ( $key eq 'FormID' );
        push( @flds, $key ) if ( $cRecord->{$key} ne $pRecord->{$key} );
    }
    $sProvider->execute( $cRecord->{'ChangeProvID'} )
      || $form->dberror("show_log: select Provider $cRecord->{'ChangeProvID'}");
    my $rProvider = $sProvider->fetchrow_hashref;
    my $ProvName =
      $rProvider->{ScreenName} eq ''
      ? qq|$rProvider->{'FName'} $rProvider->{'LName'} $rProvider->{'Suffix'}|
      : $rProvider->{'ScreenName'};
    foreach my $fld (@flds) {

        #warn qq|fld=${fld}\n|;
        #warn qq|cRecord=$cRecord->{'ID'}, $cRecord->{'ChangeDate'}\n|;
        #warn qq|pRecord=$pRecord->{'ID'}, $pRecord->{'ChangeDate'}\n|;
        $out .= qq|CHANGED|;
        $out .= qq|\t$fld|;
        $out .= qq|\t$pRecord->{$fld}|;
        $out .= qq|\t$cRecord->{$fld}|;
        $out .= qq|\t${ProvName}|;
        $out .= qq|\t$cRecord->{'ChangeDate'}|;
        $out .= qq|\n|;
    }
    return ($out);
}
############################################################################
