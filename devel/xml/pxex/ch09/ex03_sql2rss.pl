#!/usr/bin/perl

# Turn the last 15 entries of Dr. Link's Weblog into an RSS 1.0 document,
# which gets pronted to STDOUT.

use warnings;
use strict;

use XML::RSS;
use DBIx::Abstract;

my $MAX_ENTRIES = 15;

my ($output_version) = @ARGV;
$output_version ||= '1.0';
unless ($output_version eq '1.0' or $output_version eq '0.9' or 
	$output_version eq '0.91') {
  die "Usage: $0 [version]\nWhere [version] is an RSS version to output: 0.9, 0.91, or 1.0\nDefault is 1.0\n";
}

my $dbh = DBIx::Abstract->connect({dbname=>'weblog',
                                   user=>'link',
                                   password=>'dirtyape'})
  or die "Couln't connect to database.\n";

my ($date) = $dbh->select('max(date_added)',
                          'entry')->fetchrow_array;
my ($time) = $dbh->select('max(time_added)',
                          'entry')->fetchrow_array;

my $time_zone = "+05:00"; # This happens to be where I live. :)
my $rss_time = "${date}T$time$time_zone";
# base time is when I started the blog, for the syndication info
my $base_time = "2001-03-03T00:00:00$time_zone";

# I'll choose to use RSS version 1.0 here, which stuffs some
# meta-information into 'modules' that go into their own namespaces,
# such as 'dc' (for Dublin Core) or 'syn' (for RSS Syndication), but
# fortunately it doesn't make defining the document any more complex,
# as you can see below...

my $rss = XML::RSS->new(version=>'1.0', output=>$output_version);

$rss->channel(
              title=>'jmac Weblog',
              link=>'http://www.jmac.org/weblog/',
              description=>"Jason McIntosh's weblog and online journal",
              dc=> {
                    date=>$rss_time,
                    subject=>'jmac',
                    creator=>'jmac@jmac.org',
                    publisher=>'jmac@jmac.org',
                    rights=>'Copyright 2001 by Jason McIntosh',
                    language=>'en-us',
                   },
              syn=> {
                     updatePeriod=>'daily',
                     updateFrequency=>1,
                     updateBase=>$base_time,
                    },
             );


$dbh->query("select * from entry order by id desc limit $MAX_ENTRIES");
while (my $entry = $dbh->fetchrow_hashref) {

  # Replace XML-naughty characters with entities (Can you type these
  # regexes in your sleep yet?)
  $$entry{entry} =~ s/&/&amp;/g;
  $$entry{entry} =~ s/</&lt;/g;
  $$entry{entry} =~ s/'/&apos;/g;
  $$entry{entry} =~ s/"/&quot;/g;
  $rss->add_item(
                 title=>"$$entry{date_added} $$entry{time_added}",
                 link=>"http://www.jmac.org/weblog?$$entry{date_added}#$$entry{time_added}",
                 description=>$$entry{entry},
                );
}

# For lack of anything better to do, I'll just throw the results into
# standard output. :)

print $rss->as_string;
