package uCalc;
############################################################################
# sub calc... returns count.
# sub flag... adds text to returned count for display: ie.
##               Moderate
##       Treatment plan, considering
##       counseling, follow-up and/or
##           pharmacotherapy
############################################################################
sub calcTotal {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end ) = @_;

#foreach my $f ( sort keys %{$rPHQ} ) { warn "uCalc-calcTotal: rPHQ-$f=$rPHQ->{$f}\n"; }
    my $cnt = 0;
    if ( $beg eq '' || $end eq '' ) {
        $cnt = $rPHQ->{$pfx};
    }    # no loop, just this field (pfx).
    else {
        for my $i ( $beg .. $end ) {

            my $f = $pfx . $i;

            my $f_a = $f . 'a';
            my $f_b = $f . 'b';

            if ( $rPHQ->{$f_a} ne '' ) {
                $cnt += $rPHQ->{$f_a};
            }

            $cnt += $rPHQ->{$f};
        }

    }

    #warn qq|pfx=${pfx}, beg=${beg}, end=${end}, cnt=${cnt}\n|;
    return ($cnt);
}

sub calcCount    # shaded areas are 2 and 3 values
{
    my ( $self, $form, $rPHQ, $pfx, $beg, $end, $isok ) = @_;

#foreach my $f ( sort keys %{$rPHQ} ) { warn "uCalc-calcCount: rPHQ-$f=$rPHQ->{$f}\n"; }
#warn qq|\nENTER: uCalc-calcCount: beg=${beg}, end=${end}, isok=${isok}\n|;
    my ( $ok, $idx, $cnt ) = ( 0, 0, 0 );

#warn qq|     : uCalc-calcCount: q2a=$rPHQ->{q2a}, q2b=$rPHQ->{q2b}, q2c=$rPHQ->{q2c}\n|;
    for my $i ( $beg .. $end ) {
        $idx++;    # 1st 2 checked or not?
        my $f = $pfx . $i;
        if ( $idx < 3 && $rPHQ->{$f} > 1 ) { $ok++; }

        #warn qq| idx=${idx}, ok=${ok}\n|;
        $cnt++ if ( $rPHQ->{$f} > 1 );

        #warn qq| f=${f}, cnt=${cnt}\n|;
    }
    $cnt++ if ( $rPHQ->{$end} == 1 );    # last question is shaded in 1 value.
    if ( $isok && !$ok ) { $cnt = 0; }

    #warn qq|RETURN: uCalc-calcCount: isok=${isok}, ok=${ok}, cnt=${cnt}\n|;
    return ($cnt);
}

sub flagTotal {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end, $min, $med, $max, $severe ) =
      @_;
    my $val = $self->calcTotal( $form, $rPHQ, $pfx, $beg, $end );
    my $html =
         $severe ne ''
      && $val >= $severe ? $val . chr(253) . qq|STYLE="background-color: blue"|
      : $max ne ''
      && $val >= $max ? $val . chr(253) . qq|STYLE="background-color: red"|
      : $med ne ''
      && $val >= $med ? $val . chr(253) . qq|STYLE="background-color: orange"|
      : $min ne ''
      && $val >= $min ? $val . chr(253) . qq|STYLE="background-color: yellow"|
      : $min ne ''
      && $val >= 1 ? $val . chr(253) . qq|STYLE="background-color: lightgreen"|
      : $val;
    return ($html);
}

sub flagBIMSandMMSE {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end, $min, $med, $max, $severe ) =
      @_;
    my $val = $self->calcTotal( $form, $rPHQ, $pfx, $beg, $end );
    my $html =
         $severe ne ''
      && $val <= $severe ? $val . chr(253) . qq|STYLE="background-color: blue"|
      : $max ne ''
      && $val <= $max ? $val . chr(253) . qq|STYLE="background-color: red"|
      : $med ne ''
      && $val <= $med ? $val . chr(253) . qq|STYLE="background-color: orange"|
      : $min ne ''
      && $val <= $min ? $val . chr(253) . qq|STYLE="background-color: yellow"|
      : $min ne ''
      && $val <= 1 ? $val . chr(253) . qq|STYLE="background-color: lightgreen"|
      : $val;
    return ($html);
}

