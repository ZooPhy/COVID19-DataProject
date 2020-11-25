# case and Death data download
import pandas as pd
#from git import Repo

#os.chdir(os.path.dirname(__file__))
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