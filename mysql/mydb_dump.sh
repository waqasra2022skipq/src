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
  echo "Usage: $0 database_name"
  echo ""
  exit
}
if [ $# -eq 0 ]; then usage; fi
Db=$1
print "pwd=$(pwd)"
print "Save SQL db ${Db}..."
${DBBIN}/mysqldump -d ${Db} > ${Db}_tables.sql
${DBBIN}/mysqldump -t ${Db} > ${Db}_data.sql
# ------------------------------------
