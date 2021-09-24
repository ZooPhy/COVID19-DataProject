#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import dask.dataframe as dd
from datetime import datetime
from datetime import timedelta

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cdc.gov", "9gUBYw5E3QOLsHxfn8R51Jfxb", username="masauer2@asu.edu", password="MSauer200o!")

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cdc.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 702106 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("8xkx-amqh", limit=807130)
results_df = pd.DataFrame.from_records(results)
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 9, 1)
end_date = date(2021, 9, 15)
for single_date in daterange(start_date, end_date):
        var = single_date.strftime("%Y-%m-%d") + "T00:00:00.000"
	varToPrint = single_date.strftime("%Y%m%d") + "-vaccine"
	print("DATAFRAME\n")
	print(results_df['date'])
	print("VAR\n" + var)
	results = results_df[results_df['date'] == var]
	print(len(results))
	results = results[results.fips.apply(lambda x: x.isnumeric())]
	print(len(results))
	results.to_csv(varToPrint + ".csv")
