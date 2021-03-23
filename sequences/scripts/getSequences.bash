#!/bin/bash

curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/datasets';
curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/dataformat';
chmod +x datasets;
chmod +x dataformat;
./datasets version;
./datasets download virus genome taxon 2697049 --host human --geo-location USA --filename SARS2-hum-USA.zip;
unzip SARS2-hum-USA.zip;
python3 compileFASTA.py;
rm seq2.fasta;
rm seq3.fasta;
