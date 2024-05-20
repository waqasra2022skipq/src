#!/usr/bin/perl -w
# Change above line to point to your perl binary

use CGI ':standard';
use lib '/cise/homes/ppadala/mydepot/lib/perl5/site_perl';
use GD::Graph::bars;
use strict;

# Both the arrays should same number of entries.
my @data = (['Fall 01', 'Spr 01', 'Fall 02', 'Spr 02' ],
            [80, 90, 85, 75],
            [76, 55, 75, 95],
            [66, 58, 92, 83]);

my $mygraph = GD::Graph::bars->new(500, 300);
$mygraph->set(
    x_label     => 'Semester',
    y_label     => 'Marks',
    title       => 'Grade report for a student',
    # Draw bars with width 3 pixels
    bar_width   => 3,
    # Sepearte the bars with 4 pixels
    bar_spacing => 4,
    # Show the grid
    long_ticks  => 1,
    # Show values on top of each bar
    show_values => 1,
) or warn $mygraph->error;

$mygraph->set(logo => '/home/okmis/mis/src/images/eti_logo.jpg');
$mygraph->set(logo_resize => 0.5);
$mygraph->set(logo_position => 'LL');
$mygraph->set_legend_font(GD::gdMediumBoldFont);
$mygraph->set_legend('Exam 1', 'Exam 2', 'Exam 3');
my $myimage = $mygraph->plot(\@data) or die $mygraph->error;
print "Content-type: image/png\n\n";
print $myimage->png;

