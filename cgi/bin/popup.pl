#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBForm;
use login;
use DBA;
use myHTML;
use DBUtil;

#use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;

use CGI::Carp qw(fatalsToBrowser);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

use NPIRegistryAPI;
use UMLSAPI;
use JSON;
use SNOMEDAPI;

############################################################################
my $form = DBForm->parse();

#foreach my $f ( sort keys %{$form} ) { warn "popup: form-$f=$form->{$f}\n"; }
my $dbh       = $form->dbconnect();
my $cdbh      = $form->connectdb('okmis_config');
my $target    = $form->{'target'};
my $value     = $form->{'value'};
my $size      = $form->{multiple} > 1 ? qq|SIZE="$form->{multiple}"| : '';
my $multiple  = $form->{multiple} > 1 ? qq|MULTIPLE|                 : '';
my $SELVALUES = ();

#warn qq|popup: method=$form->{method}\n|;
#warn qq|popup: target=$form->{target} / ${target}\n|;
#warn qq|popup: value=$form->{value} / ${value}\n|;

############################################################################
my $out = '';
if ( $form->{method} eq 'pAllergy' ) {
    $target = 'ClientAllergies_AID_1';

    #warn qq|popup: pAllergy: pattern=$form->{pattern}=, value=${value}=\n|;
    ( my $pattern = $form->{'pattern'} ) =~ s/"/'/g;
    my ( $selected, $err, $FLDS, $bynum ) = ( '', '', 'Descr', 0 );
    my $items = ();
    my $found = ();
    my $dbh   = $form->connectdb('okmis_config');

    #warn qq|popup: pAllergy: pattern=${pattern}=, value=${value}=\n|;
    my $q = qq|select * from xAllergies where ID='${value}' |;
    $q .= qq| or Descr REGEXP "${pattern}" and Active=1 |
      unless ( $pattern eq '' );

    #warn qq|popup: pAllergy: q=${q}=\n|;
    my $sxAllergies = $dbh->prepare($q);
    $sxAllergies->execute() || $form->dberror($q);
    while ( my $rxAllergies = $sxAllergies->fetchrow_hashref ) {
        my ( $name, $dlm ) = ( '', '' );
        foreach my $fld ( split( ' ', $FLDS ) ) {
            $name .= $dlm . $rxAllergies->{$fld};
            $dlm = ' | ';
        }
        my $id    = $rxAllergies->{'ID'};
        my $match = PopUp->matchSelect( $value, $id );

        #warn qq|setxTable: id=$id, name=$name, match=$match\n|;
        $items->{$name}->{name}  = ${name};
        $items->{$name}->{val}   = ${id};
        $items->{$name}->{match} = ${match};
        $found->{$match}->{name} = $name if ( $match ne '' );
    }
    $sxAllergies->finish();

    # just uses items->{name} to sort
    my $unSel = PopUp->unMatched( $form, $value, $found, 'xAllergies', $FLDS );
    my $Sel   = PopUp->makeSelect( $items, $bynum );
    my $SelStmt = $unSel . $Sel;

    #warn qq|SelStmt=$SelStmt\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${SelStmt}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'xTaxonomy' ) {
    my $autocomplete = $form->{'Autocomplete'};
    my $target       = $form->{'Target'};
    my ( $err, $script, $FLDS ) = ( '', '', 'ID Spec Class Type' );
    my $dbh        = $form->connectdb('okmis_config');
    my $q          = qq|select * from xTaxonomy where Active=1 |;
    my $sxTaxonomy = $dbh->prepare($q);
    $sxTaxonomy->execute() || $form->dberror($q);

    while ( my $rxTaxonomy = $sxTaxonomy->fetchrow_hashref ) {
        my ( $name, $dlm, $row ) = ( '', '', '' );
        foreach my $fld ( split( ' ', $FLDS ) ) {
            $row .= qq|$dlm"$rxTaxonomy->{$fld}"|;
            $dlm = ',';
        }
        $script .= qq|[$row],|;
    }
    $script =~ s/\R//g;
    $script = qq|
var xTaxonomyData = [$script];
var columns = [
  {name: 'ID', width: '5.5em'},
  {name: 'Spec', width: '15em'},
  {name: 'Class', width: '15em'},
  {name: 'Type', minWidth: '15em'}
];
// Sets up the multicolumn autocomplete widget.
\$("#$autocomplete").mcautocomplete({
    // These next two options are what this plugin adds to the autocomplete widget.
    showHeader: true,

    columns: columns,
 		source: xTaxonomyData,

    // Event handler for when a list item is selected.
    select: 
      function (event, ui) {
        this.value = (ui.item ? (ui.item[0] + ' \| ' + ui.item[1] + ' \| ' + ui.item[2] + ' \| ' + ui.item[3]): '');
        if (document.getElementsByName('$target').length > 0) {
          document.getElementsByName('$target')[0].value = ui.item[0];
        } 
        return false;
      },

    change:
      function (event, ui) {
        if (this.value === "") {
          document.getElementsByName('$target')[0].value = '';
        }
      },

    minLength: 1
});
|;
    $out = $err eq ''
      ? qq|
  <command method="setscript">
    <target>Run this script</target>
    <content><![CDATA[${script}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'xOccupationSnomed' ) {
    my $autocomplete = $form->{'Autocomplete'};
    my $target       = $form->{'Target'};
    my ( $err, $script, $FLDS ) =
      ( '', '', 'Code Description CodeSystem CodeSystemVers CodeSystemOID' );
    my $dbh = $form->connectdb('okmis_config');
    my $q   = qq|select * from xOccupationSnomed where Active=1 |;
    my $sxOccupationSnomed = $dbh->prepare($q);
    $sxOccupationSnomed->execute() || $form->dberror($q);

    while ( my $rxOccupationSnomed = $sxOccupationSnomed->fetchrow_hashref ) {
        my ( $name, $dlm, $row ) = ( '', '', '' );
        foreach my $fld ( split( ' ', $FLDS ) ) {
            $row .= qq|$dlm"$rxOccupationSnomed->{$fld}"|;
            $dlm = ',';
        }
        $script .= qq|[$row],|;
    }
    $script =~ s/\R//g;
    $script = qq|
var xOccupationSnomedData = [$script];
var columns = [
  {name: 'Code', width: '5.5em'},
  {name: 'Descriptor', width: '15em'},
  {name: 'CodeSystem', width: '10em'},
  {name: 'Version', minWidth: '10em'},
  {name: 'CodeSystemOID', width: '10em'},
];
// Sets up the multicolumn autocomplete widget.
\$("#$autocomplete").mcautocomplete({
    // These next two options are what this plugin adds to the autocomplete widget.
    showHeader: true,

    columns: columns,
 		source: xOccupationSnomedData,

    // Event handler for when a list item is selected.
    select: 
      function (event, ui) {
        this.value = (ui.item ? ui.item[1]: '');
        document.getElementsByName('$target')[0].value = ui.item[0];
        return false;
      },

    change:
      function (event, ui) {
        if (ui.item === null) {
          document.getElementsByName('$target')[0].value = this.value;
        }
      },

    minLength: 1
});
|;
    $out = $err eq ''
      ? qq|
  <command method="setscript">
    <target>Run this script</target>
    <content><![CDATA[${script}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'xRelationship' ) {
    my $autocomplete = $form->{'Autocomplete'};
    my $target       = $form->{'Target'};
    my ( $err, $script, $FLDS ) =
      ( '', '', 'Descr ID SNOMEDID HL7OID HL7code' );
    my $dbh            = $form->connectdb('okmis_config');
    my $q              = qq|select * from xRelationship where Active=1 |;
    my $sxRelationship = $dbh->prepare($q);
    $sxRelationship->execute() || $form->dberror($q);

    while ( my $rxRelationship = $sxRelationship->fetchrow_hashref ) {
        my ( $name, $dlm, $row ) = ( '', '', '' );
        foreach my $fld ( split( ' ', $FLDS ) ) {
            $row .= qq|$dlm"$rxRelationship->{$fld}"|;
            $dlm = ',';
        }
        $script .= qq|[$row],|;
    }
    $script =~ s/\R//g;
    $script = qq|
var xRelationshipData = [$script];
var xRelationshipDataDict = {};
var columns = [
  {name: 'Descr', width: '15em'}
];
function split( val ) {
  return val.split( /,/ );
}
function extractLast( term ) {
  return split( term ).pop();
}
// Sets up the multicolumn autocomplete widget.
\$("#$autocomplete").mcautocomplete({
    // These next two options are what this plugin adds to the autocomplete widget.
    showHeader: false,

    columns: columns,
    source: function( request, response ) {
      // delegate back to autocomplete, but extract the last term
      response( \$.ui.autocomplete.filter(
        xRelationshipData, extractLast( request.term ) ) );
    },

    // Event handler for when a list item is selected.
    select: 
      function (event, ui) {
        var terms = split( this.value );
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push( ui.item ? (ui.item[0]): '' );
        // add placeholder to get the comma-and-space at the end
        terms.push( "" );
        this.value = terms.join( "," );

        var codes = document.getElementsByName('$target')[0].value;
        var codesarr = split( codes );
        if (codes === "")
          codesarr.shift();
        codesarr.push(ui.item[1]);
        document.getElementsByName('$target')[0].value = codesarr.join(",");

        if (ui.item) { xRelationshipDataDict[ui.item[0]] = ui.item[1]; }

        return false;
      },

    change:
      function (event, ui) {
        if (this.value === "") {
          document.getElementsByName('$target')[0].value = '';
        } else {
          var terms = split(this.value);
          var codes = [], descrs = [];
          terms.forEach(function (item, index) {
            if (item.length > 0 && xRelationshipDataDict.hasOwnProperty(item)) {
              codes.push(xRelationshipDataDict[item]);
              descrs.push(item);
            }
          });
          this.value = descrs.join(",");
          document.getElementsByName('$target')[0].value = codes.join(",");
        }
      },

    focus:
      function (event, ui) {
        return false;
      },

    minLength: 1
});
|;
    $out = $err eq ''
      ? qq|
  <command method="setscript">
    <target>Run this script</target>
    <content><![CDATA[${script}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'umlsProblem' ) {
    my $target  = 'ICD10Search';
    my $pattern = $form->{'pattern'} || '';
    $pattern =~ s/"/'/g;

    my $FINDING  = $form->{'FINDING'};
    my $DISORDER = $form->{'DISORDER'};
    my $NURING   = $form->{'NURING'};

    my $results =
      SNOMEDAPI::fetchSNOMED( $pattern, $DISORDER, $FINDING, $NURING );

    my $items = {};
    my $found = {};
    my $value = $form->{'value'} || '';

    foreach my $item (@$results) {
        my $name =
          "SOURCE: $item->{rootSource}, CODE: $item->{ui}, NAME: $item->{name}";

        my $ID    = $item->{ui};
        my $match = PopUp->matchSelect( $value, $ID );

        $items->{$name}->{name}  = $name;
        $items->{$name}->{val}   = $ID;
        $items->{$name}->{match} = $match;
        $found->{$match}->{name} = $name if $match ne '';
    }

    my $unSel =
      PopUp->unMatched( $form, $value, $found, 'umlsICD10',
        'sctName referencedComponentId icdName mapTarget Type' );
    my $Sel     = PopUp->makeSelect( $items, 0 );
    my $SelStmt = $unSel . $Sel;

    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${SelStmt}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}

elsif ( $form->{method} eq 'sProblem' ) {
    my $target = 'ICD10Search';

    #my $pattern = $form->{'pattern'};
    # pattern is what user enter to check/find.
    ( my $userEntered = $form->{'pattern'} ) =~ s/"/'/g;

    #warn qq|popup: sProblem: pattern=${pattern}=, value=${value}=\n|;
    my $FINDING  = $form->{'FINDING'};
    my $CORE     = $form->{'CORE'};
    my $DISORDER = $form->{'DISORDER'};

    my $check     = qq|"%a%"|;
    my $coreCheck = "";

    if ( $FINDING eq 'true' ) {
        $check = qq|"%(finding)%"|;
    }
    if ( $DISORDER eq 'true' ) {
        $check = qq|"%(disorder)%"|;
    }
    if ( $CORE eq 'true' ) {
        $coreCheck = qq|and Type LIKE "%core%"|;
    }

#warn qq|: userEntered=$userEntered,value=$value, FINDING=${FINDING}, DISORDER=${DISORDER}\n|;
    my ( $selected, $err, $FLDS, $bynum ) =
      ( '', '', 'sctName SNOMEDID icdName ICD10 Type', 0 );
    my $items = ();
    my $found = ();
    my $dbh   = $form->connectdb('okmis_config');
    my $with =
        $value eq '' && $userEntered eq '' ? ''
      : $userEntered eq ''                 ? qq|and ID="${value}"|
      : $value eq ''
      ? qq| and ((ICD10 LIKE "%${userEntered}%" or SNOMEDID LIKE "%${userEntered}%") and (sctName LIKE ${check} or icdName LIKE ${check}) ${coreCheck}) |
      : qq| and (ID="${value}" or ((ICD10 LIKE "%${userEntered}%" or SNOMEDID LIKE "%${userEntered}%") and (sctName LIKE ${check} or icdName LIKE ${check}) ${coreCheck}) )|;

    my $q =
      qq|select * from misICD10 where Active=1 ${with} group by SNOMEDID,ICD10|;

    #warn qq|: q=$q\n|;
    my $smisICD10 = $dbh->prepare($q);
    $smisICD10->execute() || $form->dberror($q);
    while ( my $rmisICD10 = $smisICD10->fetchrow_hashref ) {
        my ( $name, $dlm ) = ( '', '' );
        foreach my $fld ( split( ' ', $FLDS ) ) {
            $name .= $dlm . $rmisICD10->{$fld};
            $dlm = ' ; ';
        }
        my $ID    = $rmisICD10->{'ID'};
        my $match = PopUp->matchSelect( $value, $ID );

        #warn qq|setxTable: ID=$ID, name=$name, match=$match\n|;
        $items->{$name}->{name}  = ${name};
        $items->{$name}->{val}   = ${ID};
        $items->{$name}->{match} = ${match};
        $found->{$match}->{name} = $name if ( $match ne '' );
    }
    $smisICD10->finish();

    # just uses items->{name} to sort
    my $unSel = PopUp->unMatched( $form, $value, $found, 'misICD10',
        'sctName SNOMEDID icdName ICD10 Type' );
    my $Sel     = PopUp->makeSelect( $items, $bynum );
    my $SelStmt = $unSel . $Sel;

    #warn qq|SelStmt=$SelStmt\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${SelStmt}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'pProblem' ) {
    my $target = 'ICD10Check';
    my ( $err, $cnt ) = ( '', 0 );
    my $dbh = $form->connectdb('okmis_config');
    my $s   = $dbh->prepare(
"select sctName,referencedComponentId,icdName,mapTarget from umlsICD10 where Active=1 AND (referencedComponentId=? OR mapTarget=?)"
    );
    $s->execute( $value, $value )
      || $form->dberror("pProblem: select umlsICD10 ${value}");
    my ( $sctName, $SNOMEDID, $icdName, $ICD10 ) = $s->fetchrow_array;
    my $html = qq|${sctName}: ${SNOMEDID}: ${icdName} ${ICD10}<BR><BR>|;
    my $q =
      qq|select * from umlsICD10 where Active=1 and referencedComponentId=?|;

    #warn qq|pProblem: q=$q\n|;
    my $smisICD10 = $dbh->prepare($q);
    $smisICD10->execute($SNOMEDID) || $form->dberror($q);
    while ( my $rmisICD10 = $smisICD10->fetchrow_hashref ) {
        $cnt++;
        my $descr   = qq|$rmisICD10->{'mapRule'} $rmisICD10->{'mapAdvice'}|;
        my $ID      = $rmisICD10->{'ID'};
        my $match   = PopUp->matchSelect( $value, $ID );
        my $checked = $match eq '' ? '' : 'CHECKED';

        #warn qq|pProblem: ID=$ID, descr=$descr, match=$match\n|;
        $html .=
qq|  <INPUT TYPE="radio" NAME="$form->{'name'}" VALUE="${ID}" ${checked} > ${descr}<BR><BR>\n|;
    }
    $smisICD10->finish();
    if   ( $cnt > 1 ) { $html .= qq|Check one problem above.|; }
    else              { $html .= qq|Only one problem found.|; }

    #warn qq|pProblem: html=$html\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${html}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientProblems' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $id       = $form->{'id'};
    my $addWHERE =
      $form->{'active'} == 1 ? "and ClientProblems.ResolvedDate is null" : '';
    my $Locked = $form->{'Locked'};
    my $LINKID = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    if ($id) {
        my $dbh = $form->dbconnect();
        my $sUpdate =
          $dbh->prepare("update ClientProblems set Priority=? where ID=?");
        $sUpdate->execute( $value, $id )
          || $form->dberror("popup: update ClientProblems (Priority=${value})");
        $sUpdate->finish();
        PostUpd->renumClientProblems( $form, $ClientID );
    }
    my $list = myHTML->ListSel( $form, 'ListClientProblems', $ClientID, $LINKID,
        $Locked, '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientNoteProblems' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $TrID     = $form->{'Treatment_TrID'};
    my $id       = $form->{'id'};
    my $ContDate = $form->{'d'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: TrID=$form->{Treatment_TrID}\n|;
    #warn qq|popup: id=$form->{id}\n|;
    my $Locked = $form->{'Locked'};
    my $list   = gHTML->setClientNoteProblems( $form, $Locked, $ClientID, $TrID,
        $ContDate );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientTrPlanS' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $TrPlanID = $form->{'ClientTrPlan_ID'};
    my $row      = $form->{'row'};
    $target .= $row;

#warn qq|popup: ListClientTrPlanS: ClientID=${ClientID}/$form->{Client_ClientID}\n|;
#warn qq|popup: ListClientTrPlanS: TrPlanID=${TrPlanID}/$form->{ClientTrPlan_ID}\n|;
#warn qq|popup: ListClientTrPlanS: row=${row}/$form->{row}\n|;
#warn qq|popup: ListClientTrPlanS: value=${value}/$form->{value}\n|;
    my $dbh = $form->dbconnect();
    if ( $value eq 'delete' ) {

#warn qq|popup: ListClientTrPlanS: DELETE=${value}/$form->{value}, ID=$form->{'sid'}\n|;
        my $sDelete = $dbh->prepare("delete from ClientTrPlanS where ID=?");
        $sDelete->execute( $form->{'sid'} )
          || $form->dberror("popup: delete ClientTrPlanS ($form->{sid})");
        $sDelete->finish();
    }

    #warn qq|popup: ListClientTrPlanS: SignTrPlan: TrPlanID=${TrPlanID}\n|;
    DBA->SignTrPlan( $form, $TrPlanID ) if ( $value eq 'yes' );

    #warn qq|popup: ListClientTrPlanS: lockTrPlan: TrPlanID=${TrPlanID}\n|;
    DBA->lockTrPlan( $form, $TrPlanID );
    my $Locked = $form->{'Locked'};    # Pass in Locked if NEEDED?

    #warn qq|popup: ListClientTrPlanS: ListTrPlan: TrPlanID=${TrPlanID}\n|;
    my $list = myHTML->ListSel( $form, 'ListClientTrPlanS', $TrPlanID,
        $form->{'LINKID'}, $Locked, $row );

    #warn qq|popup: ListClientTrPlanS: html=\n${html}\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );

    #warn qq|popup: ListClientTrPlanS: out=\n${out}\n|;
}
elsif ( $form->{method} eq 'ListClientTrPlanPG' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $TrPlanID = $form->{'ClientTrPlan_ID'};
    my $id       = $form->{'id'};
    my $row      = $form->{'row'};
    $target .= $row;

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}\n|;
    #warn qq|popup: row=${row}, target=${target}\n|;
    my $dbh = $form->dbconnect();
    my $sUpdate =
      $dbh->prepare("update ClientTrPlanPG set Priority=? where ID=?");
    $sUpdate->execute( $value, $id )
      || $form->dberror("popup: update ClientTrPlanPG (Priority=${value})");
    $sUpdate->finish();
    PostUpd->renumClientTrPlanPG( $form, $TrPlanID );
    my $Locked = $form->{'Locked'};
    my $list   = myHTML->ListSel( $form, 'ListClientTrPlanPG', $TrPlanID,
        $form->{'LINKID'}, $Locked, $row );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientTrPlanOBJ' ) {
    my $ClientID   = $form->{'Client_ClientID'};
    my $TrPlanPGID = $form->{'ClientTrPlanPG_ID'};
    my $id         = $form->{'id'};
    my $row        = $form->{'row'};
    $target .= $row;

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}\n|;
    #warn qq|popup: row=${row}, target=${target}\n|;
    my $dbh = $form->dbconnect();
    my $sUpdate =
      $dbh->prepare("update ClientTrPlanOBJ set Priority=? where ID=?");
    $sUpdate->execute( $value, $id )
      || $form->dberror("popup: update ClientTrPlanOBJ (Priority=${value})");
    $sUpdate->finish();
    PostUpd->renumClientTrPlanOBJ( $form, $TrPlanPGID );
    my $Locked = $form->{'Locked'};
    my $list   = myHTML->ListSel( $form, 'ListClientTrPlanOBJ', $TrPlanPGID,
        $form->{'LINKID'}, $Locked, $row );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientFamilyProblems' ) {
    my $ClientID       = $form->{'Client_ClientID'};
    my $ClientFamilyID = $form->{'ClientFamily_ID'};
    my $id             = $form->{'id'};
    my $addWHERE =
      $form->{'active'} == 1
      ? "and ClientFamilyProblems.ResolvedDate is null"
      : '';
    my $Locked = $form->{'Locked'};
    my $LINKID = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    if ($id) {
        my $dbh     = $form->dbconnect();
        my $sUpdate = $dbh->prepare(
            "update ClientFamilyProblems set Priority=? where ID=?");
        $sUpdate->execute( $value, $id )
          || $form->dberror(
            "popup: update ClientFamilyProblems (Priority=${value})");
        $sUpdate->finish();
        PostUpd->renumClientFamilyProblems( $form, $ClientFamilyID );
    }
    my $list =
      myHTML->ListSel( $form, 'ListClientFamilyProblems', $ClientFamilyID,
        $LINKID, $Locked, '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientPDMeds' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $id       = $form->{'id'};
    my $addWHERE = $form->{'active'} == 1 ? "and PDMed.MedActive=1" : '';
    my $Locked   = $form->{'Locked'};
    my $LINKID   = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    my $list =
      myHTML->ListSel( $form, 'ListClientPDMeds', $ClientID, $LINKID, $Locked,
        '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ShowClientMeds' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $id       = $form->{'id'};
    my $addWHERE = $form->{'active'} == 1 ? "and ClientMeds.Active=1" : '';
    my $Locked   = $form->{'Locked'};
    my $LINKID   = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    my $list =
      myHTML->ListSel( $form, 'ShowClientMeds', $ClientID, $LINKID, $Locked,
        '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientAdMeds' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $id       = $form->{'id'};
    my $addWHERE = $form->{'active'} == 1 ? "and ClientAdMeds.Active=1" : '';
    my $Locked   = $form->{'Locked'};
    my $LINKID   = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    my $list =
      myHTML->ListSel( $form, 'ListClientAdMeds', $ClientID, $LINKID, $Locked,
        '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListClientAllergies' ) {
    my $ClientID = $form->{'Client_ClientID'};
    my $id       = $form->{'id'};
    my $addWHERE =
      $form->{'active'} == 1 ? "and ClientAllergies.EndDate is null" : '';
    my $Locked = $form->{'Locked'};
    my $LINKID = $form->{'LINKID'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: addWHERE=${addWHERE}\n|;
    my $list =
      myHTML->ListSel( $form, 'ListClientAllergies', $ClientID, $LINKID,
        $Locked, '', $addWHERE );

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListProviderClients' ) {
    my $id = $form->{'id'};

    #warn qq|popup: ClientID=$form->{Client_ClientID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    my $list = myHTML->set1CheckBoxColumn(
        $form,
        "select * from Client where ProvID='$id' order by LName,FName",
        'ClientIDs',
        'ClientID',
        'LName~Last Name~strcol:FName~First Name~strcol:DOB~~hdrcol',
        'Select Clients'
    );
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Medications' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $For     = qq| like "%${pattern}%" |;
    my @Display = ( 'ID', ',', 'TradeName' );
    my $opts =
      main->selmatch( $form, $cdbh, "select * from xMedNames where ID=?",
        $value, 'ID', @Display );
    $opts .=
      main->seloptions( $form, $cdbh,
        "select * from xMedNames where TradeName ${For} order by TradeName",
        $pattern, 'ID', @Display );
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'NPI' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $For = qq| like "%${pattern}%" |;
    @Display = (
        'Type', ':', 'ProvOrgName', ',', 'Addr1', ',',
        'City', ',', 'ST',          ',', 'Zip',   '[',
        'NPI',  ']'
    );
    my $opts = main->selmatch( $form, $cdbh, "select * from xNPI where NPI=?",
        $value, 'NPI', @Display );
    my $q =
      $pattern eq '*'
      ? qq|select * from xNPI order by Type desc,ProvOrgName|
      : qq|select * from xNPI where (NPI ${For} or ProvOrgName ${For} or Zip ${For}) order by Type desc,ProvOrgName|;
    $opts .= main->seloptions( $form, $cdbh, $q, $pattern, 'NPI', @Display );
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Agency' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $types = $form->{'types'};

#   my $For = qq| like "%${pattern}%" |;
#   @Display = ('Type',':','ProvOrgName',',','Addr1',',','City',',','ST',',','Zip','[','NPI',']');
#   my $opts = main->selmatch($form,$cdbh,"select * from xNPI where NPI=?",$value,'NPI',@Display);
#   my $q = $pattern eq '*'
#         ? qq|select * from xNPI where EntityTypeCode>1 order by Type desc,ProvOrgName|
#         : qq|select * from xNPI where EntityTypeCode>1 and (NPI ${For} or ProvOrgName ${For} or Zip ${For}) order by Type desc,ProvOrgName|;
# #warn qq|Agency: q=${q}\n|;
#   $opts .= main->seloptions($form,$cdbh,$q,$pattern,'NPI',@Display);
# #warn qq|Agency: opts=${opts}\n|;

    if ( $pattern eq "" ) {
        $pattern = $value;
    }
    $json_str = NPIRegistryAPI->search_api_npi( $pattern, $types );
    my $api_data = decode_json($json_str);    # Decode the JSON response

    # Handle API error
    if ( ref $api_data eq 'ARRAY' && exists $api_data->[0]->{error} ) {
        print STDERR "API Error: " . $api_data->[0]->{error} . "\n";
        return main->ierr( $target, "API Error: " . $api_data->[0]->{error} );
    }

    # Extract data from JSON response
    my $results = $api_data->[3];    # The actual data array from search_api_npi

    my $opts = '<OPTION VALUE="">unselected';    # Default empty option

    foreach my $row (@$results) {
        my ( $type, $name, $address, $city, $state, $zip, $npi ) = @$row;
        my $display_name = "$type, $name, $address, $city, $state [$npi]";
        if ( $npi eq $value ) {
            $opts .= qq|<OPTION VALUE="$npi" SELECTED>$display_name</OPTION>\n|;
        }
        else {
            $opts .= qq|<OPTION VALUE="$npi">$display_name</OPTION>\n|;

        }
    }

    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Physicians' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $types = $form->{'types'};

    if ( $pattern eq "" ) {
        $pattern = $value;
    }
    $json_str = NPIRegistryAPI->search_api_npi( $pattern, $types );
    my $api_data = decode_json($json_str);    # Decode the JSON response

    # Handle API error
    if ( ref $api_data eq 'ARRAY' && exists $api_data->[0]->{error} ) {
        print STDERR "API Error: " . $api_data->[0]->{error} . "\n";
        return main->ierr( $target, "API Error: " . $api_data->[0]->{error} );
    }

    # Extract data from JSON response
    my $results = $api_data->[3];    # The actual data array from search_api_npi

    my $opts = '<OPTION VALUE="">unselected';    # Default empty option

    foreach my $row (@$results) {
        my ( $type, $name, $address, $city, $state, $zip, $npi ) = @$row;
        my $display_name = "$type, $name, $address, $city, $state [$npi]";
        if ( $npi eq $value ) {
            $opts .= qq|<OPTION VALUE="$npi" SELECTED>$display_name</OPTION>\n|;
        }
        else {
            $opts .= qq|<OPTION VALUE="$npi">$display_name</OPTION>\n|;

        }
    }
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Pharmacy' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;

    my $types = $form->{'types'};

# my $For = qq| like "%${pattern}%" |;
# @Display = ('Type',':','ProvOrgName',',','Addr1',',','City',',','ST',',','Zip','[','NPI',']');
# my $opts = main->selmatch($form,$cdbh,"select * from xNPI where NPI=?",$value,'NPI',@Display);
# my $q = $pattern eq '*'
#       ? qq|select * from xNPI where EntityTypeCode>1 and (Taxonomy='3336C0003X' or Taxonomy='333600000X' or Taxonomy='332B00000X') order by Type desc,ProvOrgName|
#       : qq|select * from xNPI where EntityTypeCode>1 and (Taxonomy='3336C0003X' or Taxonomy='333600000X' or Taxonomy='332B00000X') and (NPI ${For} or ProvOrgName ${For} or Zip ${For}) order by Type desc,ProvOrgName|;
# $opts .= main->seloptions($form,$cdbh,$q,$pattern,'NPI',@Display);

    if ( $pattern eq "" ) {
        $pattern = $value;
    }
    $json_str = NPIRegistryAPI->search_api_npi( $pattern, $types );
    my $api_data = decode_json($json_str);    # Decode the JSON response

    # Handle API error
    if ( ref $api_data eq 'ARRAY' && exists $api_data->[0]->{error} ) {
        print STDERR "API Error: " . $api_data->[0]->{error} . "\n";
        return main->ierr( $target, "API Error: " . $api_data->[0]->{error} );
    }

    # Extract data from JSON response
    my $results = $api_data->[3];    # The actual data array from search_api_npi

    my $opts = '<OPTION VALUE="">unselected';    # Default empty option

    foreach my $row (@$results) {
        my ( $type, $name, $address, $city, $state, $zip, $npi ) = @$row;
        my $display_name = "$type, $name, $address, $city, $state [$npi]";
        if ( $npi eq $value ) {
            $opts .= qq|<OPTION VALUE="$npi" SELECTED>$display_name</OPTION>\n|;
        }
        else {
            $opts .= qq|<OPTION VALUE="$npi">$display_name</OPTION>\n|;

        }
    }

    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Axis1' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $For = qq| like "%${pattern}%" |;
    @Display = ( 'ICD9', ':', 'Descr' );
    my $opts = main->selmatch( $form, $cdbh, "select * from xAxis1 where ID=?",
        $value, 'ID', @Display );
    my $q =
qq|select * from xAxis1 where Active=1 and (ICD9 ${For} or Descr ${For}) order by ICD9,Descr|;
    $opts .= main->seloptions( $form, $cdbh, $q, $pattern, 'ID', @Display );
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'FunctionalStatus' ) {
    my $Handicap = $form->{'Handicap'};

    #warn qq|Handicap=$Handicap\n|;
    @Display = ('ConceptName');
    my $opts =
      main->selmatch( $form, $cdbh,
        "select * from xFunctionalStatus where ID=?",
        $value, 'ID', @Display );
    my $q =
qq|select * from xFunctionalStatus where Active=1 and Handicap='${Handicap}' order by ConceptName|;
    $opts .= main->seloptions( $form, $cdbh, $q, $Handicap, 'ID', @Display );
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;

    #warn qq|list=$list\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListProviderCDAparms' ) {
    my $ProvID = $form->{'Provider_ProvID'};
    my $id     = $form->{'id'};
    my $Locked = $form->{'Locked'};
    my $LINKID = $form->{'LINKID'};

    #warn qq|popup: ProvID=$form->{Provider_ProvID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    if ($id) {
        my $dbh = $form->dbconnect();
        my $sUpdate =
          $dbh->prepare("update ProviderCDAparms set Priority=? where ID=?");
        $sUpdate->execute( $value, $id )
          || $form->dberror(
            "popup: update ProviderCDAparms (Priority=${value})");
        $sUpdate->finish();
        PostUpd->renumProviderCDAparms( $form, $ProvID );
    }
    my $list = myHTML->ListSel( $form, 'ListProviderCDAparms', $ProvID, $LINKID,
        $Locked );
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'ListProviderCDAparmsT' ) {
    my $ProvID = $form->{'Provider_ProvID'};
    my $id     = $form->{'id'};
    my $Locked = $form->{'Locked'};
    my $LINKID = $form->{'LINKID'};

    #warn qq|popup: ProvID=$form->{Provider_ProvID}\n|;
    #warn qq|popup: id=$form->{id}/${id}\n|;
    #warn qq|popup: value=${value}\n|;
    if ($id) {
        my $dbh = $form->dbconnect();
        my $sUpdate =
          $dbh->prepare("update ProviderCDAparms set Visible=? where ID=?");
        my $toggle = $value eq 'off' ? 0 : 1;
        $sUpdate->execute( $toggle, $id )
          || $form->dberror(
            "popup: update ProviderCDAparms (Visible=${value}/${toggle})");
        $sUpdate->finish();
    }
    my $list = myHTML->ListSel( $form, 'ListProviderCDAparms', $ProvID, $LINKID,
        $Locked );
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
elsif ( $form->{method} eq 'Procedure' ) {
    ( my $pattern = $form->{'pattern'} ) =~ s/"//g;
    my $For = qq| like "%${pattern}%" |;
    @Display = ( 'ConceptName', '[', 'ConceptCode', ']' );
    my $opts =
      main->selmatch( $form, $cdbh,
        "select * from xProcedures where ConceptCode=?",
        $value, 'ConceptCode', @Display );
    my $q =
      $pattern eq '*'
      ? qq|select * from xProcedures order by ConceptName|
      : qq|select * from xProcedures where (ConceptName ${For} or ConceptCode ${For}) order by ConceptName|;
    $opts .=
      main->seloptions( $form, $cdbh, $q, $pattern, 'ConceptCode', @Display );
    my $list =
qq|<SELECT NAME="$form->{'name'}" ${size} ${multiple} >\n${opts}</SELECT>\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${list}]]></content>
  </command>
|
      : main->ierr( $target, $err );
}
############################################################################
#warn qq|out=$out\n|;
my $xml = qq|<response>\n${out}</response>|;

#warn qq|popup: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;
$cdbh->disconnect();
$form->complete();
exit;

############################################################################
sub ierr {
    my ( $self, $target, $err ) = @_;

    #warn qq|ierr: target=$target\n|;
    my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
    return ($out);
}

sub selmatch {
    my ( $self, $form, $dbh, $sql, $value, $ID, @Text ) = @_;

    #foreach my $id ( @Text ) { warn qq|selmatch: Textid=${id}\n|; }
    #warn qq|selmatch: sql=$sql\n|;
    return ('<OPTION SELECTED VALUE="">unselected') if ( $value eq '' );
    my $out = qq|<OPTION VALUE="">unselected\n|;
    my $s   = $dbh->prepare($sql);
    foreach my $id ( split( chr(253), $value ) ) {

        #warn qq|selmatch: id=$id\n|;
        $s->execute($id) || $form->dberror($sql);
        if ( my $r = $s->fetchrow_hashref ) {

            #foreach my $f ( sort keys %{$r} ) { warn ": r-$f=$r->{$f}\n"; }
            $SELVALUES->{ $r->{$ID} } = 1;    # globally marked.
            $out .= qq|<OPTION SELECTED VALUE="$r->{$ID}">|;
            $out .= main->seltext( $r, @Text );
            $out .= "\n";
        }
    }
    $s->finish();
    return ($out);
}

sub seloptions {
    my ( $self, $form, $dbh, $sql, $str, $ID, @Text ) = @_;
    return () if ( $str eq '' );
    my $out = '';

    #warn qq|seloptions: sql=$sql\n|;
    my $s = $dbh->prepare($sql);
    $s->execute() || $form->dberror($sql);
    while ( my $r = $s->fetchrow_hashref ) {

        #warn qq|seloptions: ID=$r->{$ID}= \n|;
        next if ( $SELVALUES->{ $r->{$ID} } );    # globally marked.
        $out .= qq|<OPTION VALUE="$r->{$ID}">|;
        $out .= main->seltext( $r, @Text );
    }
    $s->finish();
    return ($out);
}

sub seltext {
    my ( $self, $r, @Text ) = @_;
    my $out = '';

# not sure what $last is for? but if first $r val is null then rest of $out is null
    my $last = 'notonfirst';
    foreach my $fld (@Text) {

        #warn qq|last=${last}\nfld=${fld}=$r->{$fld}= \n|;
        if    ( $fld eq ':' ) { $out .= qq|${fld} |; }
        elsif ( $fld eq '[' ) { $out .= qq| ${fld}|; }
        elsif ( $fld eq ']' ) { $out .= qq|${fld}|; }
        elsif ( $last eq '' ) { null; }
        elsif ( $fld eq ';' ) { $out .= qq|${fld} |; }
        elsif ( $fld eq ',' ) { $out .= qq|${fld} |; }
        else                  { $out .= $r->{$fld}; $last = $r->{$fld}; }

        #warn qq|last=${last}\nout=${out}= \n|;
    }
    $out .= "\n";

    #warn qq|done: out=${out}= \n|;
    return ($out);
}
############################################################################
