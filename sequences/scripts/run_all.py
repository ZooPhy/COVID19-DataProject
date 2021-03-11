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

def extract_countries(entry):
    sources = [feature for feature in entry['GBSeq_feature-table']
               if feature['GBFeature_key'] == 'source']

    for source in sources:
        qualifiers = [qual for qual in source['GBFeature_quals']
                      if qual['GBQualifier_name'] == 'country']
        
        for qualifier in qualifiers:
            yield qualifier['GBQualifier_value']     

def extract_date(entry):
    sources = [feature for feature in entry['GBSeq_feature-table']
               if feature['GBFeature_key'] == 'source']

    for source in sources:
        qualifiers = [qual for qual in source['GBFeature_quals']
                      if qual['GBQualifier_name'] == 'collection_date']
        
        for qualifier in qualifiers:
            yield qualifier['GBQualifier_value']
            
# Entrez info
Entrez.api_key = "14a1b40ccaa3d634843d10fbe9f33d65c809"
Entrez.email = 'masauer2@asu.edu'

# Esearch 89383
esr = Entrez.esearch(db='nuccore',term='txid2697049[Organism]', retstart = 0, retmax = 10)

# build id list
record = Entrez.read(esr) 
idlist = []
for row in record["IdList"]: 
    idlist.append(row)
    

# fasta file storage
f = open("./../../DataFiles/Data/sequence.fasta", "w")
p = open("./../../DataFiles/Data/logging.txt", "w")
num = 0
for i in idlist: 
    num = num + 1
    print(num)
    results = Entrez.efetch(db='nuccore', id=i, retmode="xml")
    response = Entrez.read(results)
    for entry in response:
        currCountry = False
        accession = entry['GBSeq_primary-accession']
        for country in extract_countries(entry):
            if "USA" in country:
                currCountry = True
            if 'USA' in country:
                country = country.replace('USA: ', '').strip()
                abbreviation = ''
                p.write("1. " + country)
                if country == '' or len(country) > 2:
                    p.write("2. " + country + '\n')
                    if 'USA' in entry["GBSeq_definition"]:
                        abbreviation = entry["GBSeq_definition"].split('USA/')[1][:2]
                    discreteStates[abbreviation] = country
                elif country in stateHashTable.keys():
                    p.write("3. " + country + '\n')
                    abbreviation = country
                    p.write(abbreviation + '\n')
                    discreteStates[abbreviation] = country
                else:
                    p.write("4. " + entry + '\n')
                    break
                f.write("> " + accession + "|" + abbreviation + "|")
            else:
                currCountry = False
        for date in extract_date(entry):
            if currCountry == True:
                f.write(date) 
        if currCountry == True:  
            f.write("\n"+entry["GBSeq_sequence"]+"\n")
            
f.close()
p.close()

g = open('./../../DataFiles/Data/discreteStates.txt', 'w')
for key, values in discreteStates.items():
    g.write(key + '\n')
g.close()

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
