#!C:/Strawberry/perl/bin/perl
use strict;
use warnings;
use CGI;

my $q = CGI->new;
print $q->header('text/plain');

print "=== DEBUG: Environment ===\n";
foreach my $key (sort keys %ENV) {
    print "$key = $ENV{$key}\n";
}

print "\n=== DEBUG: File Check ===\n";
my $filepath = 'C:/xampp/htdocs/src/html/mis.menu';

if (-e $filepath) {
    print "File exists: $filepath\n";
    if (-r $filepath) {
        print "File is readable\n";
    } else {
        print "File is NOT readable (permission issue)\n";
    }
    if (open my $fh, '<', $filepath) {
        print "Successfully opened the file\n";
        my $line = <$fh>;
        print "First line: $line\n";
        close $fh;
    } else {
        print "Failed to open file: $!\n";
    }
} else {
    print "File does NOT exist at path: $filepath\n";
}

print "\n=== DEBUG: Current Working Directory ===\n";
use Cwd;
print "CWD: " . getcwd() . "\n";
