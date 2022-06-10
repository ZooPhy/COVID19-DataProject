import pandas as pd
import sys, getopt
import argparse
import re 
import datetime as datetime
import os 

#python code.py -date(mmddyyyy)- -sequence.fasta-
#-sd start date
#-nd end date
#- only end date? grab everything
#Has tobe a full date if not throw error

# Function to get the key value of state abbreviation
def get_key(val):
    for key, value in us_state_to_abbrev.items():
         if val == value:
            return key
 
    return "key doesn't exist"

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

parser = argparse.ArgumentParser(description='Generate Sequence fasta with only specific dates and counties.')
parser.add_argument('-start', dest = 'start', default = None, help='Start date in YYYMMDD')
parser.add_argument('-end', dest = 'end', default = None, help='End date in YYYMMDD')
parser.add_argument('-seq', dest = 'seq', default = None, help='FASTA file for sequences (accesion | location | date)')
parser.add_argument('-state', dest = 'state', default = None, help='two digit state abbreviation')
parser.add_argument('-counties', nargs='+', dest = 'counties', default = None, help='counties to pull the sequences for')
args = parser.parse_args()

startdate = str(args.start)
enddate = str(args.end)

# Check for missing parameters.

if(args.start == None or args.end == None or args.seq == None or args.state == None or args.counties == None):
    print("Missing input parameter.")
    sys.exit(1)
    
# Grab all of the different headers that begin with the specified state
# Append to the list 'parse' which will contain a list of all the different
# counties that have been encountered.
# In summary, parse by county name and make sure 

headers = open("headers.txt", 'w')
date_partitioned_sequences = open("data-dateparse.fasta", 'w')
partitioned_sequences = open(args.seq, "r")

write_to_file = False
for line in partitioned_sequences:
    if line.startswith('>'):
        
        # Define the accesion ID and the accesion county
        
        accesion_ID = line.split('|')[0]; accesion_county = line.split('|')[1]
        
        # Ensure that the county of the current sequence is in the user-input county list
        
        for counties in args.counties:
            if(counties.lower() in accesion_county.lower() and (get_key(str(args.state)).lower() in accesion_county.lower() or str(args.state).lower() in accesion_county.lower())):
                
                # Get the sequence date and ensure that it is within the user specified date range
                # Write to file if all these conditions are met.
                
                date = line.split('|')[2]; date = date[0:4] + date[5:7] + date[8:10]
                year = date[0:4]; month = date[5:7]; day = date[8:10]
                if (int(enddate) >= int(date)) and (int(startdate) <= int(date)) and accesion_ID is not None:
                    write_to_file = True
                    line = accesion_ID + '|' + date + "|" + accesion_county + '\n'
                    date_partitioned_sequences.write(line); headers.write(line)     
                else:
                    write_to_file = False
    elif line.startswith('>') != True and write_to_file is True:
        date_partitioned_sequences.write(line)
    else:
        continue

date_partitioned_sequences.close()
headers.close()
partitioned_sequences.close()

# Add the reference sequence and clean up the file directory

date_partitioned_sequences = open("data-dateparse.fasta", 'r')
reference_sequence = open('./sequences/reference.fasta', 'r')
final_file = open('output_sequences.fasta', 'w')
final_file.write(reference_sequence.read())
final_file.write(date_partitioned_sequences.read())
final_file.close()
partitioned_sequences.close()
date_partitioned_sequences.close()
headers.close()
reference_sequence.close()

os.system('mv output_sequences.fasta sequences/ && mv headers.txt sequences/')
os.system('rm data-dateparse.fasta')
