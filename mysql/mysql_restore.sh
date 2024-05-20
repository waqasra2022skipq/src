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
  echo "  restore the current mysql db and user tables"
  echo "  from table_mysql_user.[tag]"
  echo "   and table_mysql_db.[tag]"
  echo ""
  exit
}
if [ $# -eq 0 ]; then usage; fi
TAG=$1
print "pwd=$(pwd)"
print "Restore mysql user: table_mysql_user.${TAG}"
${DBCMD} mysql < table_mysql_user.${TAG}
print "Restore mysql user: table_mysql_db.${TAG}"
${DBCMD} mysql < table_mysql_db.${TAG}
print "FLUSH PRIVILEGES ..."
${DBCMD} mysql < .flush_privileges
# ------------------------------------
