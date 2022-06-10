import pandas as pd
import sys, getopt
import argparse
import datetime
import numpy as np

# Use argparse to consider the start date and the end date of the data that needs to be merged

parser = argparse.ArgumentParser(description='Generate Sequence fasta with only specific dates and counties.')
parser.add_argument('-predictor', dest = 'pred', help='an integer for the accumulator')
args = parser.parse_args()

# Columns to exclude from the statistics

exclude = ["date", "FIPS", "UID", "code3", "Lat", "Long_", "Unnamed: 0"]

# Read in the predictor file and exclude certain columns

predictor_file = str(args.pred)
df = pd.read_csv(predictor_file)
df = df.loc[:, ~df.columns.isin(exclude)]

# Group by mean

df2 = df.copy(deep = True)
df2 = df.groupby('Admin2', as_index=True).mean()
df2 = df2.add_suffix('_average')

# Group by median 

df3 = df.groupby('Admin2', as_index=True).median()
df3 = df3.add_suffix('_median')

# Group by variance
df5 = df.groupby('Admin2', as_index=True).var()
df5 = df5.add_suffix('_var')

# Merging data frames
df4 = df2.merge(df3, left_on='Admin2', right_on='Admin2')
df4 = df4.merge(df5, left_on='Admin2', right_on='Admin2')
df4.to_csv('stats.csv', encoding = 'utf-8')
