#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use myConfig;
use DBI;
use DBForm;
use DBA;
use myHTML;
use gXML;
use File::Copy;
use XML::LibXML;

############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();

#warn "importCCDA: IDs=$form->{'IDs'}, type=${type}\n";
#foreach my $f ( sort keys %{$form} ) { warn "importCCDA: form-$f=$form->{$f}\n"; }
my $ClientID = $form->{'Client_ClientID'};
##
# prepare selects...
##
my $sClientEDocs = $dbh->prepare("select * from ClientEDocs where ID=?");
$sClientEDocs->execute( $form->{'IDs'} )
  || $form->dberror("importCCDA: select ClientEDocs");
my $html = '';
my ( $cnt, $list, $err ) = ( 0, '', '' );
my $rClientEDocs = $sClientEDocs->fetchrow_hashref;
$rClientEDocs->{'filename'} = $rClientEDocs->{'Path'};
my $fromfile = qq|$form->{'DOCROOT'}$rClientEDocs->{filename}|;
my ( $directory, $filename ) = $fromfile =~ m/(.*\/)(.*)$/;
warn qq|begin: fromfile=${fromfile}\n|;
warn qq|begin: directory=${directory}\n|;
warn qq|begin: filename=${filename}\n|;

if ( -f $fromfile ) {
    if ( $form->{link} ) {
        $list = main->link( $form, $ClientID, $rClientEDocs );
    }
    else { $list = main->list($rClientEDocs); }
}
else {
    if ( $fromfile eq '' ) {
        $err  = qq|File name is empty in link!|;
        $list = qq|Zero files to link, Aborted!|;
    }
    else { $err = qq|File NOT FOUND on disk!|; $list = qq|Aborted!|; }
}
my $html = main->html( $filename, $list, $err );
$sClientEDocs->finish();
$form->complete();
print $html;
exit;
############################################################################
sub link {
    my ( $self, $form, $ClientID, $r ) = @_;
    my $list     = '';
    my $fromfile = qq|$form->{'DOCROOT'}$r->{filename}|;
    my ( $directory, $filename ) = $fromfile =~ m/(.*\/)(.*)$/;
    warn qq|link: fromfile=${fromfile}\n|;
    warn qq|link: directory=${directory}\n|;
    warn qq|link: filename=${filename}\n|;
    my ( $FName, $MName, $LName, $Gend, $DOB ) = main->getInfo($fromfile);
    $list .= qq|Add Electronic Records for ClientID: ${ClientID}.<BR>|;
    return ($list);
}

sub list {
    my ( $self, $r )   = @_;
    my ( $cnt, $list ) = ( 0, '' );
    my $fromfile = qq|$form->{'DOCROOT'}$r->{filename}|;
    my ( $directory, $filename ) = $fromfile =~ m/(.*\/)(.*)$/;
    warn qq|list: fromfile=${fromfile}\n|;
    warn qq|list: directory=${directory}\n|;
    warn qq|list: filename=${filename}\n|;
    my ( $FName, $MName, $LName, $Gend, $DOB ) = main->getInfo($fromfile);
    $LName = $MName if ( $LName eq '' );
    $list .= qq|${FName} ${LName} ${Gend} ${DOB}
             <button CLASS="confirmLINK" MYTEXT="Are you sure you want to LINK this xml to this client?<BR>If so, then click the OK button below. If NOT, click the Cancel button below." HREF="/src/cgi/bin/mis.cgi?MIS_Action=importCCDA.cgi&Client_ClientID=$r->{'ClientID'}&link=1&IDs=$form->{'IDs'}&mlt=$form->{'mlt'}" MYBUSY="Importing..." >Import</button> $r->{'ClientID'}<BR>|;
    return ($list);
}

sub html {
    my ( $self, $filename, $list, $err ) = @_;
    my $html =
      myHTML->newHTML( $form, 'Link CCDA',
        'CheckPopupWindow noclock countdown_10' )
      . qq|
<FORM ID="form" NAME="importCCDA" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
  <TABLE CLASS="main" >
    <TR> <TD CLASS="hdrcol title" >Link CCDA</TD> </TR>
  </TABLE>
  <TABLE CLASS="home fullsize" >
    <TR>
      <TD CLASS="strcol" >
        Link: ${filename}<BR>
      </TD>
    </TR>
    <TR>
      <TD CLASS="strcol hotmsg" >
        ${list}
      </TD>
    </TR>
    <TR>
      <TD CLASS="strcol hotmsg" >
        ${err}<BR>
      </TD>
    </TR>
  </TABLE>
      
</TD> </TR> </TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
</FORM>
</BODY>
</HTML>
|;
    return ($html);
}

sub getInfo {
    my ( $self, $filename ) = @_;
    my $doc = '';

    #   load_xml: initializes the parser and parse_file()
    warn "${filename}\n";
    eval { $doc = XML::LibXML->load_xml( location => $filename ); };
    return ('parse_error') if ($@);
    my $xml = XML::LibXML::XPathContext->new;    # No argument here!
    $xml->registerNs( 'x', 'urn:hl7-org:v3' );
    my ( $longname, $othername ) = ( '', '' );
    for my $node ( $xml->findnodes( '//x:patient/x:name', $doc ) ) {
        my $type =
          $xml->findvalue( '@use', $node );    # Context specified as argument.
        for my $given ( $xml->findnodes( 'x:given', $node ) ) {
            if   ( $type eq 'L' ) { $longname  .= $given->to_literal . ' '; }
            else                  { $othername .= $given->to_literal . ' '; }
        }
        for my $family ( $xml->findnodes( 'x:family', $node ) ) {
            if   ( $type eq 'L' ) { $longname  .= $family->to_literal . ' '; }
            else                  { $othername .= $family->to_literal . ' '; }
        }
    }
    my $patientname = $longname eq '' ? $othername : $longname;
    warn "$patientname\n";
    my ( $fname, $mname, $lname ) = split( ' ', $patientname );
    $fname =~ s/^\s*(.*?)\s*$/$1/g;    # trim both leading/trailing
    warn "$fname\n";
    $mname =~ s/^\s*(.*?)\s*$/$1/g;    # trim both leading/trailing
    warn "$mname\n";
    $lname =~ s/^\s*(.*?)\s*$/$1/g;    # trim both leading/trailing
    warn "$lname\n";
    my $gender =
      $xml->findvalue( '//x:patient/x:administrativeGenderCode/@code', $doc );
    warn "$gender\n";
    my $dateofbirth = $xml->findvalue( '//x:patient/x:birthTime/@value', $doc );
    warn "$dateofbirth\n";
    my $descr = qq|${patientname} ${gender} ${dateofbirth}\n|;
    return ( $fname, $mname, $lname, $gender, $dateofbirth );
}
############################################################################
