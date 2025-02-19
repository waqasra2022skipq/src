#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use myHTML;

############################################################################
my $form     = DBForm->new();
my @Sections = ();
my $Acc      = '';

# Files are: ie: Type_name...
if ( $form->{Type} eq 'INV' ) {
    @Sections = (
        {
            name  => 'Invoices',
            title => 'Invoices (generated 2nd of month)',
            dir   => 'reports4',
            sort  => 'bydate'
        }
    );
    $Acc = 'Notes2Print';
}
elsif ( $form->{Type} eq 'RPT' ) {
    @Sections = (
        {
            name  => 'scheduled',
            title => 'Provider Reports (reports from scheduled runs)',
            dir   => 'reports*',
            sort  => 'bydate'
        }
    );
    $Acc = '';
}
elsif ( $form->{Type} eq 'HIPPA' ) {
    @Sections = (
        {
            name  => '837',
            title => 'Electronic Billing Files',
            dir   => 'billing',
            sort  => 'byname'
        }
    );
    $Acc = 'Elec2Send';
}
elsif ( $form->{Type} eq 'EBT' ) {
    @Sections = (
        {
            name  => 'resp',
            title => 'Electronic Response Files',
            dir   => 'reports4',
            sort  => 'bydate'
        },
        {
            name  => 'remit',
            title => 'Electronic Remitance Files',
            dir   => 'reports4',
            sort  => 'byname'
        },
        {
            name  => 'jolts',
            title => 'Electronic JOLTS Files',
            dir   => 'reports4',
            sort  => 'bydate'
        },
        {
            name  => 'error',
            title => 'Electronic Remitance Errors',
            dir   => 'reports4',
            sort  => 'byname'
        }
    );
    $Acc = 'Notes2Print';
}
elsif ( $form->{Type} eq 'Notes' ) {
    @Sections = (
        {
            name  => 'Progress',
            title => 'Progress General Notes',
            dir   => 'reports3',
            sort  => 'bydate'
        },
        {
            name  => 'Physician',
            title => 'Physician General Notes',
            dir   => 'reports3',
            sort  => 'bydate'
        }
    );
    $Acc = 'Notes2Print';
}
elsif ( $form->{Type} eq 'HCFA' ) {
    @Sections = (
        {
            name  => 'Black',
            title => 'Black HCFA 1500 Forms',
            dir   => 'reports3',
            sort  => 'bydate'
        },
        {
            name  => 'Red',
            title => 'Red Pre-printed HCFA 1500 Forms',
            dir   => 'reports3',
            sort  => 'bydate'
        },
        {
            name  => '2nd',
            title => 'Secondary Payer HCFA 1500 Forms',
            dir   => 'reports3',
            sort  => 'bydate'
        }
    );
    $Acc = 'HCFA2Print';
}
if ( !SysAccess->verify( $form, "Privilege=${Acc}" ) ) {
    $form->error("Access Denied! (ListFiles)");
}

my $dbh = $form->dbconnect;
$xref = 'Clinics';
$s =
  $dbh->prepare("select * from Provider where Type=3 or Type=4 or ProvID=91");
$s->execute();
while ( my $r = $s->fetchrow_hashref ) { $$xref{ $r->{ProvID} } = $r; }
$xref = 'xInsurance';
$s    = $dbh->prepare("select * from xInsurance");
$s->execute();
while ( my $r = $s->fetchrow_hashref ) { $$xref{ $r->{ID} } = $r; }
$s->finish();

############################################################################
# Start out the display.
my $cnt  = 0;
my $html = myHTML->new($form) . qq|
<A NAME="top">
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="hdrcol header" >$form->{Type} files available to View</TD>
  </TR>
</TABLE>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListFiles" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
|;
$MainLinks = '';
foreach my $Section (@Sections) {
    $MainLinks .= qq|<A HREF="\#$Section->{name}" >$Section->{name}</A> |;
}
foreach my $Section (@Sections) { $html .= main->genList( $form, $Section ); }
$html .= qq|
  <TABLE CLASS="port" >
    <TR ><TD >Click on the appropriate link above to view the file.</TD></TR>
    <TR ><TD > <A HREF="#top" >top</A> </TD></TR>
  </TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>
