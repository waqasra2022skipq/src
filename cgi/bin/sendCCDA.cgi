#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBI;
use DBForm;
use DBUtil;
use Time::Local;

############################################################################
# usage:
#        creates the /tmp/phimail: file to be picked up by cronjob 'phisend.sh'
#        phisend.sh email the file to PhiMail and drops off the status file 'phistat...'
#        which this routine picks up and displays
#        (.php routines are not configured to run from html so we use a cronjob)
############################################################################
my $form = DBForm->new();
foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
my $Agent = SysAccess->verify( $form, 'Privilege=Agent' );
unless ($Agent) { $form->error("Page DENIED!"); }
my $To       = $form->{'To'};
my $sendfile = $form->{'sendfile'};

my $pathname = '/tmp/phimail:' . DBUtil->genToken();
if ( open( TEMPLATE, ">$pathname" ) ) {
    print TEMPLATE qq|${sendfile}\n${To}\n|;
}
close(TEMPLATE);

( my $outfile = $pathname ) =~ s/phimail/phistat/g;
my $str     = '';
my $outtext = '';
for ( my $i = 0 ; $i <= 10 ; $i++ ) {
    sleep 6;
    if ( -e $outfile ) {
        $str .= qq|i=${i}:|;
        $outtext = DBUtil->ReadFile($outfile);
        last;
    }
}
$outtext = qq|failed to send!| if ( $outtext eq '' );

#  my $cmd = qq|php C:/xampp/htdocs/src/phimail/PhiMail.php ${sendfile} ${to}|;
#warn qq|cmd:${cmd}\n|;
#  my $outfile = $form->{DOCROOT}.$sendfile.'.out';
#  system("${cmd} > ${outfile} 2>${outfile}");
#  my $outtext = DBUtil->ReadFile($outfile);

print qq|Content-Type: text/html \n\n
<BR>
<pre>
${outtext}
<BR>
${str}
</pre>
|;
############################################################################
$form->complete();
exit;
############################################################################
