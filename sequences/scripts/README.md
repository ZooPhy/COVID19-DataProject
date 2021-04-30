## Running the Sequences
Sequences are gathered from NCBI using built in datasets and dataformat tools provided by NCBI.

In order to gather COVID-19 sequences from NCBI and format the sequences, run the following command.
```
bash getSequences.bash
```
The bash script runs a pipeline that acquires the raw data from the NCBI website. The file `compilefasta.py` only keeps the necessary COVID-19 data in a FASTA format and `finalizeSequences.py` ensures that data adheres to the following format in the FASTA file

```
Accession ID | Two Letter State Abbreviation | DD-MM-YYYY
```

`editpredictor.py` will edit the predictor file stored as `./DataFiles/Data/current_state.csv` from the root directory so that only states included in the FASTA file are included in the predictor file.
## Aligning the Sequences

```
bash alignment.bash
```
Aligned files will be stored under the file name `alignedSequences.bash`.

## Using your own files

If you wish to use your own predictor file, make sure that it is stored under the `./DataFiles/Data` directory under the file name `current_state.csv`.

If you wish to use your own sequences, make sure that the sequences adhere to the FASTA format specified above, and run the following command.

```
python3 editpredictor.py
```

More information on datasets and dataformat are provided by NCBI at the following website: https://www.ncbi.nlm.nih.gov/datasets/docs/reference-docs/command-line/
