#!/bin/bash
export DATESTAMP=`date +%Y%m%d%H%M%S`
cd /home/okmis/mis/src/phimail
echo -e "Check messages...\n"
echo -e "\nfirst check (b1) messages"
echo -e "php phireceive.php okmis-edge2015@directtest.interopengine.com ${DATESTAMP}\n"
php phireceive.php okmis-edge2015@directtest.interopengine.com ${DATESTAMP}
./addMail
#echo -e "\nnext check (h1) messages"
#echo -e "php phireceive.php okmis@test.directproject.net ${DATESTAMP}\n"
#php phireceive.php okmis@test.directproject.net ${DATESTAMP}
#./addMail
