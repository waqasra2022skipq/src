package NPIRegistryAPI;

use LWP::UserAgent;
use JSON;
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

sub search_api_npi {
    my ( $self, $terms, $types ) = @_;

    my @json        = ();
    my @data        = ();
    my @codes       = ();
    my %ClinicTypes = ( 'NPI-1' => "Individual", 'NPI-2' => "Organization" );

    my $base_url = "https://npiregistry.cms.hhs.gov/api/";
    my $version  = "2.1";

    $types = 'NPI-2' if !$types;
    my @types = split( ',', $types );

    foreach my $type (@types) {
        my %query_params = (
            'version'          => $version,
            'enumeration_type' => $type,
            "exact_match"      => "false",
            "state"            => "OK",
            "limit"            => 200,
        );

        if ( $terms =~ /^\d+$/ ) {
            $query_params{'number'} = $terms;
            fetch_api_data( $base_url, \%query_params, \@data, \@codes, $type,
                \%ClinicTypes );
        }
        elsif ( 'NPI-1' eq $type ) {
            foreach my $field ( 'first_name', 'last_name' ) {
                my %name_query = ( %query_params, $field => $terms . "*" );
                fetch_api_data( $base_url, \%name_query, \@data, \@codes,
                    $type, \%ClinicTypes );
            }
        }
        else {
            $query_params{'organization_name'} = "*" . $terms . "*";
            fetch_api_data( $base_url, \%query_params, \@data, \@codes, $type,
                \%ClinicTypes );
        }
    }

    push @json, scalar @data, \@codes, undef, \@data;
    return encode_json \@json;
}

sub fetch_api_data {
    my (
        $base_url,  $query_params, $data_ref,
        $codes_ref, $type,         $ClinicTypes_ref
    ) = @_;

    my $query_string =
      join( "&", map { "$_=$query_params->{$_}" } keys %$query_params );
    my $api_url = "$base_url?$query_string";

    my $ua       = LWP::UserAgent->new;
    my $response = $ua->get($api_url);

    return unless $response->is_success;

    my $api_data = decode_json( $response->decoded_content );
    process_api_results( $api_data, $data_ref, $codes_ref, $type,
        $ClinicTypes_ref );
}

sub process_api_results {
    my ( $api_data, $data_ref, $codes_ref, $type, $ClinicTypes_ref ) = @_;

    return unless exists $api_data->{'results'};

    foreach my $provider ( @{ $api_data->{'results'} } ) {
        my @row  = ();
        my $npi  = $provider->{'number'} || '';
        my $name = $provider->{'basic'}->{'organization_name'}
          || ($provider->{'basic'}->{'first_name'} . " "
            . $provider->{'basic'}->{'last_name'} )
          || '';
        my $address = $provider->{'addresses'}[0]{'address_1'}   || '';
        my $city    = $provider->{'addresses'}[0]{'city'}        || '';
        my $state   = $provider->{'addresses'}[0]{'state'}       || '';
        my $zip     = $provider->{'addresses'}[0]{'postal_code'} || '';

        push @row, $ClinicTypes_ref->{$type}, $name, $address, $city, $state,
          $zip, $npi;

        unless ( grep { $_ eq $npi } @$codes_ref ) {
            push @$codes_ref, $npi;
            push @$data_ref,  \@row;
        }
    }
}

1;
