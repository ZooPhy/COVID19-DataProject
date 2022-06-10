#!/usr/bin/python3
#from pandas import compat

#compat.PY3 = True

# Imports 

import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
from datetime import date, timedelta
import sys, getopt
import argparse
import os
from tqdm import tqdm

# Define a new directory to store the data 

os.system('mkdir -p data-with-vaccine')


# Use argparse to consider the start date and the end date of the data that needs to be merged

parser = argparse.ArgumentParser(description='Generate Sequence fasta with only specific dates and counties.')
parser.add_argument('-s', dest = 'start', help='start date YYYYMMDD')
parser.add_argument('-e', dest = 'end', help='start date YYYYMMDD')
parser.add_argument('-state', dest = 'state', help='state to consider predictors for')
parser.add_argument('-counties', nargs = '*', dest = 'counties',  default = None, help='counties in args.state to consider predictors for (default. - pull all counties from args.state')
args = parser.parse_args()

# List of columns that should be included in the final data set
cols = ['date', 'FIPS', 'Admin2', 'State', 'UID', 'iso2',
       'iso3', 'code3', 'Lat', 'Long_', 'census2019', 'census2019_5pluspop', 'census2019_12pluspop', 'census2019_18pluspop', 'census2019_65pluspop', 'Cases', 'Deaths', 'TempMedian', 'TempMean', 'PrcpMedian', 'PrcpMean', 'population', 'pop_density',
       'mmwr_week', 'series_complete_pop_pct',
       'series_complete_yes', 'series_complete_12plus', 'series_complete_18plus', 'series_complete_65plus', 'completeness_pct',
       'administered_dose1_recip', 'administered_dose1_pop_pct',
       'administered_dose1_recip_12plus',
       'administered_dose1_recip_12pluspop_pct',
       'administered_dose1_recip_18plus',
       'administered_dose1_recip_18pluspop_pct',
       'administered_dose1_recip_65plus',
       'administered_dose1_recip_65pluspop_pct', 'svi_ctgy',
       'series_complete_pop_pct_svi', 'series_complete_12pluspop_pct_svi',
       'series_complete_18pluspop_pct_svi',
       'series_complete_65pluspop_pct_svi', 'metro_status',
       'series_complete_pop_pct_ur_equity',
       'series_complete_12pluspop_pct_ur_equity',
       'series_complete_18pluspop_pct_ur_equity',
       'series_complete_65pluspop_pct_ur_equity', 'administered_dose1_recip_5plus',
       'administered_dose1_recip_5pluspop_pct', 'series_complete_5plus',
       'series_complete_5pluspop_pct', 'series_complete_5pluspop_pct_svi',
       'series_complete_5pluspop_pct_ur_equity', 'booster_doses',
       'booster_doses_18plus', 'booster_doses_50plus', 'booster_doses_65plus',
       'booster_doses_vax_pct', 'booster_doses_18plus_vax_pct',
       'booster_doses_50plus_vax_pct', 'booster_doses_65plus_vax_pct', 'pop_stay_at_home','pop_not_stay_at_home','trips']

# Define function for date range

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

# Allow argparse to determine the date range to query data from

start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))
aggregate_frame  = pd.DataFrame(columns = cols)
state_subset  = pd.DataFrame()

travel_delimiter = (date.today() - timedelta(days = 21)).strftime("%Y%m%d")
overall_start = time.time()
delta = end_dt - start_dt
with tqdm(total=delta.days, unit_scale = True) as pbar:
    for dt in daterange(start_dt, end_dt):
        
        pbar.update(1)  
        # Consider the following filenames. It is neccesary to have run merge.py before this step.
        # Travel data and vaccination data also need to be available.

        vaccine_filename = dt.strftime("%Y%m%d") + "-vaccine.csv"
        merge_import_filename = dt.strftime("%Y%m%d") + ".csv"

        # Define the merged data

        merged_frame = pd.read_csv('./data/' + merge_import_filename)

        # If the current data is after the first instance of a COVID-19 vaccination (Dec. 13 2020),
        # merge to the vaccination data.

        if dt.strftime("%Y%m%d") >= '20201213':
            vaccine_frame = pd.read_csv('./vaccine/data/' + vaccine_filename)
            merged_frame = merged_frame.merge(vaccine_frame, left_on="FIPS", right_on='fips')

        # Delete unnormalized columns

        if 'Unnamed: 0_x' in merged_frame:
            del merged_frame['Unnamed: 0_x']
        if 'Unnamed: 0' in merged_frame:
            del merged_frame['Unnamed: 0']
        if 'unnamed: 0' in merged_frame:
            del merged_frame['unnamed: 0']
        if 'date' in merged_frame:
            del merged_frame['date']

        # Insert in a new (normalized) date into the data frame

        merged_frame.insert(0, 'date', dt.strftime("%Y%m%d"))

        # If the date is before the last instance of travel data (generally 2-3 week lag),
        # merge with the travel data

        if dt.strftime("%Y%m%d") <= str(travel_delimiter):

            # Consider the following filename for the travel data

            travel_filename = dt.strftime("%Y%m%d") + "-travel.csv"
            travel_frame = pd.read_csv('./travel/data/' + travel_filename)

            # Merge the travel data to the merged frame

            merged_frame = merged_frame.merge(travel_frame[['county_fips','pop_stay_at_home','pop_not_stay_at_home','trips']], left_on="FIPS", right_on='county_fips')

        # Merge the current frame with an aggregate_frame frame, which includes data from all dates
        aggregate_frame = pd.concat([aggregate_frame, merged_frame], ignore_index = True, axis = 0, copy=False)
        
# After processing the aggregate data frame, it is necessary to subset the data to the specified
# state and/or counties
overall_end = time.time()

aggregate_frame.to_csv('usa_aggregate.csv', encoding = 'utf-8')
aggregate_frame = aggregate_frame[cols]
aggregate_frame = aggregate_frame.fillna(0)

# Consider the following columns as integers

aggregate_frame[['Cases', 'Deaths','population','pop_density', 'UID']] = aggregate_frame[['Cases', 'Deaths','population','pop_density', 'UID']].astype(int)

# If the counties of the state to subset were specified, subset the aggregate data based on both and export.
# Otherwise, just subset based on the state and export.
print(aggregate_frame['FIPS'])
if(args.counties is not None):
    aggregate_frame = aggregate_frame.astype({'FIPS': int})
    county = [int(j) for j in args.counties]
    aggregate_frame = aggregate_frame.loc[aggregate_frame['FIPS'].isin(county)]
    aggregate_frame = aggregate_frame.loc[aggregate_frame['State']  == str(args.state)]
    aggregate_frame.to_csv(str(args.state) + '_aggregate.csv', encoding = 'utf-8')
    print(aggregate_frame)
else:
    state_subset = aggregate_frame[aggregate_frame['State'] == str(args.state)]
    state_subset.to_csv(str(args.state) + '_aggregate.csv', encoding = 'utf-8')

# Move the two generated files to the pre-alignment folder.

os.system('mv usa_aggregate.csv ' + str(args.state) + '_aggregate.csv ./pre-alignment/predictors')
print("Time Elapsed for Data Merge: ", overall_end-overall_start)
