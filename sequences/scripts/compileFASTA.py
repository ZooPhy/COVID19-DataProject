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

g = open('seq2.fasta', 'w')
idlist = open('idlist.txt','w')
ids = []
dateDict = {}
with open('./ncbi_dataset/data/genomic.fna') as f:
    for line in f:
        if line.startswith('>'):
            find_location = line.split('USA/')
            accession = find_location[0][1:9]
            find_date = find_location[1].split('/')
            location = find_date[0][0:2]
            date = find_date[1][:-2]
            discreteStates[location] = location
            g.write('>' + accession + '|' + location + '\n')
            if accession not in ids:
                ids.append(accession)
        else:
            g.write(line)
    idlist.write(str(ids))
    print('ID LIST COMPLETE')
idlist.close()

for id in ids:
    results = Entrez.efetch(db='nuccore', id=id, retmode="xml")
    response = Entrez.read(results)
    for entry in response:
        accession = entry['GBSeq_primary-accession']
        for date in extract_date(entry):
            dateDict[accession] = date
print('SEQUENCE DATES OBTAINED')
g.close()

finalsequences = open('seq3.fasta', 'w')
with open('seq2.fasta') as sequences:
    for line in sequences:  
        if line.startswith('>'):
            if line[1:9] in dateDict.keys():
                finalsequences.write(line + '|' + dateDict[line[1:9]] + '\n')
        else:
            finalsequences.write(line)
print('DATES WRITTEN TO FASTA')
finalsequences.close()

final = open('finalsequences.fasta', 'w')
with open('seq3.fasta') as finseq:
    for line in finseq:
        if line.startswith('>'):
            final.write(line.rstrip())
        else:
            final.write(line)
final.close()
print('FASTA SUCESSFULLY GENERATED')