sub flagTotalLabel {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end, $min, $med, $max, $severe ) =
      @_;
    my $val = $self->calcTotal( $form, $rPHQ, $pfx, $beg, $end );
    my $html =
      $severe ne '' && $val >= $severe
      ? 'Severe<BR>mmediate initiation of pharmacotherapy and, if severe impairment or poor response to therapy, expedited referral to a mental health specialist for psychotherapy and/or collaborative management'
      . chr(253)
      . qq|STYLE="background-color: blue"|
      : $max ne '' && $val >= $max
      ? 'Moderately severe<BR>Active treatment with pharmacotherapy and/or psychotherapy'
      . chr(253)
      . qq|STYLE="background-color: red"|
      : $med ne '' && $val >= $med
      ? 'Moderate<BR>Treatment plan, considering counseling, follow-up and/or pharmacotherapy '
      . chr(253)
      . qq|STYLE="background-color: orange"|
      : $min ne '' && $val >= $min
      ? 'Mild<BR>Watchful waiting; repeat PHQ-9 at follow-up'
      . chr(253)
      . qq|STYLE="background-color: yellow"|
      : $min ne '' && $val >= 1
      ? 'Minimal' . chr(253) . qq|STYLE="background-color: lightgreen"|
      : 'None';
    return ($html);
}

# PHQ9: 5-27 is positive and less than 5 is negative
sub flagCountLabel {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end, $isok ) = @_;

#foreach my $f ( sort keys %{$rPHQ} ) { warn "uCalc-flagCountLabel: rPHQ-$f=$rPHQ->{$f}\n"; }
    my $val = $self->calcCount( $form, $rPHQ, $pfx, $beg, $end, $isok );

#warn qq|uCalc-flagCountLabel: beg=${beg}, end=${end}, isok=${isok}, val=${val}\n|;
    my $html =
      $val >= 5
      ? 'Major Depressive<BR>G8431/G8434<BR>screening for clinical depression is documented as being POSITIVE and a follow-up plan is documented'
      . chr(253)
      . qq|STYLE="background-color: red"|
      : $val >= 2
      ? 'Other Depressive<BR>G8432/G8510<BR>screening for clinical depression is documented as being NEGATIVE and a follow-up plan is not required'
      . chr(253)
      . qq|STYLE="background-color: orange"|
      : $val >= 1
      ? 'Minimal<BR>G8510<BR>screening for clinical depression is documented as being NEGATIVE and a follow-up plan is not required'
      . chr(253)
      . qq|STYLE="background-color: lightgreen"|
      : 'None<BR>G8510<BR>screening for clinical depression is documented as being NEGATIVE and a follow-up plan is not required';
    return ($html);
}

sub flagSomatoform {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end ) = @_;

#foreach my $f ( sort keys %{$rPHQ} ) { warn "uCalc-flagSomatoform: rPHQ-$f=$rPHQ->{$f}\n"; }
    my $val = $self->calcSomatoform( $form, $rPHQ, $pfx, $beg, $end );

    #warn qq|uCalc-flagSomatoform: beg=${beg}, end=${end}, val=${val}\n|;
    my $html =
      $val < 3 ? $val : $val . chr(253) . qq|STYLE="background-color: red"|;
    return ($html);
}

sub phqPanicSyndrome {
    my ( $self, $form, $rPHQ ) = @_;
    my ( $val1, $val2 ) = $self->calcPanicSyndrome( $form, $rPHQ );
    my $val = $val1 . '/' . $val2;
    $html =
        $val1 < 4 ? $val
      : $val2 < 4 ? $val
      :             $val . chr(253) . qq|STYLE="background-color: red"|;

    #warn qq|phqPanicSyndrome: val1=$val1, val2=$val2, val=$val, html=$html\n|;
    return ($html);
}

sub phqAnxietySyndrome {
    my ( $self, $form, $rPHQ ) = @_;
    my $val = $self->calcAnxietySyndrome( $form, $rPHQ );
    $html =
        $val < 3       ? $val
      : $rPHQ->{'q5a'} ? $val . chr(253) . qq|STYLE="background-color: red"|
      :                  $val;
    return ($html);
}

