import requests,json,sys,os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import CRPS.CRPS as pscore
import calendar
#from Vuosaari_151028_XGBoost import *
#from Raahe_101785_XGBoost import *
#from Rauma_101061_XGBoost import *
from Malaga_000231_XGBoost import *

### Creates seasonal forecast plots against observations for wind gusts. 
### The script takes a wind speed threshold as a command line argument and calculates the percentage of ensemble members exceeding the threshold for each month.
### The script also calculates the CRPS for each ensemble member and the observations and plots the results.

pd.set_option('mode.chained_assignment', None) # turn off SettingWithCopyWarning 

# give wind threshold k as cmd argument

### ECXSF
date='20240101T000000Z-20240803T000000Z' # sf date range
#date='20190101T000000Z-20190804T000000Z'
#date='20190601T000000Z-20200102T000000Z'
yearmon=date[0:6]
data_dir='/home/ubuntu/data/OCEANIDS/'

cols1=['utctime',predictand]
f2 = 'ECXSF_'+yearmon+'_WG_PT1H_MAX_'+harbor+'_'+FMISID+'.csv' # sf XGBoost result file
#print(f1,f2) # f1 observations for predictand to compare to, from harbor specific file
df1=pd.read_csv(data_dir+f1,usecols=cols1)
df2=pd.read_csv(data_dir+f2)
df2.rename(columns={'valid_time': 'utctime'},inplace=True)
df2=df2.set_index('utctime')
dfapu=df2.copy()
df2['ensmean'] = dfapu.mean(axis=1) # add ensemble mean and spread as columns
df2['ensspread'] = dfapu.std(axis=1)
df2 = df2.reset_index()
df_xgb=pd.merge(df2, df1, on='utctime')
df_xgb=df_xgb.set_index('utctime')
#print(df_xgb)

# threshold for obs wind speed>= k, % of ECXSF ensemble members above k
k=int(sys.argv[1])
df_max=df_xgb[df_xgb.WG_PT1H_MAX>=k] # df with only rows where obs wind speed >= k
print('Observed wind speed >= '+str(k)+'m/s in '+harbor+': '+str(len(df_max))+' days')
df_max_copy=df_max.copy()
df_max_copy.index = pd.to_datetime(df_max_copy.index)
dfg = df_max_copy.groupby(df_max_copy.index.month).size().reset_index(name='counts')
dfg['utctime'] = dfg['utctime'].map(dict(zip(range(1, 13), calendar.month_name[1:])))
print('Days observed wind speed over '+str(k)+'m/s in '+harbor+' by month:')
print(dfg)
df0=df_max.drop(columns=['WG_PT1H_MAX','ensmean','ensspread'])
counts=[]
for index, row in df0.iterrows():
    list=row.tolist()
    count = len([i for i in list if i >= k])
    res=count/51*100
    counts.append(round(res,1))
df_max['wind>'+str(k)+'_%']=counts
#print(df_max)
value1=round(df_max['wind>'+str(k)+'_%'].mean(),1)

