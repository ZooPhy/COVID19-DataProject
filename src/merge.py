import pandas as pd
import numpy as np
import time

timestr = time.strftime("%Y%m%d") + ".csv"
# Merge Climate Data with Population Density Data based on FIPS/geo_id
col_list = ["geo_id", "population", "pop_density"]
densityDF = pd.read_csv('us_census_2018_population_estimates_counties.csv', dtype={'geo_id': object}, usecols=col_list, sep=',')
climateDF = pd.read_csv('./climate/climateData.csv', dtype={'FIPS': object}, sep=',')
travelDF = pd.read_csv("./travel/travelData.csv", dtype={'county_fips': object}, sep=',')


#Output final data
densityMerge = climateDF.merge(densityDF, left_on="FIPS", right_on="geo_id")
cols = ['FIPS', 'TempMedian', 'TempMean', 'PrcpMedian', 'PrcpMean', "population", "pop_density"]

travelDF = travelDF[travelDF["level"] == "County"]
travelDF = travelDF.rename(columns={"county_fips":"FIPS"})

pop_stay_at_home = travelDF.groupby('FIPS', as_index=False)['pop_stay_at_home'].mean()
pop_not_stay_at_home = travelDF.groupby('FIPS', as_index=False)['pop_not_stay_at_home'].mean()
trips = travelDF.groupby('FIPS', as_index=False)['trips'].mean()

travel1 = pop_stay_at_home.merge(pop_not_stay_at_home)
travel2 = travel1.merge(trips)

merged = travel2.merge(densityMerge, on='FIPS')
cols = merged.columns.tolist()
cols = ['state_fips', 'state_code', 'FIPS', 'county', 'TempMedian', 'TempMean', 'PrcpMedian', 'PrcpMean', 'population', 'pop_density', 'pop_stay_at_home', 'pop_not_stay_at_home', 'trips']


# Merge with COVID data
infoDataFrame = pd.read_csv("./COVID-19/covidData.csv", dtype='object')
infoDataFrame = infoDataFrame.rename(columns={"FIPS_x":"FIPS"})
del infoDataFrame['Unnamed: 0']
print(infoDataFrame.columns)
finalMerge = infoDataFrame.merge(merged, left_on="FIPS", right_on="FIPS")
cols = finalMerge.columns.tolist()

finalMerge.to_csv(timestr, encoding='utf-8')
