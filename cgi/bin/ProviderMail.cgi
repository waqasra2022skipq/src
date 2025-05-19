#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use Time::Local;
use DBI;
use DBForm;
use SysAccess;
use DBA;
use myHTML;

############################################################################
$form = DBForm->new();
my $dbh = $form->dbconnect();

#warn qq|\nENTER: ProviderMail.cgi\n|;
#warn qq|\nProviderMail: MIS_Action=$form->{MIS_Action}, section=$form->{section}, FORMID=$form->{FORMID}\n|;
##
# get list of Providers.
##
$xref = 'Providers';
$s    = $dbh->prepare("select * from Provider order by LName, FName");
$s->execute();
while ( my $r = $s->fetchrow_hashref ) { $$xref{ $r->{ProvID} } = $r; }
$s->finish;
##
# Access required: always the LOGIN Provider
##
my $ProvID   = $form->{"LOGINPROVID"};
my $ProvName = qq|$Providers{$ProvID}{FName} $Providers{$ProvID}{LName}|;
my $NoMail   = $Providers{$ProvID}{NoMail};
my $MailOff =
'Receipt of Mail Off. Click here to toggle Mail On. This will place your mail address in others To: list.';
my $MailOn =
'Receipt of Mail On. Click here to toggle Mail Off. This will remove your mail address from others To: list so you will not receive mail from others.';
my $NoMailTxt = $NoMail ? $MailOff             : $MailOn;
my $NoMailIMG = $NoMail ? '/images/mailto.gif' : '/images/mailpage.gif';
############################################################################
$qListMail =
qq|select * from ProviderMail where ProvID=? and Flag=? order by CreateDate desc|;
$sListMail = $dbh->prepare($qListMail);
$qMailUpd  = qq|update ProviderMail set Flag=? where ID=?|;
$sMailUpd  = $dbh->prepare($qMailUpd);
$qMailDEL  = qq|delete from ProviderMail where ID=?|;
$sMailDEL  = $dbh->prepare($qMailDEL);

############################################################################
my $Agent     = SysAccess->verify( $form, 'Privilege=Agent' );
my $ID        = $form->{'ProviderMail_ID'};
my $showdflag = $form->{'showd'};