df_xgb=df_xgb.drop(columns=['ensspread'])
colorsdict={
            'WG_PT1H_MAX00':'blue','WG_PT1H_MAX01':'blue','WG_PT1H_MAX02':'blue','WG_PT1H_MAX03':'blue','WG_PT1H_MAX04':'blue','WG_PT1H_MAX05':'blue','WG_PT1H_MAX06':'blue','WG_PT1H_MAX07':'blue','WG_PT1H_MAX08':'blue','WG_PT1H_MAX09':'blue','WG_PT1H_MAX10':'blue',
            'WG_PT1H_MAX11':'blue','WG_PT1H_MAX12':'blue','WG_PT1H_MAX13':'blue','WG_PT1H_MAX14':'blue','WG_PT1H_MAX15':'blue','WG_PT1H_MAX16':'blue','WG_PT1H_MAX17':'blue','WG_PT1H_MAX18':'blue','WG_PT1H_MAX19':'blue','WG_PT1H_MAX20':'blue',
            'WG_PT1H_MAX21':'blue','WG_PT1H_MAX22':'blue','WG_PT1H_MAX23':'blue','WG_PT1H_MAX24':'blue','WG_PT1H_MAX25':'blue','WG_PT1H_MAX26':'blue','WG_PT1H_MAX27':'blue','WG_PT1H_MAX28':'blue','WG_PT1H_MAX29':'blue','WG_PT1H_MAX30':'blue',
            'WG_PT1H_MAX31':'blue','WG_PT1H_MAX32':'blue','WG_PT1H_MAX33':'blue','WG_PT1H_MAX34':'blue','WG_PT1H_MAX35':'blue','WG_PT1H_MAX36':'blue','WG_PT1H_MAX37':'blue','WG_PT1H_MAX38':'blue','WG_PT1H_MAX39':'blue','WG_PT1H_MAX40':'blue',
            'WG_PT1H_MAX41':'blue','WG_PT1H_MAX42':'blue','WG_PT1H_MAX43':'blue','WG_PT1H_MAX44':'blue','WG_PT1H_MAX45':'blue','WG_PT1H_MAX46':'blue','WG_PT1H_MAX47':'blue','WG_PT1H_MAX48':'blue','WG_PT1H_MAX49':'blue',
            'WG_PT1H_MAX50':'blue',
            'WG_PT1H_MAX':'red',#'ensmean':'yellow'
        }

# CRPS
df_crps=df_xgb[['WG_PT1H_MAX','ensmean']].copy()
dfwg=df_xgb['WG_PT1H_MAX'].copy()
df_ens=df_xgb.drop(columns=['WG_PT1H_MAX','ensmean'])
scores=[]
for index, row in df_ens.iterrows():
    list=np.array(row.tolist())
    obs=dfwg.loc[index]
    crps,fcrps,acrps=pscore(list,obs).compute()
    #print(crps)
    scores.append(crps)
df_crps['CRPS-xgb']=scores

# plot with average threshold exceedance
df_wg=df_xgb['WG_PT1H_MAX'].copy()
df_xgb=df_xgb.drop(columns=['ensmean','WG_PT1H_MAX'])
mytitle='ECXSF WG_PT1H_MAX '+harbor+' '+FMISID+' '+yearmon 
plot = df_xgb.plot(figsize=(15,10),color=colorsdict, title=mytitle,linewidth=0.2)
plot = df_wg.plot(ax=plot, color='red',linewidth=2.0)
fig = plot.get_figure()
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.ylim(0,30)
n1=data_dir+'ECXSF_WG_PT1H_MAX_'+harbor+'_'+FMISID+'_'+yearmon+'-fix.png'
if os.path.exists(n1)==False:
    fig.savefig(n1,dpi=500)
else: 
    print('file already exists')

### ECSF 
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
dfapu=df_ecsf.copy()
df_ecsf['ensmean'] = dfapu.mean(axis=1)
#df_ecsf['ensspread'] = dfapu.std(axis=1)
df_ecsf = df_ecsf.reset_index()
#print(df_ecsf)

df1['utctime']=pd.to_datetime(df1['utctime'])
df_sf=pd.merge(df_ecsf, df1, on='utctime')
df_sf=df_sf.set_index('utctime')
#print(df_sf)
# threshold k for wind speed, % of ensemble members above k
df_max=df_sf[df_sf.WG_PT1H_MAX>=k]
df0=df_max.drop(columns=['WG_PT1H_MAX','ensmean'])
counts=[]
for index, row in df0.iterrows():
    list=row.tolist()
    count = len([i for i in list if i >= k])
    res=count/51*100
    counts.append(round(res,1))
