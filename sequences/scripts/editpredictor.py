#!/usr/bin/python3
import pandas as pd

discreteStates = {}
with open('sequences.fasta') as seq:
    for line in seq:
        if line.startswith('>'):
            discreteStates[line.split('|')[1]] = line.split('|')[1]

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
