#!/bin/bash
# kls, 06/30/2002
# ------------------------------------
if [ -f /etc/config.csi ]; then
   . /etc/config.csi
else
   print "\nServices not installed!"
   exit 1
fi
usage()
{
  echo ""
  echo "Usage: $0 tag"
  echo "  save the current mysql db and user tables"
  echo "  to table_mysql_user.[tag]"
  echo "  and table_mysql_db.[tag]"
  echo ""
  exit
}
if [ $# -eq 0 ]; then usage; fi
TAG=$1
print "pwd=$(pwd)"
print "Save mysql user: table_mysql_user.${TAG}"
${DBBIN}/mysqldump mysql user > table_mysql_user.${TAG}
print "Save mysql user: table_mysql_db.${TAG}"
${DBBIN}/mysqldump mysql db > table_mysql_db.${TAG}
# ------------------------------------
