#!/bin/bash
# kls, 20111022
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
  echo "Usage: $CMD DBNAME"
  echo ""
  exit
}
if [ $# -eq 0 ]; then usage; fi
DB=$1
mlt=$2
LogFile=${LOGDIR}/${CMD}
echo "RUN SetAccess Started: $(date)" > ${LogFile}
# ------------------------------------
#(
  print "Content-type: text/html"
  print
  print
  print "<!DOCTYPE html>"
  print "<HTML>"
  print "<HEAD> <TITLE>List Payroll</TITLE>"
  print "<PRE>"
  print "\n======================================"
  print "${CMD} Started: $(date)"
  print "  setSiteACL... "
  ${MISBIN}/setSiteACL DBNAME=${DB}\&mlt=${mlt}
  print "  setManagerTree..."
  ${MISBIN}/setManagerTree DBNAME=${DB}\&mlt=${mlt}
  print "\n${CMD} Complete: $(date)"
  print "======================================\n"
  print "</PRE>"
  print "</BODY>"
  print "</HTML>"
#) > ${LogFile} 2>&1
ERRCNT=$(grep Error ${LogFile} | wc -l)
cat ${LogFile} | ${MISBIN}/email -a ${WEBMASTER} -s "SetAccess: ${DB}: ${YMD}"
# ------------------------------------
