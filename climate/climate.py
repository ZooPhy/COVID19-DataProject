import pandas as pd
import numpy as np
import os 

# climate.py takes the downloaded data (climateData.py) and takes the statistics for each recorded daily data

collist = ["Station", "Date", "Temp", "Prcp", "County", "FIPS"]
df = pd.read_csv('from_download.csv', names = collist, dtype={'FIPS': object}, sep=',')

# Take the mean and the meadian of the Temperature and the Precipitation

temp_median = df.groupby('FIPS', as_index=False)['Temp'].median()
temp_mean = df.groupby('FIPS', as_index=False)['Temp'].mean()
prcp_median = df.groupby('FIPS', as_index=False)['Prcp'].median()
prcp_mean = df.groupby('FIPS', as_index=False)['Prcp'].mean()

#Rename columns

temp_median_rename = temp_median.rename(columns={"Temp":"TempMedian"})
prcp_median_rename = prcp_median.rename(columns={"Prcp":"PrcpMedian"})
temp_mean_rename = temp_mean.rename(columns={"Temp":"TempMean"})
prcp_mean_rename = prcp_mean.rename(columns={"Prcp":"PrcpMean"})

#Merge the columns based on FIPS code and save to climate data again

tempMerge = temp_median_rename.merge(temp_mean_rename)
prcpMerge = tempMerge.merge(prcp_median_rename)
climateMerge = prcpMerge.merge(prcp_mean_rename)
os.system('mv climateData.csv climateData_BACKUP.csv')
climateMerge.to_csv('climateData.csv', index=False)
