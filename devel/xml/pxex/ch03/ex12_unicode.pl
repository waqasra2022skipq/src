use Unicode::String;

my $string = "This sentence exists in ASCII and UTF-8, but not UCS2. Darn!\n";
my $u = Unicode::String->new($string);

# $u now holds an object representing a stringful of 16-bit characters

# It uses overloading so Perl string operators do what you expect!
$u .= "\n\nOh, hey, it's Unicode all of a sudden. Hooray!!\n"

# print as UCS2
print $u->ucs2;

# print as something more human-readable
print $u->utf8;
