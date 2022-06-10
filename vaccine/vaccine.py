#!/usr/bin/env python

# Imports

import pandas as pd
from sodapy import Socrata
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import sys, getopt
import argparse
from tqdm import tqdm

# Define a new directory to store the data 

os.system('mkdir -p data')

# Use argparse to consider the start date and the end date of the data that needs to be queried
try:
    overall_start = time.time()
    parser = argparse.ArgumentParser(description='Pull daily vaccination data.')
    parser.add_argument('-s', dest = 'start', help='start date YYYYMMDD')
    parser.add_argument('-e', dest = 'end', help='end date YYYYMMDD')
    args = parser.parse_args()


    # Authenticated client (needed for non-public datasets):

    client = Socrata("data.cdc.gov","-----token-----",username="-----username-----",password="-----password-----")

    # Define function for date range

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    # Allow argparse to determine the date range to query data from (First vaccination data is Dec 13, 2020)

    if(str(args.start) >= str(20201213)):
        start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
    else:
        start_dt = date(2020, 12, 13)
    end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))

    # Iterate through the date range
    
    delta = end_dt - start_dt
        
    with tqdm(total=delta.days, unit_scale = True) as pbar:
        for dt in daterange(start_dt, end_dt):

            pbar.update(1)
            
            # Query the data and specity a conditional WHERE statement to only query data
            # from a specific date

            query_date = dt.strftime('%Y-%m-%d') + "T00:00:00.000"
            query = "date = " + "'" + query_date + "'" 
            query_result = client.get("8xkx-amqh", where = query, limit=702106)

            # Convert to pandas DataFrame
            vaccine_results_df = pd.DataFrame.from_records(query_result)
            vaccine_results_df = vaccine_results_df[vaccine_results_df['date'] == query_date]
            vaccine_results_df = vaccine_results_df[vaccine_results_df.fips.apply(lambda x: x.isnumeric())]
            filename = dt.strftime('%Y%m%d')
            vaccine_results_df.to_csv('./data/' + filename + "-vaccine.csv", encoding='utf-8')
    overall_end = time.time()
    print("CDC Vaccine Data from " + str(start_dt) + " to " + str(end_dt) + " successfully pulled in "  + str(overall_end-overall_start) + " seconds.")  
except Exception as e:
    print("Encountered Exception: " + str(e))
    sys.exit(1)
