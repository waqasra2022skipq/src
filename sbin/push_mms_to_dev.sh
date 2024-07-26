#!/bin/bash
# kls, daily 11/4/08
# ------------------------------------
if [ -f /etc/config.csi ]; then
   . /etc/config.csi
else
   print "\nServices not installed!"
   exit 1
fi

# do daily save.
okmis_mms_backup_file=/home2/okmis/backups/backups/daily/Thu/okmis_mms.sqldump.gz

scp ${okmis_mms_backup_file} root@server4.okmis.com:/home/okmis/backups/