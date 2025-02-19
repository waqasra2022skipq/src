#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use myHTML;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %ENV ) { $data .= qq|ENV: $f=$ENV{$f}\n|; }
#foreach my $f ( sort keys %{$form} ) { $data .= qq|form: $f=$form->{$f}\n|; }

if ( $form->{'action'} eq 'putlogin' ) {
    my $data = qq|
  {
    "access_token" : "$form->{'mlt'}",
    "token_type" : "bearer"
    "expires_in" : "3600"
  }
|;
    print main->htmljson( 'application/json', $data );
}
elsif ( $form->{'action'} eq 'search' ) {
    print main->htmlpost();
}
elsif ( $form->{'action'} eq 'putsearch' ) {
    my $data = '[';
    $sInsurance =
      $dbh->prepare("select * from Insurance where ClientID=? and Priority=1");
    $s = $dbh->prepare(
        "select * from Client where (LName=? or FName=? or DOB=?) and (Gend=?)"
    );
    $s->execute(
        $form->{'lastname'}, $form->{'firstname'},
        $form->{'dob'},      $form->{'gender'}
    );
    while ( my $r = $s->fetchrow_hashref ) {
        $sInsurance->execute( $r->{'ClientID'} );
        my $rInsurance = $sInsurance->fetchrow_hashref;
        ( my $DOB = $r->{'DOB'} ) =~ s/-//g;
        $data .= qq|
        {
            "MRN" : "$rInsurance->{'InsIDNum'}",
            "id" : "$r->{'ClientID'}"
            "firstname" : "$r->{'FName'}"
            "lastname" : "$r->{'LName'}"
            "DoB" : "${DOB}"
            "Gender" : "$r->{'Gend'}"
        },
|;
    }
    $data .= ']';
    $s->finish();
    $sInsurance->finish();
    print main->htmljson( 'application/json', $data );
}
elsif ( $form->{'action'} eq 'encounters' ) {
    $data = qq|
        {
            "title" : "Millennium Information API Access",
            "author" : "Keith Stephenson"
            "phone" : "405-641-6109"
            "email" : "support\@okmis.com"
            "mlt" : "$form->{'mlt'}"
        }
    |;
}
elsif ( $form->{'mlt'} ne '' ) {
    $data = qq|
        {
            "token" : "$form->{'mlt'}",
        }
    |;
}
myDBI->cleanup();
exit;
############################################################################
sub htmljson {
    my ( $self, $header, $data ) = @_;
    my $html = qq|Content-type: ${header}\n\n${data}|;
    return ($html);
}

sub htmlpost {
    my ($self) = @_;
    my $html = myHTML->new( $form, "Search Patient" ) . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientInfo.js?v=20190501"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<FORM NAME="ClientAccess" ACTION="/cgi/bin/xapi.pl" METHOD="POST" >
<TABLE CLASS="home halfsize" >
  <TR ><TD CLASS="port hdrtxt heading" COLSPAN="2" >Enter patient information</TD></TR>
  <TR >
    <TD CLASS="hdrcol title" COLSPAN="2" >
      Search Patient
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="firstname" VALUE="$form->{'firstname'}" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="lastname" VALUE="$form->{'lastname'}" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="dob" VALUE="$form->{'dob'}" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="gender">
        | . DBA->selxTable( $form, 'xGend', $form->{'gender'}, 'Descr' ) . qq|
      </SELECT> 
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >

<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="hdrcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="action=putsearch" VALUE="Search">
    </TD>
  </TR>
  <TR>
    <TD CLASS="hdrcol" >
<A HREF="/cgi/bin/mis.cgi?logout=1&mlt=PBPQzssnx32a&LOGINSCREEN=xapi.pl" ONMOUSEOVER="window.status='Logout of MIS'; return true;" ONMOUSEOUT="window.status=''" >close</A>
</ul>
    </TD>
  </TR>
</TABLE>
</FORM>
|;
    return ($html);
}
############################################################################
#  print qq|Content-type: text/html\n\n
#<HTML>
#<HEAD> <TITLE>KLS</TITLE> </HEAD>
#<BODY >
#<H3>READ</H3>
#<PRE>
#${out}
#</PRE>
#</BODY>
#</HTML>
#|;
