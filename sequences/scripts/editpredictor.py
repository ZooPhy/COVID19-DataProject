#!/usr/bin/python3
import pandas as pd

def func(row):
    xml = ['<item>']
    for field in row.index:
        xml.append('  <field name="{0}">{1}</field>'.format(field, row[field]))
    xml.append('</item>')
    return '\n'.join(xml)

discreteStates = {}
with open('sequences.fasta') as seq:
    for line in seq:
        if line.startswith('>'):
            discreteStates[line.split('|')[1]] = line.split('|')[1]
print(discreteStates)
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
del newdf['Unnamed: 0'], newdf['state_code'],  newdf['state']
print('\n'.join(newdf.apply(func, axis=1)))
h.write('\n'.join(newdf.apply(func, axis=1)))
newdf.to_csv(g, sep='\t', index=False)
h.close()
g.close()
