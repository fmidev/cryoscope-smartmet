import requests, json, sys, os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import CRPS.CRPS as pscore
import calendar
#from Vuosaari_151028_XGBoost import *
#from Raahe_101785_XGBoost import *
from Rauma_101061_XGBoost import *
pd.set_option('mode.chained_assignment', None)  # turn off SettingWithCopyWarning 

# Date and data directories
date='20240101T000000Z-20240803T000000Z' # sf date range
yearmon = date[0:6]
data_dir = '/home/ubuntu/data/OCEANIDS/'

# Monthly thresholds for each month (January to December)
monthly_thresholds = {month: threshold for month, threshold in enumerate(threshold_values, start=1)}

# Load and preprocess forecast data
f2 = 'ECXSF_'+yearmon+'_WG_PT1H_MAX_'+harbor+'_'+FMISID+'.csv' # sf XGBoost result file
df = pd.read_csv(data_dir + f2)
df.rename(columns={'valid_time': 'utctime'}, inplace=True)
df = df.set_index('utctime')
#df.index = pd.to_datetime(df.index)

# How many ensemlble members exceed the threshold (%)
over_th = df.iloc[:, 1:] >= th_wind
count_over_th = over_th.sum(axis=1)
df['percent_over_threshold'] = (count_over_th / 51) * 100

# Load observation data
f1 = 'obs-oceanids-'+date+'-all-'+harbor+'-daymean-daymax.csv' # observations 
cols1 = ['utctime', predictand]
df_obs = pd.read_csv(data_dir + f1, usecols=cols1)
df_all = pd.merge(df, df_obs, on='utctime')
df_all = df_all.set_index('utctime')
df_all.index = pd.to_datetime(df_all.index)

# Apply monthly thresholds to identify rows exceeding each month's threshold
monthly_results = []
for month, threshold in monthly_thresholds.items():
    # Filter data for the specific month
    df_month = df_all[df_all.index.month == month]
    
    # Filter by the monthly threshold
    df_max = df_month[df_month['percent_over_threshold'] >= threshold]
    
    # Save results for the month
    monthly_results.append(df_max)
    
# Combine results for all months
df_max_all = pd.concat(monthly_results)

# Group by month for summary
dfg_ecxsf = df_max_all.groupby(df_max_all.index.month).size().reset_index(name='counts')
dfg_ecxsf['utctime'] = dfg_ecxsf['utctime'].map(dict(zip(range(1, 13), calendar.month_name[1:])))

# Process observations in a similar way for comparison
df_obs_max = df_obs[df_obs.WG_PT1H_MAX >= th_wind]
df_obs_max.index = pd.to_datetime(df_obs_max['utctime'])
dfg_obs = df_obs_max.groupby(df_obs_max.index.month).size().reset_index(name='counts')
dfg_obs['utctime'] = dfg_obs['utctime'].map(dict(zip(range(1, 13), calendar.month_name[1:])))

# Print results
print(harbor +' ECXSF by month for '+str(th_wind)+' m/s wind threshold (sf '+yearmon+'):')
print(dfg_ecxsf)
print('obs by month:')
print(dfg_obs)

# ECSF
sf='FFG-MS:ECSF:5014:1:0:1:0'
sf0='FFG-MS:ECSF:5014:1:0:3'#:ensnro
name='ecsf'
pardict={
    'ens0':sf,'ens1':''+sf0+':1','ens2':''+sf0+':2','ens3':''+sf0+':3','ens4':''+sf0+':4','ens5':''+sf0+':5','ens6':''+sf0+':6','ens7':''+sf0+':7','ens8':''+sf0+':8','ens9':''+sf0+':9',
    'ens10':''+sf0+':10','ens11':''+sf0+':11','ens12':''+sf0+':12','ens13':''+sf0+':13','ens14':''+sf0+':14','ens15':''+sf0+':15','ens16':''+sf0+':16','ens17':''+sf0+':17','ens18':''+sf0+':18','ens19':''+sf0+':19',
    'ens20':''+sf0+':20','ens21':''+sf0+':21','ens22':''+sf0+':22','ens23':''+sf0+':23','ens24':''+sf0+':24','ens25':''+sf0+':25','ens26':''+sf0+':26','ens27':''+sf0+':27','ens28':''+sf0+':28','ens29':''+sf0+':29',
    'ens30':''+sf0+':30','ens31':''+sf0+':31','ens32':''+sf0+':32','ens33':''+sf0+':33','ens34':''+sf0+':34','ens35':''+sf0+':35','ens36':''+sf0+':36','ens37':''+sf0+':37','ens38':''+sf0+':38','ens39':''+sf0+':39',
    'ens40':''+sf0+':40','ens41':''+sf0+':41','ens42':''+sf0+':42','ens43':''+sf0+':43','ens44':''+sf0+':44','ens45':''+sf0+':45','ens46':''+sf0+':46','ens47':''+sf0+':47','ens48':''+sf0+':48','ens49':''+sf0+':49','ens50':''+sf0+':50'
    }
source='desm.harvesterseasons.com:8080'
start=date[0:16]
origintime=date[0:16]
lat=str(lat)
lon=str(lon)
query='http://'+source+'/timeseries?latlon='+lat+','+lon+'&param=utctime,'
for par in pardict.values():
    query+=par+','
query=query[0:-1]
query+='&starttime='+start+'&timesteps=215&hour=00&format=json&precision=full&tz=utc&timeformat=sql&origintime='+origintime
#print(query)
response=requests.get(url=query)
df_ecsf=pd.DataFrame(json.loads(response.content))
df_ecsf.columns=['utctime']+[*pardict] # change headers to params.keys
df_ecsf['utctime']=pd.to_datetime(df_ecsf['utctime'])
df_ecsf=df_ecsf.set_index('utctime')
#print(df_ecsf)

over_th = df_ecsf.iloc[:, 1:] >= th_wind
count_over_th = over_th.sum(axis=1)
df_ecsf['percent_over_threshold'] = (count_over_th / 51) * 100
df_ecsf.index = pd.to_datetime(df_ecsf.index)

# Apply monthly thresholds to identify rows exceeding each month's threshold
monthly_results = []
for month, threshold in monthly_thresholds.items():
    # Filter data for the specific month
    df_month = df_ecsf[df_ecsf.index.month == month]
    
    # Filter by the monthly threshold
    df_max = df_month[df_month['percent_over_threshold'] >= threshold]
    
    # Save results for the month
    monthly_results.append(df_max)
    
# Combine results for all months
df_max_ecsf = pd.concat(monthly_results)

# Group by month for summary
dfg_ecsf = df_max_ecsf.groupby(df_max_ecsf.index.month).size().reset_index(name='counts')
dfg_ecsf['utctime'] = dfg_ecsf['utctime'].map(dict(zip(range(1, 13), calendar.month_name[1:])))

print('ecsf by month:')
print(dfg_ecsf)

