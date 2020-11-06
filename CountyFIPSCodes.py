import requests #Used for API calls
import json #Used to handle JSON file
import pandas as pd #Used to handle csv files as DataFrame objects
import time #Used to compute time used by the script and each API call

start_time = time.time() #Start timer


#Step 1 - Import the station data and read the data into a Data Frame and add METADATA as the first row of the DataFrame
CSV_FILE = pd.read_csv(R'C:\Users\micha\Downloads\COVID19\sortSTATIONV2.csv')
dt = pd.DataFrame(CSV_FILE)
dt.columns = ['STATIONID', 'Lat', 'Long', 'IDK', 'STATE', 'CITY']

#Step 2 - Create a new column for the County names and subset the data so only the latitude and longitude
#         information is used as inputs
dt['County'] = ""
dt['FIPS'] = ""
subsetData = dt.iloc[:,1:3]

#Step 3 - Loop through the station data and use the lat and long info as input for the FCC API call
for i in subsetData.index:
    dataCall_time = time.time() #Start timer to record how long each API call takes
    LAT = subsetData.iloc[i,0]
    LONG = subsetData.iloc[i,1]
    try:
        req = requests.get('https://geo.fcc.gov/api/census/area?lat='+str(LAT)+'&lon='+str(LONG)+'&format=json'); #Format for the api call can be found at the FCC website
    except:
        pass
#Step 4 - Load each API call as a JSON file and sort through the JSON file to find the county name
#
# The county name is located under the results key.
# The value of the 'results' key is a dictionary stored in a single-element array.
# The county name is stored as a key-value pair within this dictionary.

    reqText = req.text
    loaded_json = json.loads(reqText)
    for x in loaded_json:
        if x == 'results': #Search in 'results' key
                y = loaded_json[x]

                #Exception Handler is used to pass any potential errors -> Let me run this code while I slept without crashes
                try:
                    z = y[0] #Expose dictionary behind the single-element array -> z is equal to the dictionary that stores the county name
                except: pass
                itemsList = z.items()
#Step 5 - Find the county name element in the JSON dictionary and add the county name value to the original data frame
                for item in itemsList:
                    if item[0] == 'county_name':
                        dt.at[i, "County"] = item[1]
                        print("Input:", loaded_json['input'], "County Name:", item[1], " ------ This data call took", time.time() - dataCall_time, "seconds to run") #Debug info
                    if item[0] == 'county_fips':
                        dt.at[i, "FIPS"] = item[1]
                        print("Input:", loaded_json['input'], "FIPS:", item[1], " ------ This data call took", time.time() - dataCall_time, "seconds to run")  # Debug info

#Step 6 - Print the final DataFrame with the county name values included and save this DataFrame as a csv file
print(dt)
dt.to_csv('FINALMERGEDATAV3.csv')

#Step 7 - Calculate time taken by the process
#
#There might be ways to make this process more efficient i.e using functional programming, less loops etc.
print ("My program took", time.time() - start_time, "seconds to run") # Time needed to complete entire function