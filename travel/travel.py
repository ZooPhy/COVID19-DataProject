# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.bts.gov", None)

import pandas as pd
import numpy as np
from sodapy import Socrata
from datetime import date, timedelta
import os
import sys, getopt
import argparse
import time
from tqdm import tqdm

# Define a new directory to store the data 

os.system('mkdir -p data')

try:
    # Authenticated client (needed for non-public datasets):
    
    overall_start = time.time()
    client = Socrata("data.bts.gov","-----token here-----",username="-----email-----",password="-----password-----")
    
    # Use argparse to consider the start date and the end date of the data that needs to be queried
    
    parser = argparse.ArgumentParser(description='Pull daily travel data.')
    parser.add_argument('-s', dest = 'start', help='start date YYYYMMDD')
    parser.add_argument('-e', dest = 'end', help='end date YYYYMMDD')
    args = parser.parse_args()

    # Define function for date range

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    # Allow argparse to determine the date range to query data from

    start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
    end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))
    delta = end_dt - start_dt
    
    # Iterate through the date range
    with tqdm(total=delta.days, unit_scale = True) as pbar:
        for dt in daterange(start_dt, end_dt):

            pbar.update(1)
            
            # Query the data and specity a conditional WHERE statement to only query data
            # from a specific date

            querydate = dt.strftime('%Y-%m-%d')
            query = "date = " + "'" + querydate + "'" 
            query_results = client.get("w96p-f2qv", where = query , limit=30000)

            # Convert to pandas DataFrame

            travel_results_df = pd.DataFrame.from_records(query_results)
            filename = dt.strftime('%Y%m%d') + '-travel.csv'
            travel_results_df.to_csv('./data/' + filename,  encoding='utf-8')
    overall_end = time.time()
    print("BTS Travel Data from " + str(start_dt) + " to " + str(end_dt) + " successfully pulled in "  + str(overall_end-overall_start) + " seconds.")  
except Exception as e:
    print("Encountered Exception: " + str(e))
    sys.exit(1)
