package graphs;
use myDBI;

#############################################################################
sub selData
{
  my ($self,$form,$sel,$data_array,$y_values,$charttype) = @_;
#warn qq|selData: sel=$sel, y_values=$y_values, charttype=$charttype\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
if ( $form->{LOGINPROVID} == 91 )
{
  open OUT, ">>/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  print OUT qq|sel=\n$sel\n|;
  print OUT qq|y_values=$y_values\n|;
  close(OUT);
}
  my $cnt = 0;
  my $s = $dbh->prepare($sel);
  $s->execute() || myDBI->dberror("graph: selData: $sel");
  my $RecordCount = $s->rows;
#warn qq|selData: RecordCount=$RecordCount\n|;
  while ( my $r = $s->fetchrow_hashref )
  { 
    $cnt++;
#   ie: y_values=MyY1|BillAmt:MyY2|IncAmt
    foreach my $v ( split(':',$y_values) )
    {
      my ($yval,$appendvalue) = split(/\|/,$v);
#warn qq|v=$v, yval=$yval, appendvalue=$appendvalue\n|;
      my $key = $r->{'MyKey'};
      my $x = $appendvalue eq '' ? $r->{'MyX'} : $r->{'MyX'}.' '.$appendvalue;
      my $y = $r->{$yval} eq '' ? '0' : $r->{$yval};
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
#warn qq|key=$key, x=$x, y=$y\n|;
      push(@{$data_array->{$key}},$x,$y);
    }
  }
  $s->finish();
  return($cnt,$data_array);
}
sub d3_chart
{
  my ($self,$params,$dataset) = @_;
#print qq|params: are...\n|;
#foreach my $f ( keys %{$params} ) { print ": params-$f=$params->{$f}\n"; }
#  <script type="text/javascript" src="/cgi/d3lib/my.d3.js"></script>
  my $chartfunc = $params->{'function'};
  my $height = 500;
  my $width = 1000;
  if($chartfunc !~ /line_chart/){
  $height = $params->{'height'} ? $params->{'height'} : 500;
  $width = $params->{'width'} ? $params->{'width'} : 1000;
  }
  my $chartstyle = qq|STYLE="HEIGHT: ${height}; WIDTH: ${width}; $params->{'style'}"|;
  my $html = qq|

  <div id="chart1" >
    <svg ${chartstyle} ></svg>
  </div>

| . $self->$chartfunc($params,$dataset);
#  my $html = $self->$chartfunc($params,$dataset);
  return($html);
}
sub stackedbar_chart
{
  my ($self,$params,$dataset) = @_;
#$dataset = qq|
#var data = [ { key: "Male", values: [ { "x" : "MCS Enid" , "y" : 507 } , { "x" : "MCS Talihina" , "y" : 436 } , { "x" : "MCS Norman" , "y" : 346 } , { "x" : "MCS Poteau" , "y" : 343 }, ] }, { key: "Female", values: [ { "x" : "MCS Enid" , "y" : 407 } , { "x" : "MCS Talihina" , "y" : 336 } , { "x" : "MCS Norman" , "y" : 246 } , { "x" : "MCS Poteau" , "y" : 243 }, ] }, ];
#|;
  my $html = qq|

  <script>

${dataset}

  var chart;
  nv.addGraph(function() {
      chart = nv.models.multiBarChart()
           .margin({top: 40, bottom: 100, left: 70, right: 50})
           .reduceXTicks(true)    //If 'false', every single x-axis tick label will be rendered.
           .rotateLabels(45)      //Angle to rotate x-axis labels.
           .showControls(true)    //Allow user to switch between 'Grouped' and 'Stacked' mode.
           .groupSpacing(0.1)     //Distance between each group of bars.
//           .useInteractiveGuideline(true)    //tooltip display all values in group
    //.controlLabels({stacked: "Stacked"})
    //      .barColor(d3.scale.category20().range())
          .duration(300)
      ;

      chart.reduceXTicks(false).staggerLabels(true);

      chart.xAxis
          .axisLabel("$params->{'xlabel'}")
          .axisLabelDistance(35)
          .showMaxMin(false)
          //.tickFormat(d3.format('$params->{'xformat'}'))
      ;

      chart.yAxis
          .axisLabel("$params->{'ylabel'}")
          .axisLabelDistance(-5)
          .tickFormat(d3.format('$params->{'yformat'}'))
      ;
d3.select(".nv-legendWrap")
  .attr("transform", "translate(100,100)");

      d3.select('#chart1 svg')
        .append("text")
          .attr("x", 450)
          .attr("y", 10)
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .style("text-decoration", "underline")
          .text("$params->{'title'}")
        ;
      d3.select('#chart1 svg')
        .append("text")
          .attr("x", 450)
          .attr("y", 25)
          .attr("text-anchor", "middle")
          .style("font-size", "12px")
          .style("text-decoration", "underline")
          .text("$params->{'subtitle'}")
        ;
      
      chart.dispatch.on('renderEnd', function(){
          nv.log('Render Complete');
      });

      d3.select('#chart1 svg')
        .datum(data)
        .call(chart)
        ;

//    var legend2 = nv.models.legend().align(false);
//    d3.select('#chart1 svg').datum(data).call(legend2);

      nv.utils.windowResize(chart.update);

      return chart;
  });

</script>

|;
  return($html);
}
sub bar_chart
{
  my ($self,$params,$dataset) = @_;
  my $html = qq|
  <script>

${dataset}
    var cheight = $params->{'height'};
    var cwidth = $params->{'width'};

    nv.addGraph(function() {
      var chart = nv.models.discreteBarChart()
        //.x(function(d) { return d.label })
        //.y(function(d) { return d.value })
        .margin({top: 40, bottom: 200, left: 70, right: 70})
        .rotateLabels(45)      //Angle to rotate x-axis labels.
        .staggerLabels(true)
        //.staggerLabels(data[0].values.length > 8)
        .showValues(true)
        .valueFormat(d3.format('$params->{'yformat'}'))
        .duration(250)
        ;

//alert("2: h="+cheight+", w="+cwidth);
      d3.select('#chart1 svg')
        .append("text")
          .attr("x", cwidth / 2)
          .attr("y", 10)
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .style("text-decoration", "underline")
          .text("$params->{'title'}")
        ;
      d3.select('#chart1 svg')
        .append("text")
          .attr("x", cwidth / 2)
          .attr("y", 25)
          .attr("text-anchor", "middle")
          .style("font-size", "12px")
          .style("text-decoration", "underline")
          .text("$params->{'subtitle'}")
        ;

      chart.xAxis
          .axisLabel("$params->{'xlabel'}")
          .axisLabelDistance(60)
          .showMaxMin(false)
          //.tickFormat(d3.format('$params->{'xformat'}'))
      ;

      chart.yAxis
          .axisLabel("$params->{'ylabel'}")
          .axisLabelDistance(-5)
          .tickFormat(d3.format('$params->{'yformat'}'))
      ;

      d3.select('#chart1 svg')
        .datum(data)
        .call(chart)
//.style({ 'width': width, 'height': height })     // change it here?
        ;

//d3.selectAll(".nv-bar")   //Center value in bar??
//.append("text")
//.attr("x", chart.xAxis.rangeBand()/4)
//.attr("y", 40)
//.text(function (d) { return d.Value });

      nv.utils.windowResize(chart.update);
      return chart;
    });

  </script>
|;
  return($html);
}