sub phqBulimiaNervosa {
    my ( $self, $form, $rPHQ ) = @_;
    my $val = $self->calcBulimiaNervosa( $form, $rPHQ );
    $html =
        $val < 3      ? $val
      : $rPHQ->{'q8'} ? $val . chr(253) . qq|STYLE="background-color: red"|
      :                 $val;
    return ($html);
}

sub phqBingeEatingDisorder {
    my ( $self, $form, $rPHQ ) = @_;
    my $val = $self->calcBingeEatingDisorder( $form, $rPHQ );
    $html =
        $val < 3      ? $val
      : $rPHQ->{'q8'} ? $val
      :                 $val . chr(253) . qq|STYLE="background-color: red"|;
    return ($html);
}

sub phqAlcoholAbuse {
    my ( $self, $form, $rPHQ ) = @_;
    my $val = $self->calcAlcoholAbuse( $form, $rPHQ );
    $html =
      $val < 1 ? $val : $val . chr(253) . qq|STYLE="background-color: red"|;

    #warn qq|phqAlcoholAbuse: val=$val, html=$html\n|;
    return ($html);
}
############################################################################
sub calcSomatoform {
    my ( $self, $form, $rPHQ, $pfx, $beg, $end ) = @_;

  #warn qq|\nENTER: uCalc-flagSomatoform: beg=${beg}, end=${end}, pfx=${pfx}\n|;
    my $cnt = 0;
    for my $i ( $beg .. $end ) {
        my $f = $pfx . $i;
        $cnt++ if ( $rPHQ->{$f} > 1 );
    }
    return ($cnt);
}

sub calcPanicSyndrome {
    my ( $self, $form, $rPHQ ) = @_;
    my ( $cnt1, $cnt2 ) = ( 0, 0 );
    for my $i ( "a" .. "d" ) {
        my $f = 'q3' . $i;
        $cnt1++ if ( $rPHQ->{$f} > 0 );
    }
    for my $i ( "a" .. "k" ) {
        my $f = 'q4' . $i;
        $cnt2++ if ( $rPHQ->{$f} > 0 );
    }
    return ( $cnt1, $cnt2 );
}

sub calcAnxietySyndrome {
    my ( $self, $form, $rPHQ ) = @_;
    my $cnt = 0;
    for my $i ( "b" .. "g" ) {
        my $f = 'q5' . $i;
        $cnt++ if ( $rPHQ->{$f} > 1 );
    }
    return ($cnt);
}

sub calcBulimiaNervosa {
    my ( $self, $form, $rPHQ ) = @_;
    my $cnt = 0;
    for my $i ( "a" .. "c" ) {
        my $f = 'q6' . $i;
        $cnt++ if ( $rPHQ->{$f} > 0 );
    }
    return ($cnt);
}

sub calcBingeEatingDisorder {
    my ( $self, $form, $rPHQ ) = @_;
    my $cnt = 0;
    for my $i ( "a" .. "c" ) {
        my $f = 'q6' . $i;
        $cnt++ if ( $rPHQ->{$f} > 0 );
    }
    return ($cnt);
}

