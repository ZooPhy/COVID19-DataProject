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
results = client.get("8xkx-amqh", limit=702106)
results_df = pd.DataFrame.from_records(results)
print(results_df['date'])
var = datetime.today()
var = var - timedelta(days = 1)
var = var.strftime('%Y-%m-%d') + "T00:00:00.000"
print(var)
print(len(results_df))
results_df = results_df[results_df['date'] == var]
print(len(results_df))
results_df = results_df[results_df.fips.apply(lambda x: x.isnumeric())]
print(len(results_df))
results_df.to_csv("data.csv")
