#!/bin/bash
# kls, 20030205
# ------------------------------------
if [ -f /etc/config.csi ]; then
   . /etc/config.csi
else
   echo -e "\nServices not installed!"
   exit 1
fi
MONTH=$1; shift
# ------------------------------------
#
# Usage: Process271 thismonth/nextmonth
#        where thismonth or nextmonth is month to clear
Usage()
{
   echo $1
   echo "Usage: ${CMD} MONTH "
   echo "where: MONTH is month to clear Eligibility"
   echo "             is thismonth(default)|nextmonth"
   echo
   exit
}
# ------------------------------------
if [ -z "${MONTH}" ]; then Usage "No MONTH given!!"; fi
LogFile=${ADMINDIR}/logs/${CMD}
DBS=$(${MISBIN}/dbs LIVE)
if [ -d ${ADMINDIR}/271 ]; then
  cd ${ADMINDIR}/271
else
  echo -e "\nDirectory ${ADMINDIR}/271 not found!\n"
  exit
fi
# ------------------------------------
(
  echo "${CMD} Started: $(date)"
  echo "Process .271 files...$(pwd)"
  echo "======================================"
  # ------------------------------------
  echo ""
  for DBNAME in $DBS; do
    echo "dump Eligible ${DBNAME}..."
    mysqldump ${DBNAME} Eligible > ${DBNAME}.Eligible
  done
  # ------------------------------------
  echo ""
  for DBNAME in $DBS; do
    if /bin/ls ${DBNAME}*.271 2>/dev/null; then
      echo "Clear ${DBNAME}..."
      ${MISBIN}/p271 DBNAME=${DBNAME}\&clear=1\&daterange=${MONTH}
    else
      echo "Skip ${DBNAME}..."
    fi
  done
  # ------------------------------------
  echo ""
  for File in $(/bin/ls *.271 2>/dev/null ); do
    dbname=$(echo ${File} | awk -F. '{print $1}')
    echo "Process ${File}..."
    ${MISBIN}/p271 DBNAME=${dbname}\&path=${File} > ${File}.xls
    mv ${File} ${BACKDIR}/271
  done
  echo ""
  # ------------------------------------
  echo "======================================"
  echo "${CMD} Complete: $(date)"
) | tee ${LogFile}
# ------------------------------------
ATTFILES=$(grep "^-f " ${LogFile})
cat ${LogFile} | ${MISBIN}/email -a billing@okmis.com -s "${CMD}: ${YMD}" ${ATTFILES}