df_max['wind>'+str(k)+'_%']=counts
#print(df_max)
value2=round(df_max['wind>'+str(k)+'_%'].mean(),1)
#df_sf=df_sf.drop(columns=['ensspread'])
colorsdict={
    'ens0':'blue','ens1':'blue','ens2':'blue','ens3':'blue','ens4':'blue','ens5':'blue','ens6':'blue','ens7':'blue','ens8':'blue','ens9':'blue','ens10':'blue',
    'ens11':'blue','ens12':'blue','ens13':'blue','ens14':'blue','ens15':'blue','ens16':'blue','ens17':'blue','ens18':'blue','ens19':'blue','ens20':'blue',
    'ens21':'blue','ens22':'blue','ens23':'blue','ens24':'blue','ens25':'blue','ens26':'blue','ens27':'blue','ens28':'blue','ens29':'blue','ens30':'blue',
    'ens31':'blue','ens32':'blue','ens33':'blue','ens34':'blue','ens35':'blue','ens36':'blue','ens37':'blue','ens38':'blue','ens39':'blue','ens40':'blue',
    'ens41':'blue','ens42':'blue','ens43':'blue','ens44':'blue','ens45':'blue','ens46':'blue','ens47':'blue','ens48':'blue','ens49':'blue',
    'ens50':'blue',
    'WG_PT1H_MAX':'red'#,'ensmean':'yellow'
    }

# CRPS
dfwg=df_sf['WG_PT1H_MAX'].copy()
df_ens=df_sf.drop(columns=['WG_PT1H_MAX','ensmean'])
scores=[]
for index, row in df_ens.iterrows():
    list=np.array(row.tolist())
    obs=dfwg.loc[index]
    crps,fcrps,acrps=pscore(list,obs).compute()
    scores.append(crps)
df_crps['CRPS-sf']=scores
df_crps=df_crps.drop(columns=['WG_PT1H_MAX','ensmean'])
#print(df_crps)
mean1=round(df_crps['CRPS-xgb'].mean(),1)
mean2=round(df_crps['CRPS-sf'].mean(),1)
print('xgb crps mean: '+str(mean1)+', sf crps mean: '+str(mean2))
std1= round(df_crps['CRPS-xgb'].std(),1)
std2= round(df_crps['CRPS-sf'].std(),1)
print('xgb crps std: '+str(std1)+', sf crps std: '+str(std2))
print('xgb gust>='+str(k)+'m/s: '+str(value1)+'%, sf gust >='+str(k)+'m/s: '+str(value2)+'%')
#df_xgb=pd.merge(df2, df1, on='utctime')
#df_xgb=df_xgb.set_index('utctime')

# plot crps
mytitle='CRPS WG_PT1H_MAX '+harbor+' '+FMISID+' '+yearmon
plot = df_crps.plot(figsize=(15,10), title=mytitle)
fig = plot.get_figure()
plt.legend(bbox_to_anchor=(1.0, 1.0))
n2=data_dir+'CRPS_WG_PT1H_MAX_'+harbor+'_'+FMISID+'_'+yearmon+'-fix.png'
if os.path.exists(n2)==False:
    fig.savefig(n2,dpi=500)
else: 
    print('file already exists')

df_crps = df_crps.reset_index()
df_crps['utctime']=pd.to_datetime(df_crps['utctime'])
df_crps_month = df_crps.resample('M', on='utctime').mean()
print(df_crps_month)

# plot ecsf with average threshold exceedance
mytitle='ECSF WG_PT1H_MAX '+harbor+' '+FMISID+' '+yearmon
df_sf=df_sf.drop(columns=['ensmean','WG_PT1H_MAX'])
plot = df_sf.plot(figsize=(15,10),color=colorsdict, title=mytitle,linewidth=0.2)
plot = dfwg.plot(ax=plot, color='red',linewidth=2.0)
fig = plot.get_figure()
plt.ylim(0,30)
plt.legend(bbox_to_anchor=(1.0, 1.0))
n3=data_dir+'ECSF_WG_PT1H_MAX_'+harbor+'_'+FMISID+'_'+yearmon+'-fix.png'
if os.path.exists(n3)==False:
    fig.savefig(n3,dpi=500)
else: 
    print('file already exists')

