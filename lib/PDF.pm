package PDF;
use DBI;
use afm;
use Compress::Zlib;

############################################################################
# warnings come from...
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 178.
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 225.
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 250.
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 268.
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 287.
# Using an array as a reference is deprecated at C:/xampp/htdocs/src/lib/PDF.pm line 299.
# so we suppress the warnings...
no warnings;

sub start {
    my ( $self, $template, $flag ) = @_;

   #warn qq|start: pdf\n|;
   #foreach my $f ( sort keys %{$self} ) { warn "start: pdf-$f=$self->{$f}\n"; }

    # first open the pdf template and read thru all the objects
    #   there can be multiple objects we must determine the
    #   starting byte count on
    #   and
    #   multiple font objects we must be able to reference in the
    #   Page object.
    # restrictions: each object must start on its own line such as
    #                        1 0 obj
    #                        2 0 obj
    #                        3 0 obj
    #               and each resource description (font) must 'follow'
    #               the object (obj) line on its own line.

    open( F, "<$template" ) or die "Couldn't open $template! ($!)";
    my ( $objnum, $objflg ) = ( 1, 0 );
    my @objts = ();
    my %rsrcs = ();
    my $inPDT;
    while (<F>) {
        $inPDT .= $_;
        if ( $_ =~ /^${objnum} 0 obj/ ) {
            $objflg = 1;
            push( @objts, index( $inPDT, "${objnum} 0 obj" ) );
        }
        elsif ($objflg) {
            my $line = $_;
            $line =~ s/<//g;
            $line =~ s/>//g;
            my ( $type, $typeflg, $name, $nameflg ) = ( '', 0, '', 0 );
            foreach my $ref ( split( '/', $line ) ) {
                if    ( $ref =~ /^type$/i ) { $typeflg = 1; }
                elsif ($typeflg)            { $type    = $ref; $typeflg = 0; }
                elsif ( $ref =~ /^name$/i ) { $nameflg = 1; }
                elsif ($nameflg)            { $name    = $ref; $nameflg = 0; }
                elsif ( $type ne '' && $name ne '' ) {
                    $rsrcs{$type} .= "/${name} ${objnum} 0 R";
                    ( $type, $name ) = ( '', '' );
                }
            }
            $objnum += 1;
            $objflg = 0;
        }
    }
    close(F);

    # the content object is always the last one in the template.
    my $contobj = $objnum - 1;

    #warn "contentobj=$contobj\ninPDT=\n$inPDT\n";

    # we can go ahead an put the next object in the array.
    #   because it is the start and when we build a new object
    #   we count the number of objects in this array to get the number.
    my $cm = $flag == 1 ? "BT\n" : "10 0 0 10 0 0 cm BT\n";
    push( @objts, length($inPDT) );
    my %times = &afm::load('/usr/share/ghostscript/fonts/n021003l.afm');
    $self = {
        objectStart  => \@objts,
        resourceObjs => \%rsrcs,
        contentObj   => $contobj,
        outStream    => $cm,
        outText      => $inPDT,
        pageObjects  => [],
        times        => \%times
    };

#warn qq|end start: pdf\n|;
#foreach my $f ( sort keys %{$self} ) { warn "end start: pdf-$f=$self->{$f}\n"; }
    bless $self;
}

############################################################################
# routine to set the font in the template.
sub setFont {
    my ( $self, $font, $size ) = @_;
    $self->{outStream} .= qq|${font} ${size} Tf\n|;
    return ($self);
}

