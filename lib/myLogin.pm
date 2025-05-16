package myLogin;
use CGI       qw(:standard escape);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use myConfig;
use myForm;
use DBA;
use DBUtil;
############################################################################

sub chkLogin {
    my ($self) = @_;
    my $form = $myForm::FORM;

#foreach my $f ( sort keys %{$form} ) { warn qq|chkLogin: form: $f=$form->{$f}\n|; }
    $self->{'DBNAME'} = $form->{'DBNAME'};

    # get login using Name and password.
    #warn qq|1. LOGINID=$form->{LOGINID}=$self->{LOGINID}\n|;
    #warn qq|1. mlt=$form->{mlt}=$self->{mlt}\n|;
    #warn qq|1. Login=$form->{Login}=$self->{Login}\n|;
    #warn qq|1. vlogin=$form->{vlogin}=$self->{vlogin}\n|;
    #warn qq|1. LOGINSCREEN=$form->{LOGINSCREEN}=$self->{LOGINSCREEN}\n|;
    #warn qq|1. LOGINPROVID=$form->{LOGINPROVID} = $self->{LOGINPROVID}\n|;
    #warn qq|1. RenewLogin=$form->{RenewLogin} = $self->{RenewLogin}\n|;
    myLogin->renewLogin($form) if ( $form->{RenewLogin} );

    # Login comes from Login screen (Login='Login').
    # mlt is set upon successful login.
    myLogin->setLogin($form) if ( $form->{Login} || $form->{mlt} eq '' );

    #warn qq|2. LOGINID=$form->{LOGINID}=$self->{LOGINID}\n|;
    #warn qq|2. mlt=$form->{mlt}=$self->{mlt}\n|;
    #warn qq|2. LOGINPROVID=$form->{LOGINPROVID}=$self->{LOGINPROVID}\n|;
    #warn qq|2. LOGINSCREEN=$form->{LOGINSCREEN}=$self->{LOGINSCREEN}\n|;
    # get login from 'mlt' token and 'Login' table.
    unless ( myLogin->getLogin($form) ) {

        #warn qq|!. login failed: mlt=$form->{mlt}\n|;
        myDBI->cleanup();
        print myLogin->login( $form, 'Please Login' );
        exit;
    }

    #warn qq|3. LOGINID=$form->{LOGINID}=$self->{LOGINID}\n|;
    #warn qq|3. mlt=$form->{mlt}=$self->{mlt}\n|;
    #warn qq|3. LOGINPROVID=$form->{LOGINPROVID}=$self->{LOGINPROVID}\n|;
    #$form->{'KLS'} = 'YES I CHANGED IT!';     # this will change $myForm::FORM
    return ($form);
}
############################################################################
sub setLogin {
    my ( $self, $form ) = @_;

#warn qq|ENTER: setLogin\n|;
#foreach my $f ( sort keys %{$form} ) { warn qq|setLogin: form: $f=$form->{$f}\n|; }
#warn qq|setLogin: LOGINSCREEN=$form->{LOGINSCREEN}=$self->{LOGINSCREEN}\n|;
    my $Location = qq|Location: https://$ENV{SERVER_NAME}\n\n|;

    # $LOGINID = $user;     # i.e. wlhamil
    $self->{user}    = $form->{user};
    $self->{pass}    = $form->{pass};
    $self->{newpass} = $form->{newpass};
    $self->{verpass} = $form->{verpass};
    $self->{xx}      = $form->{xx};
    $self->{LOGINID} = $ENV{HTTP_USER_AGENT} ? $self->{user} : getpwuid($>);

    #warn qq|setLogin: LOGINID=$self->{LOGINID}\n|;
    if ( $self->{LOGINID} eq '' ) {
        $Location = myLogin->login( $form, 'Please Login' );
    }
    elsif ( $self->{xx} > 3 ) {
        $self->{xx} = 0;

        #warn qq|setLogin: Location=Please Login - too many attempts\n|;
        $Location = myLogin->login( $form, 'Please Login - too many attempts' );
    }
    else {

        #warn qq|setLogin: DBNAME=$form->{DBNAME}\n|;
        #warn qq|setLogin: LOGINID=$self->{LOGINID}, pass=$self->{pass}\n|;
        my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
        my $q =
qq|select * from UserLogin where BINARY UserLogin.loginid='$self->{LOGINID}' and UserLogin.dbname='$form->{DBNAME}' |;
        my $qpass = $dbh->quote( $self->{pass} );
        $q .= qq|and BINARY UserLogin.Password=${qpass}|
          if ( $ENV{HTTP_USER_AGENT} );

        #warn qq|setLogin: q=${q}\n|;
        my $s = $dbh->prepare($q);
        $s->execute() || myLogin->error("sql error: setLogin checkpass");
        ##check if login from office 365
        unless ( $s->rows() ) {
            if ( $form->{'office_365_login'} ) {
                $q =
qq|select * from UserLogin where BINARY UserLogin.email='$self->{LOGINID}' and UserLogin.dbname='$form->{DBNAME}' |;
                $s = $dbh->prepare($q);
                $s->execute()
                  || myLogin->error("sql error: setLogin checkpass");
            }
        }
        if ( my $r = $s->fetchrow_hashref ) {

      #foreach my $f ( sort keys %{$r} ) { warn qq|setLogin r: $f=$r->{$f}\n|; }
      #warn qq|setLogin: loginid=$r->{loginid}, renew=$r->{renew}\n|;
            $s->finish();
            myLogin->renewPasswd( $form, $r )
              if ( $r->{renew} && $ENV{HTTP_USER_AGENT} );
            $self->{mlt}         = DBUtil->genToken(12);
            $self->{LOGINUSERID} = $r->{UserID};
            $self->{LOGINPROVID} = $r->{UserID};
            my $Browser =
              $ENV{HTTP_USER_AGENT} ? $ENV{HTTP_USER_AGENT} : 'Telnet Session';
            ( $self->{Browser}, $rest ) = split( / /, $Browser );
            my $s = $dbh->prepare(
"insert into Login (Token,UserID,Name,Browser) values ('$self->{mlt}','$self->{LOGINUSERID}','$self->{LOGINID}','$self->{Browser}')"
            );
            $s->execute() || myLogin->error("sql error: setLogin insert");
            $s->finish();
            my $LoginScreen =
                $form->{'LOGINSCREEN'} eq ''
              ? $r->{'loginscreen'} eq ''
                  ? 'ManagerTree.cgi'
                  : $r->{'loginscreen'} . '.cgi'
              : $form->{'LOGINSCREEN'};

#warn qq|myLogin: setLogin: LoginScreen=$r->{'loginscreen'}/$form->{LOGINSCREEN}/${LoginScreen}\n|;
            $Location =
              qq|Location: /src/cgi/bin/${LoginScreen}?mlt=$self->{mlt}\n\n|;

            #warn qq|myLogin: setLogin: Location=$Location\n|;
            #warn qq|myLogin: setLogin: ID=$r->{ID}\n|;
            $form->{LOGINSCREEN} = $LoginScreen;
            $form->{USERLOGINID} = $r->{ID};
            $form->{LOGINID}     = $self->{LOGINID};
            $form->{LOGINPROVID} = $self->{LOGINPROVID};
            $form->{mlt}         = $self->{mlt};
            $form->{Browser}     = $self->{Browser};
            $form->{LOGINUSERID} = $r->{UserID};
            $form->{LOGINUSERDB} = $r->{dbname};
            $form->{LOGINTYPE}   = $r->{type};
        }
        else {
            $s->finish();

            #warn qq|setLogin: Location=Login Failed!\n|;
            $Location = myLogin->login( $form, 'Login Failed!' );
        }
    }

    #warn qq|setLogin: END: ENV=$ENV{HTTP_USER_AGENT}\n|;
    #warn qq|setLogin: END: Location=${Location}\n|;
    if ( $ENV{HTTP_USER_AGENT} )    # HTTP or non telnet session.
    { myDBI->cleanup(); print $Location; exit; }
    return ($form);
}

