#!/usr/bin/python3
#from pandas import compat

#compat.PY3 = True

# Imports

import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
import sys, getopt
import argparse

# Define a new directory to store the data 

os.system('mkdir -p data')

# Define function for date range

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
        
# Use argparse to consider the start date and the end date of the data that needs to be merged

parser = argparse.ArgumentParser(description='Merge county metadata, census data, covid data and climate data.')
parser.add_argument('-s', dest = 'start', help='start date YYYYMMDD')
parser.add_argument('-e', dest = 'end', help='end date YYYYMMDD')
args = parser.parse_args()

# Allow argparse to determine the date range to query data from

start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))

# Iterate through the date range

for dt in daterange(start_dt, end_dt):
    
    # Define the filenames to merge on - it is neccesary to have queried climate data,
    # covid data, travel data, and vaccination data before merging 
    
    export_filename = dt.strftime('%Y%m%d') + '.csv'
    covid_filename =  dt.strftime("%Y%m%d") + "-covid.csv"

    # Define the population density data from census csv file
    
    census_col_list = ["geo_id", "population", "pop_density"]
    population_frame = pd.read_csv('us_census_2018_population_estimates_counties.csv', dtype={'geo_id': object}, usecols=census_col_list, sep=',')
    population_frame = population_frame.rename(columns={"geo_id":"FIPS"})

    # Define the county metadata from csv file
    
    county_metadata_frame = pd.read_csv('./COVID-19/FIPSMetadata.csv', dtype=object, sep=',')
    county_metadata_frame = county_metadata_frame.drop(['State','ExpandedState'], axis=1)
    
    # Define the COVID-19 data frame dependent on the data located in ./COVID-19/data

    covid_frame = pd.read_csv("./COVID-19/data/" + covid_filename, dtype='object')
    covid_frame = covid_frame.rename(columns={"FIPS_x":"FIPS"})

    # Merge the population density data and the county metadata
    
    metadata_merge = population_frame.merge(county_metadata_frame, left_on="FIPS", right_on="FIPS")
    covid_merge = covid_frame.merge(metadata_merge, left_on="FIPS", right_on="FIPS")

    # Define the climate data from climateData.csv
    
    climate_frame = pd.read_csv('./climate/climateData.csv', dtype=object, sep=',')
    
    # Make sure that the FIPS column is a string
    
    climate_frame['FIPS']=climate_frame['FIPS'].astype('string')
    covid_merge['FIPS']=covid_merge['FIPS'].astype('string')
    covid_merge = covid_merge.join(climate_frame.set_index('FIPS'), on="FIPS", how="outer")
    
    # Export merged datafile
    
    covid_merge.to_csv('./data/' + export_filename, encoding='utf-8')
