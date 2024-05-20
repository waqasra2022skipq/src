#!/usr/bin/perl

use warnings;
use strict;
use CGI;

my $form = new CGI;

print $form->header; #Print HTML header. this is mandatory

my $web_home = "$ENV{DOCUMENT_ROOT}/simple_ajax_cgi_example";

my $UPLOAD_FH = $form->upload("file");

my $newfilename = "new_file";

umask 0000; #This is needed to ensure permission in new file

open my $NEWFILE_FH, "+>", "$web_home/tmp/$newfilename.txt" 
    or die "Problems creating file '$newfilename': $!";

while ( <$UPLOAD_FH> ) {
    print $NEWFILE_FH "$_";
}

close $NEWFILE_FH or die "I cannot close filehandle: $!";

##this is the only way to send msg back to the client
print "<script>parent.callback('upload file success')</script>";

exit;