sub calcAlcoholAbuse {
    my ( $self, $form, $rPHQ ) = @_;
    my $cnt = 0;
    for my $i ( "a" .. "e" ) {
        my $f = 'q10' . $i;
        $cnt++ if ( $rPHQ->{$f} > 0 );
    }
    return ($cnt);
}
############################################################################
sub ClientPHQ {
    my ( $self, $rPHQ ) = @_;
    my $r = ();
    my ( $cnta, $cntb, $cntc, $cntd1, $cntd2, $cnte, $cntf, $cntg, $cnth, $cnt )
      = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );
    for my $i ( "a" .. "m" ) {
        my $f = 'q1' . $i;
        $cnta++ if ( $rPHQ->{$f} > 1 );
    }
    for my $i ( "a" .. "i" ) {
        my $f = 'q2' . $i;
        $cntb++ if ( $rPHQ->{$f} > 1 );
    }
    $cntb++ if ( $rPHQ->{'q2i'} == 1 );
    for my $i ( "a" .. "i" ) {
        my $f = 'q2' . $i;
        $cntc++ if ( $rPHQ->{$f} > 1 );
    }
    $cntc++ if ( $rPHQ->{'q2i'} == 1 );
    for my $i ( "a" .. "d" ) {
        my $f = 'q3' . $i;
        $cntd1++ if ( $rPHQ->{$f} > 0 );
    }
    for my $i ( "a" .. "k" ) {
        my $f = 'q4' . $i;
        $cntd2++ if ( $rPHQ->{$f} > 0 );
    }
    my $cntd = $cntd1 . '/' . $cntd2;
    for my $i ( "b" .. "g" ) {
        my $f = 'q5' . $i;
        $cnte++ if ( $rPHQ->{$f} > 1 );
    }
    for my $i ( "a" .. "c" ) {
        my $f = 'q6' . $i;
        $cntf++ if ( $rPHQ->{$f} > 0 );
    }
    for my $i ( "a" .. "c" ) {
        my $f = 'q6' . $i;
        $cntg++ if ( $rPHQ->{$f} > 0 );
    }
    for my $i ( "a" .. "e" ) {
        my $f = 'q10' . $i;
        $cnth++ if ( $rPHQ->{$f} > 0 );
    }
    $r->{'a'} = $cnta < 3 ? 'NEG ' . $cnta : 'POS ' . $cnta;
    $r->{'b'} = $cntb < 5 ? 'NEG ' . $cntb : $rPHQ->{'q2a'}
      || $rPHQ->{'q2b'} ? 'POS ' . $cntb : 'NEG ' . $cntb;
    $r->{'c'} = $cntc < 1 ? 'NEG ' . $cntc : $rPHQ->{'q2a'}
      || $rPHQ->{'q2b'} ? 'POS ' . $cntc : 'NEG ' . $cntc;
    $r->{'d'} =
        $cntd1 < 4 ? 'NEG ' . $cntd
      : $cntd2 < 4 ? 'NEG ' . $cntd
      :              'POS ' . $cntd;
    $r->{'e'} =
        $cnte < 3      ? 'NEG ' . $cnte
      : $rPHQ->{'q5a'} ? 'POS ' . $cnte
      :                  'NEG ' . $cnte;
    $r->{'f'} =
        $cntf < 3     ? 'NEG ' . $cntf
      : $rPHQ->{'q8'} ? 'POS ' . $cntf
      :                 'NEG ' . $cntf;
    $r->{'g'} =
        $cntg < 3     ? 'NEG ' . $cntg
      : $rPHQ->{'q8'} ? 'NEG ' . $cntg
      :                 'POS ' . $cntg;
    $r->{'h'} = $cnth < 1 ? 'NEG ' . $cnth : 'POS ' . $cnth;
    for my $i ( "a" .. "h" ) { $cnt++ if ( $r->{$i} =~ /POS/ ); }
    $r->{'Status'} =
        $cnt == 1 ? 'Mild'
      : $cnt == 2 ? 'Moderate'
      : $cnt > 2  ? 'Severe'
      :             'None';
    $r->{'StatusColor'} =
        $cnt == 1 ? 'yellow'
      : $cnt == 2 ? 'orange'
      : $cnt > 2  ? 'red'
      :             'lightgreen';
    return ($r);
}

sub mtValue {
    my ( $self, $form, $r, $table, $fld ) = @_;

    #warn qq|mtValue: table=${table},fld=${fld}\n|;
    #foreach my $f ( sort keys %{$r} ) { warn qq|mtValue: $f=$r->{$f}\n|; }
    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.

#  my $smisTables=$cdbh->prepare("select * from misTables where theTable=? and theField=?");
    my $sxTables = $cdbh->prepare(
"select xTables.theTable,xTableFields.* from xTables left join xTableFields on xTableFields.TableID=xTables.ID where xTables.theTable=? and xTableFields.theField=?"
    );
    $sxTables->execute( $table, $fld );
    my $rxTables = $sxTables->fetchrow_hashref;
    my @d        = split( '\|', $rxTables->{'descriptors'} );

    #warn qq|d=@d\n|;
    my $value = $d[ $r->{$fld} ];

    #warn qq|fld=$fld, $r->{'qB'}, value=$value\n|;
    $sxTables->finish();
    return ($value);
}

