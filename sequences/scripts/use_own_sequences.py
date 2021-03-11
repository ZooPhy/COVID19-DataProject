# User would like to use their own sequences but our predictor file

from Bio import SeqIO
discreteStates = open('./DataFiles/Data/discreteStates.txt', 'w')
for seq_record in SeqIO.parse(open('./DataFiles/Data/sequence.fasta', mode='r'), 'fasta'): 
    discreteStates.write(seq_record .id.split('|')[1] + "\n")
discreteStates.close()

discreteStates = open('./DataFiles/Data/discreteStates.txt', 'r')
discreteStates = discreteStates.read().split('\n')

h = open('./DataFiles/Data/new_predictors.txt', 'w')
samples = pd.read_csv('./DataFiles/Data/current_state.csv', sep=',') # Pull in current predictor file
newdf = pd.DataFrame()
stateabbr = samples['State']
for index in stateabbr:
    if index in discreteStates:
        newdf = newdf.append(samples[samples['State'].str.contains(index)])
    else:
        print(index, discreteStates)
newdf.to_csv(h, sep='\t')
h.close()