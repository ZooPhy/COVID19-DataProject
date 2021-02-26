stateHashTable = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
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

# Esearch 46487
esr = Entrez.esearch(db='nuccore', term='txid2697049[Organism]', retstart=0, retmax=200)

# build id list
record = Entrez.read(esr)
idlist = []
for row in record["IdList"]:
    idlist.append(row)

# fasta file storage
f = open("sequenceFINAL.fasta", "w")
for i in idlist:
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
                if country == '':
                    if 'USA' in entry["GBSeq_definition"]:
                        abbreviation = entry["GBSeq_definition"].split('USA/')[1][:2]
                elif country in stateHashTable.keys():
                    abbreviation = stateHashTable[country]
                    discreteStates[abbreviation] = '1'
                f.write("> " + accession + "|" + abbreviation + "|")
            else:
                currCountry = False
        for date in extract_date(entry):
            if currCountry == True:
                f.write(date)
        if currCountry == True:
            f.write("\n" + entry["GBSeq_sequence"] + "\n")

g = open('discreteStates.txt', 'w')
for key in discreteStates.keys():
    g.write(key + '\n')

samples = pd.read_csv('./DataFiles/Data/current_state.csv', sep=',')  # Pull in current predictor file
newdf = pd.DataFrame()
stateabbr = samples['State']
for index in stateabbr:
    if index in discreteStates.keys():
        newdf = newdf.append(samples[samples['State'].str.contains(index)])
print(newdf)