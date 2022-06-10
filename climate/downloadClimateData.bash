#!/bin/bash
wget ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2020.csv.gz
zcat 2020.csv.gz > 2020.csv
grep 'TMAX' 2020.csv | grep 'USC\|USS\|USR\|USW' | cut -d, -f1,2,4 | sort -t , -k 1,1 | awk -F, '{new_var=$1"\t"$2; print new_var "," $3}' > F-temp.csv
grep 'PRCP' 2020.csv | grep 'USC\|USS\|USR\|USW' | cut -d, -f1,2,4 | sort -t , -k 1,1 | awk -F, '{new_var=$1"\t"$2; print new_var "," $3}' > F-prcp.csv
join -t, -1 1 -2 1 F-temp.csv F-prcp.csv | awk -F'\t' '{printf "%s,%s\n",$1,$2}' | sort -t , -k 1,1 > sortedClimateDownload.csv #Sort the Temp data by station ID
join -t , -1 1 -2 1 sortedClimateDownload.csv StationMetadata.csv > from_download.csv #Merge based on station IDget ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2020.csv.gz
