import cdsapi

abr='eu'
years=[#"2000", "2001", "2002","2003"
      #"2004", "2005","2006", "2007"
      #"2008","2009", "2010"#
      "2011","2012"
      ]

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "surface_latent_heat_flux",
        "surface_net_solar_radiation",
        "surface_net_thermal_radiation",
        "surface_sensible_heat_flux",
        "surface_solar_radiation_downwards",
        "surface_thermal_radiation_downwards",
        "total_column_cloud_liquid_water",
        "evaporation",
        "eastward_turbulent_surface_stress",
        "northward_turbulent_surface_stress"
    ],
    "year": years,
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
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
    "time": [
        "00:00", "03:00", "06:00",
        "09:00", "12:00", "15:00",
        "18:00", "21:00"
    ],
    "data_format": "grib",
    "download_format": "unarchived",
    "area": [75, -30, 25, 50]
}
target = '/home/ubuntu/data/era5-%s-%s-ML-3h-%s.grib'%(years[0],years[-1],abr)
client = cdsapi.Client()
client.retrieve(dataset, request, target)
#client = cdsapi.Client()
#client.retrieve(dataset, request).download()
