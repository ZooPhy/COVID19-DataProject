#!/usr/bin/python3

import os
os.system('cd climate && bash ./downloadClimateData.bash')
os.system('cd COVID-19 && python covid.py')
os.system('cd travel && python travel.py')
os.system('cd climate && python climate.py')
os.system('cd vaccine && python vaccine.py')
os.system('python merge.py')
os.system('mv 2021* ./data')
os.system('python merge2.py')
os.system('python arizonarun.py')
#os.system('cd climate && rm 2020* && rm F-* && rm sortedClimateDownload.csv')
