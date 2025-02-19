#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
############################################################################
# I use this routine to split out what cgi script is called.
# ClientList.cgi, ChartList.cgi, ProviderList.cgi
# because the SearchString is 1 field and the ACTION is 1.
############################################################################
my $form = myForm->new();
if ( $form->{'SearchType'} eq 'ClientID' ) {
    print
qq|Location: /cgi/bin/ClientList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ClientSSN' ) {
    print
qq|Location: /cgi/bin/ClientList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ClientFirstName' ) {
    print
qq|Location: /cgi/bin/ClientList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ClientLastName' ) {
    print
qq|Location: /cgi/bin/ClientList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ClientInsNum' ) {
    print
qq|Location: /cgi/bin/ClientList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ClientNote' ) {
    ( my $TrID = $form->{'SearchString'} ) =~ s/\.{3}//g;
    print
qq|Location: /cgi/bin/ChartList.cgi?Treatment_TrID=${TrID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ProviderID' ) {
    print
qq|Location: /cgi/bin/ProviderList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ProviderFirstName' ) {
    print
qq|Location: /cgi/bin/ProviderList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
elsif ( $form->{'SearchType'} eq 'ProviderLastName' ) {
    print
qq|Location: /cgi/bin/ProviderList.cgi?SearchType=$form->{SearchType}&SearchString=$form->{SearchString}&mlt=$form->{mlt}\n\n|;
}
else { myDBI->error("Search.cgi: Type '$form->{SearchType} not defined!"); }
myDBI->cleanup();
exit;
############################################################################
