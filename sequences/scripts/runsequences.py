#!/usr/bin/python3

stateHashTable = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}
discreteStates = {}

# Import packages for Entrez
import pandas as pd
from Bio import Entrez
from Bio import SeqIO
import eutils
import os

os.system('curl -o datasets \'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/datasets\'')
os.system('chmod +x datasets')
os.system('/datasets version')
os.system('./datasets download virus genome taxon 2697049 --host human --geo-location USA --filename SARS2-hum-USA.zip')
os.system('unzip SARS2-hum-USA.zip')
g = open('newseq.fasta', 'w')
with open('./SARS2-hum-USA/data/cds.fna') as f:
    for line in f:
        if line.startswith('>'):
            find_location = line.split('USA/')
            accession = find_location[0][0:11]
            find_date = find_location[1].split('/')
            location = find_date[0][0:2]
            date = find_date[1][:-2]
            discreteStates[location] = location
            g.write(accession + '|' + location + '|' + date + '\n')
        else:
            g.write(line +'\n')


states = open('./../../DataFiles/Data/discreteStates.txt', 'w')
for key, values in discreteStates.items():
    states.write(key + '\n')
states.close()

h = open('./../../DataFiles/Data/new_predictors.txt', 'w')
samples = pd.read_csv('./../../DataFiles/Data/current_state.csv', sep=',') # Pull in current predictor file
newdf = pd.DataFrame()
stateabbr = samples['State']
for index in stateabbr:
    if index in discreteStates.keys():
        newdf = newdf.append(samples[samples['State'].str.contains(index)])
del newdf['Unnamed: 0'], newdf['state_code'],  newdf['state']
newdf.to_csv(h, sep='\t', index=False)
h.close()
