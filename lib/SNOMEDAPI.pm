package SNOMEDAPI;

use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use CGI       qw(:standard);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

sub fetchSNOMED {
    my ( $term, $tag ) = @_;
    $tag ||= "finding";    # Default tag if not provided

    my $base_url =
"https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN%2FSNOMEDCT-US/descriptions";
    my $query_string =
"?term=depression&active=true&conceptActive=true&lang=english&semanticTags=finding&groupByConcept=true";

    my $ua       = LWP::UserAgent->new;
    my $response = $ua->get( $base_url . $query_string );

    if ( $response->is_success ) {

        # my $data = decode_json( $response->decoded_content );
        return $response->{'items'};    # Return matched SNOMED items
    }
    else {
        return { "error" => "Failed to fetch SNOMED data: "
              . $response->status_line };
    }
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
