# Weekly data read w/ cron script
# Merge Temp and Travel data
# Calculate ratios
#Dependent on FIPSDATA.csv

import pandas as pd
import numpy as np

cases_data_frame = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
deaths_data_frame = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

metadata_frame = cases_data_frame.iloc[:, 0:10] #define metadata as new dataframe

# Define new data frames for raw data, ongoing as new data is added to github
case_data = cases_data_frame.iloc[:,11:]
death_data = deaths_data_frame.iloc[:,11:]

rows, columns = cases_data_frame.shape #Count of rows and columns

# Cummulative sum calculation for cases and death
case_data['sum'] = case_data[list(case_data.columns)].sum(axis=1)
death_data['sum'] = death_data[list(death_data.columns)].sum(axis=1)

# Define new columns for ongoing death and case information
# This is provided by the github repo as a running total (no need to find cummulative case count)
metadata_frame["Cases"]= cases_data_frame.iloc[:,[columns-1]]
metadata_frame["Deaths"]= deaths_data_frame.iloc[:,[columns-1]]
# Export Data Frame to CSV file
#metadata_frame.to_csv('new_covid_data.csv')
station_data = pd.read_csv('FIPSMetadata.csv', dtype=object)


station_data.columns = ['FIPS', 'Admin2', 'State', 'ExpandedState']

mergedData = station_data.merge(metadata_frame, left_on=["Admin2", "ExpandedState"], right_on=["Admin2", "Province_State"])
mergedData = mergedData.reindex(columns = ['FIPS_x', 'Admin2', 'State', 'UID', 'iso2', 'iso3', 'code3', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Cases', 'Deaths'])
mergedData.to_csv('covidData.csv', encoding='utf-8')
