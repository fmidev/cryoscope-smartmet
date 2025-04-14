#!/bin/bash
#
# script for fetching ERA5 post-processed daily statistics data from cdsapi
# and setting it up in the smartmet-server
#
# 12.1.2025 Anni Kröger
#eval "$(conda shell.bash hook)"
eval "$(/home/ubuntu/mambaforge/bin/conda shell.bash hook)"

source ~/.smart

year=$1
var=$2

cd /home/smartmet/data

echo "fetch ERA5 daily sums for year: $year var: $var"

[ -f ERA5D_${year}0101T000000_${year}1231T120000_${var}.nc ] || ../bin/cds-era5-dailysums.py $year $var

conda activate cdo
cdo -s -b P8 -O --eccodes -f grb2 copy ERA5D_${year}0101T000000_${year}1231T120000_${var}.nc grib/ERA5D_20000101T000000_${year}_${var}.grib
rm ERA5D_${year}0101T000000_${year}1231T120000_${var}.nc
#sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0