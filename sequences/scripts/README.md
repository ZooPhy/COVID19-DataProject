## Running the Sequences
Sequences are gathered from NCBI using built in datasets and dataformat tools provided by NCBI.

In order to gather COVID-19 sequences from NCBI and format the sequences, run the following command.
```
bash getSequences.bash
```
The bash script runs a pipeline that acquires the raw data from the NCBI website. Compilefasta.py only keeps the necessary COVID-19 data in a fasta format. FinalizeSequences.py ensures that data adheres to the following format in the FASTA file

```
Accession ID | Two Digit State ID | DD-MM-YYYY
```

Editpredictor.py will edit the predictor file stored as ./../../DataFiles/Data/current_state.csv so that only states included in the fasta file are included in the predictor file.

## Using your own files

If you wish to use your own predictor file, make sure that it is stored under the ./DataFiles/Data directory under the file name 'current_state.csv'.

If you wish to use your own sequences, make sure that the sequences adhere to the FASTA format specified above, and run the following command.

```
python3 editpredictor.py
```

More information on datasets and dataformat are provided by NCBI at the following website: https://www.ncbi.nlm.nih.gov/datasets/docs/reference-docs/command-line/
