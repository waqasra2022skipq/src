var ImgName; 
function ImgShow(Name)
{
  ImgName = Name;
  NewImg = "/images/" + ImgName + "_show.gif"; 
  document.images[ImgName].src=NewImg;
} 
function ImgHide()
{
  NewImg = "/images/" + ImgName + "_hide.gif";
  document.images[ImgName].src=NewImg;
} 
