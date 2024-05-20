#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';

use CGI::Carp qw(fatalsToBrowser);
use DBI;
use myForm;
use myDBI;
use myHTML;
use DBUtil;
use Cwd;
use Time::Local;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});

############################################################################
my $CloseButton = qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;
my $html =  myHTML->close(1,$form->{'mlt'});

if($form->{submit}) {
    $html = main->submit($form);
} else {
    $html = main->printNotesType();
}
myDBI->cleanup();
print $html;
exit;

sub printNotesType {
    my $html = myHTML->newHTML($form,'Unreconcile Form','CheckPopupWindow noclock countdown_10') . qq|
                    <P>
                    <P>
                    <SCRIPT LANGUAGE="JavaScript" src="/cgi/js/novalidate.js"> </SCRIPT>
                    <SCRIPT LANGUAGE="JavaScript" src="/cgi/js/tablesort.js"> </SCRIPT>
                    <LINK href="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
                    <DIV CLASS="home title hdrcol" >
                        <FORM  ACTION='/cgi/bin/unRecNoteForm.pl' NAME='submit' METHOD='POST'>
                            <TABLE CLASS='home hdrcol' >
                                <TR>
                                    <TD CLASS="numcol" >Enter TrID:</TD>
                                    <TD>
                                        <INPUT TYPE='TEXT' NAME='TrIDs' >
                                    </TD>
                                </TR>
                                <TR >
                                    <TD CLASS="numcol" >Note Type:</TD>
                                    <TD CLASS='hdrcol' >
                                        <UL>
                                            <LI><INPUT TYPE='radio' NAME='noteType' VALUE='Sch' > Scholorshiped</LI>
                                            <LI><INPUT TYPE='radio' NAME='noteType' VALUE='Auto' > Auto</LI>
                                            <LI><INPUT TYPE='radio' NAME='noteType' VALUE='New' > New</LI>
                                            <LI><INPUT TYPE='radio' NAME='noteType' VALUE='notetobilled' > note to billed</LI>
                                        </UL>
                                    </TD >
                                </TR>
                                <TR>
                                <TD>
                                    <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="Reconcile" >
                                </TD>
                                    <INPUT TYPE='hidden' NAME='mlt' VALUE=$form->{mlt} >
                                    <INPUT TYPE='hidden' NAME='misLINKS' VALUE=$form->{misLINKS} >
                                    <INPUT TYPE='hidden' NAME='LINKID' VALUE=$form->{LINKID} >

                                </TR>
                            </TABLE >
                        </FORM>
                        </DIV>
                </BODY>
            </HTML>
            |;
        return($html);
}

sub submit {
    my $SBIN = myConfig->cfg('SRCSBIN');
    $cmd = qq|${SBIN}/unRecNote|;

    $TrIDs = $form->{TrIDs};

    $cmd .= qq| "DBNAME=$form->{'DBNAME'}&mlt=$form->{'mlt'}&TrIDs=$TrIDs&$form->{noteType}=1"|; 
    my $output = `$cmd 2>&1`;  # Capture both standard output and error output
    my $exit_status = $? >> 8;  # Get the lower 8 bits of the exit status
    if ($exit_status ne 0) {
       # Command encountered an error
       print "Command encountered an error. Exit status: $exit_status\n";
    }

    $html = my $html = myHTML->newHTML($form,"UnReconcilled Queries",'CheckPopupWindow noclock countdown_10') . qq|
        <P>
        <P>
        <SCRIPT LANGUAGE="JavaScript" src="/cgi/js/novalidate.js"> </SCRIPT>
        <FORM NAME="submit" ACTION="" METHOD="POST">
        <DIV CLASS="strcol" >
        Results:
        <PRE>
        ${output}
        </PRE>
        </DIV>
        <P>
        <DIV CLASS="strcol" >
        </DIV>
        <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
        <INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
        <INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
        </FORM>
        <SCRIPT>
            window.close()
        </SCRIPT>
        </BODY>
        </HTML>
        |;
    return($html);
}
