//function myClock1()
//{
//  var t = new Date();
//  var h = t.getHours();
//  var m = t.getMinutes();
//  var s = t.getSeconds();
//  var c = "AM";
//  if (h > 11) { c = "PM"; }
//  if (h < 11) { h -= 12; }
//  if (m < 10) { m = "0" + min; }
//  if (s < 10) { s = "0" + s; }
//  document.clock.time.value = h + ":" + m + ":" + s + " " + c;
//  window.setTimeout("clock()", 900);
//}
alert("in myClock");
function myClock()
{
//alert("in myClock");
//  if (!document.layers && !document.all) { return; }
  var runTime = new Date();
  var hours = runTime.getHours();
  var minutes = runTime.getMinutes();
  var seconds = runTime.getSeconds();
  var dn = "AM";
  if (hours >= 12) { dn = "PM"; hours = hours - 12; }
  if (hours == 0) { hours = 12; }
  if (minutes <= 9) { minutes = "0" + minutes; }
  if (seconds <= 9) { seconds = "0" + seconds; }
  movingtime = "<b>"+ hours + ":" + minutes + ":" + seconds + " " + dn + "</b>";
//alert("t=" + movingtime);
  if (document.layers)
  {
    document.layers.clock.document.write(movingtime);
    document.layers.clock.document.close();
  }
  else { document.getElementById("clock").innerHTML = movingtime; }
  setTimeout("myClock()", 1000)
}
