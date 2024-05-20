#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
############################################################################
# Require Necessary Routines for this script to run.
##
my $form = DBForm->parse();

# where $form->{p} is $rProvider->{'password'}...

my $c = main->getPswd($form,$form->{p});
print qq|$form->{p}, $c\n|;

##my $c = crypt($form->{p},'junk');
##print qq|$form->{p}, $c\n|;

exit;

sub getPswd
{
  my ($self,$form,$pswd) = @_;
  my $dbh = $form->dbconnect();
  my $qmd5 = qq|select MD5(?)|;
  my $smd5 = $dbh->prepare($qmd5);
  $smd5->execute($pswd);
  my $md5 = $smd5->fetchrow_array;
  $smd5->finish();
  return($md5);
}
