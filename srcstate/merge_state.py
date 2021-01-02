import pandas as pd
import numpy as np
import time

timestr = time.strftime("%Y%m%d") + "State" + ".csv"

# Merge Climate Data with Population Density Data based on FIPS/geo_id
col_list = ["state", "state_name", "geo_id", "population", "pop_density"]
densityDF = pd.read_csv('us_census_2018_population_estimates_states.csv', dtype={'geo_id': object}, usecols=col_list, sep=',')
densityDF = densityDF.drop(["state_name", "geo_id"], axis=1)
climateDF = pd.read_csv('./climate_state/climateData.csv', dtype={'FIPS': object}, sep=',')
travelDF = pd.read_csv("./travel_state/travelData.csv", dtype={'county_fips': object}, sep=',')



#Output final data
densityMerge = climateDF.merge(densityDF, left_on="State", right_on="state")
travelDF = travelDF[travelDF["level"] == "State"]
travelDF = travelDF.rename(columns={"county_fips":"FIPS"})
pop_stay_at_home = travelDF.groupby('state_code', as_index=False)['pop_stay_at_home'].mean()
pop_not_stay_at_home = travelDF.groupby('state_code', as_index=False)['pop_not_stay_at_home'].mean()
trips = travelDF.groupby('state_code', as_index=False)['trips'].mean()
travel1 = pop_stay_at_home.merge(pop_not_stay_at_home)
travel2 = travel1.merge(trips)
merged = travel2.merge(densityMerge, left_on='state_code', right_on='state')


# Merge w COVID data
infoDataFrame = pd.read_csv("./covid_state/covidData.csv", dtype='object')
infoDataFrame = infoDataFrame.rename(columns={"FIPS_x":"FIPS"})
del infoDataFrame['Unnamed: 0']
del densityMerge['state']
finalMerge = infoDataFrame.merge(densityMerge, left_on="State", right_on="State")
cols = finalMerge.columns.tolist()


finalMerge.to_csv(timestr, encoding='utf-8')
