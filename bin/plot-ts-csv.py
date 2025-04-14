import requests,json,sys,os
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import CRPS.CRPS as pscore
import calendar
from Vuosaari_151028_XGBoost import *
#from Raahe_101785_XGBoost import *
#from Rauma_101061_XGBoost import *
pd.set_option('mode.chained_assignment', None) # turn off SettingWithCopyWarning 

data_dir='/home/ubuntu/data/OCEANIDS/'

yearmon=sys.argv[1]

f2 = 'ECXSF_'+yearmon+'_WG_PT1H_MAX_'+harbor+'_'+FMISID+'.csv' # sf XGBoost result file
df_csv=pd.read_csv(data_dir+f2)
print(df_csv)
firstDate= df_csv['valid_time'].iloc[0]
lastDate= df_csv['valid_time'].iloc[-1]
print(firstDate,lastDate)

df_plot=df_csv.set_index('valid_time')

keys= [f'WG_PT1H_MAX{i:02d}' for i in range(51)]
num_shades = len(keys)
blues = cm.Blues(np.linspace(0.3, 0.9, num_shades))

#colorsdict = {key: blues[i] for i, key in enumerate(keys[:num_shades])}
colorsdict = {
    'WG_PT1H_MAX00': 'blue',
    'WG_PT1H_MAX01': 'orange',
    'WG_PT1H_MAX02': 'green',
    'WG_PT1H_MAX03': 'red',
    'WG_PT1H_MAX04': 'purple',
    'WG_PT1H_MAX05': 'brown',
    'WG_PT1H_MAX06': 'pink',
    'WG_PT1H_MAX07': 'gray',
    'WG_PT1H_MAX08': 'olive',
    'WG_PT1H_MAX09': 'cyan',
    'WG_PT1H_MAX10': 'magenta',
    'WG_PT1H_MAX11': 'teal',
    'WG_PT1H_MAX12': 'lime',
    'WG_PT1H_MAX13': 'navy',
    'WG_PT1H_MAX14': 'gold',
    'WG_PT1H_MAX15': 'salmon',
    'WG_PT1H_MAX16': 'coral',
    'WG_PT1H_MAX17': 'khaki',
    'WG_PT1H_MAX18': 'lightblue',
    'WG_PT1H_MAX19': 'lightgreen',
    'WG_PT1H_MAX20': 'darkorange',
    'WG_PT1H_MAX21': 'indigo',
    'WG_PT1H_MAX22': 'orchid',
    'WG_PT1H_MAX23': 'darkviolet',
    'WG_PT1H_MAX24': 'chartreuse',
    'WG_PT1H_MAX25': 'skyblue',
    'WG_PT1H_MAX26': 'lightcoral',
    'WG_PT1H_MAX27': 'wheat',
    'WG_PT1H_MAX28': 'peru',
    'WG_PT1H_MAX29': 'tan',
    'WG_PT1H_MAX30': 'powderblue',
    'WG_PT1H_MAX31': 'lightpink',
    'WG_PT1H_MAX32': 'slategray',
    'WG_PT1H_MAX33': 'mediumseagreen',
    'WG_PT1H_MAX34': 'lightgoldenrodyellow',
    'WG_PT1H_MAX35': 'lightsteelblue',
    'WG_PT1H_MAX36': 'darkslategray',
    'WG_PT1H_MAX37': 'burlywood',
    'WG_PT1H_MAX38': 'mintcream',
    'WG_PT1H_MAX39': 'lightyellow',
    'WG_PT1H_MAX40': 'mediumslateblue',
    'WG_PT1H_MAX41': 'tan',
    'WG_PT1H_MAX42': 'seashell',
    'WG_PT1H_MAX43': 'lavender',
    'WG_PT1H_MAX44': 'snow',
    'WG_PT1H_MAX45': 'darkkhaki',
    'WG_PT1H_MAX46': 'steelblue',
    'WG_PT1H_MAX47': 'seagreen',
    'WG_PT1H_MAX48': 'lightsalmon',
    'WG_PT1H_MAX49': 'lightcyan',
    'WG_PT1H_MAX50': 'salmon'
}

plt.figure(figsize=(15, 10))
for column in df_plot.columns:
    if column in colorsdict:
        df_plot[column].plot(color=colorsdict[column], linewidth=0.4, label=column)

plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.ylim(0, 30)
plt.title(f'ECXSF WG_PT1H_MAX {harbor} {FMISID} {yearmon}')

n1 = data_dir + f'ECXSF_WG_PT1H_MAX_{harbor}_{FMISID}_{yearmon}-test.png'
plt.savefig(n1, dpi=500)
plt.show()