# check for given mlt to exist.
#  https://xxx.okmis.com executes vlogin.cgi and getCookie will pass it to here if set.
#  on logout the Login-mlt is deleted.
sub getLogin {
    my ( $self, $form ) = @_;
    my $ok  = 0;
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

#warn qq|getLogin: form mlt=$form->{mlt}\n|;
#foreach my $f ( sort keys %{$form} ) { warn qq|getLogin 1: form: $f=$form->{$f}\n|; }
    $self->{mlt} = $form->{mlt};

    #warn qq|getLogin: self mlt=$self->{mlt}\n|;
    my $sLogin = $dbh->prepare(
"select * from Login left join UserLogin on UserLogin.UserID=Login.UserID where Login.Token='$self->{mlt}'"
    );
    $sLogin->execute() || myLogin->error("sql error: getLogin select");
    if ( my $rLogin = $sLogin->fetchrow_hashref ) {

#warn qq|getLogin: passed LOGINID=$rLogin->{Name}\n|;
#foreach my $f ( sort keys %{$rLogin} ) { warn qq|getLogin 1: rLogin: $f=$rLogin->{$f}\n|; }
        $self->{LOGINID}     = $rLogin->{Name};
        $self->{LOGINUSERID} = $rLogin->{UserID};
        $self->{LOGINPROVID} =
          $rLogin->{UserID};    # preserve until all changed to LOGINUSERID
        my $Browser =
          $ENV{HTTP_USER_AGENT} ? $ENV{HTTP_USER_AGENT} : 'Telnet Session';
        ( $self->{Browser}, $rest ) = split( / /, $Browser );
        my $sReplace = $dbh->prepare(
"replace into Login (Token,UserID,Name,Browser) values ('$self->{mlt}','$self->{LOGINUSERID}','$self->{LOGINID}','$self->{Browser}')"
        );
        $sReplace->execute() || myLogin->error("getLogin: replace");
        $sReplace->finish();

#warn qq|getLogin: reread: ID=$rLogin->{ID}\n|;
#warn qq|getLogin: reread: LOGINSCREEN=$rLogin->{loginscreen}/$form->{LOGINSCREEN}\n|;
        $form->{USERLOGINID} = $rLogin->{ID};
        $form->{LOGINID}     = $self->{LOGINID};
        $form->{LOGINPROVID} = $self->{LOGINPROVID};
        $form->{Browser}     = $self->{Browser};
        $form->{LOGINUSERID} = $rLogin->{UserID};
        $form->{LOGINUSERDB} = $rLogin->{dbname};
        $form->{LOGINSCREEN} =
            $form->{'LOGINSCREEN'} eq ''
          ? $rLoginr->{'loginscreen'} eq ''
              ? 'ManagerTree.cgi'
              : $rLogin->{'loginscreen'} . '.cgi'
          : $form->{'LOGINSCREEN'};
        $form->{LOGINTYPE} = $rLogin->{type};
        $ok = 1;
    }
    $sLogin->finish();

#warn qq|getLogin: return: ok=$ok, LOGINID=$form->{LOGINID}=\n|;
#warn qq|getLogin: return: ok=$ok, DBNAME=$form->{DBNAME}=\n|;
#foreach my $f ( sort keys %{$form} ) { warn qq|getLogin 2: form: $f=$form->{$f}\n|; }
# FALL THROUGH UNLESS OK...
    return ($ok) if ( $form->{LOGINID} eq 'root' );    # always let root in.

#warn qq|getLogin: return1: ok=$ok, DBNAME=$form->{'DBNAME'} LOGINPROVID=$form->{'LOGINPROVID'}\n|;
    unless ( $form->{DBNAME} eq 'okmis_kls' )          # stop this db/account.
    {
        my $syslock = 0;
        return ($ok) unless ($syslock);
    }    # stop ALL account access.

    #warn qq|getLogin: exit: ok=$ok, DBNAME=$form->{DBNAME}\n|;
    myDBI->cleanup();
    print myLogin->login( $form,
'System Unavailable: Upgrades/Enhancements: <BR>Please try again around 5am on 03/05/2019.'
    );
    exit;
}
############################################################################
sub renewPasswd {
    my ( $self, $form, $rPasswd ) = @_;
    my ( $msg, $renew ) = ( '', 1 );
    $self->{xx}++;

#warn qq|renewPasswd: xx=$self->{xx}, newpass=$self->{newpass}, verpass=$self->{verpass}\n|;
    if    ( $self->{newpass} eq '' ) { $msg = "Please enter a new password."; }
    elsif ( $self->{newpass} eq $self->{user} ) { $msg = "Illegal Password."; }
    elsif ( $self->{newpass} eq $self->{pass} ) {
        $msg = "Please change your Password.";
    }
    elsif ( $self->{newpass} ne $self->{verpass} ) {
        $msg = "Passwords don't match, please reenter both.";
    }
    elsif ( length( $self->{newpass} ) < 6 ) {
        $msg = "Passwords must be at least 6 characters.";
    }
    elsif ( $self->{newpass} !~ /[A-Z]/ ) {
        $msg = qq|Passwords must contain at least 1 capital letter.\n|;
    }
    elsif ( $self->{newpass} !~ /[a-z]/ ) {
        $msg = qq|Passwords must contain at least 1 lower-case letter.\n|;
    }
    elsif ( $self->{newpass} !~ /\d/ ) {
        $msg = qq|Passwords must contain at least 1 digit.\n|;
    }
    elsif ( $self->{newpass} !~ /[\@\#\%\=\-\+\:\.\!\_]/ ) {
        $msg = qq|Passwords must contain at least 1 special character.\n|;
    }
    elsif ( $self->{newpass} ) {

#warn qq|renewPasswd: SET: DBNAME=$self->{DBNAME}, form=$form->{DBNAME}\n|;
#warn qq|renewPasswd: SET: Password=$self->{newpass}, UserID=$rPasswd->{UserID}, dbname=$form->{DBNAME}\n|;
        my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
        my $s   = $dbh->prepare(
"update UserLogin set Password='$self->{newpass}', renew=0 where UserID=$rPasswd->{UserID} and dbname='$form->{DBNAME}'"
        );
        $s->execute() || myLogin->error("sql error: renewPasswd update ");
        $s->finish();
        return (1);    # good password change.
    }
    elsif ( $self->{xx} > 3 ) {
        $renew      = 0;
        $self->{xx} = 0;
        $msg        = 'Please Login - too many renew attempts';
    }
    myDBI->cleanup();
    print myLogin->login( $form, $msg, $renew );
    exit;
}

sub renewLogin {
    my ( $self, $form )  = @_;
    my ( $msg,  $renew ) = ( '', 0 );

    #warn qq|renewLogin: DBNAME=$form->{DBNAME}, user=$form->{user}\n|;
    if ( $form->{user} )    # because first link is <A> does not send user.
    {
        my $dbh        = myDBI->dbconnect( $form->{'DBNAME'} );
        my $sUserLogin = $dbh->prepare(
"select * from UserLogin where BINARY UserLogin.loginid='$form->{user}' and dbname='$form->{DBNAME}'"
        );
        $sUserLogin->execute()
          || myLogin->error("renewLogin: $form->{user} $form->{DBNAME}");
        if ( my $rUserLogin = $sUserLogin->fetchrow_hashref ) {
            my ( $DB, $ID ) = split( ':', $rUserLogin->{'ID'} );
            my $mdbh = myDBI->dbconnect($DB);
            my $qUser =
              $rUserLogin->{'type'} == 0
              ? qq|select * from Provider where ProvID=?|
              : qq|select * from Client where ClientID=?|;

            #warn qq|renewLogin: DB=${DB}, ID=${ID}, qUser=${qUser}\n|;
            my $sUser = $mdbh->prepare($qUser);
            $sUser->execute( $rUserLogin->{'UserID'} )
              || myLogin->error("renewLogin: ${qUser} $rUserLogin->{'UserID'}");
            my $rUser = $sUser->fetchrow_hashref;

            #warn qq|renewLogin: ssn=$form->{ssn}, SSN=$rUser->{SSN}\n|;
            if ( $form->{ssn} eq $rUser->{SSN} ) {
                my $Password = DBA->genPassword();
                my $sUpd     = $dbh->prepare(
"update UserLogin set Password='${Password}', renew=1 where UserID=$rUserLogin->{UserID} and dbname='$form->{DBNAME}'"
                );
                $sUpd->execute()
                  || myLogin->error(
"renewLogin: ERROR: update $form->{user}/$rUserLogin->{UserID}, Password=${Password}"
                  );
                $sUpd->finish();
                $msg =
qq|Temporary password sent via email.<BR>use that password to login.|;
                my $Subject = qq|Temporary Login|;
                my $Text =
qq|Use '${Password}' to login and reset your password.\nPassword reset requested from IP: $ENV{REMOTE_ADDR}.\nIf you did not request this password reset for MIS, please forward this email to: support\@okmis.com for review.\n\nMessage sent to $rUser->{Email}.|;
                DBUtil->email( $form, $rUser->{Email}, $Subject, $Text );
                $form->{'LOGINPROVID'} = 0;    # dummy up saveLINK
                myForm->saveLINK( 'renewLogin',
                    "$ENV{SCRIPT_NAME}?$ENV{QUERY_STRING}" );
            }
            else { $msg = qq|'SSN' mismatch!|; }
        }
        else { $msg = qq|'LOGIN ID' not located!|; }
        $sUserLogin->finish();
    }
    else {
        $msg =
qq|Enter 'LOGIN ID' to reset.<BR>Email with temporary password will be sent to provider's email on file.|;
        $renew = 2;
    }
    myDBI->cleanup();
    print myLogin->login( $form, $msg, $renew );
    exit;
}

sub login {
    my ( $self, $form, $msg, $renew ) = @_;
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
    my $s   = $dbh->prepare("select Name from Provider where ProvID=91");
    $s->execute() || myLogin->error("sql error: chklogin SITENAME");
    ( $self->{SITENAME} ) = $s->fetchrow_array;
    $self->{SITENAME} =
"DEVELOPMENT<BR>$self->{SITENAME}<BR>DEVELOPMENT<BR>DO NOT USE THIS SITE FOR PRODUCTION WORK"
      if ( substr( $form->{DBNAME}, 0, 3 ) eq 'dev' );
    $self->{SITENAME} =
"DEVELOPMENT<BR>$self->{SITENAME}<BR>DEVELOPMENT<BR>DO NOT USE THIS SITE FOR PRODUCTION WORK"
      if ( $form->{DBNAME} =~ /_dev/ );

    #warn qq|login: DBNAME=$form->{DBNAME}\n|;
    $s->finish();
    $self->{LOGO}        = myConfig->cfgfile( 'logo', 1 );
    $self->{LOGINSCREEN} = $form->{LOGINSCREEN};
    return ( myLogin->logintxt( $msg, $renew ) );
}

sub logintxt {
    my ( $self, $msg, $renew ) = @_;
    my $fn = "C:/xampp/htdocs/src/html/$self->{DBNAME}.login";
    unless ( -f $fn ) { $fn = qq|C:/xampp/htdocs/src/html/default.login| }
    if     ( $renew == 1 ) {
        $fn = "C:/xampp/htdocs/src/html/$self->{DBNAME}.renewpasswd";
        unless ( -f $fn ) {
            $fn = qq|C:/xampp/htdocs/src/html/default.renewpasswd|;
        }
    }
    elsif ( $renew == 2 ) {
        $fn = "C:/xampp/htdocs/src/html/$self->{DBNAME}.renewlogin";
        unless ( -f $fn ) {
            $fn = qq|C:/xampp/htdocs/src/html/default.renewlogin|;
        }
    }
    #warn qq|logintxt: renew=$renew, fn=$fn\n|;
    my $html = DBUtil->ReadFile($fn);
    $html =~ s/{LOGO}/$self->{LOGO}/g;
    $html =~ s/{SITENAME}/$self->{SITENAME}/g;
    $html =~ s/{XX}/$self->{xx}/g;
    $html =~ s/{LOGINSCREEN}/$self->{LOGINSCREEN}/g;
    $html =~ s/{USER}/$self->{user}/g;
    $html =~ s/{PASS}/$self->{pass}/g;
    $html =~ s/{MSG}/$msg/g;
    return ($html);
}

sub error {
    my ( $self, $msg ) = @_;
    if ( $ENV{HTTP_USER_AGENT} ) {
        my $servername = qq|https://$ENV{SERVER_NAME}/|;
        $msg =~ s/\n/<BR>/g;
        print <<HTML_END;
Content-Type: text/html

<HTML>
<HEAD> <TITLE>${msg}</TITLE> </HEAD>
<BODY BGCOLOR=black LINK=white VLINK=white >
  <DIV ALIGN=center>
  <FONT SIZE=+3 COLOR="red"><B>HTML Access Error</B></FONT>
  <P>
  <TABLE WIDTH=50% BGCOLOR=red BORDER=5 CELLSPACING=0 >
    <TR VALIGN=center >
      <TD ALIGN=center ><FONT SIZE=+2 ><B>${msg}</B></FONT></TD>
    </TR>
  </TABLE>
  <P>
  <TABLE WIDTH=50% BORDER=0 CELLSPACING=0 >
    <TR VALIGN=center >
      <FONT SIZE=+2 >
      <TD ALIGN=left ><A HREF="javascript:window.history.go(-1);">Back</A></TD>
      <TD ALIGN=right ><A HREF="${servername}" TARGET="_top" >Home</A></TD>
      </FONT>
    </TR>
  </TABLE>
</BODY>
</HTML>
HTML_END
    }
    else { print qq|$msg|; }
    exit;
}

sub SysAdmin {
    my ( $self, $dbname, $mlt, $userid, $name ) = @_;
    my $val = 0;
    my $dbh = myDBI->dbconnect($dbname);
    my $s   = $dbh->prepare("select * from Login where Token=?");
    $s->execute($mlt) || myDBI->error("sql error: SysAdmin check mlt");
    if ( my $r = $s->fetchrow_hashref ) { $val = 1; }
    else {
        my $sLogin = $dbh->prepare(
"insert into Login (Token,UserID,Name,Browser) values (?,?,?,'SysAdmin')"
        );
        $sLogin->execute( $mlt, $userid, $name );
        $sLogin->finish();
    }
    return ($val);
}
############################################################################
1;
