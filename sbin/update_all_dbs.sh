#!/bin/bash

# List of databases
databases=(
    "okmis_1smdp"
    "okmis_4hc"
    "okmis_adv"
    "okmis_afc"
    "okmis_anv"
    "okmis_anw"
    "okmis_base"
    "okmis_ccc"
    "okmis_ccs"
    "okmis_csl"
    "okmis_elf"
    "okmis_fho"
    "okmis_foh"
    "okmis_gcs"
    "okmis_gpr"
    "okmis_ibf"
    "okmis_ipi"
    "okmis_lbhp"
    "okmis_lkt"
    "okmis_nbc"
    "okmis_oays"
    "okmis_opa"
    "okmis_pcd"
    "okmis_scs"
    "okmis_tccp"
    "okmis_cti"
    "okmis_tsi"
    "okmis_mms"
)

# Loop through each database and run the command
for db in "${databases[@]}"; do
    ./updateMCOInsPrio "DBNAME=$db"
done

echo "All databases updated."

