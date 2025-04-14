#!/usr/bin/env python3
import sys
import cdsapi

c = cdsapi.Client()
year= sys.argv[1]
month= sys.argv[2]
stat= sys.argv[3]
abr = sys.argv[4]
area = sys.argv[5]

dataset = "derived-era5-land-daily-statistics"
request = {
    "variable": [
        "2m_dewpoint_temperature",
        "2m_temperature",
        "skin_temperature",
        "soil_temperature_level_1",
        "soil_temperature_level_2",
        "soil_temperature_level_3",
        "soil_temperature_level_4",
        "lake_ice_depth",
        "snow_albedo",
        "snow_cover",
        "snow_density",
        "snow_depth",
        "snow_depth_water_equivalent",
        "temperature_of_snow_layer",
        "skin_reservoir_content",
        "volumetric_soil_water_layer_1",
        "volumetric_soil_water_layer_2",
        "volumetric_soil_water_layer_3",
        "volumetric_soil_water_layer_4",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "surface_pressure",
        "leaf_area_index_high_vegetation",
        "leaf_area_index_low_vegetation",
        "forecast_albedo"
    ],
    "year": year,
    "month": month,
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "daily_statistic": "daily_%s"%stat,
    "time_zone": "utc+00:00",
    "frequency": "3_hourly",
    "data_format": "grib",
    "area": area
}
target='/home/smartmet/data/ERA5LD_{:0>2}{:0>2}01T000000_{:0>4}-6h.grib'.format(year,month,stat)
c.retrieve(dataset, request, target)
