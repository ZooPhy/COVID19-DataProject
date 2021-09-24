#!/usr/bin/python3
#from pandas import compat

#compat.PY3 = True


import pandas as pd
import numpy as np
import time

timestr = time.strftime("%Y%m%d") + ".csv"

# Merge Climate Data with Population Density Data based on FIPS/geo_id
col_list = ["geo_id", "population", "pop_density"]
densityDF = pd.read_csv('us_census_2018_population_estimates_counties.csv', dtype={'geo_id': object}, usecols=col_list, sep=',')

climateDF = pd.read_csv('./climate/climateData.csv', dtype={'FIPS': object}, sep=',')
#travelDF = pd.read_csv("./travel/travelData.csv", dtype={'county_fips': object}, sep=',')


# Climate data merge with density data
densityMerge = climateDF.merge(densityDF, left_on="FIPS", right_on="geo_id")

# Sort through travel data Note: Change once travel data is back working
travelDF = travelDF[travelDF["level"] == "County"]
fipsdataDF = pd.read_csv('./COVID-19/FIPSMetadata.csv', dtype=object, sep=',')
fipsdataDF = fipsdataDF.drop(['State','ExpandedState'], axis=1)
pop_stay_at_home = travelDF.groupby('county_fips', as_index=False)['pop_stay_at_home'].mean()
pop_not_stay_at_home = travelDF.groupby('county_fips', as_index=False)['pop_not_stay_at_home'].mean()
trips = travelDF.groupby('county_fips', as_index=False)['trips'].mean()
travel1 = pop_stay_at_home.merge(pop_not_stay_at_home, on='county_fips')
travel2 = travel1.merge(trips, on='county_fips')
travel2 = travel2.merge(fipsdataDF, left_on='county_fips', right_on='FIPS')
merged = travel2.merge(densityMerge, on='FIPS')
print(merged.columns)
# Merge with COVID data

infoDataFrame = pd.read_csv("./COVID-19/covidData.csv", dtype='object')
infoDataFrame = infoDataFrame.rename(columns={"FIPS_x":"FIPS"})
del infoDataFrame['Unnamed: 0']
print(infoDataFrame, densityMerge)
finalMerge = infoDataFrame.merge(merged, left_on="FIPS", right_on="FIPS")
cols = finalMerge.columns.tolist()
finalMerge.columns = finalMerge.columns.str.strip().str.lower()
print(finalMerge.columns)
finalMerge.to_csv(timestr, encoding='utf-8')
