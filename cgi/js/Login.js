function setCookie(name,val,min)
{
  var exp = new Date();
  var cookieTimeToLive = exp.getTime() + (60 * min * 1000);
  exp.setTime(cookieTimeToLive);
  document.cookie = name + "=" + escape(val) + "; path=/; secure; expires=" + exp.toGMTString();
  document.cookie = name + "NP=" + escape(val) + "; path=/; secure; expires=";
//alert('setCookie: name=' + name + ', val=' + val + ', min=' + min + ', timeToLive=' + cookieTimeToLive);
}
function getCookie(name)
{
  var search = name + "=";
  var cookie = document.cookie;

//alert('getCookie: cookie=' + cookie);
  if (document.cookie.length > 0)
  {
    // if there are any cookies
    offset = document.cookie.indexOf(search)
    if (offset != -1)
    {                                            // if cookie exists
      offset += search.length                    // set index of beginning of value
      end = document.cookie.indexOf(";", offset) // set index of end of cookie value
      if (end == -1)
      { end = document.cookie.length; }
      return unescape(document.cookie.substring(offset, end))
    }
  }
}
