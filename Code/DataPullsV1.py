#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
from sodapy import Socrata


# In[60]:


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.bts.gov", None)

#Example authenticated client (needed for non-public datasets):
client = Socrata("data.bts.gov",
                 "9gUBYw5E3QOLsHxfn8R51Jfxb",
                  username="masauer2@asu.edu",
                password="MSauer200o!")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("w96p-f2qv", limit=2117622)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("travel.csv")


# In[ ]:


# Merge Temp and Travel data
# - old - 
import pandas

tempData = pandas.read_csv("out.csv", dtype='object')
tempDF = pandas.DataFrame(tempData)
travelData = pandas.read_csv("travel.csv", dtype='object')
travelDF = pandas.DataFrame(travelData)
output = tempDF.merge(travelDF, on='county_fips')
output.to_csv("mergedCOVIDTraveldata.csv")


# In[53]:


# Weekly data read w/ cron script
# Merge Temp and Travel data
# Calculate ratios

countyDf = pd.read_csv("travel.csv", dtype='object')
county_data = countyDf[countyDf["level"] == "County"]
#print(county_data[["county_fips", "date", "pop_stay_at_home","trips_1","trips_1_3","trips_3_5","trips_5_10", "trips_10_25", "trips_25_50", "trips_50_100", "trips_100_250", "trips_250_500"]])
weather = pd.read_csv("out.csv", dtype='object')
merged = county_data.merge(weather, on='county_fips')
merged.drop(columns=['level','Unnamed: 0'])
merged['pop_stay_at_home'] = pd.to_numeric(merged['pop_stay_at_home'])
merged['pop_not_stay_at_home'] = pd.to_numeric(merged['pop_not_stay_at_home'])
merged["PercentStayAtHome"] = merged['pop_stay_at_home']/(merged['pop_stay_at_home']+merged['pop_not_stay_at_home'])
merged["PercentNotStayAtHome"] = merged['pop_not_stay_at_home']/(merged['pop_stay_at_home']+merged['pop_not_stay_at_home'])
cols = merged.columns.tolist()
cols = ['date', 'state_fips', 'state_code', 'county_fips', 'county', 'TempMedian', 'TempMean', 'PrcpMedian', 'PrcpMean', 'population', 'pop_density', 'PercentStayAtHome', 'PercentNotStayAtHome', 'pop_stay_at_home', 'pop_not_stay_at_home', 'trips', 'trips_1', 'trips_1_3', 'trips_3_5', 'trips_5_10', 'trips_10_25', 'trips_25_50', 'trips_50_100', 'trips_100_250', 'trips_250_500', 'trips_500']
merged = merged[cols]
merged = merged.rename(columns={'county_fips':'FIPS'})
merged.to_csv("traveloutput.csv")


# In[22]:


# Case and Death data download
import pandas as pd

# Import csv files from github repo
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
metadata_frame.to_csv('new_covid_data.csv')

station_data = pd.read_csv("FIPSDATA.csv", dtype='object')
station_data.columns = ['FIPS', 'Admin2', 'State']

mergedData = station_data.merge(metadata_frame, on="Admin2")
mergedData = mergedData.reindex(columns = ['FIPS_x', 'Admin2', 'State', 'UID', 'iso2', 'iso3', 'code3', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Cases', 'Deaths'])
mergedData.to_csv('caseData.csv')


# In[61]:


#Aggregate data

import pandas as pd


travelDataFrame = pd.read_csv("traveloutput.csv", dtype='object')
infoDataFrame = pd.read_csv("caseData.csv", dtype='object')
infoDataFrame.columns = (['Unnamed: 0','FIPS', 'Admin2', 'State', 'UID', 'iso2', 'iso3', 'code3',
       'Province_State', 'Country_Region', 'Lat', 'Long_', 'Cases', 'Deaths'])
del infoDataFrame['Unnamed: 0']

finalMerge = infoDataFrame.merge(travelDataFrame, on='FIPS')
cols = finalMerge.columns.tolist()
del finalMerge['Unnamed: 0']

finalMerge.to_csv('aggregateDataFile.csv')


# In[ ]:




