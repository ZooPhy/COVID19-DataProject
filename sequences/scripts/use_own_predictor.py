# User would like to use their own predictor file but our sequences

discreteStates = open('./DataFiles/Data/discreteStates.txt', 'r')
discreteStates = discreteStates.read().split('\n')

h = open('./../DataFiles/Data/new_predictors.txt', 'w')
samples = pd.read_csv('./../DataFiles/Data/current_state.csv', sep=',')
newdf = pd.DataFrame()
stateabbr = samples['State']
for index in stateabbr:
    if index in discreteStates:
        newdf = newdf.append(samples[samples['State'].str.contains(index)])
newdf.to_csv(h, sep='\t')
g.close()
h.close()