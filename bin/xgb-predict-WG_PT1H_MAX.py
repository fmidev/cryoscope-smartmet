import xarray as xr
import cfgrib,time,sys
import pandas as pd
import xgboost as xgb
#from Vuosaari_151028_XGBoost import *
#from Raahe_101785_XGBoost import *
#from Rauma_101061_XGBoost import *
from Malaga_000231_XGBoost import *

#startTime=time.time()

def filter_points(df,lat,lon,nro,names):
    df0=df.copy()
    filter1 = df0['latitude'] == lat
    filter2 = df0['longitude'] == lon
    df0.where(filter1 & filter2, inplace=True)
    idx='-'+str(nro)
    headers=[s + idx for s in names]
    df0.columns=headers
    df0=df0.dropna()
    return df0

mod_dir='/home/ubuntu/data/MLmodels/'

# read in input and output
instant = sys.argv[1] # ecsf 00 UTC data
dailysums = sys.argv[2] # ecsf disaccumulated data
outFile = sys.argv[3] # output csv filename
ensmem = sys.argv[4] # ensemble member

# 00 UTC
sl=xr.open_dataset(instant, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('valid_time','verifying_time'),indexpath=''))
df_00=sl.to_dataframe()
df_00.reset_index(['latitude','longitude'],inplace=True)
df_00=df_00.drop(columns=['surface'])
# filter points
lat=60.00
lon=25.00
df1=filter_points(df_00,lat,lon,1,pred00)
lat=60.25
lon=25.25
df2=filter_points(df_00,lat,lon,2,pred00)
lat=60.25
lon=25.00
df3=filter_points(df_00,lat,lon,3,pred00)
lat=60.00
lon=25.25
df4=filter_points(df_00,lat,lon,4,pred00)
# merge dataframes
df_new1 = pd.concat([df1,df2,df3,df4],axis=1,sort=False).reset_index()
# df from datetime
df_result = df_new1[['valid_time','lat-1']]
df_new1 = df_new1.drop(['valid_time','lat-1','lon-1','lat-2','lon-2','lat-3','lon-3','lat-4','lon-4'], axis=1)

# DSUMS
sl=xr.open_dataset(dailysums, engine='cfgrib', 
                    backend_kwargs=dict(time_dims=('valid_time','verifying_time'),indexpath=''))
df_DSUM=sl.to_dataframe()
df_DSUM.reset_index(['latitude','longitude'],inplace=True)
df_DSUM=df_DSUM.drop(columns=['surface'])
# filter points
lat=60.00
lon=25.00
df1=filter_points(df_DSUM,lat,lon,1,predDSUM)
lat=60.25
lon=25.25
df2=filter_points(df_DSUM,lat,lon,2,predDSUM)
lat=60.25
lon=25.00
df3=filter_points(df_DSUM,lat,lon,3,predDSUM)
lat=60.00
lon=25.25
df4=filter_points(df_DSUM,lat,lon,4,predDSUM)

# merge dataframes
df_new2 = pd.concat([df1,df2,df3,df4],axis=1,sort=False).reset_index()
df_new2 = df_new2.drop(['valid_time','lat-1','lon-1','lat-2','lon-2','lat-3','lon-3','lat-4','lon-4'], axis=1)
 
# merge 00 utc and dsums
df_fin= pd.concat([df_new1,df_new2],axis=1,sort=False).reset_index()
if 'index' in df_fin.columns:
    df_fin=df_fin.drop(columns=['index'])
df_fin=df_fin[cols_own] # check that column order same as in fitting
#print(df_fin)
# XGBoost predict
fitted_mdl=xgb.XGBRegressor()
fitted_mdl.load_model(mod_dir+mdl_name)
result=fitted_mdl.predict(df_fin)
ensname='WG_PT1H_MAX'+ensmem
df_result[ensname]=result.tolist()
df_result=df_result.drop(columns=['lat-1']) # dummy way because with only datetime df did not work and quick googling not help
df_result.to_csv(outFile,index=False)

#executionTime=(time.time()-startTime)
#print('Fitting execution time per member in minutes: %.2f'%(executionTime/60))