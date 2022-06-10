import pandas as pd
import sys, getopt
import argparse
import datetime
import os
# # Use argparse to consider the start date and the end date of the data that needs to be merged

parser = argparse.ArgumentParser(description='Generate Sequence fasta with only specific dates and counties.')
parser.add_argument('-s', dest = 'start', help='an integer for the accumulator')
parser.add_argument('-e', dest = 'end', help='an integer for the accumulator')
parser.add_argument('-state', nargs = '?', dest = 'state', default='none', help='file containing seuqences')
parser.add_argument('-predictor', dest = 'pred', help='an integer for the accumulator')
parser.add_argument('-o', dest = 'output', default = "parsed_predictors.csv", help='an integer for the accumulator')
args = parser.parse_args()

# Get the start date and end date from argparse and use it to parse the data frame

startdate = str(args.start)
enddate = str(args.end)
startday = startdate[6:8]
startyear = startdate[0:4]
startmonth = startdate[4:6]
endday = enddate[6:8]
endyear = enddate[0:4]
endmonth = enddate[4:6]

# Read in the predictor file and add a formatted date index

predictor_file = str(args.pred)
df = pd.read_csv(predictor_file)
df['date_formatted'] = pd.to_datetime(df['date'], format = '%Y%m%d')

# Set the index and sort

df = df.set_index(df['date_formatted'])
df = df.sort_index()

# Search the parsed data frame for instances between the two dates from argparse

start = startyear  + startmonth + startday
end = endyear + endmonth + endday
start = df.index.searchsorted(datetime.datetime(int(startyear), int(startmonth), int(startday)))
end = df.index.searchsorted(datetime.datetime(int(endyear), int(endmonth), int(endday)))
parsed_data = df.iloc[start:end]

# Only get the predictor file for the specified state

if(args.state != 'none'):
    parsed_data = parsed_data.loc[parsed_data['State'] == str(args.state)]
del parsed_data['Unnamed: 0']
del parsed_data['date_formatted']

# Export to csv file

parsed_data.to_csv(str(args.output))