sub viewASAM {
    my ( $self, $form, $rASAM ) = @_;

#foreach my $f ( sort keys %{$rASAM} ) { warn qq|calcviewASAM: $f=$rASAM->{$f}\n|; }
#warn qq|viewASAM: subview=$form->{subview}\n|;
    ( my $Level = $rASAM->{'Level'} ) =~ s/\.//g;
    $Level = length($Level) == 2 ? $Level : $Level . '0';
    my $view =
        'view=ASAM_'
      . $rASAM->{'AdultChild'} . '_'
      . $rASAM->{'Type'} . '_L'
      . $Level . '.cgi';

    #warn qq|viewASAM: Level=${Level}, view=${view}\n|;
    return ($view);
}

sub mfqDepression {
    my ( $self, $form, $rMFQ ) = @_;

    #      Child Parent
    my ( $cnt1, $cnt2, $both ) = ( 0, 0 );
    for my $i ( 1 .. 13 ) { my $f = 'qC' . $i; $cnt1 += $rMFQ->{$f}; }
    for my $i ( 1 .. 13 ) { my $f = 'qP' . $i; $cnt2 += $rMFQ->{$f}; }
    for my $i ( 1 .. 13 ) {
        my $f = 'qP' . $i;
        $both = 1 if ( $rMFQ->{$f} ne '' );
    }
    my $total = $cnt1 + $cnt2;
    $html =
        $both
      ? $total >= 12
          ? "$cnt1/$cnt2" . chr(253) . qq|STYLE="background-color: red"|
          : "$cnt1/$cnt2" . chr(253) . qq|STYLE="background-color: green"|
      : $cnt1 >= 8 ? $cnt1 . chr(253) . qq|STYLE="background-color: red"|
      : $cnt2 > 0
      ? "$cnt1/$cnt2" . chr(253) . qq|STYLE="background-color: blue"|
      : $cnt1 . chr(253) . qq|STYLE="background-color: green"|;
    return ($html);
}

sub calcAudit {
    my ( $self, $form, $rAUDIT ) = @_;
    my ( $cnt, $html ) = ( 0, '' );
    my $dbh   = myDBI->dbconnect( $form->{'DBNAME'} );
    my $sGend = $dbh->prepare(
        "select Gend from Client where ClientID='$rAUDIT->{ClientID}'");
    $sGend->execute()
      || myDBI->dberror("InfoLink: select Gend ($rAUDIT->{ClientID})");
    my ($Gend) = $sGend->fetchrow_array;

    # warn qq|Gender: $Gend|;
    for my $i ( 1 .. 10 ) { my $f = 'q' . $i; $cnt += $rAUDIT->{$f}; }
    $html = $cnt;
    if ( $Gend eq 'M' ) {
        $html =
            $cnt >= 15 ? $cnt . chr(253) . qq|STYLE="background-color: red"|
          : $cnt >= 7  ? $cnt . chr(253) . qq|STYLE="background-color: orange"|
          : $cnt >= 1  ? $cnt . chr(253) . qq|STYLE="background-color: green"|
          :              $cnt . chr(253) . qq|STYLE="background-color: white"|;
    }
    if ( $Gend eq 'F' ) {
        $html =
            $cnt >= 15 ? $cnt . chr(253) . qq|STYLE="background-color: red"|
          : $cnt >= 5  ? $cnt . chr(253) . qq|STYLE="background-color: orange"|
          : $cnt >= 1  ? $cnt . chr(253) . qq|STYLE="background-color: green"|
          :              $cnt . chr(253) . qq|STYLE="background-color: white"|;
    }
    $sGend->finish();
    return ($html);
}

