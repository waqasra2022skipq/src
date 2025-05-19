#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
############################################################################
use CGI       qw(:standard escape);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use DBI;
use myForm;
use login;
use SysAccess;
use myConfig;
use DBA;
use myDBI;
use myHTML;
use Time::Local;

#use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;

############################################################################
# Allows for argument now in new('instring');
##
#warn "\nmis: ENTER: MIS_Action=$form->{'MIS_Action'}, fwdLINK=$form->{fwdLINK}\n";

my $form = myForm->new();

#warn "\nmis: ENTER: MIS_Action=$form->{'MIS_Action'}, fwdLINK=$form->{fwdLINK}\n";
#warn "mis: ENTER: view=$form->{'view'}, newurl=$form->{newurl}, fwdLINK=$form->{fwdLINK}\n";
#foreach my $f ( sort keys %{$form} ) { warn "mis: $f=$form->{$f}\n"; }
#warn "mis: ENTER: LOGINSCREEN=$form->{'LOGINSCREEN'}\n";

my $dbh         = myDBI->dbconnect( $form->{'DBNAME'} );
my $post_update = '';
my $LOGDIR      = myConfig->cfg('LOGDIR');

############################################################################
# Main routine for all HTML FORMs.
# This routine is called:
# 1) by links on the Manager Tree, Client & Chart Lists, and Client Page.
#    this methods uses both GET and POST.
# 2) from the dynamic htmls created for input FORMS.
#    this methods normally uses just POST.
############################################################################

############################################################################
##
# eg: <A HREF="/src/cgi/bin/mis.cgi?MIS_Action=action&id=${id}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}" >action<A>
# eg: <INPUT TYPE=submit NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
##

############################################################################
if ( $form->{'logout'} ) {

    #warn "mis: logout: mlt=$form->{'mlt'}\n";
    #warn "mis: logout: LOGINSCREEN=$form->{'LOGINSCREEN'}\n";
    if ( $form->{mlt} ) {
        my $s = $dbh->prepare("delete from Login where token='$form->{mlt}'");
        $s->execute();
        $s = $dbh->prepare("delete from History where Token='$form->{mlt}'");
        $s->execute();
        $s->finish();
    }
    myDBI->cleanup();

#foreach my $f ( sort keys %{$form} ) { warn "mis: logout: $f=$form->{$f}\n"; }
# suprisingly the self for login is preserved from the myForm->new() call above.
# but I added form anyway.
    print login->login( $form, 'You have been successfully logged out.' );
    exit;
}
elsif ( $form->{'UpdateTables'} ) {

#warn qq|WATCH POST_UPDATE: $form->{OPENTABLES}.\n|;
#foreach my $f ( sort keys %{$form} ) { warn "UpdateTables: $f=$form->{$f}\n"; }
    $post_update = DBA->updSQL($form);

    #warn qq|post_update:${post_update}:\n|;
}
elsif ( defined( $form->{'post_update'} ) ) {

# ADD THIS ELSE FOR UPDATING NOTES WITHOUT UPDATING ALL THE FIELDS - TO CALL POSTUPDATE ONLY
#warn qq|WATCH ELSE POST_UPDATE: $form->{OPENTABLES}.\n|;
    unless ( DBA->updSQLdone($form) ) {

        #warn qq|WATCH ELSE POST_UPDATE: $form->{OPENTABLES} NOT DONE YET.\n|;
        $post_update = myDBI->exFunc( $form, $form->{'post_update'} );
        delete $form->{'post_update'};
        ##
 # Close/Clear our internal array.
 #   Do this AFTER updates to leave Header tables Open for Detail tables to use.
        ##
        foreach my $TABLE ( split( /,/, $form->{'OPENTABLES'} ) ) {
            DBA->clrFields( $form, $TABLE );
            delete $form->{ 'OPENTABLE:' . $TABLE };
        }
        delete $form->{'OPENTABLES'};
    }
}

my $NextLocation = qq|Location: /index.shtml\n\n|;
my $PostLocation = qq|/index.shtml|;
my $disLoc       = '';
############################################################################
# Send back HTML response.  If redirection is used, redirect user to the
# URL.  If there is a template being used, parse it and send it to the user
# or send out a generic response if neither of the above is defined.
############################################################################
# >>> ADD <<<
# >>> ADD <<< form->{prompt} to NexLocation
# >>> ADD <<<
# keep for vlogin.cgi (both cookies set)
#   used when already logged in and they hit the browser url reload
#   takes them back to their LOGINSCREEN

if ( $form->{'vlogin'} ) {

#warn qq|mis-vlogin: vlogin=$form->{'vlogin'}, LOGINSCREEN=$form->{LOGINSCREEN}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "$f=$form->{$f}\n"; }
    $form->{'MIS_Action'}    = $form->{'LOGINSCREEN'};
    $form->{ProviderID}      = $form->{LOGINPROVID};
    $form->{Provider_ProvID} = $form->{LOGINPROVID};
}
my $url = $form->{misPOP} ? myForm->popLINK( $form->{misPOP} ) : '';

