package NPIRegistryAPI;

use LWP::UserAgent;
use JSON;
use strict;
use warnings;

use CGI::Carp qw(fatalsToBrowser);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

sub search_api_npi {
    my ( $self, $terms, $tax_desc ) = @_;

    $tax_desc = "Skilled Nursing Facility";

    my @json  = ();
    my @data  = ();
    my @codes = ();
    our %ClinicTypes = ( 'NPI-1' => "Individual", 'NPI-2' => "Organization" );

    my $base_url = "https://npiregistry.cms.hhs.gov/api/";
    my $version  = "2.1";
    my @types    = ( 'NPI-2', 'NPI-1' );

    foreach my $type (@types) {
        my %query_params = (
            'version'          => $version,
            'enumeration_type' => $type,
            "exact_match"      => "false",
            "state"            => "OK",
            "limit"            => 100,

            # "taxonomy_description" => $tax_desc
        );

        if ( $terms =~ /^\d+$/ ) {
            $query_params{'number'} = $terms;
        }
        else {
            if ( 'NPI-1' eq $type ) {
                my @names = split( ':', $terms );
                $query_params{'first_name'} = $names[0] if defined $names[0];
                $query_params{'last_name'}  = $names[1] if defined $names[1];
            }
            else {
                $query_params{'organization_name'} = "*" . $terms . "*";
            }
        }

        my $query_string =
          join( "&", map { "$_=$query_params{$_}" } keys %query_params );
        my $api_url = "$base_url?$query_string";

        my $ua       = LWP::UserAgent->new;
        my $response = $ua->get($api_url);

        if ( $response->is_success ) {
            my $api_data = decode_json( $response->decoded_content );
            if ( exists $api_data->{'results'} ) {
                foreach my $provider ( @{ $api_data->{'results'} } ) {
                    my @row  = ();
                    my $npi  = $provider->{'number'} || '';
                    my $name = $provider->{'basic'}->{'organization_name'}
                      || ($provider->{'basic'}->{'first_name'} . " "
                        . $provider->{'basic'}->{'last_name'} )
                      || '';
                    my $address =
                      $provider->{'addresses'}[0]{'address_1'} || '';
                    my $city  = $provider->{'addresses'}[0]{'city'}      || '';
                    my $state = $provider->{'addresses'}[0]{'state'}     || '';
                    my $zip = $provider->{'addresses'}[0]{'postal_code'} || '';

                    push( @row,
                        $ClinicTypes{$type}, $name, $address, $city, $state,
                        $zip, $npi );
                    push( @codes, $npi );
                    push( @data,  \@row );
                }
            }
        }
        else {
            push(
                @json,
                {
                    "error" => "Failed to fetch data from API: "
                      . $response->status_line
                }

            );
        }
    }

    push( @json, scalar @data );
    push( @json, \@codes );
    push( @json, undef );
    push( @json, \@data );

    return encode_json \@json;
}

1;