# routine to add an element to the template.
sub addElement {
    my ( $self, $x, $y, $data, $font, $size ) = @_;
    ( my $str = $data ) =~ s/([\\()])/\\$1/g;

    #warn qq|str=\n$str\ndata\n$data\n|;
    $str = qq|1 0 0 1 ${x} ${y} Tm ($str) Tj\n|;
    $str = qq|${font} ${size} Tf\n| . $str if ($size);
    $self->{outStream} .= $str;
    return ($self);
}
## Use this one ... new for same as addElement but for flowing Text.
# The $x,$y,$width,$height define a bounding box.  The first text will appear
# on a baseline of $y - $pointsize.
sub addText {
    my ( $self, $x, $y, $width, $height, $text, $pointsize ) = @_;
    $text =~ s/[\r\x92]//g;
    my $y_final = $y - $height;
    my @words   = split( ' ', $text );
    return ($self) if ( !scalar(@words) );
    my ( $streamlen, $line ) = ( 0, shift @words );
    my $linelen =
      afm::stringwidth( ' ' . $line, $pointsize, %{ $self->{times} } );
    foreach my $word (@words) {
        my $wordlen =
          afm::stringwidth( ' ' . $word, $pointsize, %{ $self->{times} } );
        if ( $linelen + $wordlen > $width ) {
            $y -= $pointsize;
            return ($self) if ( $y < $y_final );
            $line =~ s/([\\()])/\\$1/g;
            $self->{outStream} .= "1 0 0 1 $x $y Tm ($line) Tj\n";
            $line = $word;
            $linelen =
              afm::stringwidth( $word, $pointsize, %{ $self->{times} } );
        }
        else {
            $line .= ' ' . $word;
            $linelen += $wordlen;
        }
    }

    # there will always be a remainder, so print it:
    $y -= $pointsize;
    return ($self) if ( $y < $y_final );
    $line =~ s/([\\()])/\\$1/g;
    $self->{outStream} .= "1 0 0 1 $x $y Tm ($line) Tj\n";
    return ($self);
}
##
# routine to add a page to the template.
#   we can choose to compress or deflate the output.
sub add {
    my ( $self, $filter, $data, $flag ) = @_;

    my ( $stream, $filterref ) = ( '', '' );
    my $str = $self->{outStream} . $data . "ET\n";
#################################################################
    # ignore deflate until we get our compression routines online.
    if ( $filter =~ /deflate/i ) {
        my $d = deflateInit;
        $stream = $d->deflate($str);
        $stream .= $d->flush;
        $filterref = "/Filter /FlateDecode";
    }
    else { $stream = $str; }

    # when we do --- delete this next line and use the above if
    #  $stream = $str;
#################################################################
    my $streamlen = length($stream);
    my $obj       = scalar @{ $self->{objectStart} };
    my $out       = "${obj} 0 obj
<< /Length ${streamlen} ${filterref} >>
stream
${stream}
endstream
endobj
";
    my $array_ref = $self->{objectStart};
    my $curlen    = $array_ref->[$#$array_ref];

    push( @{ $self->{objectStart} }, $curlen + length($out) );
    push( @{ $self->{pageObjects} }, $obj );
    $self->{outText} .= $out;

    # set up for next page of output.
    my $cm = $flag == 1 ? "BT\n" : "10 0 0 10 0 0 cm BT\n";
    $self->{outStream} = $cm;

    #  $self->{outStream} = "10 0 0 10 0 0 cm BT\n";
    #warn qq|outText=$self->{outText}\n|;
    return ($self);
}

############################################################################
# routine to print the Pages, Page, Info, Root objects
#   and the cross-reference to finish the pdf.
sub finish {
    my ($self) = @_;

    my $pagesobj = scalar @{ $self->{objectStart} };
    $self->setPagesObj($pagesobj);
    my $rootobj = scalar @{ $self->{objectStart} };
    $self->setRootObj( $pagesobj, $rootobj );
    my $infoobj = scalar @{ $self->{objectStart} };
    $self->setInfoObj($infoobj);
    $self->setXRef( $rootobj, $infoobj );

    #warn qq|outText=$self->{outText}\n|;

    return ($self);
}

############################################################################
sub setPagesObj($) {
    my ( $self, $pagesobj ) = @_;

    # this is the reference object to all the other pages.
    my $out = "${pagesobj} 0 obj\n<<\n/Type /Pages\n/Kids [\n";

    # start the page objects after the reference object to these pages.
    my $pageobj = $pagesobj;
    foreach my $page ( @{ $self->{pageObjects} } ) {
        $pageobj += 1;
        $out .= "${pageobj} 0 R\n";
    }
    my $pagecnt = $pageobj - $pagesobj;

    $out .= "]\n/Count ${pagecnt}\n>>\nendobj\n";
    $self->{outText} .= $out;
    my $array_ref = $self->{objectStart};
    my $lastlen   = $array_ref->[$#$array_ref];

    push( @{ $self->{objectStart} }, $lastlen + length($out) );

    foreach my $page ( @{ $self->{pageObjects} } ) {

        # the pdf template is object 3 0 R below.
        my $objnum = scalar @{ $self->{objectStart} };
        my $out    = "$objnum 0 obj
<<
/Type /Page
/MediaBox [0 0 612 792]
/Parent $pagesobj 0 R
/Resources << /ProcSet [/PDF /Text]
";
        foreach my $rsrc ( sort keys %{ $self->{resourceObjs} } ) {
            $out .= "/$rsrc <<$self->{resourceObjs}{$rsrc}>>\n";
        }
        $out .= ">>
/Contents [
$self->{contentObj} 0 R
$page 0 R
]
>>
endobj
";
        $self->{outText} .= $out;
        my $array_ref = $self->{objectStart};
        my $lastlen   = $array_ref->[$#$array_ref];
        push( @{ $self->{objectStart} }, $lastlen + length($out) );
    }

    return ($self);
}

############################################################################
sub setRootObj($$) {
    my ( $self, $pagesobj, $rootobj ) = @_;

    # this is the new object.
    my $out = "${rootobj} 0 obj
<< /Type /Catalog /Pages $pagesobj 0 R >>
endobj
";
    $self->{outText} .= $out;

    my $array_ref = $self->{objectStart};
    my $lastlen   = $array_ref->[$#$array_ref];
    push( @{ $self->{objectStart} }, $lastlen + length($out) );
    return ($self);
}

############################################################################
sub setInfoObj {
    my ( $self, $infoobj ) = @_;

    # this is the new object.
    my ( $s, $m, $h, $day, $mon, $year ) = localtime;
    my $date = sprintf(
        '%4d%02d%02d%02d%02d%02d',
        $year + 1900,
        $mon + 1, $day, $h, $m, $s
    );
    my $out = "${infoobj} 0 obj
<< /CreationDate (D:$date) /Producer (Keith L. Stephenson) >>
endobj
";
    $self->{outText} .= $out;
    my $array_ref = $self->{objectStart};
    my $lastlen   = $array_ref->[$#$array_ref];
    push( @{ $self->{objectStart} }, $lastlen + length($out) );
    return ($self);
}

############################################################################
sub setXRef($$$) {
    my ( $self, $rootobj, $infoobj ) = @_;

    # this is the cross-reference object.
    my $xrefcount = $#{ $self->{objectStart} };

    my $array_ref  = $self->{objectStart};
    my $xrefoffset = $array_ref->[$#$array_ref];
    my $xref       = $self->{objectStart};

    #warn "xref=$xref, xrefoffset=$xrefoffset, xrefcount=$xrefcount\n";
    my $out = "xref\n0 " . ( $xrefcount + 1 ) . "\n0000000000 65535 f \n";
    for ( my $i = 0 ; $i < $xrefcount ; $i++ ) {
        $out .= sprintf( "%010d 00000 n \n", $xref->[$i] );
    }

    # this is the last object.
    my $finalobj = scalar @{ $self->{objectStart} };
    $out .= "trailer
<<
/Root ${rootobj} 0 R
/Info ${infoobj} 0 R
/Size ${finalobj}
>>
startxref
${xrefoffset}
%%EOF
";
    $self->{outText} .= $out;

    return ($xrefoffset);
}

############################################################################
# The $x,$y,$width,$height define a bounding box.  The first text will appear
# on a baseline of $y - $pointsize.
sub flowText {
    my ( $self, $x, $y, $width, $height, $text, $pointsize ) = @_;

    #warn "s=$self, x=$x, y=$y, width=$width, height=$height, p=$pointsize\n";
    $text =~ s/[\r\x92]//g;
    my $out     = '';
    my $y_final = $y - $height;
    my @words   = split( ' ', $text );
    return $out if ( !scalar(@words) );
    my ( $streamlen, $line ) = ( 0, shift @words );
    my $linelen =
      afm::stringwidth( ' ' . $line, $pointsize, %{ $self->{times} } );

    #my $k=0;
    foreach my $word (@words) {
        my $wordlen =
          afm::stringwidth( ' ' . $word, $pointsize, %{ $self->{times} } );

        #warn qq|l=$linelen, w=$wordlen, word=$word, width=$width\n|;
        if ( $linelen + $wordlen > $width ) {
            $y -= $pointsize;

            #warn qq|k=$k\n|;
            return ($out) if ( $y < $y_final );
            $line =~ s/([\\()])/\\$1/g;

            #$k+=length($line);
            $out .= "1 0 0 1 $x $y Tm ($line) Tj\n";
            $line = $word;
            $linelen =
              afm::stringwidth( $word, $pointsize, %{ $self->{times} } );
        }
        else {
            $line .= ' ' . $word;
            $linelen += $wordlen;
        }
    }

    # there will always be a remainder, so print it:
    $y -= $pointsize;
    return ($out) if ( $y < $y_final );

    #$k+=length($line);
    $line =~ s/([\\()])/\\$1/g;
    $out .= "1 0 0 1 $x $y Tm ($line) Tj\n";

    #warn qq|k=$k\n|;
    return ($out);
}

############################################################################
sub create_fdf($%) {
    my ( $PDFName, %FormFields ) = @_;

    my $FDF = qq{%FDF-1.2

1 0 obj
<< 
/FDF << /Fields 
[
};
    foreach $key ( sort keys %FormFields ) {
        next if ( $key =~ /TABLE_OPEN/ );
        next if ( $key =~ /TABLE_FIELDS/ );
        my $Text = $FormFields{$key};
        $Text =~ s/\\//g;
        $Text =~ s/\(/\\\(/g;
        $Text =~ s/\)/\\\)/g;
        $FDF .= "<< /V ($Text)/T ($key)>>\n";
    }
    $FDF .= qq{
] 
/F ($PDFName)>>
>> 
endobj
trailer
<<
/Root 1 0 R 

>>
%%EOF
};
    return $FDF;
}

##/F (https://www.hsrts-dev.com/cgi/IntakeForm.pdf)>>
############################################################################
sub genFDF {
    my ( $PDFName, $form ) = @_;

    my $FDF = qq{%FDF-1.2

1 0 obj
<< 
/FDF << /Fields 
[
};
    foreach $key ( sort keys %{$form} ) {
        next if ( $key =~ /OPENTABLE/ );
        my $Text = $form->{$key};
        $Text =~ s/[\r\x92]//g;
        $Text =~ s/\\//g;
        $Text =~ s/\(/\\\(/g;
        $Text =~ s/\)/\\\)/g;
        $FDF .= "<< /V ($Text)/T ($key)>>\n";
    }
    $FDF .= qq{
] 
/F ($PDFName)>>
>> 
endobj
trailer
<<
/Root 1 0 R 

>>
%%EOF
};
    return $FDF;
}
############################################################################

1;

