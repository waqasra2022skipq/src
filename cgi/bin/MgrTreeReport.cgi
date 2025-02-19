#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
my $form   = DBForm->new();
my $dbh    = $form->dbconnect();
my $addURL = "mlt=$form->{mlt}&misLINKS=$form->{misLINKS}";
$form->pushLINK();    # save this link/page to return to.

# Access Required.
if ( !$form->{Provider_ProvID} ) {
    $form->error("Provider Manager Tree Report / denied ProvID NULL");
}
unless ( SysAccess->chkPriv( $form, 'ProviderACL' ) ) {
    $form->error("Access Denied! (Provider Manager Tree Report)");
}

my $html = myHTML->new($form) . qq|
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD >
|;
$html .= main->genTreeFlat( $form, $form->{'Provider_ProvID'} );
$html .= qq|
    </TD>
  </TR>
</TABLE>
|;
$form->complete();
print $html;
exit;
############################################################################
# Print out the Tree for this Provider.
sub genTreeFlat {
    my ( $self, $form, $ProvID ) = @_;
    my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
    $sProvider->execute($ProvID);
    my $rProvider = $sProvider->fetchrow_hashref;
    my $out       = qq|
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" >
    <TD CLASS="hdrcol heading" COLSPAN="2" >Managerial Tree for $rProvider->{'FName'} $rProvider->{'LName'}</TD>
  </TR>
|;
    my $mtree        = '';
    my $sManagerTree = $dbh->prepare(
        "select * from ManagerTree where TreeProvID=? order by Cnt");
    $sManagerTree->execute($ProvID);

    while ( my $r = $sManagerTree->fetchrow_hashref ) {
        $mtree .= main->genHTML( $form, $r );
    }
    $out .= $mtree . qq|
</TABLE>
|;
    $sManagerTree->finish();
    $sProvider->finish();
    return ($out);
}

# Print out this Provider.
sub genHTML {
    my ( $self, $form, $r ) = @_;
    my $Spacer =
      qq|  <IMG HEIGHT=1 WIDTH="$r->{Indent}" SRC="/images/blank.gif">|;
    my $ProvInfo = '';
    if ( $r->{Clinician} ) {
        $ProvInfo .= qq|
      <IMG BORDER=0 ALT="Client-List by Provider" SRC="/images/icon_folder.gif">
      <IMG BORDER=0 ALT="Chart-List by Provider" SRC="/images/clipboard.gif">
      &nbsp;
|;
    }
    $ProvInfo .= qq|$r->{Name}|;
    my $Info  = '';
    my $Email = qq|<A HREF="mailto:$r->{Email}">$r->{Email}</A>|;
    my $out .= qq|
    <TR>
      <TD CLASS="title" >
        ${Spacer}
        ${ProvInfo}
        ${Info}
        ${Email}
      </TD>
    </TR>
|;
    return ($out);
}
############################################################################
