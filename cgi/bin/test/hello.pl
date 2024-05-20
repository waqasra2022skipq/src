#!/usr/bin/perl
#
# PDFlib client: hello example in Perl
#

use PDFlib::PDFlib 9.1;
use strict;

eval {
    my $p = new PDFlib::PDFlib;
    my $searchpath = "/tmp/test/data";

    # This means we must check return values of load_font() etc.
    $p->set_option("errorpolicy=return");

    # Set the search path for font files 
    $p->set_option("SearchPath={{" . $searchpath . "}}");


    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    if ($p->begin_document("hello.pdf", "") == -1) {
	die("Error: %s\n", $p->get_errmsg());
    }

    $p->set_info("Creator", "hello.pl");
    $p->set_info("Author", "Thomas Merz");
    $p->set_info("Title", "Hello world (Perl)!");

    $p->begin_page_ext(0, 0, "width=a4.width height=a4.height");

    my $fontopt =
        "fontname=NotoSerif-Regular encoding=unicode fontsize=24";

    $p->fit_textline("Hello world!", 50, 700, $fontopt);
    $p->fit_textline("(says Perl)",  50, 676, $fontopt);

    $p->end_page_ext("");


    $p->end_document("");
};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}