sub line_chart
{
   my ($self,$params,$dataset) = @_;
  my $html = qq|
  <script>

  console.log('line chart')

${dataset}
       var chart;

    var randomizeFillOpacity = function() {
        var rand = Math.random(0,1);
        for (var i = 0; i < 100; i++) { // modify sine amplitude
            data[4].values[i].y = Math.sin(i/(5 + rand)) * .4 * rand - .25;
        }
        data[4].fillOpacity = rand;
        chart.update();
    };

    nv.addGraph(function() {
        chart = nv.models.lineChart()
            .options({
                duration: 300,
                useInteractiveGuideline: true,
                margin: {top: 40, bottom: 100, left: 70, right: 50}
            })
        ;
        var x__axis = [];
        var total_months = [];
        if(data[0] && data[0].values){
          for(var i = 0; i< data[0].values.length; i++){
            x__axis.push(data[0].values[i].x);
            total_months.push(i);
            data[0].values[i].x = i;
          }
        }

        // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
        chart.xAxis
            .axisLabelDistance(35)
            .axisLabel("$params->{'xlabel'}")
            .tickValues(total_months)
            .tickFormat(function(d){
                return x__axis[d]
            });

      chart.yAxis
          .axisLabel("$params->{'ylabel'}")
          .axisLabelDistance(-5)
          .tickFormat(d3.format('0.2f'))
      ;

       chart.forceY([-3,3])
      d3.select(".nv-legendWrap")
  .attr("transform", "translate(0,0)");

      d3.select('#chart1 svg')
        .append("text")
          .attr("x", 450)
          .attr("y", 10)
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .style("text-decoration", "underline")
          .text("$params->{'title'}")
        ;
      d3.select('#chart1 svg')
        .append("text")
          .attr("x", 450)
          .attr("y", 25)
          .attr("text-anchor", "middle")
          .style("font-size", "12px")
          .style("text-decoration", "underline")
          .text("$params->{'subtitle'}")
        ;
      
      chart.dispatch.on('renderEnd', function(){
          nv.log('Render Complete');
      });

        var ndata = sinAndCos(data, total_months);

        d3.select('#chart1 svg')
            .datum(ndata)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });

    function sinAndCos(data, t_months) {
        let ndata = [];
        let colors = ['#ff7f0e', '#2ca02c', '#2222ff']
        for (var i = 0; i < data.length; i++) {
          for(var j = 0; j<t_months.length; j++){
            data[i].values[j].x = j;
          }

          let obj = {
                values: data[i].values,
                key: data[i].key,
                color: colors[i]
            }
            ndata.push(obj)
        }
        return ndata;
    }

  </script>
|;
  return($html);
}

