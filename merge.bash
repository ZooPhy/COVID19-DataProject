#!/bin/bash 
sort -t , -k 1,1 export_final.csv > sortData.csv #Sort the Temp data by station ID
join -t , -1 1 -2 1 sortData.csv STATION_DATA.csv > mergedDataTEMPLOCATIONV2.csv #Merge based on station ID
#cut -d, -f 2,8,9 mergedSTATIONNAME_COUNTY.csv > mergedSTATIONNAME_COUNTYV2.csv
#sed 's/*,/,/g' mergedSTATIONNAME_COUNTYV2.csv > mergedSTATIONNAME_COUNTYV3.csv 
#join -t , -1 1 -2 1 mergedDataTEMPLOCATIONV2.csv mergedSTATIONNAME_COUNTYV3.csv > mergedDataTEMPLOCATIONV3.csv #Merge based on station ID
#sed 's/*,/,/g' mergedDataTEMPLOCATIONV3.csv
