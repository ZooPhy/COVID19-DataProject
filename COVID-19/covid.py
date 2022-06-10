# Weekly data read w/ cron script
# Merge Temp and Travel data
# Calculate ratios
#Dependent on FIPSDATA.csv

import pandas as pd
import numpy as np
import time
from datetime import date, timedelta
from datetime import datetime
from datetime import timedelta
import os
from tqdm import tqdm
import sys
import argparse

# Create a new directory to store the data and read in the data from the provided data
# table from the Johns Hopkins git page
parser = argparse.ArgumentParser(description='Pull county level COVID-19 data.')
parser.add_argument('-s', dest = 'start', help='start date YYYYMMDD')
parser.add_argument('-e', dest = 'end', help='end date YYYYMMDD')
args = parser.parse_args()

os.system('mkdir -p data')
try:
    overall_start = time.time()
    cases_data_frame = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
    deaths_data_frame = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

    # Define the metadata of the data as a new dataframe (first 10 lines)

    covid_frame = cases_data_frame.iloc[:, 0:10] 

    # Define new data frames for raw data, ongoing as new data is added to github  
    # each column past the 10th column defines a new date

    case_data = cases_data_frame.iloc[:,11:]
    death_data = deaths_data_frame.iloc[:,11:]

    # Count of rows and columns

    rows, columns = cases_data_frame.shape 

    # Cummulative sum calculation for cases and death
    case_data['sum'] = case_data[list(case_data.columns)].sum(axis=1)
    death_data['sum'] = death_data[list(death_data.columns)].sum(axis=1)

    # Consider the following date range

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    # Collect data from the beginning of data recording (Jan 22 2020) until yesterday

    reference_start_dt = date(2020, 1, 22) 
    start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
    end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))

    # Iterate through the date range and pull the corresponding column (depends on iterator n)
    reference_delta = start_dt - reference_start_dt
    n = reference_delta.days

    delta = end_dt - start_dt
    with tqdm(total=delta.days, unit_scale = True) as pbar:
        for dt in daterange(start_dt, end_dt):
            
            # Add data
           
            pbar.update(1)
            covid_frame["Cases"]= cases_data_frame.iloc[:,[11+n]]
            covid_frame["Deaths"]= deaths_data_frame.iloc[:,[11+n]]

            # Import the climate station data

            county_metadata = pd.read_csv('FIPSMetadata.csv', dtype=object)
            county_metadata.columns = ['FIPS', 'Admin2', 'State', 'ExpandedState']

            # Merge the COVID data (metadata_frame) with the climate metadata (station_data)

            mergedData = county_metadata.merge(covid_frame, left_on=["Admin2", "ExpandedState"], right_on=["Admin2", "Province_State"])
            mergedData = mergedData.reindex(columns = ['FIPS_x', 'Admin2', 'State', 'UID', 'iso2', 'iso3', 'code3', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Cases', 'Deaths'])

            # Export and update iterator

            timestr = dt.strftime("%Y%m%d") + "-covid.csv"
            mergedData.columns = mergedData.columns.str.rstrip('_x') 
            mergedData.to_csv("./data/" + timestr, encoding='utf-8')
            n = n + 1
    overall_end = time.time()
    print("COVID-19 Data Pulled Successfully in " + str(overall_end-overall_start)  + " seconds.")
except Exception as e:
    print("Encountered Exception: " + str(e))
    sys.exit(1)
