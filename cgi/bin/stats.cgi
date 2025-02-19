#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use DBA;
use myForm;
use myHTML;
use DBUtil;

############################################################################
my $form = myForm->new();

#foreach my $f ( sort keys %{$form} ) { warn "vitals.cgi: 2: form-$f=$form->{$f}\n"; }
my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
if ( $form->{LOGINPROVID} == 91 ) {
    open OUT, ">/var/www/okmis/src/debug/stats.out"
      or die "Couldn't open file: $!";
    foreach my $f ( sort keys %{$form} ) {
        print OUT "vitals.cgi: form-$f=$form->{$f}\n";
    }
    close(OUT);
}
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;
my $userdata = main->setuser( $form, $ClientID );
my $html     = myHTML->new(
    $form,
    'Millennium Client Statistics',
    'CheckPopupWindow SetD3lib',
    'STYLE="background-color: white"'
  )
  . qq|
<head>
        <title>hGraph - Health Score Graphing</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no">
        <meta name="description" content="hGraph">
        <link href="https://fonts.googleapis.com/css?family=Merriweather&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="./css/style.css">

        <script src="jquery.min.js" type="text/javascript"></script>
        <script src="d3.js" type="text/javascript"></script>
        <script src="hammer.js" type="text/javascript"></script>
        <script src="hg.js" type="text/javascript"></script>
</head>

<body>

        <section id="userinfo">

                <div id="user-info">
                        <div class="user selected">
                                <div class="image">
                                        <img src="" id="userimg">
                                </div>
                                <h1 class="name" id="username" style="font-size:40px"></h1>
                                <div class="intro" id="intro"> <span id="userage"></span>yo <span
                                                id="usergender"></span></div>
                        </div>

                </div>

        </section>
        <div id="main"></div>

        <div id="user-selection">
                <ul>
                </ul>
        </div>
        <script >
${userdata}
/* show users data on graph */
function showGraphs(userdata) 
{
  document.getElementById("main").innerHTML = ''
  var graph = new HGraph({
                container: document.getElementById("main"),
                showLabels: true,
                userdata: userdata
        });
  graph.initialize();
  $('#user-info #userimg').attr('src', './img/' + userdata.image)
  $('#user-info #username').text(userdata.name)
  $('#user-info #userage').text(userdata.age)
  $('#user-info #usergender').text(userdata.gender)
  $('#main').on('dblclick', function () 
  {
    if (graph.isZoomed)
    {
      graph.zoomOut();
    } else { graph.zoomIn(); }
  });

}
showGraphs(users[0]);

/* show users list */
function showUser(uid) {
        var foundUser = users.filter(function (item) {
                return item.id == uid
        })
        foundUser = foundUser[0]
        showGraphs(foundUser)
}

listHtml = ''
users.forEach(function (item) {

        listHtml += `
        <li onclick="showUser('${item.id}')">
                <div class="image">
                        <img src="img/${item.image}" id="userimg">
                </div>
                <h3 class="name" id="username">${item.name}</h3>
        </li>
        `
})
$('#user-selection ul').html(listHtml)
        </script>

|;
$html .= qq|
<TABLE CLASS="list fullsize" >
  <TR >
    <TD CLASS="numcol" >${CloseButton}</TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;
myDBI->cleanup();
print $html;
exit;
#############################################################################
sub setuser {
    my ( $self, $form, $ClientID ) = @_;
    my $data = '';
    return ($data);
}