#warn qq|mis-url: ${url}\n|;
my $link = myForm->genLINK( $form->{MIS_Action} );
if ($url) {

    #warn qq|mis-url: ${url}\n|;
    $NextLocation = qq|Location: $url\n\n|;

    #warn qq|NextLocation: ${NextLocation}\n|;
    $PostLocation = $url;    # for post_update.
}
elsif ($link) {

    # need to continue this using ForProvID, ForClientID...or maybe for ARGS...
    #warn qq|mis-link: ${link}\n|;
    $NextLocation = qq|Location: $link\n\n|;
}
elsif ( $form->{'CLOSEWINDOW'} eq 'CLOSE' )    # for this to work DON'T misPOP=1
{
    #warn qq|mis-close: \n|;
    $NextLocation = myHTML->close();
}
elsif ($form->{'MIS_Action'} eq 'MgrTree'
    || $form->{'MIS_Action'} eq 'ManagerTree' )
{
    #warn qq|mis-MgrTree: Action=$form->{'MIS_Action'}\n|;
    $NextLocation =
qq|Location: /src/cgi/bin/ManagerTree.cgi?mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
    $disLoc = 'MgrTree';
}
elsif ( $form->{'MIS_Action'} eq 'Note' ) {
    $view = DBA->getNoteView( $form, $form->{Treatment_TrID} );

    #warn qq|mis: Note=$view\n|;
    my $html = myHTML->getHTML( $form, ${view} );
    $NextLocation = $html;
    $disLoc       = $view;
}
elsif ( $form->{'MIS_Action'} eq 'ClientList' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/ClientList.cgi?Provider_ProvID=$form->{Provider_ProvID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'MIS_Action'} eq 'ChartList' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/ChartList.cgi?Provider_ProvID=$form->{Provider_ProvID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'MIS_Action'} eq 'ClientPage' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/ClientPage.cgi?Client_ClientID=$form->{Client_ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&FULL=$form->{FULL}\n\n|;
}
elsif ( defined( $form->{'view'} ) ) {

    #warn qq|mis-view: $form->{'view'}\n|;
    my $html = myHTML->getHTML( $form, $form->{view} );
    $NextLocation = $html;
    $disLoc       = $form->{view};

}
elsif ( defined( $form->{'newurl'} ) ) {
    ( my $url = $form->{'newurl'} ) =~ s/\^/\?/;
    $url =~ s/\^/\&/g;

    #warn qq|\nurl=${url}\n|;
    $NextLocation =
      qq|Location: ${url}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'MIS_Action'} eq 'ClientPortal' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/ClientPortal.cgi?mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'MIS_Action'} eq 'ManagePortal' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/ManagePortal.cgi?mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'LOGINSCREEN'} ne '' ) {
    $NextLocation =
qq|Location: /src/cgi/bin/$form->{LOGINSCREEN}?mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
else {
    warn "WARN: Access Denied at END OF mis.cgi\n";
    warn "WARN: NextLocation=$NextLocation\n";
    open AERR, ">>${LOGDIR}/ENDOF" or warn "Can't open errors file (!$).";
    $now = localtime();
    print AERR qq|\n$form->{LOGINUSERNAME}: END OF mis.cgi @ $now\n|;
    foreach my $f ( sort keys %{$form} ) { print AERR "$f=$form->{$f}\n"; }
    close(AERR);
}
############################################################################
main->post() if ($post_update);

$disLoc = $NextLocation if ( $disLoc eq '' );
myDBI->cleanup();

# warn qq|\n\nnow print NextLocation=\n$NextLocation| if ( $form->{LOGINPROVID} );
print $NextLocation;
exit;

############################################################################
sub post {

    #warn qq|WATCH sub post ${post_update}\n|;
    #warn qq|PostLocation=${PostLocation}=\n|;
    print myHTML->new( $form, "Continue" );
    print qq|

<FORM ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<DIV ALIGN="center" >
<HR WIDTH="90%" >
${post_update}
<HR WIDTH="90%" >
<A HREF="${PostLocation}" >continue</A>
</FORM>
|;
##  print myHTML->rightpane($form,'search');
    myDBI->cleanup();
    exit;
}

sub env {
    print "content-type: text/html\n\n";
    print "<HTML>
<HEAD><TITLE>Environment Varibles</TITLE></HEAD>
<BODY BGCOLOR=\"FFFFFF\"
<CENTER><H1>Environment Variables</H1></CENTER>
<P>";
    foreach $var ( sort keys %ENV )     { print "$var = $ENV{$var}<BR>\n"; }
    foreach $var (@_SERVER)             { print "$var = $_SERVER[$var]<BR>\n"; }
    foreach $var ( sort keys %{$form} ) { print "$var = $form->{$var}<BR>\n"; }

    print "</BODY></HTML>\n";
    exit;
}
############################################################################
