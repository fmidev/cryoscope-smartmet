#!/usr/bin/env python
import cdsapi
import sys
# CMIP6 monthly 1995-2014 (historical) Europe

mod=sys.argv[1]
var=sys.argv[2]

target='/home/ubuntu/data/cmip6/%s_%s_1995-2014_CMIP6_monthly_euro.zip'%(mod,var)
print(target)

c = cdsapi.Client()

c.retrieve(
    'projections-cmip6',
    {
        'format': 'zip',
        'temporal_resolution': 'monthly',
        'experiment': 'historical',
        'level': 'single_levels',
        'variable': var,
        'model': mod,
        'date': '1995-01-01/2014-12-31',
        'area': [
            75, -30, 25,
            50,
        ],
    },
    dataset)

