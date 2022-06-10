#!/usr/bin/python3

# Imports
import os
import sys, getopt
import argparse
from datetime import datetime
from datetime import date, timedelta
import pandas as pd
import numpy
# Use argparse to consider what to do with the pipeline
# It is neccesary to include a start date, an end date, and a state to subset the data by
# Sequences are not a necessary requirement

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
-------------------------------------------------------------------------------------------------
Generate a csv file containing COVID-19 predictor data.
-------------------------------------------------------------------------------------------------
The output csv is ./results/parsed_predictors.csv.
If a sequence file is included, pre-alignment results can be found in the ./pre-alignment folder.
The following example command will use county names to pull predictor data from
between 01.01.2022 and 01.05.2022 from Hennepin County, MN and Olmsted County, MN.
---------------------------------------------------------------------------------------------------------------------
Example Command: python3 run_sequences.py -start 20220101 -end 20220105 -codes 0 -state MN -counties Hennepin Olmsted
---------------------------------------------------------------------------------------------------------------------''')
parser.add_argument('-start', dest = 'start', help='start date YYYYMMDD')
parser.add_argument('-end', dest = 'end', help='end date YYYYMMDD')
parser.add_argument('-codes', dest = 'codes', default = 0, help='use county names (0) or fips codes (1)')
parser.add_argument('-seq', nargs ='*', dest = 'seq', default = None, help='file containing seuqences')
parser.add_argument('-state', dest = 'state', default = None, help='state abbreviation to pull data from (use two letter code)')
parser.add_argument('-counties', nargs = '*', dest = 'counties', default = None, help='county names/county FIPS codes to pull data from (space delimited list)')
parser.add_argument('-pred', nargs = '*', dest = 'pred', default = None, help='predictor file name')
parser.add_argument('-climate', dest = 'climate', action = 'store_const', const = 1, help='specify this option to pull climate data.')

args = parser.parse_args()
county_list = []
for i in args.counties:
    county_list.append(i)
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",  "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC", "American Samoa": "AS",
    "Guam": "GU", "Northern Mariana Islands": "MP", "Puerto Rico": "PR", "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

# Make sure that all of the arguments provided are valid

start_dt = date(int(args.start[0:4]), int(args.start[4:6]), int(args.start[6:8]))
end_dt = date(int(args.end[0:4]), int(args.end[4:6]), int(args.end[6:8]))
reference_start_dt = date(2020, 1, 22)
today = date.today()


if (start_dt.strftime("%Y%m%d") <= reference_start_dt.strftime("%Y%m%d")):
    print("Start date out of range. Did you use a date before the start of the COVID-19 pandemic (01/22/2020) or after today's current date?")
    sys.exit(1)
    
if (end_dt.strftime("%Y%m%d") >= today.strftime("%Y%m%d")):
    print("End date out of range. Did you use a date after today's current date or before 01/22/2020?")
    sys.exit(1)
    
if (args.state is None or str(args.state) not in us_state_to_abbrev.values()):
    print("Must specify a 2-Letter state code. Did you specify [-state state_name]?")
    sys.exit(1)


df = pd.read_csv('./COVID-19/FIPSMetadata.csv', dtype=object)
df.columns = ['FIPS', 'Admin2', 'State', 'ExpandedState'] 
if (int(args.codes) == 0):    
    for i in args.counties:
        if df['Admin2'].str.contains(i).any():
            continue
        else:
            print("County with name " + str(i) + " not found in FIPSMetadata.csv.")
            print("Perhaps you meant to use the option for FIPS codes [-codes 1]?")
            sys.exit(1)

elif (int(args.codes) == 1):
    for i in args.counties:
        if df['FIPS'].str.contains(i).any():
            continue
        else:
            print("County with FIPS code " + str(i) + " not found in FIPSMetadata.csv.")
            print("Perhaps you meant to use the option for county names [-codes 0]?")
            sys.exit(1)
else:
    print("You have specified an invalid value for codes. Make sure that either 0 (county names) or 1 (FIPS code) are used.")
    sys.exit(1)

if (int(args.codes) == 0 and args.counties is not None):
    counties_list = ''
    for i in args.counties:
        df2 = df.loc[df['Admin2'] == i]
        df3 = df2.loc[df2['State'] == str(args.state)]
        counties_list += '\'' + str(df3['FIPS'].values[0]) + '\' '

if (int(args.codes) == 1 and args.counties is not None):
    counties_list = ''
    for i in args.counties:
        df2 = df.loc[df['FIPS'] == i]
        df3 = df2.loc[df2['State'] == str(args.state)]
        counties_list += '\'' + str(df3['FIPS'].values[0]) + '\' '

# Check to see if climate data should be re-pulled.

if (args.climate == 1):
    print('----------------------------\n----------------------------\n----------------------------\n\nWARNING: Pulling new climate data from current weather station data.\n\n----------------------------\n----------------------------\n----------------------------')
    os.system('cd climate && bash downloadClimateData.bash')
    os.system('cd climate && python3 climate.py')

# System calls are used to pull the COVID data, travel data, vaccination data, and climate data.

os.system('cd COVID-19 && python3 covid.py -s ' + str(args.start) + ' -e ' + str(args.end))
os.system('cd travel && python3 travel.py -s ' + str(args.start) + ' -e ' + str(args.end))
os.system('cd vaccine && python3 vaccine.py -s ' + str(args.start) + ' -e ' + str(args.end))

# system calls are used to run the first merge

os.system('python3 merge_prelim.py -s ' + str(args.start) + ' -e ' + str(args.end))

# system calls are used to run the second merge
if (args.counties is not None):
    os.system('python3 merge_finalize.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -state ' + str(args.state) + ' -counties ' + counties_list)
else:
    os.system('python3 merge_finalize.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -state ' + str(args.state))
# If the sequences and predictor file are not provided, and the counties argument is provided, read the predictor file
# according to the output of merge2.py. system calls are used to run the predictor sort and stats.

if(args.seq is None):
    if(args.pred is None):
        predictor = str(args.state) + '_aggregate.csv'
        os.system('cd pre-alignment/predictors && python3 predictor_sort.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -state ' + str(args.state) + ' -pred ' + str(predictor))
        os.system('cd pre-alignment/predictors && python3 stats.py -pred parsed_predictors.csv')
    elif(args.pred != 'none'):
        os.system('cd pre-alignment/predictors && python3 predictor_sort.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -pred ' + str(args.pred))
        
elif(args.seq is not None):
    if(args.pred is None):
        predictor = str(args.state) + '_aggregate.csv'
        os.system('cd pre-alignment/predictors && python3 predictor_sort.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -state ' + str(args.state) + ' -pred ' + str(predictor))
        os.system('cd pre-alignment/predictors && python3 stats.py -pred parsed_predictors.csv')
    elif(args.pred is not None):
        os.system('cd pre-alignment/predictors && python3 predictor_sort.py -s ' + str(args.start) + ' -e ' + str(args.end) + ' -pred ' + str(args.pred))

# Cleanup files
if(args.climate == 1):
    os.system('cd climate && rm 2020* && rm F-* && rm sortedClimateDownload.csv && rm from_download.csv')
os.system('rm -r COVID-19/data && rm -r vaccine/data && rm -r travel/data && rm -r data')
os.system('mkdir -p results && cp pre-alignment/predictors/parsed_predictors.csv results')
os.system('rm pre-alignment/predictors/' + str(predictor))
