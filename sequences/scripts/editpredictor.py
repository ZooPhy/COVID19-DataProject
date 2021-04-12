#!/usr/bin/python3
import pandas as pd

# Function to convert csv file to xml file for use in BEAGLE analysis
def func(row):
    xml = ['<item>']
    for field in row.index:
        xml.append('  <field name="{0}">{1}</field>'.format(field, row[field]))
    xml.append('</item>')
    return '\n'.join(xml)

#Create a new dictionary with all states in fasta file
discreteStates = {}
with open('sequences.fasta') as seq:
    for line in seq:
        if line.startswith('>'):
            discreteStates[line.split('|')[1]] = line.split('|')[1]
print(discreteStates)

# Create a new predictor file that contains the appropriate data
# Predictor file should be placed in ./DataFiles/Data/current_state.csv
h = open('./../../DataFiles/Data/new_predictors.xml', 'w')
g = open('./../../DataFiles/Data/new_predictors2.txt', 'w')
samples = pd.read_csv('./../../DataFiles/Data/current_state.csv', sep=',') # Pull in current predictor file
newdf = pd.DataFrame()
stateabbr = samples['State']
for index in stateabbr:
    print(index)
    if index in discreteStates.keys():
        print('Discrete: ' + index)
        newdf = newdf.append(samples[samples['State'].str.contains(index)])
        
# Delete extra columns in data
del newdf['Unnamed: 0'], newdf['state_code'],  newdf['state']

#Convert dataframe to txt file and xml file
print('\n'.join(newdf.apply(func, axis=1)))
h.write('\n'.join(newdf.apply(func, axis=1)))
newdf.to_csv(g, sep='\t', index=False)
h.close()
g.close()
