function showImage(tag,num,max)
{
alert('num='+num);
    var i = 1;
    var el;
    while (el = document.getElementById(tag + i))
    {
      if (i == num.value)
      { el.style.display = 'block'; }
      else
      { el.style.display = 'none'; }
      i++;
    }
    num.value++;
    if (num.value>max) { num.value=1; }
}
function showTab(tag,num,min,max)
{
    var i = min;
    var el;
    while ( i <= max )
    {
      if (el = document.getElementById(tag + i))
      {
        if (i == num)
        { el.style.display = 'block'; }
        else
        { el.style.display = 'none'; }
        i++;
      }
    }
}