#warn qq|\nENTER: ProviderMail.cgi\nshowd=$form->{showd}, $showdflag\n|;
if ( $form->{MIS_Action} =~ /update/i ) {
    unless ( DBA->updSQLdone($form) ) {
        my $ToProvID = $form->{'ProviderMail_ToProvID_1'};
        my $Subject  = $form->{'ProviderMail_Subject_1'};
        my $Message  = $form->{'ProviderMail_Message_1'};
        my $DateSent = DBUtil->Date( '', 'stamp', 'long' );

#foreach my $f ( sort keys %{$form} ) { warn "ProviderMail: form-$f=$form->{$f}\n"; }
        my $qInsert = qq|
INSERT INTO ProviderMail (ProvID,FromProvID,ToProvID,Subject,Message,DateSent,Flag,CreateProvID,CreateDate,ChangeProvID) 
                  VALUES (?,?,?,?,?,?,?,?,?,?)|;
        my $sInsert = $dbh->prepare($qInsert);
        $sInsert->execute(
            $ProvID,        $ProvID,   $ToProvID, $Subject,
            $Message,       $DateSent, 'sent',    $ProvID,
            $form->{TODAY}, $ProvID
        ) || $form->dberror($qInsert);
        foreach my $p ( split( chr(253), $ToProvID ) ) {
            $sInsert->execute(
                $p,             $ProvID,   $ToProvID, $Subject,
                $Message,       $DateSent, 'inbox',   $ProvID,
                $form->{TODAY}, $ProvID
            ) || $form->dberror($qInsert);
        }
        $sInsert->finish();
    }
    print
qq|Location: /cgi/bin/ProviderMail.cgi?mlt=$form->{mlt}\&showd=$form->{showd}\&prompt=$form->{prompt}\n\n|;
}
elsif ( $form->{MIS_Action} =~ /delete/i || $form->{MIS_Action} =~ /purge/i ) {
    unless ( DBA->updSQLdone($form) ) {
        my $qMail = qq|select * from ProviderMail where ID=?|;
        my $sMail = $dbh->prepare($qMail);

        #warn qq|ProviderMail: ID=$ID, qMail=$qMail\n|;
        $sMail->execute($ID) || $form->dberror($qMail);
        if ( my $rMail = $sMail->fetchrow_hashref ) {

#warn qq|ProviderMail: $form->{MIS_Action}: ID=$ID=$rMail->{ID}, Flag=$rMail->{Flag}, qMailUpd=\n$qMailUpd\n|;
            if ( $form->{MIS_Action} =~ /purge/i ) {
                my $qMailLog =
                  DBA->genInsert( $form, 'ProviderMailLog', $rMail );
                $sMailLog = $dbh->prepare($qMailLog);
                $sMailLog->execute()               || $form->dberror($qMailLog);
                $sMailDEL->execute( $rMail->{ID} ) || $form->dberror($qMailDEL);
            }
            else {
                $sMailUpd->execute( 'deleted', $rMail->{ID} )
                  || $form->dberror($qMailUpd);
            }
        }
        $sMail->finish();
    }
    print
qq|Location: /cgi/bin/ProviderMail.cgi?mlt=$form->{mlt}\&showd=$form->{showd}\&prompt=$form->{prompt}\n\n|;
}
elsif ( $form->{MIS_Action} =~ /back/i ) {
    print
qq|Location: /cgi/bin/mis.cgi?MIS_Action=MgrTree&mlt=$form->{mlt}\&showd=$form->{showd}\n\n|;
}
elsif ( $form->{MIS_Action} =~ /read/i )    { main->Mail( 'read',    $ID ); }
elsif ( $form->{MIS_Action} =~ /forward/i ) { main->Mail( 'forward', $ID ); }
elsif ( $form->{MIS_Action} =~ /send/i )    { main->Mail( 'send',    '' ); }
elsif ( $form->{MIS_Action} =~ /nomail/i ) {
    $NoMail = $NoMail ? 0 : 1;
    my $qNoMail = qq|update Provider set NoMail=$NoMail where ProvID=?|;
    my $sNoMail = $dbh->prepare($qNoMail);
    $sNoMail->execute($ProvID) || $form->dberror($qNoMail);
    $NoMailTxt = $NoMail ? $MailOff             : $MailOn;
    $NoMailIMG = $NoMail ? '/images/mailto.gif' : '/images/mailpage.gif';
    main->ListMail();
}
elsif ( $form->{MIS_Action} =~ /delall/i || $form->{MIS_Action} =~ /purall/i ) {

  #warn qq|ProviderMail: before: $form->{MIS_Action}: FORMID=$form->{FORMID}\n|;
    unless ( DBA->updSQLdone($form) ) {
        my $section = $form->{section};

  #warn qq|ProviderMail: inside: $form->{MIS_Action}: FORMID=$form->{FORMID}\n|;
        $sListMail->execute( $ProvID, $section )
          || $form->dberror("List Mail=$ProvID ($section)");
        while ( my $rListMail = $sListMail->fetchrow_hashref ) {

#warn qq|ProviderMail: $form->{MIS_Action}: ID=$ID=$rListMail->{ID},$rListMail->{Flag}\n|;
            if ( $form->{MIS_Action} =~ /purall/i ) {
                my $qMailLog =
                  DBA->genInsert( $form, 'ProviderMailLog', $rListMail );
                $sMailLog = $dbh->prepare($qMailLog);
                $sMailLog->execute() || $form->dberror($qMailLog);
                $sMailDEL->execute( $rListMail->{ID} )
                  || $form->dberror($qMailDEL);
            }
            else {
                $sMailUpd->execute( 'deleted', $rListMail->{ID} )
                  || $form->dberror($qMailUpd);
            }
        }
    }

   #warn qq|ProviderMail: after: $form->{MIS_Action}: FORMID=$form->{FORMID}\n|;
    main->ListMail();
}
else { main->ListMail(); }

