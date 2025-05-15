#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use strict;
use LWP::UserAgent;
use XML::DOM;
use DBI;
use DBForm;
use DBA;

###################################################################################
## Production: http://production.shippingapis.com/ShippingAPI.dll
## Production: https://secure.shippingapis.com/ShippingAPI.dll
## Testing: http://stg-production.shippingapis.com/ShippingAPI.dll
## Testing: https://stg-secure.shippingapis.com/ShippingAPI.dll

## https://www.usps.com/business/web-tools-apis/address-information-api.htm
## Your Username is 773MILLE6990
## Your Password is 282FV16XQ576
##
my $form = DBForm->new();
my $dbh  = $form->dbconnect();
my $html = '';

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }

my $UseProduction = 1;
my $proxy =
  $UseProduction
  ? 'http://production.shippingapis.com/ShippingAPI.dll'
  : 'http://stg-production.shippingapis.com/ShippingAPI.dll';
my $xml = main->uspsXML( $form->{'Tag'}, $form );

#warn qq|Tag: $form->{'Tag'}\n${xml}\n|;
my $req = new HTTP::Request 'POST', $proxy;
$req->content_type('application/x-www-form-urlencoded');
$req->content($xml);
my $ua       = new LWP::UserAgent;
my $response = $ua->request($req);
if ( $response->is_success ) {
    $html = main->parseTag( $response->content,
        'Address', 'Address1', 'Address2', 'City', 'State', 'Zip5', 'Zip4' );
}
else { $html = "<p>usps: error processing request!</p>\n<pre>${xml}</pre>"; }
print main->prtHTML( $form->{'Tag'}, $html );
$form->complete();
exit;

#  @details = ();
#  $DetList = $InfoNode->getElementsByTagName('Det');
#  $l = $DetList->getLength;
#  for ($j = 0; $j < $l; $j++) {
#    $details[$j] = $DetList->item($j)->getFirstChild->getNodeValue;
#    $details[$j] =~ tr/\n/ /s;
#  }
#  if ($#details > 0) {
#    $html .= " <DL>\n";
#    $html .= " <DT>Details:\n";
#    $LI = " <DD>";
#    $html .= $LI . join("\n" . $LI, @details) . "\n";
#    $html .= " </DL>\n";
#  }
###################################################################################
sub uspsXML {
    my ( $self, $tag, $r ) = @_;
    my $USERID = "773MILLE6990";
    my $xml;
    if ( $tag eq 'Address' ) {
        my $State = $r->{'State'} eq '' ? 'OK' : $r->{'State'};
        my ( $Zip5, $Zip4 ) = split( '-', $r->{Zip} );
        $Zip5 = '00000' if ( $Zip5 eq '' );
        $Zip4 = '0000'  if ( $Zip4 eq '' );
        $xml =
qq|API=Verify&XML=<AddressValidateRequest USERID="${USERID}"><Address>|;
        $xml .= qq|<Address1>$r->{'Addr1'}</Address1>|
          ;    ## unless ( $r->{'Addr1'} eq '' );
        $xml .= qq|<Address2>$r->{'Addr2'}</Address2>|
          ;    ## unless ( $r->{'Addr2'} eq '' );
        $xml .= qq|<City>$r->{'City'}</City>|; ## unless ( $r->{'City'} eq '' );
        $xml .= qq|<State>${State}</State>|;
        $xml .= qq|<Zip5>${Zip5}</Zip5>|;
        $xml .= qq|<Zip4>${Zip4}</Zip4>|;
        $xml .= qq|</Address></AddressValidateRequest>|;
    }
    else { $xml = "<p>uspsXML: tag not recognized! (${tag})</p>"; }

    #warn qq|xml=$xml\n|;
    return ($xml);
}

sub parseTag {
    my ( $self, $resp, $tag, @elements ) = @_;
    my $html;
    my $parser  = new XML::DOM::Parser;
    my $RespDoc = $parser->parse($resp);
    if ( $RespDoc->getDocumentElement->getNodeName eq 'Error' ) {
        return ("<p>usps: error parsing request!</p>\n");
    }

    my $InfoList = $RespDoc->getElementsByTagName($tag);
    my $n        = $InfoList->getLength;
    for ( my $i = 0 ; $i < $n ; $i++ ) {
        $html .= qq|<P>\n|;
        my $InfoNode = $InfoList->item($i);

        foreach my $etag (@elements) {
            my $val = '';
            my $el  = $InfoNode->getElementsByTagName($etag)->item(0);
            if ( defined $el ) {
                $val = $el->getFirstChild->getNodeValue;
                $val =~ tr/\n/ /s;
                $val =~ s/(\w+)/\u\L$1/g if ( $etag ne 'State' );
                $val =~ s/Po Box /PO Box /g;
                $val =~ s/ Ne / NE /g;
                $val =~ s/ Nw / NW /g;
                $val =~ s/ Se / SE /g;
                $val =~ s/ Sw / SW /g;
                $val =~ s/ Ne/ NE/g;
                $val =~ s/ Nw/ NW/g;
                $val =~ s/ Se/ SE/g;
                $val =~ s/ Sw/ SW/g;
            }
            $html .=
                $etag eq 'Zip5' ? qq| ${val}|
              : $etag eq 'Zip4' ? qq|-${val} <BR>\n|
              :                   qq| ${val} <BR>\n|;
        }
    }
    return ($html);
}

sub prtHTML {
    my ( $self, $title, $body ) = @_;
    my $html = qq|Content-Type: text/html; charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<HTML>
 <HEAD> <TITLE>${title}</TITLE> </HEAD>
 <BODY>
<H3>USPS Check ${title}</H3>
${body}
 </BODY>
</HTML>
|;
    return ($html);
}
###################################################################################
