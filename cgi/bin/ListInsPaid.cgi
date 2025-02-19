#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBUtil;
use myHTML;

############################################################################
$form = DBForm->new();
my $ClientID = $form->{'Client_ClientID'};
unless ( SysAccess->verify( $form, 'hasClientAccess', $ClientID ) ) {
    $form->error("List Insurance Payments Access Page / Not Client");
}

my $addLinks  = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;
my $BackLinks = gHTML->setLINKS( $form, 'back' );
$form->{'FORMID'} = $form->getFORMID;

my $dbh     = $form->dbconnect();
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
$sClient->execute($ClientID);
my $rClient    = $sClient->fetchrow_hashref;
my $ClientName = qq|$rClient->{FName} $rClient->{LName} ($rClient->{ClientID})|;
my $sProvider  = $dbh->prepare("select * from Provider where ProvID=?");
############################################################################
my $html = myHTML->newPage( $form, "Insurance Payments" ) . qq|
<FORM NAME="List" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript"> function validate(form) { return(1); } </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/tablesort.js"> </SCRIPT>
<LINK HREF="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >Insurance Payments Unreconciled: ${ClientName} </TD>
    <TD CLASS="numcol" > ${BackLinks}</TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="port strcol" >
      These Insurance Payments can be assigned to notes entered for this client from the Chart List Screen. These Insurance payments with a Reconcile amount less than the Paid amount will show up there and can be tagged to one of the notes entered and thereby reconciled to that note.<BR>Wait to apply these to a note until the note is billed/reconciled, otherwise if you apply a payment to a note it 'Reconciles' the note and then the note cannot be billed.
    </TD>
  </TR>
</TABLE>
|;
$html .= main->List( $form, $ClientID );
$html .= qq|
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="hdrcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" ONMOUSEOVER="window.status='new';return true;" ONMOUSEOUT="window.status=''" NAME="view=InsPaid.cgi&fwdTABLE=InsPaid&InsPaid_ID=new&Client_ClientID=${ClientID}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="Add Payment" >
    </TD>
  </TR>
</TABLE>
</FORM >
|;
$html .= myHTML->rightpane( $form, 'search' );
$sClient->finish();
print $html;
exit;

############################################################################
# Output the List part of the HTML.
sub List {
    my ( $self, $form, $ClientID ) = @_;
    my $dbh = $form->dbconnect();
    my $qList =
qq|select InsPaid.*, Client.LName, Client.FName from InsPaid left join Client on Client.ClientID=InsPaid.ClientID where Client.ClientID='${ClientID}' order by InsPaid.TransDate desc|
      ;    #  and PaidAmt!=RecAmt|;

    #warn "ListInsPaid.cgi: query=$query\n";
    $sList = $dbh->prepare($qList);
    my $html = qq|
<TABLE class="chartsort table-autosort table-stripeclass:alternate fullsize">
<THEAD>
  <TR >
    <TH CLASS="table-sortable:default" >Type</TD>
    <TH CLASS="table-sortable:date" >StartDate</TD>
    <TH CLASS="table-sortable:date" >EndDate</TD>
    <TH CLASS="table-sortable:default" >InsCode</TD>
    <TH CLASS="table-sortable:default" >RefID</TD>
    <TH CLASS="table-sortable:date" >TransDate</TD>
    <TH CLASS="table-sortable:currency" >BillAmt</TD>
    <TH CLASS="table-sortable:currency" >PaidAmt</TD>
    <TH CLASS="table-sortable:numeric" >ICN</TD>
    <TH CLASS="table-sortable:currency" >RecAmt</TD>
    <TH CLASS="table-sortable:default" >EnteredBy</TD>
    <TH CLASS="table-sortable:date" >EnteredOn</TD>
    <TH CLASS="table-nosort" >&nbsp;</TD>
  </TR>
</THEAD>
<TBODY>
|;
    my ( $BillTot, $PaidTot, $RecTot ) = ( 0, 0, 0 );
    my $count = 0;
    $sList->execute();
    while ( $rList = $sList->fetchrow_hashref ) {
        $count += 1;
        my $printlink =
qq|  <A HREF="javascript:ReportWindow('/cgi/bin/genReceipt.cgi?InsPaid_ID=$rList->{ID}&mlt=$form->{mlt}','PrintWindow')" ONMOUSEOVER="textMsg.show('print')" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 SRC="/images/icon_print.gif" ></A>|;
        my $even      = int( $count / 2 ) == $count / 2 ? '1' : '0';
        my $class     = $even ? qq|CLASS="alternate"|         : '';
        my $StartDate = DBUtil->Date( $rList->{StartDate}, 'fmt', 'MM/DD/YY' );
        my $EndDate   = DBUtil->Date( $rList->{EndDate},   'fmt', 'MM/DD/YY' );
        my $TransDate = DBUtil->Date( $rList->{TransDate}, 'fmt', 'MM/DD/YY' );
        my $TrIDs     = qq|<OPTION SELECTED VALUE="" >unselected|;

        foreach my $TrID ( sort keys %{ $Client_TrIDs->{$ClientKey} } ) {
            $TrIDs .= qq|<OPTION VALUE="$TrID" >$TrID|;
        }
        my $amt = $rList->{PaidAmt} - $rList->{RecAmt};
        $sProvider->execute( $rList->{CreateProvID} );
        $rProvider = $sProvider->fetchrow_hashref;
        my $EnteredOn = DBUtil->Date( $rList->{CreateDate}, 'fmt', 'MM/DD/YY' );
        my $button =
          $rList->{InsCode} eq ''
          ? qq|    <INPUT TYPE="submit" ONCLICK="return validate(this.form)" ONMOUSEOVER="window.status='$rList->{ID}';return true;" ONMOUSEOUT="window.status=''" NAME="view=InsPaid.cgi&fwdTABLE=InsPaid&InsPaid_ID=$rList->{ID}&Client_ClientID=$rList->{ClientID}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="View/Edit" >|
          : "&nbsp;";
        $html .= qq|
  <TR ${class} >
    <TD >${printlink}$rList->{Type}</TD>
    <TD >${StartDate}</TD>
    <TD >${EndDate}</TD>
    <TD >$rList->{InsCode}</TD>
    <TD >$rList->{RefID}</TD>
    <TD >${TransDate}</TD>
    <TD >$rList->{BillAmt}</TD>
    <TD >$rList->{PaidAmt}</TD>
    <TD >$rList->{ICN}</TD>
    <TD >$rList->{RecAmt}</TD>
    <TD >$rProvider->{LName}</TD>
    <TD >${EnteredOn}</TD>
    <TD >${button}</TD>
  </TR>
|;
        $BillTot += $rList->{BillAmt};
        $PaidTot += $rList->{PaidAmt};
        $RecTot  += $rList->{RecAmt};
    }
    $BillTot = sprintf( "%.2f", $BillTot );
    $PaidTot = sprintf( "%.2f", $PaidTot );
    $RecTot  = sprintf( "%.2f", $RecTot );
    $html .= qq|
</TBODY>
  <TR CLASS="port" >
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >${BillTot}</TD>
    <TD >${PaidTot}</TD>
    <TD >&nbsp;</TD>
    <TD >${RecTot}</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
    <TD >&nbsp;</TD>
  </TR>
</TABLE>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('print','Click here to print this Receipt.');</SCRIPT>
|;
    $sList->finish();
    return ($html);
}
############################################################################