$sListMail->finish();
$sMailUpd->finish();
$sMailDEL->finish();
$form->complete();
exit;
############################################################################
# Send mail for this Provider.
sub Mail {
    my ( $self, $Action, $MailID, $ProvList ) = @_;

    $form->{'FORMID'} = $form->getFORMID;
    my $ToMsg =
qq|Reply/Forward has all recipients (reply all)<BR>(use ctrl-key to select/deselect multiples)|;
    my ( $FromList, $ToList, $SubList, $MsgList, $Focus ) = (
        $ProvName,
        '',
        '',
        '',
'<SCRIPT LANGUAGE="JavaScript">document.ProviderMail.elements[0].focus();</SCRIPT>'
    );
    my ( $FromProvID, $ToProvID, $Subject, $Message, $ReplyButton ) =
      ( '', '', '', '', '' );
    my $list = ();

    # add to list all Providers for each Agency for this Provider.
    foreach my $a ( SysAccess->getACL( $form, $form->{LOGINPROVID}, 'Agency' ) )
    {
        foreach my $p ( SysAccess->getACL( $form, $a, 'Provider' ) ) {
            next if ( $Providers{$p}{NoMail} );
            next unless ( $Providers{$p}{Active} );
            $list->{"$Providers{$p}{LName}, $Providers{$p}{FName} ($p)"} = $p;
        }
    }
    my $selProv =
      DBA->makeSelect( $form, $ToProvID, $list, 'Provider', 'LName:FName' );
    if ( $Action eq 'read' || $Action eq 'forward' ) {
        my $qMail = qq|select * from ProviderMail where ID=?|;
        my $sMail = $dbh->prepare($qMail);
        $sMail->execute($MailID) || $form->dberror($qMail);
        if ( my $rMail = $sMail->fetchrow_hashref ) {
            if ( $rMail->{Flag} eq 'inbox' || $rMail->{Flag} eq '' ) {
                my ( $sec, $min, $hrs, $day, $month, $year, $wday, $julian ) =
                  localtime();
                $month++;
                $year += 1900;
                $month = length($month) == 2 ? $month : '0' . $month;
                $day   = length($day) == 2   ? $day   : '0' . $day;
                $hrs   = length($hrs) == 2   ? $hrs   : '0' . $hrs;
                $min   = length($min) == 2   ? $min   : '0' . $min;
                my $qMailRead =
qq|update ProviderMail set Flag='read', DateRead='$year$month$day$hrs$min' where ID=?|;
                my $sMailRead = $dbh->prepare($qMailRead);
                $sMailRead->execute($MailID) || $form->dberror($qMail);
                $sMailRead->finish();
            }
            $FromProvID = $rMail->{FromProvID};
            $Subject    = $rMail->{Subject};
            $Message    = $rMail->{Message};
            $DateSent   = $rMail->{DateSent};
            if ( $Action eq 'forward' ) {
                my $sc = '';
                foreach my $p ( split( chr(253), $rMail->{ToProvID} ) ) {
                    $ToList .=
                      qq|${sc}$Providers{$p}{FName} $Providers{$p}{LName}|;
                    $sc = '; ';
                }
                $Message =
qq|\n\n\n---- Original Message ----\nFrom:    $Providers{$FromProvID}{FName} $Providers{$FromProvID}{LName}\nTo:      $ToList\nSent:    $DateSent\nSubject: $Subject\n\n$Message|;
                $Subject = qq|Re: $Subject|
                  if ( substr( $Subject, 0, 4 ) ne 'Re: ' );

                # add who it came from and anyone else except LOGIN Provider.
                $ToProvID = $FromProvID == $ProvID ? '' : $FromProvID;
                foreach my $p ( split( chr(253), $rMail->{ToProvID} ) ) {
                    $ToProvID .= chr(253) . $p if ( $p != $ProvID );
                }

                #$selProv = DBA->selProviders($form,$ToProvID);
                $ToList =
qq|    <SELECT NAME="ProviderMail_ToProvID_1" MULTIPLE SIZE=5 >${selProv}</SELECT>|;
                $SubList =
qq|  <INPUT TYPE="text" NAME="ProviderMail_Subject_1" VALUE="${Subject}" ONFOCUS="select()" SIZE=60>|;
                $MsgList =
qq|  <TEXTAREA NAME="ProviderMail_Message_1" COLS=80 ROWS=18 WRAP="virtual" onFocus="select()" >${Message}</TEXTAREA>|;
                $DateSent = DBUtil->Date( '', 'stamp', 'long' );
            }
            else {
                $FromList = '';
                my $sc = '';
                foreach my $p ( split( chr(253), $rMail->{FromProvID} ) ) {
                    $FromList .=
                      qq|${sc}$Providers{$p}{FName} $Providers{$p}{LName}|;
                    $sc = '; ';
                }
                my $sc = '';
                foreach my $p ( split( chr(253), $rMail->{ToProvID} ) ) {
                    $ToList .=
                      qq|${sc}$Providers{$p}{FName} $Providers{$p}{LName}|;
                    $sc = '; ';
                }
                $SubList = qq|${Subject}|;
                ( $MsgList = $Message ) =~ s/[\n]/<BR>/g;
                $Focus = '';
            }
        }
        $sMail->finish();
        if ( $Action eq 'read' ) {
            $ToMsg       = qq|&nbsp;|;
            $ReplyButton = qq|
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="hdrtxt" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('DeleteMsg','Click here to DELETE this Mail Message.');</SCRIPT>
      Delete
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=delete&ProviderMail_ID=$MailID&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('DeleteMsg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
    <TD CLASS="hdrtxt" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('ForwardMsg','Click here to REPLY or FORWARD this Mail Message.');</SCRIPT>
      Reply
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=forward&ProviderMail_ID=$MailID&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('ForwardMsg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/icon_go_right.gif" ></A>
    </TD>
  </TR>
</TABLE>
|;
        }
    }
    elsif ( $Action eq 'send' ) {

        #$selProv = DBA->selProviders($form,$ToProvID);
        $ToList =
qq|    <SELECT NAME="ProviderMail_ToProvID_1" MULTIPLE SIZE=5 >${selProv}</SELECT>|;
        $SubList =
qq|  <INPUT TYPE="text" NAME="ProviderMail_Subject_1" VALUE="${Subject}" ONFOCUS="select()" SIZE=60>|;
        $MsgList =
qq|  <TEXTAREA NAME="ProviderMail_Message_1" COLS=80 ROWS=18 WRAP="virtual" onFocus="select()" >${Message}</TEXTAREA>|;
        $DateSent = DBUtil->Date( '', 'stamp', 'long' );
    }

    print myHTML->newPage( $form, "Send Mail" ) . qq|
<FORM NAME="ProviderMail" ACTION="/src/cgi/bin/ProviderMail.cgi" METHOD="POST" >
<HR WIDTH=90% >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Secure Mail to Providers on Network<BR>for ${ProvName}
    </TD>
    <TD CLASS="numcol" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Cancel','Click here for your Mail Listing or to Cancel.');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?mlt=$form->{mlt}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Cancel');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/mailbox.gif" ></A>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol subtitle" >From:</TD>
    <TD CLASS="strcol subtitle" COLSPAN="2" >${FromList}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Sent:</TD>
    <TD CLASS="strcol subtitle" COLSPAN="2" >${DateSent}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >To:</TD>
    <TD CLASS="strcol subtitle" >${ToList}</TD>
    <TD CLASS="strcol subtitle" >${ToMsg}</TD> </TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Subject:</TD>
    <TD CLASS="strcol subtitle" COLSPAN="2" >${SubList}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Message:</TD>
    <TD CLASS="strcol subtitle" COLSPAN="2" >${MsgList}</TD>
  </TR>
</TABLE>
${ReplyButton}
|;
    if ( $Action eq 'send' ) {
        print
qq|<TABLE CLASS="main fullsize" ><TR > <TD CLASS="numcol" > <INPUT TYPE="submit" NAME="MIS_Action=updatesend" VALUE="Send"> </TD> </TR></TABLE>|;
    }
    if ( $Action eq 'forward' ) {
        print
qq|<TABLE CLASS="main fullsize" ><TR > <TD CLASS="numcol" > <INPUT TYPE="submit" NAME="MIS_Action=updateforward" VALUE="Forward"> </TD> </TR></TABLE>|;
    }
    print qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="showd" VALUE="$form->{showd}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
</FORM>
${Focus}
|;
    print myHTML->rightpane( $form, 'search' );
    return (1);
}
############################################################################
############################################################################
# List this Providers mail.
sub ListMail {
    my ($self) = @_;

    $form->{'FORMID'} = $form->getFORMID;
    print myHTML->newPage( $form, "Secure Mail" ) . qq|
<FORM NAME="ProviderMail" ACTION="/src/cgi/bin/ProviderMail.cgi" METHOD="POST" >
<HR WIDTH=90% >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Secure Mail to Providers on Network<BR>for ${ProvName}
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('NoMail','$NoMailTxt');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=nomail&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('NoMail');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="$NoMailIMG" ></A>
    </TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="MIS_Action=send" VALUE="New">
      <INPUT TYPE="submit" NAME="MIS_Action=back" VALUE="Back">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >From</TD>
    <TD CLASS="port hdrtxt" >To</TD>
    <TD CLASS="port hdrtxt" >Subject</TD>
    <TD CLASS="port hdrtxt" >Date</TD>
    <TD CLASS="port hdrtxt" WIDTH="10%" >Read</TD>
    <TD CLASS="port hdrtxt" WIDTH="10%" >Reply</TD>
    <TD CLASS="port hdrtxt" WIDTH="10%" >Delete</TD>
    <TD CLASS="port hdrtxt" WIDTH="10%" >Purge</TD>
  </TR>
|;
    main->DisplayMail('inbox');
    main->DisplayMail('read');
    main->DisplayMail('sent');
    main->DisplayMail('deleted') if ( $showdflag =~ /yes/ );
    print qq|
</TABLE>
|;

    if ( $showdflag !~ /yes/ ) {
        print qq|
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Click on this button to display the delete section.
    </TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="showd=yes" VALUE="Show deleted section">
    </TD>
  </TR>
</TABLE>
|;
    }
    else {
        print qq|
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Click on this button to NOT display the delete section.
    </TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="showd=no" VALUE="Remove deleted section">
    </TD>
  </TR>
</TABLE>
|;
    }
    print qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
</FORM>
|;
    print myHTML->rightpane( $form, 'search' );
    return (1);
}
##
# Display mail types.
sub DisplayMail {
    my ( $self, $Flag ) = @_;

    print qq|  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="6" >${Flag}</TD>
|;
    if ( $Flag eq 'deleted' ) {
        print qq|    <TD CLASS="port hdrcol" >&nbsp;</TD>|;
    }
    else {
        print qq|
    <TD CLASS="port hdrtxt" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('DeleteAll${Flag}Msg','Click here to DELETE ALL Mail Messages for the entire [${Flag}] section.\\nThis is a safety which still allows you to see the message in the delete section.');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=delall&section=${Flag}&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('DeleteAll${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
|;
    }
    print qq|
    <TD CLASS="port hdrtxt" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('PurgeAll${Flag}Msg','Click here to PURGE ALL Mail Messages for the entire [${Flag}] section.\\nTHIS CANNOT BE UNDONE!\\nThe message is REMOVED!');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=purall&section=${Flag}&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('PurgeAll${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
  </TR>|;
    my $cnt = 0;
    $sListMail->execute( $ProvID, $Flag )
      || $form->dberror("List Mail=$ProvID ($Flag)");
    while ( my $rListMail = $sListMail->fetchrow_hashref ) {
        $cnt += 1;
        my $even  = int( $cnt / 2 ) == $cnt / 2 ? '1' : '0';
        my $class = qq|CLASS="rptodd"|;
        if ($even) { $class = qq|CLASS="rpteven"|; }
        my $FromProv =
qq|$Providers{$rListMail->{FromProvID}}{FName} $Providers{$rListMail->{FromProvID}}{LName}|;
        my $ToProv = '';
        my $sc     = '';
        foreach my $p ( split( chr(253), $rListMail->{ToProvID} ) ) {
            $ToProv .= qq|${sc}$Providers{$p}{FName} $Providers{$p}{LName}|;
            $sc = '; ';
        }
        print qq|
  <TR ${class} >
    <TD CLASS="strcol" >$FromProv</TD>
    <TD CLASS="strcol" >$ToProv</TD>
    <TD CLASS="strcol" >$rListMail->{Subject}</TD>
    <TD CLASS="hdrcol" >$rListMail->{DateSent}</TD>
    <TD CLASS="hdrcol" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Read${Flag}Msg','Click here to READ this Mail Message.');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=read&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Read${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/icon_go_left.gif" ></A>
    </TD>
    <TD CLASS="hdrcol" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Forward${Flag}Msg','Click here to REPLY or FORWARD this Mail Message.');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=forward&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Forward${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/icon_go_right.gif" ></A>
    </TD>
|;
        if ( $Flag eq 'deleted' ) {
            print qq|
    <TD CLASS="hdrcol" >&nbsp;</TD>
    <TD CLASS="hdrcol" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Purge${Flag}Msg','Click here to PURGE this Mail Message.\\nTHIS CANNOT BE UNDONE!\\nThe message is REMOVED!');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=purge&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Purge${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
|;
        }
        else {
            print qq|
    <TD CLASS="hdrcol""" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Delete${Flag}Msg','Click here to DELETE this Mail Message.\\nThis is a safety which still allows you to see the message in the delete section.');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=delete&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Delete${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
    <TD CLASS="hdrcol" >
      <SCRIPT LANGUAGE="JavaScript">newtextMsg('Purge${Flag}Msg','Click here to PURGE this Mail Message.\\nTHIS CANNOT BE UNDONE!\\nThe message is REMOVED!');</SCRIPT>
      <A HREF="/src/cgi/bin/ProviderMail.cgi?MIS_Action=purge&ProviderMail_ID=$rListMail->{ID}&mlt=$form->{mlt}&FORMID=$form->{FORMID}&showd=$form->{showd}" ONMOUSEOVER="textMsg.show('Purge${Flag}Msg');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 ALT="" SRC="/images/redx.gif" ></A>
    </TD>
|;
        }
        print qq|  </TR>|;
        if ( $cnt > 100 ) {
            print qq|  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="6" >Count greater than 100 (delete or purge section)</TD>
|;
            last;
        }
    }
    print qq|<TR ><TD CLASS="hdrcol" COLSPAN="8" >&nbsp;</TD></TR>|;
    return ($cnt);
}
############################################################################
