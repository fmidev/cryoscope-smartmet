#!/bin/bash
#
# monthly script for XGBoost prediction for OCEANIDS ML in ERA5 grid
# get-seasonal.sh must be run first to get the predictors
# give year month as cmd

source ~/.smart
# source harbor
#source Vuosaari_151028_XGBoost.py
#source Raahe_101785_XGBoost.py
source Rauma_101061_XGBoost.py

eval "$(conda shell.bash hook)"

conda activate xgb
TMPDIR=/home/smartmet/data/tmp
cd /home/smartmet/data

year=$1
month=$2
grid='era5'
echo $year $month $predictand $FMISID $harbor
echo $predictors00 $predictorsDSUM

# Instantaneous parameters at 00 UTC (10u,10v,2d,2t,10fg) to ERA5 grid, and fitting grid points
[ -s ens/ec-sf_${year}${month}_all-24h-eu-50.grib ] && ! [ -s ens/ec-sf_${year}${month}_inst-${harbor}-50.grib ] && \
seq 0 50 | parallel cdo -b P12 -O --eccodes sellonlatbox,$bbox -remap,$grid-$abr-grid,ec-sf-$grid-$abr-weights.nc -selname,$predictors00 ens/ec-sf_${year}${month}_all-24h-eu-{}.grib ens/ec-sf_${year}${month}_inst-${harbor}-{}.grib

# Disaccumulated daily sums (ewss,nsss,e,slhf,sshf,ssr,ssrd,strd,tp) to ERA5 grid, and fitting grid points
[ -s ens/disacc_${year}${month}_50.grib ] && ! [ -s ens/ec-sf_${year}${month}_dailysums-${harbor}-50.grib ] && \
seq 0 50 | parallel cdo -b P12 -O --eccodes sellonlatbox,$bbox -remap,$grid-$abr-grid,ec-sf-$grid-$abr-weights.nc -selname,$predictorsDSUM ens/disacc_${year}${month}_{}.grib ens/ec-sf_${year}${month}_dailysums-${harbor}-{}.grib

# XGBoost prediction (ouput is XGBoost SF timeseries as a csv file for harbor point location for each ens member)
seq 0 50 | parallel python /home/ubuntu/bin/xgb-predict-oceanids.py ens/ec-sf_${year}${month}_inst-${harbor}-{}.grib ens/ec-sf_${year}${month}_dailysums-${harbor}-{}.grib OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-{}.csv {}

# join csv files (keep datetime in ensmember 0)
seq 1 50 | parallel "cut -f2 -d, OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-{}.csv | sed 's:\(.*\),\(.*\):\2 \1:' > OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-{}-fix.csv"
seq 1 50 | parallel rm OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-{}.csv
paste -d ',' OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-*.csv > OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}.csv
rm OCEANIDS/ECXSF_${year}${month}_${predictand}_${harbor}_${FMISID}-*.csv

#k=12
#python /home/ubuntu/bin/xgb-analyse-oceanids.py k # analysis of the XGBoost prediction, k threshold for wind speed