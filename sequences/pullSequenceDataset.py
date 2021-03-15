#!/usr/bin/python3
import os
print("NOTE: To use your own sequences, place sequence file under DataFiles/Sequence or predictor file under DataFiles/Data")
user = input("Enter your choice" + "\n\n" + "1. Use own sequences 2. Use own predictors 3. Run sequences and predictors")
if (user == 1):
        os.system('cd scripts && python3 use_own_sequences.py')
elif (user == 2):
        os.system('cd scripts && python3 use_own_predictor.py')
else:
        os.system('cd scripts && python3 runsequences.py')
