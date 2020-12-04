# COVID19-DataProject

### Pulling the Dashboard Data
In order to pull the aggregate data file, three scripts must be run. The scripts and their dependencies can all be found under ./Code. A description of each script can be found below.

## DownloadClimateData.bash 
This bash script is used to download a sorted list of the climate data based on FIPS county code. This climate data comes from the Global Historical Climatology Network - Daily (GHCN-Daily) datasets. Both the maximum daily temperature and the daily total precipitation are added to our data set.

## TravelCaseDataDownload.py
This python script is used to download travel data and daily COVID-19 case and death data. The COVID-19 case and death data comes from the Johns Hopkins Whiting School of Engineering and their source code and be found here https://github.com/CSSEGISandData/COVID-19. The travel data is sourced from hte Bureau of Transportation Statistics and their data source can be found here https://data.bts.gov/Research-and-Statistics/Trips-by-Distance/w96p-f2qv/data. Information about population density comes from the 2018 USA Census and the data source is from the COVID tracking project that provides an online resource for population density download, which can be found here https://github.com/COVID19Tracking/associated-data/blob/master/us_census_data/us_census_2018_population_estimates_counties.csv.

## TravelCaseDataMerge.py
This python script is used to merge the travel and case data. The output is aggregateDataFile.py. This is the complete aggregate data file used for this project, which can be found stored under ./Data.