|;
$html .= myHTML->rightpane( $form, 'search' );
$form->complete();
print $html;
exit;
############################################################################
sub genList {
    my ( $self, $form, $Section ) = @_;

    my $out = qq|<A NAME="$Section->{name}">|;

#warn qq|Section=: $Section->{name}, $Section->{title}, $Section->{dir}, $Section->{sort}\n|;
    my $Files        = main->getFiles( $form, $Section );
    my $SectionLinks = '';
    foreach my $sortkey ( sort { $b cmp $a } keys %{$Files} ) {

        #warn qq|sortkey=$sortkey\n|;
        unless ( $sortkey eq '' ) {
            my $odate =
                substr( $sortkey, 5, 2 )
              . substr( $sortkey, 8, 2 )
              . substr( $sortkey, 0, 4 );
            my $oddate =
              $sortkey eq ''
              ? ''
              : substr( $sortkey, 5, 2 ) . '&#47;'
              . substr( $sortkey, 8, 2 ) . '&#47;'
              . substr( $sortkey, 0, 4 );
            $SectionLinks .=
              qq|<A HREF="#$Section->{name}${odate}" >${oddate}</A> |;
        }
    }

# ascending: { $a <=> $b }; descending: { $b <=> $a } <=> works better for numbers: 20050321
# ascending: { $a cmp $b }; descending: { $b cmp $a } cmp works better for text: '2005-03-21'
    foreach my $sortkey ( sort { $b cmp $a } keys %{$Files} ) {
        my $odate =
          $sortkey eq ''
          ? ''
          : substr( $sortkey, 5, 2 )
          . substr( $sortkey, 8, 2 )
          . substr( $sortkey, 0, 4 );
        my $oddate =
          $sortkey eq ''
          ? ''
          : substr( $sortkey, 5, 2 ) . '&#47;'
          . substr( $sortkey, 8, 2 ) . '&#47;'
          . substr( $sortkey, 0, 4 );
        my $SectionLink =
          $odate eq '' ? '' : qq|<A NAME="$Section->{name}${odate}">|;
        $out .= qq|
${SectionLink}
<TABLE CLASS="port fullsize" >
  <TR >
    <TD >
      <TABLE CLASS="port fullsize" >
        <TR CLASS="port" >
          <TD WIDTH="5%" >&nbsp;</TD>
          <TD >${MainLinks}</TD>
          <TD WIDTH="5%" >&nbsp;</TD>
        </TR>
|;
        $out .= qq| 
        <TR CLASS="port" >
          <TD WIDTH="5%" >&nbsp;</TD>
          <TD >${SectionLinks}</TD>
          <TD WIDTH="5%" >&nbsp;</TD>
        </TR>
| if ($SectionLinks);
        $out .= qq| 
        <TR >
          <TD WIDTH="5%" >&nbsp;</TD>
          <TD >$Section->{title}</TD>
          <TD WIDTH="5%" >&nbsp;</TD>
        </TR>
|;
        $out .= qq| 
        <TR >
          <TD WIDTH="5%" >&nbsp;</TD>
          <TD >${oddate}</TD>
          <TD WIDTH="5%" >&nbsp;</TD>
        </TR>
| if ($SectionLinks);

        foreach my $rptid ( sort keys %{ $Files->{$sortkey} } ) {
            my ( $Clinic, $Ins, $Date, $Count, $Stamp, $Token ) =
              $rptid =~ m/(.*)\_(.*)\_(.*)\_(.*)\_(.*)\_(.*)$/;
            my $link  = '/' . $Files->{$sortkey}->{$rptid};
            my $Total = $Count eq 'x' ? '' : qq|[Total: ${Count}]|;
            my $name =
              $Section->{sort} eq 'bydate'
              ? qq|${Clinic} ${Ins} ${Total} (${Stamp})|
              : qq|${Clinic} ${Ins} ${Date} ${Total} (${Stamp})|;
            $cnt++;
            my $cls = int( $cnt / 2 ) == $cnt / 2 ? qq|rpteven| : qq|rptodd|;
            $out .= qq|
        <TR >
          <TD >&nbsp;</TD>
          <TD CLASS="strcol ${cls}" >
            <A HREF="javascript:ReportWindow('${link}','ListFiles')" >${name}</A>
          </TD>
          <TD >&nbsp;</TD>
        </TR>
|;
        }
        $out .= qq|
      </TABLE>
    </TD>
  </TR>
</TABLE>
|;
    }
    return ($out);
}

sub getFiles() {
    my ( $self, $form, $Section ) = @_;

    my $Dir =
      qq|$form->{DOCROOT}/$Section->{dir}/$form->{Type}_$Section->{name}_*|;

    #warn qq|Dir=$Dir\n|;
    my @TmpFiles = glob($Dir);
    my $Files    = ();
    foreach my $filepath (@TmpFiles) {
        my ( $path, $file ) = $filepath =~ /(.*\/)?(.+)/s;

        #warn qq|\nfilepath=$filepath\n|;
        #warn qq|p=$path, f=$file\n|;
        my $dir = ( split( '/', $path ) )[-1];

        #warn qq|d=$dir\n|;
        my ( $filename, $filesuffix ) = $file =~ m/(.*)\.(.*)$/;

        #warn qq|filename=$filename, filesuffix=$filesuffix\n|;
        my ( $type, $section, $clinicid, $insid, $daterange, $reccnt, $stamp,
            $token )
          = $filename =~ m/(.*)\_(.*)\_(.*)\_(.*)\_(.*)\_(.*)\_(.*)\_(.*)$/;
        my $clinicname    = $Clinics{$clinicid}{Name};
        my $providerlname = $Clinics{$clinicid}{LName};
        my $providerfname = $Clinics{$clinicid}{FName};
        my $rptforname =
            $clinicname eq ''
          ? $providerlname eq ''
              ? $provid
              : qq|${providerfname} ${providerlname}|
          : $clinicname;
        my $insurancename = $xInsurance{$insid}{Name};
        $insurancename = $insid if ( $insurancename eq '' ); # did not translate

        #warn qq|s=$section, c=$clinicid, i=$insid, d=$daterange\n|;
        my $sortkey = $Section->{sort} eq 'bydate' ? $daterange : '';
        my $rptid =
qq|${rptforname}_${insurancename}_${daterange}_${reccnt}_${stamp}_${token}|;

#warn qq|sort=$Section->{sort}, sortkey=$sortkey, rptid=$rptid, d=$daterange\n|;
        if ( $Acc eq '' ) {
            if (   $form->{LOGINPROVID} == 91
                || $form->{LOGINPROVID} == $clinicid )
            {
                $Files->{$sortkey}->{$rptid} = $dir . '/' . $file;
            }
        }
        elsif ( SysAccess->tstACL( $form, $clinicid ) ) {
            $Files->{$sortkey}->{$rptid} = $dir . '/' . $file;
        }
    }
    return ($Files);
}
#####################################################################
