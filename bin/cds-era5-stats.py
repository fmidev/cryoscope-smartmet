#!/usr/bin/env python3                                                                                                                                                     
import sys
import cdsapi
# source ~/.smart 
c = cdsapi.Client()
abr = sys.argv[1]
area = sys.argv[2]
years= sys.argv[3:]

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'grib',
        'area' : area,
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            'maximum_2m_temperature_in_the_last_24_hours','minimum_2m_temperature_in_the_last_24_hours',
            '2m_dewpoint_temperature', '2m_temperature',
            'evaporation', 'potential_evaporation', 'runoff',
            'skin_reservoir_content', 'skin_temperature',
            'snow_albedo','snow_density', 'snow_depth',
            'snow_depth_water_equivalent', 'snow_evaporation', 'snowfall',
            'snowmelt', 'soil_temperature_level_1', 'soil_temperature_level_2',
            'soil_temperature_level_3', 'soil_temperature_level_4', 'sub_surface_runoff',
            'surface_runoff', 'temperature_of_snow_layer', 'volumetric_soil_water_layer_1',
            'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'surface_pressure',
            'total_precipitation'
        ],
        'year': [
            '2010', '2011', '2012',
            '2013', '2014', '2015',
            '2016', '2017', '2018',
            '2019',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'time': '00:00',
    },
    '/home/smartmet/data/era5_2010-2009_stats-%s.grib'%(abr)
    )
