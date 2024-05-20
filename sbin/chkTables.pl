#!/usr/bin/perl
##
use lib '/home/okmis/mis/src/lib';
use DBForm;
$form = DBForm->new();
my $dbh = $form->dbconnect;

#############################################

$form->complete();
exit;

NOT used yet,,,fix up to work.
## BUILDS: chkuploadxTables
$t= $dbh->prepare("show tables like 'x%'");
$t->execute() || print qq|ugh\n|;;
while ( my ($tn) = $t->fetchrow_array )
{
  my $str = 'select '; my $comma = '';
  my $id = '';
  $s= $dbh->prepare("show fields from ${tn}");
  $s->execute() || print qq|ugh\n|;;
  while ( my $r = $s->fetchrow_hashref )
  {
    next if ( $r->{Field} eq 'CreateProvID' );
    next if ( $r->{Field} eq 'CreateDate' );
    next if ( $r->{Field} eq 'ChangeProvID' );
    next if ( $r->{Field} eq 'ChangeDate' );
    next if ( $r->{Field} eq 'RecDOLC' );
    next if ( $r->{Field} eq 'FormID' );
    $str .= qq|${comma}$r->{Field}|;
    $comma = ',';
    $id = $r->{Field} if ( $id eq '' );
  }
  $str .= qq| from ${tn} order by ${id};\n|;
  print $str;
}
$form->complete();
exit;
