#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBForm;
use myHTML;

############################################################################
my $form = DBForm->new();
my $html = myHTML->newHTML(
    $form,
    'Support Message',
    'CheckPopupWindow noclock countdown_1'
  )
  . qq|
  <P CLASS="heading" >$form->{'heading'}</P>
  <P CLASS="title" >$form->{'title'}</P>
  <P CLASS="subtitle" >
Contact Information:<BR>
Autumn Wisenberg<BR>Millennium Information Services<BR>672-837-7308<BR>autumn@okmcs.com</P>
</BODY>
<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
</HTML>
|;
print $html;
$form->complete();
exit;
############################################################################

