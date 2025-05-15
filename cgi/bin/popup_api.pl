#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

use DBI;
use login;
use DBForm;
use DBA;
use myHTML;
use DBUtil;
use JSON;
use strict;

use warnings;
use LWP::UserAgent;
use CGI;
use NPIRegistryAPI;
use SNOMEDAPI;

############################################################################
my $form = DBForm->parse();
$form = login->chkLogin($form);

#foreach my $f ( sort keys %{$form} ) { warn "popup: form-$f=$form->{$f}\n"; }
my $dbh  = $form->dbconnect();
my $cdbh = $form->connectdb('okmis_config');

############################################################################
my $json_str;

if ( $form->{method} eq 'Agency' || $form->{method} eq 'Physicians' ) {
    ( my $terms = $form->{'terms'} ) =~ s/"//g;
    my $types = $form->{'types'};

    $json_str = NPIRegistryAPI->search_api_npi( $terms, $types );
}
elsif ( $form->{method} eq 'snomedSearch' ) {

    my $terms = $form->{terms};

    my $results = SNOMEDAPI::fetchSNOMED($terms);

    # Get the count of the results
    my $count = scalar(@$results);
    my @json  = ();
    my @items = ($count);

    my @data  = ();
    my @codes = ();
    foreach my $item (@$results) {
        my $code = $item->{ui};
        my $name = $item->{name};
        my $type = $item->{rootSource};

        push( @codes, $code );
        push( @data,  [ $code, $name, $type ] );
    }

    push( @items, [@codes] );
    push( @items, undef );
    push( @items, [@data] );

    # @json = [@items];

    $json_str = encode_json \@items;
}
elsif ( $form->{method} eq 'xLDO' ) {
    my @json = ();
    ( my $terms = $form->{'terms'} ) =~ s/"//g;
    my $FLD      = $form->{FLD};
    my $PREVFLDS = $form->{PREVFLDS};

    my ( $FLDS, $CodeFLD, $limit, $maxLimit, $q, $SelectQ, $CountQ ) =
      ( 'Code Descr', 'Code', 20, 500, '', '', '' );

    if ( $FLD ne '' ) {
        $SelectQ = qq|select xLDO${FLD}.Code, xLDO${FLD}.Descr|
          if $FLD ne 'Descr';
        $SelectQ = qq|select xLDO.Code, xLDO.Descr| if $FLD eq 'Descr';
        $CountQ  = qq|select count(*) as cnt|;

        $q = qq| from xLDO |;
        $q .= qq| left join xLDO${FLD} on xLDO.${FLD}=xLDO${FLD}.Code |
          if $FLD ne 'Descr';
        if ( $PREVFLDS ne '' ) {
            foreach my $fv ( split( ';', $PREVFLDS ) ) {
                my ( $f, $v ) = split( ':', $fv );
                $q .= qq| left join xLDO${f} on xLDO.Code=xLDO${f}.Code |
                  if ( $f ne '' && $v ne '' && $f ne 'Descr' );
            }
        }
        $q .= qq| where xLDO.Active=1 |;
        $q .= qq| and xLDO${FLD}.Active=1 and xLDO.${FLD} is not null |
          if $FLD ne 'Descr';
        $q .= qq| and xLDO${FLD}.Descr like "%${terms}%" |
          if ( $FLD ne 'Descr' && $terms ne '' && $terms ne '*' );
        $q .= qq| and xLDO.Descr like "%${terms}%" |
          if ( $FLD eq 'Descr' && $terms ne '' && $terms ne '*' );
        if ( $PREVFLDS ne '' ) {
            foreach my $fv ( split( ';', $PREVFLDS ) ) {
                my ( $f, $v ) = split( ':', $fv );
                $q .= qq| and xLDO.${f} = "${v}" |
                  if ( $f ne '' && $v ne '' && $f ne 'Descr' );
                $q .= qq| and xLDO.Code = "${v}" |
                  if ( $f eq 'Descr' and $v ne '' );
            }
        }
        $q .= qq| group by xLDO.${FLD} | if $FLD ne 'Descr';

        my $sxLDOCount =
          $cdbh->prepare(qq|${CountQ} from (${SelectQ} ${q}) as ss|);
        $sxLDOCount->execute() || $form->dberror(qq|${CountQ} $q|);

        if ( my $rxLDOCount = $sxLDOCount->fetchrow_hashref ) {
            if ( $rxLDOCount->{'cnt'} > 0 ) {
                my $cnt = $rxLDOCount->{'cnt'};
                my ( @codes, @data ) = ( (), () );
                push( @json, $cnt );

                if ( exists $form->{'maxList'} ) {
                    $q .= qq| limit $maxLimit |;
                }
                else {
                    $q .= qq| limit $limit |;
                }

                my $sxLDO = $cdbh->prepare(qq|${SelectQ} ${q}|);
                $sxLDO->execute() || $form->dberror(qq|${SelectQ} ${q}|);

                while ( my $rxLDO = $sxLDO->fetchrow_hashref ) {
                    my @row = ();
                    foreach my $fld ( split( ' ', $FLDS ) ) {
                        if ( $fld eq $CodeFLD ) {
                            push( @codes, $rxLDO->{$fld} );
                        }
                        else {
                            $rxLDO->{$fld} = '' if $rxLDO->{$fld} eq '';
                            push( @row, $rxLDO->{$fld} );
                        }
                    }
                    push( @data, \@row );
                }
                push( @json, \@codes );
                push( @json, undef );
                push( @json, \@data );

                $sxLDO->finish();
            }
        }

        $json_str = encode_json \@json;
        $sxLDOCount->finish();
    }
}
elsif ( $form->{method} eq 'getxLDODetail' ) {
    my %json = ();
    ( my $terms = $form->{'terms'} ) =~ s/"//g;
    my $FLDS = 'SubjectMatterDomain Role Setting TypeOfService Kind';

    if ( $terms ne '' ) {
        my $q = qq|
select xLDO.SubjectMatterDomain, xLDOSubjectMatterDomain.Descr as SubjectMatterDomainDescr,
  xLDO.Role, xLDORole.Descr as RoleDescr,
  xLDO.Setting, xLDOSetting.Descr as SettingDescr,
  xLDO.TypeOfService, xLDOTypeOfService.Descr as TypeOfServiceDescr,
  xLDO.Kind, xLDOKind.Descr as KindDescr
from xLDO
left join xLDOSubjectMatterDomain
  on xLDOSubjectMatterDomain.Code = xLDO.SubjectMatterDomain
left join xLDORole
  on xLDORole.Code = xLDO.Role
left join xLDOSetting
  on xLDOSetting.Code = xLDO.Setting
left join xLDOTypeOfService
  on xLDOTypeOfService.Code = xLDO.TypeOfService
left join xLDOKind
  on xLDOKind.Code = xLDO.Kind
where xLDO.Active = 1 and xLDO.Code = "${terms}"
|;

        my $sxLDO = $cdbh->prepare($q);
        $sxLDO->execute() || $form->dberror($q);

        if ( my $rxLDO = $sxLDO->fetchrow_hashref ) {
            foreach my $fld ( split( ' ', $FLDS ) ) {
                $json{$fld} = $rxLDO->{$fld};
                $json{ $fld . 'Descr' } = $rxLDO->{ $fld . 'Descr' };
            }
        }

        $json_str = encode_json \%json;
        $sxLDO->finish();
    }
}
elsif ( $form->{method} eq 'xTaxonomy' ) {
    my @json = ();
    ( my $terms = $form->{'terms'} ) =~ s/"//g;
    if ( $terms ne '' ) {
        my ( $FLDS, $CodeFLD, $limit, $maxLimit ) =
          ( 'ID Spec Class Type', 'ID', 20, 500 );

        my $SelectQ = qq|select *|;
        my $CountQ  = qq|select count(*) as cnt|;
        my $For     = qq| like "%${terms}%" |;
        my $WhereQ =
          qq| and (ID ${For} or Spec ${For} or Class ${For} or Type ${For}) |;

        my $q = qq| from xTaxonomy where Active=1 |;
        $q .= qq| ${WhereQ} | if $terms ne '*';

        my $sxTaxonomyCount = $cdbh->prepare(qq|${CountQ} ${q}|);
        $sxTaxonomyCount->execute() || $form->dberror(qq|${CountQ} ${q}|);

        if ( my $rxTaxonomyCount = $sxTaxonomyCount->fetchrow_hashref ) {
            if ( $rxTaxonomyCount->{'cnt'} > 0 ) {
                my $cnt = $rxTaxonomyCount->{'cnt'};
                my ( @codes, @data ) = ( (), () );
                push( @json, $cnt );

                $q .= qq| order by ID |;
                if ( exists $form->{'maxList'} ) {
                    $q .= qq| limit $maxLimit |;
                }
                else {
                    $q .= qq| limit $limit |;
                }

                my $sxTaxonomy = $cdbh->prepare(qq|${SelectQ} $q|);
                $sxTaxonomy->execute() || $form->dberror(qq|${SelectQ} $q|);

                while ( my $rxTaxonomy = $sxTaxonomy->fetchrow_hashref ) {
                    my @row = ();
                    foreach my $fld ( split( ' ', $FLDS ) ) {
                        if ( $fld eq $CodeFLD ) {
                            push( @codes, $rxTaxonomy->{$fld} );
                        }
                        $rxTaxonomy->{$fld} = '' if $rxTaxonomy->{$fld} eq '';
                        push( @row, $rxTaxonomy->{$fld} );
                    }
                    push( @data, \@row );
                }
                push( @json, \@codes );
                push( @json, undef );
                push( @json, \@data );

                $sxTaxonomy->finish();
            }
        }

        $json_str = encode_json \@json;
        $sxTaxonomyCount->finish();
    }
}
elsif ( $form->{method} eq 'xOccupationSnomed' ) {
    my @json = ();
    ( my $terms = $form->{'terms'} ) =~ s/"//g;
    if ( $terms ne '' ) {
        my ( $FLDS, $CodeFLD, $limit, $maxLimit ) = (
            'Code Description CodeSystem CodeSystemVers CodeSystemOID',
            'Code', 20, 500
        );

        my $SelectQ = qq|select *|;
        my $CountQ  = qq|select count(*) as cnt|;
        my $For     = qq| like "%${terms}%" |;
        my $WhereQ  = qq| and (Code ${For} or Description ${For}) |;

        my $q = qq| from xOccupationSnomed where Active=1 |;
        $q .= qq| ${WhereQ} | if $terms ne '*';

        my $sxOccupationSnomedCount = $cdbh->prepare(qq|${CountQ} ${q}|);
        $sxOccupationSnomedCount->execute()
          || $form->dberror(qq|${CountQ} ${q}|);

        if ( my $rxOccupationSnomedCount =
            $sxOccupationSnomedCount->fetchrow_hashref )
        {
            if ( $rxOccupationSnomedCount->{'cnt'} > 0 ) {
                my $cnt = $rxOccupationSnomedCount->{'cnt'};
                my ( @codes, @data ) = ( (), () );
                push( @json, $cnt );

                $q .= qq| order by Description |;
                if ( exists $form->{'maxList'} ) {
                    $q .= qq| limit $maxLimit |;
                }
                else {
                    $q .= qq| limit $limit |;
                }

                my $sxOccupationSnomed = $cdbh->prepare(qq|${SelectQ} $q|);
                $sxOccupationSnomed->execute()
                  || $form->dberror(qq|${SelectQ} $q|);

                while ( my $rxOccupationSnomed =
                    $sxOccupationSnomed->fetchrow_hashref )
                {
                    my @row = ();
                    foreach my $fld ( split( ' ', $FLDS ) ) {
                        if ( $fld eq $CodeFLD ) {
                            push( @codes, $rxOccupationSnomed->{$fld} );
                        }
                        $rxOccupationSnomed->{$fld} = ''
                          if $rxOccupationSnomed->{$fld} eq '';
                        push( @row, $rxOccupationSnomed->{$fld} );
                    }
                    push( @data, \@row );
                }
                push( @json, \@codes );
                push( @json, undef );
                push( @json, \@data );

                $sxOccupationSnomed->finish();
            }
        }

        $json_str = encode_json \@json;
        $sxOccupationSnomedCount->finish();
    }
}
############################################################################
#warn qq|json_str=$json_str\n|;
print qq|Content-type: application/json\n\n${json_str}|;
$dbh->disconnect();
$cdbh->disconnect();
$form->complete();
exit;

############################################################################
