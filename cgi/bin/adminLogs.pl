#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use myConfig;
use myHTML;
use File::stat;
use Time::localtime;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $type = $form->{'type'};

unless ( SysAccess->chkPriv( $form, 'Agent' ) ) {
    myDBI->error("Access Denied! (List ${type} Electronic Files)");
}

my $typename =
    $type eq '837'  ? 'Billing'
  : $type eq '835'  ? 'Remittances'
  : $type eq '271'  ? 'Eligibility'
  : $type eq 'logs' ? 'AutoJobs'
  :                   'Unknown';
my $wildcard =
    $type eq '837'  ? '*.log *.out *.999 *.999.rsp'
  : $type eq '835'  ? '*.log *.out'
  : $type eq '271'  ? '*.log *.out *.xls *.999.rsp'
  : $type eq 'logs' ? '*'
  :                   'Unknown';
my $process =
    $type eq '837' ? 'pro999'
  : $type eq '271' ? 'pro999'
  :                  '';
my $directory = $type;

############################################################################
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;

my $html =
  myHTML->newHTML( $form, 'Log Panel', 'CheckPopupWindow noclock countdown_10' )
  . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="adminFiles" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
| . main->listFiles( $directory, $wildcard ) . qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>

</BODY>
</HTML>
|;

myDBI->cleanup();
print $html;
exit;
############################################################################
sub listFiles {
    my ( $self, $dir, $wildcards ) = @_;

    #warn qq|dir=${dir}\n|;
    my $ADMINDIR = myConfig->cfg('ADMINDIR');
    my ( $adminpath, $admindir ) = $ADMINDIR =~ m/(.*\/)(.*)$/;

    #warn qq|ADMINDIR=${ADMINDIR}\n|;
    #warn qq|adminpath=${adminpath}\n|;
    #warn qq|admindir=${admindir}\n|;
    my $dirpath = qq|${ADMINDIR}/${dir}|;
    my $htmpath = qq|/${admindir}/${dir}|;

    #warn qq|htmpath=${htmpath}\n|;
    my $html = '';

    foreach my $wildcard ( split( ' ', $wildcards ) ) {
        my $cnt = 0;
        $typename .= ' Response' if ( $wildcard =~ /999/ );
        $html     .= qq|
<P>
<TABLE CLASS="home" >
  <TR > <TD CLASS="hdrtxt title" COLSPAN="2" >${typename} ${wildcard} available files.</TD> </TR>
  <TR >
    <TD CLASS="hdrtxt" >file</TD>
    <TD CLASS="hdrtxt" >date/time</TD>
    <TD CLASS="hdrtxt" >download</TD>
  </TR>
|;
        foreach my $file ( main->getFiles("${ADMINDIR}/${dir}/${wildcard}") ) {
            $cnt++;
            my $filepath = qq|${dirpath}/${file}|;
            my $filedt   = ctime( stat($filepath)->mtime );
            ( my $sfx ) =
              $file =~ /\.([^.]*)$/;    # get the suffix/sfx of the filename
            my $href =
              $sfx =~ /log|txt|out/
              ? qq|javascript:ReportWindow('/cgi/bin/disHTML.cgi?IDs=${file}&page=ADMINDIR&subpage=${dir}&action=read&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','DisplayFile')|
              : $sfx =~ /999/
              ? qq|javascript:ReportWindow('/cgi/bin/disHTML.cgi?IDs=${file}&page=ADMINDIR&subpage=${dir}&process=${process}&action=read&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','DisplayFile')|
              : $sfx =~ /rsp/
              ? qq|javascript:ReportWindow('/cgi/bin/disHTML.cgi?IDs=${file}&page=ADMINDIR&subpage=${dir}&process=${process}&action=read&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','DisplayFile')|
              : $htmpath . '/' . $file;
            $html .= qq|
  <TR >
    <TD CLASS="strcol" >${file}</TD>
    <TD CLASS="strcol" >${filedt}</TD>
    <TD CLASS="hdrcol" ><A HREF="${href}" download >click here</A></TD>
  </TR>
|;
        }
        my $result =
          $cnt
          ? ''
          : qq|<TR><TD CLASS="hdrcol" COLSPAN="2" >No files to list.</TD></TR>|;
        $html .= qq|${result}
</TABLE>
<P>
|;
    }
    return ($html);
}

sub getFiles() {
    my ( $self, $Dir ) = @_;

    #warn qq|Dir=$Dir\n|;
    my @TmpFiles = glob($Dir);
    my @Files    = ();
    foreach my $filepath (@TmpFiles) {
        my ( $path, $file ) = $filepath =~ /(.*\/)?(.+)/s;

        #warn qq|\nfilepath=$filepath\n|;
        #warn qq|p=$path, f=$file\n|;
        my $dir = ( split( '/', $path ) )[-1];

        #warn qq|d=$dir\n|;
        my ( $filename, $filesuffix ) = $file =~ m/(.*)\.(.*)$/;

        #warn qq|filename=$filename, filesuffix=$filesuffix\n|;
        push( @Files, $file );
    }
    return (@Files);
}
#####################################################################
