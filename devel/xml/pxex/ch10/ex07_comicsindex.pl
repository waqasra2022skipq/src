#!/usr/bin/perl

# A very simple ComicsML muncher; given a list of URLs pointing to
# ComicsML documents, fetch them, flatten their strips into one list,
# and then build a web page listing, linking to, and possibly
# displaying these strips, sorted with newest first.

use warnings;
use strict;

use ComicsML2;		# ...so that we can build ComicsML objects
use CGI qw(:standard);
use LWP;
use Date::Manip;     	# Cuz we're too bloody lazy to do our own date math

# Let's assume that the URLs of my favorite Internet funnies' ComicsML
# documents live in a plaintext file on disk, with one URL per line
# (What, no XML? For shame...)

my $url_file = $ARGV[0] or die "Usage: $0 url-file\n";

my @urls;			# List of ComicsML URLs
open (URLS, $url_file) or die "Can't read $url_file: $!\n";
while (<URLS>) { chomp; push @urls, $_; }
close (URLS) or die "Can't close $url_file: $!\n";

# Make an LWP user agent
my $ua = LWP::UserAgent->new;
my $parser = XML::ComicsML->new;

my @strips; # This will hold objects representing comic strips

foreach my $url (@urls) {
  warn "Working on $url.\n";
  my $request = HTTP::Request->new(GET=>$url);
  my $result = $ua->request($request);
  my $comic;			# Will hold the comic we'll get back
  if ($result->is_success) {
    # Let's see if the ComicsML parser likes it.
    unless ($comic = $parser->parse_string($result->content)) {
      # Doh, this is not a good XML document.
      warn "The document at $url is not good XML!\n";
      next;
    }
  } else {
    warn "Nothing at $url.\n";
    next;
  }
  # Now peel all the strips out of the comic, pop each into a little
  # hashref along with some information about the comic itself.
  foreach my $strip ($comic->strips) {
    push (@strips, {strip=>$strip, comic_title=>$comic->title, comic_url=>$comic->url});
  }
}

# Sort the list of strips by date.  (We use Date::Manip's exported
# UnixDate function here, to turn their unweildy Gregorian calendar
# dates into nice clean Unixy ones)
my @sorted = sort {UnixDate($$a{strip}->date, "%s") <=> UnixDate($$b{strip}->date, "%s")} @strips;

# Now we build a web page!

print header;
print start_html("Latest comix");
print h1("Links to new comics...");

# Go through the sorted list in reverse, to get the newest at the top.
foreach my $strip_info (reverse(@sorted)) {
  my ($title, $url, $svg);
  my $strip = $$strip_info{strip};
  $title = join (" - ", $strip->title, $strip->date);
  # Hyperlink the title to a URL, if there is one provided
  if ($url = $strip->url) {
    $title = "<a href='$url'>$title</a>";
  }

  # Give similar treatment to the comics' title and URL
  my $comic_title = $$strip_info{comic_title};
  if ($$strip_info{comic_url}) {
    $comic_title = "<a href='$$strip_info{comic_url}'>$comic_title</a>";
  }

  # Print the titles
  print p("<b>$comic_title</b>: $title");
  # If there is SVG, print it right out to the browser.
  if ($svg = $strip->svg) {
    print p($svg);
  }
  
  print "<hr />";
}

print end_html;
