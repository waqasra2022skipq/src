#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBUtil;
use myConfig;
use Time::Local;

############################################################################
# usage: phimail
############################################################################
my $clear = shift;
my $cmd = qq|php |.myConfig->cfg('PHIBIN').qq|/phisend.php|;   # location of CMD

my $DT=localtime();
print "phimail started @ $DT\n";
chdir("/tmp");
my @files = glob("phimail:*");
foreach $f ( @files )
{
  print qq|f=$f\n|;
  my @file = DBUtil->readasarray($f);
  my $sendfile = $file[0];
  my $to = $file[1];
  (my $outfile = $f) =~ s/phimail/phistat/g;
  print qq|phimail: ${cmd} ${sendfile} ${to} > ${outfile}\n|;
  if ( myConfig->cfg('PHISEND') )
  {
    print qq|send: ${sendfile} ${to}\n|;
    my $out = `${cmd} ${sendfile} ${to} > ${outfile} 2>${outfile}`;
    if ( open(TEMPLATE, ">>$outfile") ) 
    { print TEMPLATE qq|${out}\n|; }
    close(TEMPLATE);
    unlink($f);     # delete so next loop we don't get it.
  }
  else
  {
    print qq|phisend turned off.\n|;
    unlink($f) if ( $clear );
  }
}
my $DT=localtime();
print "phimail ended @ $DT\n";
exit;
############################################################################
