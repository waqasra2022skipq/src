#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use strict;
use LWP::UserAgent;
use XML::DOM;
use DBI;
use DBForm;
use DBA;

###################################################################################
## Occupation URL: https://services.onetcenter.org/ws/online/occupations/{code}

## https://services.onetcenter.org/
## Your Username is okmis
## Your Password is 4438jne
##
my $form   = DBForm->parse();
my $dbh    = $form->dbconnect();
my $target = $form->{'target'};
my $value  = $form->{'value'};
my %parsedData;
my $xml;

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }

my $proxy = 'https://services.onetcenter.org/ws/online/occupations';
my $req   = new HTTP::Request 'GET', $proxy . qq|/${value}|;
$req->authorization_basic( 'okmis', '4438jne' );
my $ua       = new LWP::UserAgent;
my $response = $ua->request($req);
if ( $response->is_success ) {
    %parsedData = main->parseTag( $response->content, 'occupation', 'title' );
}

###################################################################################
my $out = '';
if ( $form->{method} eq 'getOccupationInfo' ) {
    my ( $err, $script ) = ( '', '' );

    if ( ( keys %parsedData ) eq 0 ) {
        $err    = 'Invalid Request';
        $script = qq|
document.getElementById('$target').value = '';
|;
    }
    else {
        $script = qq|
document.getElementById('$target').value = "$parsedData{'title'}";
|;
    }

    $out = $err eq ''
      ? qq|
  <command method="setscript">
    <target>executeit</target>
    <content><![CDATA[${script}]]></content>
  </command>
|
      : main->ierr( $target, $err, $script );
}

###################################################################################
#warn qq|out=$out\n|;
$xml = qq|<response>\n${out}</response>|;

#warn qq|popup: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;

$form->complete();
exit;

###################################################################################
sub parseTag {
    my ( $self, $resp, $tag, @elements ) = @_;
    my %data    = ();
    my $parser  = new XML::DOM::Parser;
    my $RespDoc = $parser->parse($resp);
    if ( $RespDoc->getDocumentElement->getNodeName eq 'Error' ) {
        return ("<p>usps: error parsing request!</p>\n");
    }

    my $InfoList = $RespDoc->getElementsByTagName($tag);
    my $n        = $InfoList->getLength;
    for ( my $i = 0 ; $i < $n ; $i++ ) {
        my $InfoNode = $InfoList->item($i);

        foreach my $etag (@elements) {
            my $val = '';
            my $el  = $InfoNode->getElementsByTagName($etag)->item(0);
            if ( defined $el ) {
                $val = $el->getFirstChild->getNodeValue;
                $data{$etag} = $val;
            }
        }
    }
    return %data;
}

###################################################################################
sub ierr {
    my ( $self, $target, $err, $script ) = @_;

    #warn qq|ierr: target=$target\n|;
    my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
    if ( $script ne '' ) {
        $out .= qq|
  <command method="setscript">
    <target>executeit</target>
    <content><![CDATA[${script}]]></content>
  </command>
|;
    }
    return ($out);
}
