package utils;
use Cwd;
use DBI;
use DBForm;
use myDBI;
use DBA;
use DBUtil;
use myConfig;
#############################################################################
our $HANDLES;
our @LINES;
our $FUNCERROR='';
our $FUNCCODE=0;
############################################################################
sub readFILE 
{
  my ($self,$filepath,$delm) = @_;
  my ($directory,$filename) = $filepath =~ m#((?:[^/]*/)*)(.*)#;
#print qq|path=${filepath}\n|;
#print qq|dir=${directory}, name=${filename}\n|;
  my $fh;
  if ( $HANDLES->{$filename}->{'HANDLE'} )
  {
    $fh = $HANDLES->{$filename}->{'HANDLE'}; 
#print qq|exists: fh=${fh}\n|;
  }
  else
  {
    if ( !open($fh, "<", "${filepath}") )
    { myDBI->dberror("readFILE: Can't open ${filename} ($!)."); }
    $HANDLES->{$filename}->{CONNECT} = 1;
    $HANDLES->{$filename}->{HANDLE} = $fh;
#print qq|open: fh=${fh}\n|;
  }
  my $line = <$fh>;
  foreach my $str ( split($delm,$line) ) { push(@LINES,$str); }
  my $text = shift @LINES;
#print qq|return: line=${line}\n|;
  return($text);
}
############################################################################
sub writesid
{
  my ($self,$form,$fileid) = @_;
  my $out = '';
#warn qq|writesid: ENTER: fileid=$fileid\n|;
  foreach $key ( sort keys %{ $form } )
  { $out .= qq|${key}\n$form->{$key}\n<EOT>\n|; }
  $form->{'sesid'} = $self->savefile($form,$out,$fileid);
#warn qq|writesid: EXIT: sesid=$form->{'sesid'}\n|;
  return($form);
}
sub readsid
{
  my ($self,$form,$skip) = @_;           # skip probably not needed, saved before everything that changed.
  my $dirname = $form->{'DOCROOT'}.'/tmp/';
  my $sesid = $form->{'sesid'};
#warn qq|readsid: ENTER: dirname=${dirname} sesid=${sesid}\n|;
  if ( !open(TMP, "<", "${dirname}${sesid}.ses") )
  { $form->dberror("readsid: Can't open ${dirname}${sesid} ($!)."); }

  my $keyflag=1;
  while ( <TMP> )
  {
    if ( $keyflag )
    { chomp($_); $key = $_; $keyflag = 0; $value = ''; }
    elsif ( $_ eq "<EOT>\n" )
    {
#warn qq|readsid: BEFORE: $key=$form->{$key}\n|;
      chomp($value);
      # if FORM value is NULL then assign what was in the template
      # if it was not NULL then it was read from GET or POST.
      # this applies mostly to radio buttons and fields in submit buttons
      $form->{$key} = $value if ( !$skip->{$key} );
      $keyflag = 1;
#warn qq|readsid: AFTER: $key=$form->{$key}\n|;
    }
    else { $value .= $_; }
  }
  close(TMP);
#warn qq|readsid: EXIT: sesid=$form->{'sesid'}\n|;
  return($form);
}
sub savefile
{
  my ($self,$form,$out,$fileid) = @_;
  my $dirname = $form->{'DOCROOT'}.'/tmp/';
#warn qq|savefile: ENTER: fileid=${fileid}\n|;
  my $sesid = $fileid eq '' ? DBUtil->Date('','stamp').'_'.DBUtil->genToken() : $fileid;
#warn qq|savefile: dirname=${dirname} sesid=${sesid}\n|;
  if ( !open(TMP, ">", "${dirname}${sesid}.ses") )
  { $form->dberror("writefile: Can't open ${dirname}${sesid} ($!)."); }
  print TMP $out;
  close(TMP);
#warn qq|savefile: EXIT: dirname=${dirname} sesid=${sesid}\n|;
  return($sesid);
}
sub test
{ 
  my ($self,$id) = @_;
  $self->copyfile('kls','kls2','-p') || print "<<<ERROR>>>: copyfile failed: ${FUNCCODE}: ${FUNCERROR}\n";;
  return(0);
}
sub syncMISEDoc
{ 
  my ($self,$id) = @_;

#warn qq|syncMISEDoc: id=${id}\n|;
  chdir(myConfig->cfg('WORKDIR'));
  my $pwd=cwd();
#warn qq|syncMISEDoc: pwd=${pwd}\n|;
  my $MAINDB = myConfig->cfg('MAINDB');
  my $form = DBForm->new("DBNAME=$MAINDB");
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cdbh = myDBI->dbconnect('okmis_config');
  my ($trash,$maindir) = split('_',$MAINDB);
  my $fromdir = myConfig->cfg('WWW').'/'.$maindir;
  my $todir = myConfig->cfg('FORMDIR');

#warn qq|syncMISEDoc: MAINDB=${MAINDB}\n|;
#warn qq|syncMISEDoc: fromdir=${fromdir}\n|;
#warn qq|syncMISEDoc: todir=${todir}\n|;
  my $sProviderEDocs=$dbh->prepare("select * from ProviderEDocs where ID=?");
  $sProviderEDocs->execute($id);
  if ( my $rProviderEDocs = $sProviderEDocs->fetchrow_hashref )
  {
    my $query = DBA->genReplace($form,$cdbh,'MISEDocs',$rProviderEDocs,"ID=${id}",'ID');
#warn qq|syncMISEDoc: query=${query}\n|;
    print qq|  sync: $rProviderEDocs->{'ID'}=$rProviderEDocs->{'Title'}:$rProviderEDocs->{'Path'}\n|;
    my $sMISEDocs = $cdbh->prepare($query);
    $sMISEDocs->execute() || $form->dberror($query);
    $sMISEDocs->finish();

    my $ProvID = $rProviderEDocs->{'ProvID'};
    my $Path = $rProviderEDocs->{'Path'};
#warn "syncMISEDoc: CHECK: Path=${Path}\n";
# ADD THIS CHECK...
    if ( $Path ne '' )
    {
      my $Tag = DBA->getxref($form,'xEDocTags',$rProviderEDocs->{Type},'Tags');
#warn "syncMISEDoc: ProvID=${ProvID}, Path=${Path}, Tags=${Tags}\n";
      my ($directory,$filename) = $Path =~ m/(.*\/)(.*)$/;
#warn "syncMISEDoc: directory=${directory}, filename=${filename}\n";
      my $fromfile = "${fromdir}${Path}";
      my $tofile = "${todir}/${ProvID}/${Tags}:${filename}";
      print qq|  copy: ${fromfile}\n|;
      print qq|    to: ${tofile}\n|;
      $self->copyfile($fromfile,$tofile,'-p') || print "<<<ERROR>>>: copyfile failed: ${FUNCCODE}: ${FUNCERROR}\n";;
    }
  }
  $sProviderEDocs->finish();
  $form->complete();
  return();
}
#############################################################################
# where: 0 = only warn of missing data/files
#        1 = warn of everything
#       99 = warn and remove missing data/files
#############################################################################
# deleted SQL record but not file
sub chkNoSQL
{
  my ($self,$form,$Del,$Dir,$SQLFile) = @_;

  my $pwd=cwd();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  print qq|\nchkNoSQL (Del=$Del): ${Dir} and ${SQLFile} (${pwd})\n|;
  my @DirFiles = glob($Dir);
  my @ExpFiles = ();
  my $cnt = 0;
  my $s=$dbh->prepare("select * from ${SQLFile} where Path=?");
  foreach $file ( @DirFiles )
  {
    $cnt++;
    print qq|${cnt}: file=${file}\n| if($cnt % 1000 == 0);
#   must put a / before filename because the html has Dir as home.
    $s->execute("/$file") || $form->dberror("select from ${SQLFile}");
    if ( $r=$s->fetchrow_hashref )
    { print "Found ${SQLFile}: $file\n" if ( $Del == 1 ); }
    elsif ( $Del == 99 )
    {
      print "File on disk: ${file}! NOT in SQL:${SQLFile}! DELETE\n"; 
      push(@ExpFiles, $file);
    }
    else
    { print "File on disk: ${file}! NOT in SQL:${SQLFile}!\n"; }
  }
  $s->finish();
  unlink(@ExpFiles) if ( $Del == 99 );
  return(1);
}
# file aborted on upload?
sub chkNoFile
{
  my ($self,$form,$Del,$Dir,$SQLFile,$selWith) = @_;

  my $pwd=cwd();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  print qq|\nchkNoFile (Del=$Del): ${Dir} and ${SQLFile} ${selWith} (${pwd})\n|;
  my $qReset = qq|update Treatment set Path='/mycfg/ENoteMissing.htm' where TrID=?|;
  my $sReset=$dbh->prepare($qReset);
  my $qDel = qq|delete from ${SQLFile} where ID=?|;
  my $sDel=$dbh->prepare($qDel);
  my $q = qq|select * from ${SQLFile} ${selWith}|;
  my $s=$dbh->prepare($q);
  $s->execute() || $form->dberror("select ERROR ${SQLFile}");
  while ( $r=$s->fetchrow_hashref )
  {
    my $file = substr($r->{Path},1,length($r->{Path}));
    my $TrID = $SQLFile eq 'Treatment' ? $r->{TrID} : '';
    if ( -f "${file}" )
    { print "File FOUND on disk: ${file} ${TrID}\n" if ( $Del == 1 ); }
    elsif ( $Del == 99 )
    { 
      print "File MISSING on disk: ${file} ";
      if ( $SQLFile eq 'Treatment' )
      {
        print "-Electronic note NO document! ${TrID}!\n    Reset Path: '/mycfg/ENoteMissing.htm'\n";
        $sReset->execute("$r->{TrID}") || $form->dberror("reset ERROR $r->{TrID},${file}");
      }
      else
      {
        print "... deleted SQL record!\n";
        $sDel->execute("$r->{ID}") || $form->dberror("delete ERROR $r->{ID},${file}");
      }
    }
    else
    { print "File MISSING! NOT on disk: ${file} ${TrID}\n"; }
  }
  $s->finish();
  $sDel->finish();
  return(1);
}
#############################################################################
sub copyfile
{
  my ($self,$fromfile,$tofile,$args) = @_;
#warn qq|copyfile: fromfile=${fromfile}= tofile=${tofile}= args=${args}=\n|;

  my ($dir,$file) = $tofile =~ m/(.*\/)(.*)$/;
  unless ( -f $fromfile ) { $FUNCCODE=-1; $FUNCERROR = "from: ${fromfile} NOT FOUND!"; return(0); }
  if ( $tofile eq '' ) { $FUNCCODE=-1; $FUNCERROR = "to: ${tofile} IS NULL!"; return(0); }
  if ( $dir ne '' )
  { unless ( -d $dir ) { $FUNCCODE=-1; $FUNCERROR = "to: ${dir} NOT FOUND!"; return(0); } }

  my $cmd = qq|cp ${args} "${fromfile}" "${tofile}"|;
#warn qq|copyfile: ${cmd}\n|;
  my $outfile = myConfig->cfg('WORKDIR').'/tmp/'.DBUtil->genToken().'_'.DBUtil->Date('','stamp') . '.sec';
  $FUNCCODE = system("${cmd} > ${outfile} 2>&1");
  $FUNCERROR = $! . DBUtil->ReadFile($outfile);
#warn qq|error: 1=$!= 2=$?= 3=$@=\n|;
#warn qq|clean: ${outfile}\n|;
  system("rm ${outfile}");      # cleanup...
  return( $FUNCCODE == 0 ? 1 : 0 );   # swap for or (||)
}
############################################################################
1;