sub setKey
{
  my ($self,$r,$data) = @_;
  my $key = $r->{'MyKey'};
  my $x = $r->{'MyX'};
  my $y = $r->{'MyY'};
#warn qq|key=$key, x=$x, y=$y\n|;
  push(@{$data->{$key}},$x,$y);
  return($data);
}
sub setData
{
  my ($self,$d) = @_;
  $d = $self->setyZero($d);
  my $data = qq|
  data = 
  [
|;
  foreach my $v ( sort keys %{$d} )
  {
    $data .= qq|
    {
      key: "${v}",
      values: [
|;
    my $val = 0;
    foreach my $xy ( @{$d->{$v}} )
    {
      $val++;
#warn qq|xy=$xy\n|;
      if ( $val == 1 )
      { $data .= qq|        { x:'${xy}', |; }
      else
      { $data .= qq|y:${xy} },\n|; $val = 0; }
    }
    $data .= qq|      ]
    },
|;
  }
  $data .= qq|
  ];
|;
#warn qq|data=kls${data}kls\n|;
#if ( $form->{LOGINPROVID} == 91 )
#{
  open OUT, ">>/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  print OUT qq|data=\n${data}\n|;
  close(OUT);
#}
  return($data);
}
sub setyZero
{
  my ($self,$data) = @_;
  my $keys = ();
  my $xs = ();
  my @xvalues = ();
  foreach my $v ( sort keys %{$data} )
  {
    my ($val,$key,$x,$y) = (0,'','','');
    foreach my $xy ( @{$data->{$v}} )
    {
      $val++;
      if ( $val == 1 ) { $x = $xy; }
      else
      {
        $y = $xy;
        $key = "${v}_${x}_${y}";
        $keys->{$key}->{'key'} = $v;
        $keys->{$key}->{'x'} = $x;
        $keys->{$key}->{'y'} = $xy;
        push(@xvalues,$x);
        $key = "${v}_${x}";
        $xs->{$key} = $key; 
        $val = 0;
      }
    }
  }
#foreach my $f ( sort keys %{$keys} ) { warn "graph-setyZero: keys-$f=$keys->{$f}\n"; }
#foreach my $f ( sort keys %{$xs} ) { warn "graph-setyZero: xs-$f=$xs->{$f}\n"; }
  foreach my $v ( sort keys %{$data} )
  {
#warn qq|1. v=${v}\n|;
    foreach my $x ( @xvalues )
    {
#warn qq|2. x=${x}\n|;
      my $vxkey = "${v}_${x}";
#warn qq|3. vxkey=${vxkey}\n|;
      if ( $xs->{$vxkey} eq '' )
      { my $key = "${v}_${x}_0"; $keys->{$key}->{'key'} = $v; $keys->{$key}->{'x'} = $x; $keys->{$key}->{'y'} = 0; }
    }
  }
  my $newdata = ();
  foreach my $keyx ( sort keys %{$keys} )
  {
#foreach my $v ( sort keys %{$keys->{$keyx}} ) { warn "graph-setyZero: keys-$keyx-$v=$keys->{$keyx}->{$v}\n"; }
    my $key = $keys->{$keyx}->{'key'}; 
    my $x = $keys->{$keyx}->{'x'}; 
    my $y = $keys->{$keyx}->{'y'}; 
    push(@{$newdata->{$key}},$x,$y);
  }
  return($newdata);
}
#############################################################################
1;
