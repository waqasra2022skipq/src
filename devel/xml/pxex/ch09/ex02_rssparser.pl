#!/usr/bin/perl

use XML::RSS;
# Accept file from user arguments
my @rss_docs = @ARGV;
# For now, we'll assume they're all files on disk...
foreach my $rss_doc (@rss_docs) {
  # First, create a new RSS object that will represent the parsed doc
  my $rss = XML::RSS->new;
  # Now parse that puppy
  $rss->parsefile($rss_doc);
  # And that's all. Do whatever else we may want here.
}
