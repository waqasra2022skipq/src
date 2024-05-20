#!/usr/bin/perl 
use lib '/home/okmis/mis/src/lib';
use CGI::Upload;
use Time::Local;
use DBI;
use myForm;
use myDBI;
use myConfig;
 
my $debug = 0;
warn "ENTER->Upload\n" if ( $debug );
############################################################################
# installed because new CGI::Upload->param() warns:
#   'CGI::param called in list context'
#   'Fetching the value or values of a single named parameter'
#  makes no sense since I'm calling param as a single named parameter??
$CGI::LIST_CONTEXT_WARN = 0;
my $upload = CGI::Upload->new;
my $Path = $upload->file_name('TheFile');
my $Type = $upload->file_type('TheFile');
$upload->mime_magic('/etc/mime.types');
my $Mime = $upload->mime_type('TheFile');
my $Handle = $upload->file_handle('TheFile');
my @Path = split(/\\/,$Path);
my $Title = pop(@Path);
my $cgi = $upload->query;
my $Action = $cgi->param('Action');
my $DocType = $cgi->param('DocType');
my $DocID = $cgi->param('DocID');
my $DocTitle = $cgi->param('DocTitle');
my $DocDescr = $cgi->param('DocDescr');
my $DocTag = $cgi->param('DocTag');
my $DocLink = $cgi->param('DocLink');
my $ProvID = $cgi->param('Provider_ProvID');
my $ClientID = $cgi->param('Client_ClientID');
my $TrID = $cgi->param('Treatment_TrID');
my $mlt = $cgi->param('mlt');
my $misLINKS = $cgi->param('misLINKS');
my $DirName = '';
my $FileName = '';

############################################################################
my $form = myForm->new("mlt=$mlt&misLINKS=$misLINKS");
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|ENTER: Upload.cgi: DocType=${DocType}, ProvID=${ProvID}, ClientID=${ClientID}, TrID=${TrID}\n| if ( $debug );
warn qq|DocID=${DocID}, DocTitle=${DocTitle}, DocTag=${DocTag}, DocDescr=${DocDescr}\n| if ( $debug );

############################################################################
my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime();
$year += 1900;
$month += 1;
$month = length($month) == 2 ? $month : '0'.$month;
$day = length($day) == 2 ? $day : '0'.$day;
$hrs = length($hrs) == 2 ? $hrs : '0'.$hrs;
$min = length($min) == 2 ? $min : '0'.$min;
$sec = length($sec) == 2 ? $sec : '0'.$sec;
$DT = $year . $month . $day . $hrs . $min . $sec;

