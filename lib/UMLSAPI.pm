package UMLSAPI;

use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use URI::Escape;

use Exporter 'import';
our @EXPORT_OK = qw(search_umls);

my $APIKEY = 'b5d6de26-2803-473a-ac00-96e0e8c33c9a';

sub search_umls {
    my ( $pattern, $DISORDER, $FINDING ) = @_;
    return [] unless $pattern;

    my $ua = LWP::UserAgent->new( timeout => 10 );
    $ua->agent("okmis-umls-client/1.0");

    # Step 1: Get TGT
    my $tgt_res = $ua->post(
        'https://utslogin.nlm.nih.gov/cas/v1/api-key',
        {
            apikey => $APIKEY
        }
    );

    unless ( $tgt_res->is_success ) {
        warn "UMLS TGT error: " . $tgt_res->status_line;
        return [];
    }

    my ($tgt_url) = $tgt_res->decoded_content =~ /action="([^"]+)"/;
    return [] unless $tgt_url;

    # Step 2: Get ST
    my $st_res = $ua->post(
        $tgt_url,
        {
            service => 'http://umlsks.nlm.nih.gov'
        }
    );

    return [] unless $st_res->is_success;
    my $service_ticket = $st_res->decoded_content;

    # Step 3: Search UMLS
    my $encoded = uri_escape($pattern);
    my $search_url =
"https://uts-ws.nlm.nih.gov/rest/search/current?string=$encoded&ticket=$service_ticket";

    my $res = $ua->get($search_url);
    return [] unless $res->is_success;

    my $data = eval { decode_json( $res->decoded_content ) };
    return [] unless $data;

    my $results = $data->{result}->{results} || [];
    my @final_results;

    foreach my $item (@$results) {
        my $name = $item->{name} // '';
        my $ui   = $item->{ui}   // '';

        next if !$ui || $ui eq 'NONE';    # skip if no valid UI (CUI)

        # Only look for SNOMED concepts (optional but safe)
        if ( $DISORDER eq "true" ) {
            next
              unless $item->{rootSource}
              && $item->{rootSource} eq 'SNOMEDCT_US';
        }

        # Now, attempt Crosswalk: SNOMED CT → ICD-10-CM
        my $crosswalk_url =
"https://uts-ws.nlm.nih.gov/rest/crosswalk/current/source/SNOMEDCT_US/$ui?ticket=$service_ticket&targetSource=ICD10CM";

        # my $crosswalk_res = $ua->get($crosswalk_url);

        my @crosswalks;

        # if ( $crosswalk_res->is_success ) {
        #     my $cross_data =
        #       eval { decode_json( $crosswalk_res->decoded_content ) };
        #     if (   $cross_data
        #         && $cross_data->{result}
        #         && ref $cross_data->{result} eq 'ARRAY' )
        #     {
        #         foreach my $cw ( @{ $cross_data->{result} } ) {
        #             push @crosswalks,
        #               {
        #                 icd10_code => $cw->{ui}   || '',
        #                 icd10_name => $cw->{name} || '',
        #               };
        #         }
        #     }
        # }

        push @final_results, {
            name       => $name,
            snomed_id  => $ui,
            crosswalks => \@crosswalks,    # List of ICD10 matches
        };
    }

    return \@final_results;
}

1;
