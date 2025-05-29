#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
use myConfig;
use DBA;
use myForm;
use myDBI;
use myHTML;

############################################################################
my $form = myForm->new();
my $cdbh = myDBI->dbconnect('okmis_config');

my ( $title, $hdr ) = ( 'Treatment Plan Problems/Goals', '' );
my @Nums  = ();
my @Probs = ();
my @Goals = ();
my @Cnts  = ();
my @Objs  = ();
my $sxNS  = $cdbh->prepare("select * from xNS where ID=?");
$sxNS->execute( $form->{'id'} )
  || $form->dberror("TPPG: select id error ($form->{'id'}");

if ( my $rxNS = $sxNS->fetchrow_hashref ) {
    $hdr = $rxNS->{'Descr'};
    my $sxPG = $cdbh->prepare("select * from xPG where NSID=? order by Num");
    $sxPG->execute( $rxNS->{'ID'} )
      || $form->dberror("TPPG: select PG error ($rxNS->{'ID'}");
    while ( my $rxPG = $sxPG->fetchrow_hashref ) {
        push( @Nums,  $rxPG->{'Num'} );
        push( @Probs, $rxPG->{'Problem'} );
        push( @Goals, $rxPG->{'Goal'} );
        my $rOBJ = ();
        my $cnt  = 0;
        my $sxOBJ =
          $cdbh->prepare("select * from xOBJ where PGID=? order by Num");
        $sxOBJ->execute( $rxPG->{'ID'} )
          || $form->dberror("TPPG: select OBJ error ($rxPG->{'ID'}");
        while ( my $rxOBJ = $sxOBJ->fetchrow_hashref ) {
            $cnt++;
            $rOBJ->{$cnt} = $rxOBJ->{'Descr'};
            $rOBJ->{$cnt} .= '(number mismatch)' if ( $cnt != $rxOBJ->{'Num'} );
        }
        push( @Objs, $rOBJ );
        $sxOBJ->finish();
    }
    $sxPG->finish();
}
if ( scalar(@Nums) == 0 ) {
    push( @Nums,  0 );
    push( @Probs, 'None found' );
}
$sxNS->finish();
myDBI->cleanup();
main->html($form);
exit;
############################################################################
sub html {
    my ( $self, $form ) = @_;
    my $viewedby =
      $form->{LOGINUSERTYPE} > 3 ? $form->{LOGINUSERNAME} : $form->{LOGINNAME};
    print qq|Content-type: text/html\n\n
<!DOCTYPE html>
<HTML>
<HEAD> <TITLE>Provider Reports</TITLE>
  <LINK REL="stylesheet" TYPE="text/css" HREF="|
      . myConfig->cfgfile( 'main.css', 1 ) . qq|" >
  <LINK REL="stylesheet" TYPE="text/css" HREF="/cgi/jcal/calendar-forest.css" >
  <SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/utils.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-en.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-setup.js"></SCRIPT>
  <SCRIPT TYPE="text/javascript" >setTimeout('self.close();',3600000);</SCRIPT>
</HEAD>
<BODY ONCLICK="checkInputWindow()" ONUNLOAD="checkInputWindow()" >
<DIV ID="textMsgLayer" STYLE="position: absolute; z-index: 1000; visibility: hidden; left: 0px; top: 0px; width: 10px">&nbsp;</DIV>
<DIV CLASS="heading" >Problem/Goals</DIV>
<DIV CLASS="title" >for ${viewedby}</DIV>
<DIV ALIGN=center > 
<DIV CLASS="title" >${title}</DIV>
<DIV CLASS="title" >${hdr}</DIV>
<TABLE CLASS="home" >
  <TR CLASS="home" >
    <TH ALIGN="left" >Number</TH>
    <TH ALIGN="left" >Problems</TH>
    <TH ALIGN="left" >Goals</TH>
  </TR>
|;
    my $i = 0;
    foreach my $Num (@Nums) {
        print
qq|<TR CLASS="home" ><TD CLASS="strcol" >${Num}</TD><TD CLASS="strcol" >$Probs[$i]<TD CLASS="strcol" >$Goals[$i]</TD>\n|;
        my $rOBJ = $Objs[$i];
        foreach my $cnt ( sort { $a <=> $b } keys %{$rOBJ} ) {
            print
qq|<TR CLASS="home" ><TD CLASS="strcol" >&nbsp;</TD><TD CLASS="strcol" >Objective ${cnt}:</TD><TD CLASS="strcol" >$rOBJ->{$cnt}</TD>\n|;
        }
        $i++;
    }
    print qq|</TABLE>\n|;
    print qq|</FORM></BODY></HTML>\n|;
    return ();
}
############################################################################
