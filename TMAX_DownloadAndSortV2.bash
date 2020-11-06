#!/bin/bash
wget ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2020.csv.gz
gunzip 2020.csv.gz
grep 'TMAX' 2020.csv > 2020_TMAX.csv
grep 'PRCP' 2020.csv > 2020_PRCP.csv
grep 'USC\|USS\|USR\|USW' 2020_TMAX.csv > 2020_TMAX_USA.csv 
grep 'USC\|USS\|USR\|USW' 2020_PRCP.csv > 2020_PRCP_USA.csv
cut -d, -f1,2,4 2020_TMAX_USA.csv > 2020_TMAX_USA_CUT.csv 
sort -t , -k 1,1 2020_TMAX_USA_CUT.csv > 2020_TMAX_USA_SORTED.csv  
cut -d, -f1,2,4 2020_PRCP_USA.csv > 2020_PRCP_USA_CUT.csv
sort -t , -k 1,1 2020_PRCP_USA_CUT.csv > 2020_PRCP_USA_SORTED.csv
awk -F, '{new_var=$1"\t"$2; print new_var "," $3}' 2020_TMAX_USA_SORTED.csv >F1.csv
awk -F, '{new_var=$1"\t"$2; print new_var "," $3}' 2020_PRCP_USA_SORTED.csv >F2.csv
join -t, -1 1 -2 1 F1.csv F2.csv > downloaded_export.csv
awk -F'\t' '{printf "%s,%s\n",$1,$2}' downloaded_export.csv > export_final.csv
