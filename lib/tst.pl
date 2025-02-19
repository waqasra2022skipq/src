#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use tst;

############################################################################
my $form  = myForm->new();
my $dbh   = myDBI->dbconnect( $form->{'DBNAME'} );
my $debug = $form->{'debug'};

print qq|ENTER: tst, DBNAME=$form->{'DBNAME'}, debug=${debug}\n| if ($debug);
if ($debug) {
    foreach my $f ( sort keys %{$form} ) { print "tst: form-$f=$form->{$f}\n"; }
}

############################################################################
print "## " . localtime() . "\n";

exit if ( $debug == 2 );

my $TABLE = $form->{'TABLE'};
my $ID    = $form->{'ID'};
my $RECID = myDBI->getTableConfig( $TABLE, 'RECID' );

print qq|tst: TABLE=${TABLE}, RECID=${RECID}, ID=${ID}\n| if ($debug);

my $list = '';
my $s    = $dbh->prepare("select * from ${TABLE} where ${RECID}='${ID}'");
$s->execute() || myDBI->dberror("getTABLE: select ${TABLE} ${RECID}=${ID}");
if ( my $r = $s->fetchrow_hashref ) {
    $list = DBA->genInsert( $form, $TABLE, $r ) . ";\n";
    $list .= tst->getSubTables( $form, $TABLE, $ID );
}
$s->finish();
print $list;

#my $cnt = 0;
#foreach my $r ( @records )
#{
#  $cnt++;
#  foreach my $f ( sort keys %{$r} )
#  {
#    print qq|tst: record(${cnt})-$f=$r->{$f}\n|;
#  }
#}
myDBI->cleanup();
############################################################################
exit;
