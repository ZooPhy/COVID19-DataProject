import pandas as pd

travelDataFrame = pd.read_csv("traveloutput.csv", dtype='object')
infoDataFrame = pd.read_csv("caseData.csv", dtype='object')
infoDataFrame = infoDataFrame.rename(columns={"FIPS_x":"FIPS"})
del travelDataFrame['Unnamed: 0']
del infoDataFrame['Unnamed: 0']
print(travelDataFrame.columns)
print(infoDataFrame.columns)
finalMerge = infoDataFrame.merge(travelDataFrame, on='FIPS')
cols = finalMerge.columns.tolist()

finalMerge.to_csv('aggregateDataFile.csv')
