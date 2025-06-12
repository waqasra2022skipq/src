#!/bin/bash

# Define variables
echo "Define variables"
DB_USER="root"
DB_PASSWORD="}zI2ZH.TENcyMRwY"
DB_NAME="okmis_lkt"
DEV_BACKUP_DIR="/var/www/okmis/backups"
DUMP_FILE=$(ls -t $DEV_BACKUP_DIR/okmis_mms.sqldump.gz | head -1)

# Extract the dump file
gunzip -k $DUMP_FILE
# Get the extracted file name
EXTRACTED_DUMP_FILE="${DUMP_FILE%.gz}"

echo "Clean the File"
# Remove invalid lines and save to the clean dump file
sed -i 's/\\- enable the sandbox mode/enable the sandbox mode/' $EXTRACTED_DUMP_FILE

# Remove the problematic 'NO_AUTO_CREATE_USER' from the sql_mode setting
sed -i "s/NO_AUTO_CREATE_USER//g" $EXTRACTED_DUMP_FILE
# Remove any redundant commas from the sql_mode setting
sed -i "s/,,/,/g" $EXTRACTED_DUMP_FILE
# Remove any trailing commas in the sql_mode setting
sed -i "s/,\s*'/\1/" $EXTRACTED_DUMP_FILE

echo "Replace all instances of 'okmis_mms' with 'okmis_dev'"

# Replace all instances of 'okmis_mms' with 'okmis_dev'
sed -i "s/okmis_mms/okmis_dev/g" $EXTRACTED_DUMP_FILE

# Import the dump file into the development database
mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME < $EXTRACTED_DUMP_FILE

# Delete the File
echo "Delete the File"

rm ${EXTRACTED_DUMP_FILE}

# Update the dbname column in the user_login table
# mysql -e "UPDATE user_login SET dbname = 'okmis_dev' WHERE dbname = 'okmis_mms';" $DB_NAME
