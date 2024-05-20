package afm;

sub load ($) {
    my ($filename) = @_;
    open(AFM, "<$filename") or die "Couldn't open: $filename $!";
    while (defined($_ = <AFM>) && $_ !~ /^StartCharMetrics/) {}
    my (%metrics);
    while ($_ = <AFM>) {
	last if $_ =~ /^EndCharMetrics/;
	my @fields = split ';';
	my %values;
	foreach $field (@fields) {
	    @val = split(' ', $field);
	    $values{$val[0]} = $val[1] if $val[0];
	}
	$metrics{chr($values{C})} = $values{WX}
	    if exists $values{C} && $values{C} != -1;
    }
    close(AFM);
    %metrics;
}

sub stringwidth ($$%) {
    my ($string, $pointsize, %metrics) = @_;
    die unless scalar %metrics;
    my $length = 0;
    for (my $i = 0; $i < length($string); $i++) {
	my $c = substr($string, $i, 1);
	#warn "$c (" . ord($c), ') not found' unless exists $metrics{$c};
	$length += $metrics{$c};
    }
    $length * $pointsize / 1000;
}

1;
