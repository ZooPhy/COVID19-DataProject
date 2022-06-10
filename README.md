# COVID19 Data Project

This code is used to aggregate county-level COVID-19 statistics (Cases, deaths, and vaccinations), climate data, and travel data. 

## Information about Tokens

In order to use this code, BTS (Bureau of Transportation Statistics) and CDC (Center for Disease Control) requires an app token in order to make API calls to their data sets. Information on how to acquire the tokens for the travel and vaccine datasets can be found at the following websites. Replace line 31 in `./vaccine/vaccine.py` and line 23 with `./travel/travel.py` with the respective account information and app token. Note: will be adding a feature to use app tokens from the command line.


### Website for travel app token
`https://dev.socrata.com/foundry/data.bts.gov/w96p-f2qv`


### Website for vaccine app token
`https://dev.socrata.com/foundry/data.cdc.gov/8xkx-amqh`


## Running the code

The following command can be run to access the command line help section which provides information on each of the command line options. 

`python3 run_sequences.py -h`

Results are stored in the `./results` folder. 

For example, the following command will use county names to pull predictor data from
between 01.01.2022 and 01.05.2022 from Hennepin County, MN and Olmsted County, MN. This sample output can be found as `./results/parsed_predictors.csv`.

`python3 run_sequences.py -start 20220101 -end 20220105 -codes 0 -state MN -counties Hennepin Olmsted`
