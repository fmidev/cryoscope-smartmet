#!/usr/bin/env python3
import sys
import cdsapi

c = cdsapi.Client()
abr = sys.argv[1]
area = sys.argv[2]
mon = sys.argv[3]
years = sys.argv[4:]
year = sys.argv[4]+'-'+sys.argv[-1]
print(years, year, abr, area)

c.retrieve(
    'seasonal-monthly-single-levels',
    {
        'format': 'grib',
        'originating_centre': 'ecmwf',
        'system': '5',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind',
            '10m_wind_gust_since_previous_post_processing',
            '10m_wind_speed',
            '2m_dewpoint_temperature', '2m_temperature',
            'evaporation', 'maximum_2m_temperature_in_the_last_24_hours', 'mean_sea_level_pressure',
            'minimum_2m_temperature_in_the_last_24_hours', 'runoff', 'sea_ice_cover',
            'sea_surface_temperature', 'snow_density', 'snow_depth','snowfall','soil_temperature_level_1',
#            'soil_temperature_level_2','soil_temperature_level_3','soil_temperature_level_4',
            '39.128', '40.128', '41.128','42.128',
            'surface_latent_heat_flux','surface_sensible_heat_flux', 'surface_solar_radiation', 'surface_solar_radiation_downwards',
            'surface_thermal_radiation', 'surface_thermal_radiation_downwards',
            'top_solar_radiation','top_thermal_radiation',
            'total_cloud_cover', 'total_precipitation',
        ],
        'product_type': [
#            'ensemble_mean', 'hindcast_climate_mean', 'monthly_maximum','monthly_minimum',
            'monthly_mean', 'monthly_standard_deviation',
        ],
        'month': mon,
        'leadtime_month': [
            '1', '2', '3',
            '4', '5', '6',
        ],
        'area': area,
        'year': years,
    },
    '/home/smartmet/data/ens/ec-sf-%s-stats-%s-%s-fcmean.grib'%(year,mon,abr))
