bbox='24.9459,25.4459,59.95867,60.45867'
harbor='Vuosaari'
FMISID='151028'
lat=60.20867
lon=25.1959
predictand='WG_PT1H_MAX'
mdl_name='mdl_WGPT1MAX_2013-2023_sf_test_2.txt'
predictors00='10u,10v,2d,2t,10fg'
predictorsDSUM='ewss,nsss,slhf,sshf,ssr,ssrd,strd,tp'
cols_own='ewss-1','ewss-2','ewss-3','ewss-4','fg10-1','fg10-2','fg10-3','fg10-4','nsss-1','nsss-2','nsss-3','nsss-4','slhf-1','slhf-2','slhf-3','slhf-4','sshf-1','sshf-2','sshf-3','sshf-4','ssr-1','ssr-2','ssr-3','ssr-4','ssrd-1','ssrd-2','ssrd-3','ssrd-4','strd-1','strd-2','strd-3','strd-4','t2-1','t2-2','t2-3','t2-4','td2-1','td2-2','td2-3','td2-4','tp-1','tp-2','tp-3','tp-4','u10-1','u10-2','u10-3','u10-4','v10-1','v10-2','v10-3','v10-4'
pred00='lat','lon','u10','v10','fg10','td2','t2'
predDSUM='lat','lon','ewss','nsss','slhf','ssr','sshf','ssrd','strd','tp'

f1 = 'obs-oceanids-20240101T000000Z-20240803T000000Z-all-'+harbor+'-daymean-daymax.csv' # observations 
threshold_values = [33.55, 30.78, 24.84, 18.33, 8.71, 17.0, 12.58, 16.77, 18.67, 30.97, 31.33, 35.16]
th_wind=15