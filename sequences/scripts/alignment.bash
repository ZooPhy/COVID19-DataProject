#!/bin/bash

wget https://mafft.cbrc.jp/alignment/software/mafft_7.475-1_amd64.deb
sudo dpkg -i mafft_7.475-1_amd64.deb
which mafft
mafft --version
mafft sequences.fasta > alignedSequences.fasta