my $errmsg = '';
my $query = '';
if ( $Action =~ /cancel/i )
{
  myDBI->cleanup();
  $Location = myForm->popLINK();
  print qq|Location: ${Location}\n\n|;
  exit;
}
elsif ( ${DocType} eq 'MisEDocs' )     # Millennium Electronic Forms, HelpDesk only
{
  $DirName = qq|/Provider/EDocs/${ProvID}|;
  $FileName = main->setFILENAME($DT . '_' . $Title);
  my $PathName = $DirName . '/' . $FileName;
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  $DocTitle = $Title if ( $DocTitle eq '' );
  my $r = ();
  $r->{ProvID} = $ProvID;
  $r->{Title} = $DocTitle;
  $r->{Descr} = $DocDescr;
  $r->{Type} = $DocTag;
  $r->{Path} = $PathName;
  $r->{Link} = $DocLink;
  $r->{CreateProvID} = $form->{LOGINPROVID};
  $r->{CreateDate} = $form->{TODAY};
  $r->{Public} = 0;
  $query = DBA->genReplace($form,$dbh,'ProviderEDocs',$r,"ID=${DocID}");
#warn qq|Upload.cgi: query=$query\n|;
  my $flds = '';
#foreach my $f ( sort keys %{ $r } ) { warn qq|: r-$f=$r->{$f}\n|; }
  my $id = $DocID ? $DocID : 'NEWID';
  $Location = qq|/cgi/bin/mis.cgi?ProviderEDocs_ID=${id}&view=MisEDocs.cgi&Provider_ProvID=${ProvID}&mlt=${mlt}&misLINKS=$misLINKS&misPop=2\n\n|;
}
elsif ( ${DocType} eq 'Provider' )
{
  $DirName = qq|/Provider/EDocs/${ProvID}|;
  $FileName = main->setFILENAME($DT . '_' . $Title);
  my $PathName = $DirName . '/' . $FileName;
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  my $r = ();
  $r->{ProvID} = $ProvID;
  $r->{Title} = $Title;
  $r->{Path} = $PathName;
  $r->{CreateProvID} = $form->{LOGINPROVID};
  $r->{CreateDate} = $form->{TODAY};
  $r->{Public} = 1;
  $query = DBA->genInsert($form,'ProviderEDocs',$r);
#warn qq|Upload.cgi: query=$query\n|;
  $Location = qq|/cgi/bin/mis.cgi?ProviderEDocs_ID=NEWID&view=ProviderEDocs.cgi&Provider_ProvID=${ProvID}&mlt=${mlt}&misLINKS=$misLINKS\n\n|;
}
elsif ( ${DocType} eq 'Client' )
{
  $DirName = qq|/Client/EDocs/${ClientID}|;
  $FileName = main->setFILENAME($DT . '_' . $Title);
  my $PathName = $DirName . '/' . $FileName;
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  my $r = (); $r->{ClientID} = $ClientID; $r->{Title} = $Title; $r->{Path} = $PathName; $r->{CreateProvID} = $form->{LOGINPROVID}; $r->{CreateDate} = $form->{TODAY};
  $query = DBA->genInsert($form,'ClientEDocs',$r);
#warn qq|Upload.cgi: query=$query\n|;
  $Location = qq|/cgi/bin/mis.cgi?ClientEDocs_ID=NEWID&view=ClientEDocs.cgi&Client_ClientID=${ClientID}&mlt=${mlt}&misLINKS=$misLINKS\n\n|;
}
elsif ( ${DocType} eq 'Note' )
{
  $DirName = qq|/Client/Notes/${ClientID}|;
  $FileName = main->setFILENAME($DT . '_' . $Title);
  my $PathName = $DirName . '/' . $FileName;
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  my $r = (); $r->{TrID} = $TrID; $r->{Path} = $PathName;
  $query = DBA->genUpdate($form,'Treatment',$r);
#warn qq|Upload.cgi: query=$query\n|;
  $Location = myForm->popLINK();
}
elsif ( ${DocType} eq 'LOGO' )
{
  $DirName = qq|/Provider/EFiles/LOGO/${ProvID}|;
  $FileName = main->setFILENAME($Title);
  my $PathName = $DirName . '/' . $FileName;
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  my $r = ();
  $r->{ProvID} = $ProvID;
  $r->{LOGO} = $PathName;
  $r->{CreateProvID} = $form->{LOGINPROVID};
  $r->{CreateDate} = $form->{TODAY};
  $query = DBA->genReplace($form,$dbh,'ProviderControl',$r,"ProvID=${ProvID}");
#warn qq|Upload.cgi: query=$query\n|;
  $Location = myForm->popLINK();
}
elsif ( ${DocType} eq 'ERA' )
{
  $DirName = qq|/Provider/EFiles/835|;
  $FileName = main->setFILENAME($Title);
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  $Location = myForm->popLINK();
}
elsif ( ${DocType} eq '837' )
{
  myDBI->cleanup();
  $DirName = qq|/admin/837|;
  $FileName = main->setFILENAME($Title);
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  $Location = qq|/cgi/bin/adminFiles.pl?type=${DocType}&mlt=${mlt}&misLINKS=$misLINKS&misPop=2\n\n|;
warn qq|Upload: Location=${Location}\n| if ( $debug );
  #print qq|Location: ${Location}\n\n|;
  #exit;
}
elsif ( ${DocType} eq '835' )
{
  $DirName = qq|/admin/835|;
  $FileName = main->setFILENAME($Title);
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  $Location = qq|/cgi/bin/adminFiles.pl?type=${DocType}&mlt=${mlt}&misLINKS=$misLINKS&misPop=2\n\n|;
warn qq|Upload: Location=${Location}\n| if ( $debug );
}
elsif ( ${DocType} eq '271' )
{
  $DirName = qq|/admin/271|;
  $FileName = main->setFILENAME($Title);
warn qq|Upload: DirName=${DirName}, FileName=${FileName}, PathName=${PathName}\n| if ( $debug );
  $Location = qq|/cgi/bin/adminFiles.pl?type=${DocType}&mlt=${mlt}&misLINKS=$misLINKS&misPop=2\n\n|;
warn qq|Upload: Location=${Location}\n| if ( $debug );
}
else
{ $errmsg = qq|DataBase upload error: DocType=${DocType}|; }
if ( $errmsg ) { myDBI->dberror($errmsg); }

############################################################################
##
# make sure the directory exists
##
my $RootPath = $form->{DOCROOT} . $DirName;
system("/bin/mkdir -pm 777 ${RootPath}");
# fix FileName for bad characters...

my $RootName = $RootPath . '/' . $FileName;
warn qq|Upload: RootName=${RootName}, FileName=${FileName}\n| if ( $debug );
open NEWFILE, ">${RootName}" || myDBI->error("Couldn't open file: ${Title} $!"); 
print NEWFILE $_ while(<$Handle>);
close($Handle);
close(NEWFILE);
warn qq|Upload: close: FileName=${FileName}\n| if ( $debug );

if ( $query ne '' )
{
  my $sql = $dbh->prepare($query);
  $sql->execute() || myDBI->dberror($query);
  my $NEWID = $sql->{'mysql_insertid'};
  $Location =~ s/NEWID/${NEWID}/g;
}
myDBI->cleanup();
#warn qq|Location: ${Location}\n\n|;
print qq|Location: ${Location}\n\n|;
exit;
############################################################################
sub setFILENAME
{
  my ($self,$inNAME) = @_;
  my $outNAME = $inNAME;
#warn qq|setFILENAME1: FileName: ${outNAME}\n|;
  $outNAME =~ s/\#//g;              # bad char
  $outNAME =~ s/\&//g;              # bad char
  $outNAME =~ s/\r//g;              # carriage return
  $outNAME =~ s/\n//g;              # new line
  $outNAME =~ s/\t//g;              # tab to space
  $outNAME =~ s/^M//g;              # new line
  $outNAME =~ s/ /_/g;              # space
  $outNAME =~ s/\,/_/g;             # bad char
  $outNAME =~ s/\;/_/g;             # bad char
  $outNAME =~ s/\(/_/g;             # bad char
  $outNAME =~ s/\)/_/g;             # bad char
#warn qq|setFILENAME2: FileName: ${outNAME}\n|;
  return($outNAME);
}
############################################################################
