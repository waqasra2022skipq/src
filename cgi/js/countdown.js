var CountDownTargetDate = new Date();
var CountDownBackColor = "palegreen";
var CountDownForeColor = "navy";
var CountDownCountActive = true;
var CountDownCountStepper = 1;
var SetTimeOutPeriod = (Math.abs(CountDownCountStepper)-1)*1000 + 990;
var CountDownLeadingZero = true;
var CountDownDisplayFormat = "Window automatically closes after 5 minutes %%M%%:%%S%%.";
var CountDownFinishMessage = "It is finally here!";

function countdown(mins,msg)
{
  var timeleft = mins*60000;
  CountDownDisplayFormat = msg;
  setTimeout("self.close();",timeleft);
  if (typeof(CountDownBackColor)=="undefined") { CountDownBackColor = "white"; }
  if (typeof(CountDownForeColor)=="undefined") { CountDownForeColor= "black"; }
  if (typeof(CountDownTargetDate)=="undefined") { CountDownTargetDate = "12/31/2020 5:00 AM"; }
  if (typeof(CountDownDisplayFormat)=="undefined") { CountDownDisplayFormat = "%%D%% Days, %%H%% Hours, %%M%% Minutes, %%S%% Seconds."; }
  if (typeof(CountDownCountActive)=="undefined") { CountDownCountActive = true; }
  if (typeof(CountDownFinishMessage)=="undefined") { CountDownFinishMessage = ""; }
  if (typeof(CountDownCountStepper)!="number") { CountDownCountStepper = -1; }
  if (typeof(CountDownLeadingZero)=="undefined") { CountDownLeadingZero = true; }

  CountDownCountStepper = Math.ceil(CountDownCountStepper);
  if (CountDownCountStepper == 0) { CountDownCountActive = false; }
  SetTimeOutPeriod = (Math.abs(CountDownCountStepper)-1)*1000 + 990;
  //putspan(CountDownBackColor, CountDownForeColor);
  var dthen = new Date(CountDownTargetDate);
  var dnow = new Date();
  if(CountDownCountStepper>0)
  { ddiff = new Date(dnow-dthen); }
  else
  { ddiff = new Date(dthen-dnow); }
  gsecs = Math.floor(ddiff.valueOf()/1000);
  CountBack(gsecs);
}
function calcage(secs, num1, num2)
{
  s = ((Math.floor(secs/num1))%num2).toString();
  if (CountDownLeadingZero && s.length < 2) { s = "0" + s; }
  return "<b>" + s + "</b>";
}
function CountBack(secs)
{
  if (secs < 0) 
  {
    document.getElementById("cntdwn").innerHTML = CountDownFinishMessage;
    return;
  }
  DisplayStr = CountDownDisplayFormat.replace(/%%D%%/g, calcage(secs,86400,100000));
  DisplayStr = DisplayStr.replace(/%%H%%/g, calcage(secs,3600,24));
  DisplayStr = DisplayStr.replace(/%%M%%/g, calcage(secs,60,60));
  DisplayStr = DisplayStr.replace(/%%S%%/g, calcage(secs,1,60));

  document.getElementById("cntdwn").innerHTML = DisplayStr;
  if (CountDownCountActive)
  { setTimeout("CountBack(" + (secs+CountDownCountStepper) + ")", SetTimeOutPeriod); }
}
//function putspan(backcolor, forecolor)
//{
//  document.write("<span id='cntdwn' style='background-color:" + backcolor + "; color:" + forecolor + "'></span>");
//}