sub calcAuditC {
    my ( $self, $form, $rAUDITC ) = @_;
    my ( $cnt, $html ) = ( 0, '' );
    my $dbh   = myDBI->dbconnect( $form->{'DBNAME'} );
    my $sGend = $dbh->prepare(
        "select Gend from Client where ClientID='$rAUDITC->{ClientID}'");
    $sGend->execute()
      || myDBI->dberror("InfoLink: select Gend ($rAUDITC->{ClientID})");
    my ($Gend) = $sGend->fetchrow_array;

    # warn qq|Gender: $Gend|;
    for my $i ( 1 .. 3 ) { my $f = 'q' . $i; $cnt += $rAUDITC->{$f}; }
    $html = $cnt;
    if ( $Gend eq 'M' ) {
        $html =
            $cnt >= 4
          ? $cnt . chr(253) . qq|STYLE="background-color: red"|
          : $cnt . chr(253) . qq|STYLE="background-color: green"|;
    }
    if ( $Gend eq 'F' ) {
        $html =
            $cnt >= 3
          ? $cnt . chr(253) . qq|STYLE="background-color: red"|
          : $cnt . chr(253) . qq|STYLE="background-color: green"|;
    }
    $sGend->finish();
    return ($html);
}

sub calcB32 {
    my ( $self, $form, $r ) = @_;
    my @counts = ();

    #warn "calcB32: ClientID=$r->{'ClientID'}, ID=$r->{ID}\n";
    foreach my $id ( sort keys %{$r} ) {

        #warn "calcB32: $id=$r->{$id}\n";
        # Relation to Self/Others
        if (   $id eq 'B07'
            || $id eq 'B08'
            || $id eq 'B10'
            || $id eq 'B11'
            || $id eq 'B12'
            || $id eq 'B14'
            || $id eq 'B15' )
        {
            $counts[1][1] += 1;
            $counts[1][2] += $r->{$id};
        }

        # Daily Livig / Role Functioning
        elsif ($id eq 'B01'
            || $id eq 'B02'
            || $id eq 'B05'
            || $id eq 'B13'
            || $id eq 'B16'
            || $id eq 'B21'
            || $id eq 'B32' )
        {
            if ( $id eq 'B02' ) {
                $id = 'B03' if ( $r->{B03} > $r->{$id} );
                $id = 'B04' if ( $r->{B04} > $r->{$id} );
            }

            #warn "calcB32: $id=$r->{$id}\n";
            $counts[2][1] += 1;
            $counts[2][2] += $r->{$id};
        }

        # Depression / Anxiety
        elsif ($id eq 'B06'
            || $id eq 'B09'
            || $id eq 'B17'
            || $id eq 'B18'
            || $id eq 'B19'
            || $id eq 'B20' )
        {
            $counts[3][1] += 1;
            $counts[3][2] += $r->{$id};
        }

        # Impulsive / Addictive
        elsif ($id eq 'B25'
            || $id eq 'B26'
            || $id eq 'B28'
            || $id eq 'B29'
            || $id eq 'B30'
            || $id eq 'B31' )
        {
            $counts[4][1] += 1;
            $counts[4][2] += $r->{$id};
        }

        # Psychosis
        elsif ( $id eq 'B22' || $id eq 'B23' || $id eq 'B24' || $id eq 'B27' ) {
            $counts[5][1] += 1;
            $counts[5][2] += $r->{$id};
        }
    }

#for ($k=1; $k<=5; $k++) { warn qq|calcB32: k=${k}, cnt=$counts[$k][1], tot=$counts[$k][2]\n|; }
    return (@counts);
}

sub setB32 {
    my ( $self, $form, $r, $i ) = @_;
    my @counts = $self->calcB32( $form, $r );

#for ($k=1; $k<=5; $k++) { warn qq|setB32: k=${k}, cnt=$counts[$k][1], tot=$counts[$k][2]\n|; }
    my $average =
      sprintf( "%.2f", $counts[$i][1] ? $counts[$i][2] / $counts[$i][1] : 0 );

#warn qq|setB32: average=${average}, total=$counts[$i][2], count==$counts[$i][1]\n|;
    return ($average);
}
############################################################################
1;
