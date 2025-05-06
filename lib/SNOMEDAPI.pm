package SNOMEDAPI;

use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use CGI       qw(:standard);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

use LWP::UserAgent;
use JSON;
use URI::Escape;

my $UMLS_APIKEY = 'b5d6de26-2803-473a-ac00-96e0e8c33c9a';

sub fetchSNOMED {
    my ( $term, $DISORDER, $FINDING, $NURING ) = @_;

    # $term = "depression";
    return { error => "Missing search term" } unless $term;

    my $ua = LWP::UserAgent->new( timeout => 10 );
    $ua->agent("snomed-fetcher/1.0");

    # Step 1: Get TGT
    my $tgt_res = $ua->post( 'https://utslogin.nlm.nih.gov/cas/v1/api-key',
        { apikey => $UMLS_APIKEY } );

    unless ( $tgt_res->is_success ) {
        return { error => "TGT error: " . $tgt_res->status_line };
    }

    my ($tgt_url) = $tgt_res->decoded_content =~ /action="([^"]+)"/;
    return { error => "TGT URL not found" } unless $tgt_url;

    # Step 2: Get ST
    my $st_res =
      $ua->post( $tgt_url, { service => 'http://umlsks.nlm.nih.gov' } );
    return { error => "ST error: " . $st_res->status_line }
      unless $st_res->is_success;
    my $service_ticket = $st_res->decoded_content;

    # Step 3: Search SNOMEDCT_US
    my $encoded = uri_escape($term);

    my $sabs = "SNOMEDCT_US,ICD10CM";

    if ( $DISORDER eq "true" ) {
        $sabs = "ICD10CM";
    }
    elsif ( $FINDING eq "true" ) {
        $sabs = "SNOMEDCT_US";
    }
    elsif ( $NURING eq "true" ) {
        $sabs = "ICNP";
    }
    my $search_url =
"https://uts-ws.nlm.nih.gov/rest/search/current?string=$encoded&ticket=$service_ticket&sabs=${sabs}&pageSize=100&returnIdType=code";

    my $res = $ua->get($search_url);
    return { error => "Search failed: " . $res->status_line }
      unless $res->is_success;

    my $data = eval { decode_json( $res->decoded_content ) };
    return { error => "JSON parse error" } unless $data;

    my $results = $data->{result}->{results} || [];
    return $results;
}

sub fetchSNOMEDByConceptId {
    my ($conceptId) = @_;
    return unless $conceptId;

    my $url =
"https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN%2FSNOMEDCT-US/concepts/$conceptId";

    my $ua       = LWP::UserAgent->new;
    my $response = $ua->get($url);

    if ( $response->is_success ) {
        return decode_json( $response->decoded_content );
    }
    else {
        return { "error" => "Failed to fetch SNOMED concept: "
              . $response->status_line };
    }
}

sub loadAllSavedSNOMED {
    my @conceptIds = @_;    # Array of saved concept IDs

    my @results;
    foreach my $conceptId (@conceptIds) {
        my $conceptData = fetchSNOMEDByConceptId($conceptId);
        if ( $conceptData && !$conceptData->{"error"} ) {
            push @results,
              {
                conceptId => $conceptData->{'conceptId'},
                term      => $conceptData->{'fsn'}{'term'}
              };
        }
        else {
            push @results,
              { conceptId => $conceptId, term => "Invalid SNOMED Code" };
        }
    }

    return encode_json( \@results );
}

1;
