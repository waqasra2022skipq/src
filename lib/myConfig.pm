package myConfig;
require('/var/www/okmis/src/cfg/system.cfg');
require('/var/www/okmis/src/cfg/tables.cfg');

############################################################################
sub cfg { return ( $SYSTEM{ $_[1] } ); }

sub cfgfile {
    my ( $self, $file, $html ) = @_;

    #warn qq|file=$file\n|;
    my ( $www, $sys, $img ) =
      ( $SYSTEM{DOCROOT} . '/' . 'mycfg', $SYSTEM{CFG}, $SYSTEM{IMG} );

    # ie: www=/home/okmms/www/mms/mycfg, sys=/var/www/okmis/src/cfg
    my ( $wpath, $wdir ) = $www =~ /(.*\/)?(.+)/s;

    # ie: wpath=/home/okmms/www/mms/, wdir=mycfg
    my ( $spath, $sdir ) = $sys =~ /(.*\/)?(.+)/s;

    # ie: spath=/var/www/okmis/src/, sdir=cfg
    my ( $ipath, $idir ) = $img =~ /(.*\/)?(.+)/s;

    # ie: spath=/var/www/okmis/src/, sdir=img

    #warn qq|www=$www, wpath=$wpath, wdir=$wdir\n|;
    #warn qq|sys=$sys, spath=$spath, sdir=$sdir\n|;
    #warn qq|img=$img, ipath=$ipath, idir=$idir\n|;

    my ( $path, $dir ) = ( '', '' );
    if ( -f $www . '/' . $file ) { $path = $wpath; $dir = $wdir . '/' . $file; }
    elsif ( -f $sys . '/' . $file ) {
        $path = $spath;
        $dir  = $sdir . '/' . $file;
    }
    elsif ( -f $img . '/' . $file ) {
        $path = $ipath;
        $dir  = $idir . '/' . $file;
    }
    elsif ( -f $www . '/' . $file . '.gif' ) {
        $path = $wpath;
        $dir  = $wdir . '/' . $file . '.gif';
    }
    elsif ( -f $sys . '/' . $file . '.gif' ) {
        $path = $spath;
        $dir  = $sdir . '/' . $file . '.gif';
    }
    elsif ( -f $www . '/' . $file . '.jpg' ) {
        $path = $wpath;
        $dir  = $wdir . '/' . $file . '.jpg';
    }
    elsif ( -f $sys . '/' . $file . '.jpg' ) {
        $path = $spath;
        $dir  = $sdir . '/' . $file . '.jpg';
    }
    elsif ( -f $www . '/' . $file . '.png' ) {
        $path = $wpath;
        $dir  = $wdir . '/' . $file . '.png';
    }
    elsif ( -f $sys . '/' . $file . '.png' ) {
        $path = $spath;
        $dir  = $sdir . '/' . $file . '.png';
    }
    return ( $html ? '/' . $dir : $path . $dir );
}
sub tbl { return ( $TABLES{ $_[1] }{ $_[2] } ); }

sub settbl {
    my ( $self, $table, $fld, $val ) = @_;
    if ( $table ne '' && $fld ne '' ) { $TABLES{$table}{$fld} = $val; }
    return ();
}
sub SCR { return ( $SCREENS{ $_[1] } ); }
sub scr { return ( $SCREENS{ $_[1] }{ $_[2] } ); }

# okmis/a1000, demo/demo123, db/kls5773
sub dbu {
    my ( $self, $dbname ) = @_;
    my $u = $dbname eq 'okmis_config' ? 'okmis' : $dbname;
    my $u = 'root';

    #warn qq|dbu: dbname=$dbname, u=$u\n|;
    return ($u);
}

sub dbp {
    my ( $self, $dbname ) = @_;
    my $p =
        $dbname =~ /_demo$/  ? 'demo123'
      : $dbname =~ /^graphs/ ? 'a1000'
      :                        'kls5773';

    #warn qq|dbp: dbname=$dbname, p=$p\n|;
    #  my $p = '7years5773';
    my $p = 'stayAwayRoot@123';
    return ($p);
}

sub test {
    my ( $self, $file, $html ) = @_;
    require( $self->cfg('CFG') . '/tables.cfg' );
}
############################################################################
1;
