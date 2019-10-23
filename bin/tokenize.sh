#!/usr/bin/env bash

cd ..
BASEDIR=$(pwd)
echo $BASEDIR
echo '>>>> Start Tokenizing Raw Corpus...'

#DATA_DIR=/home/meanimo/data/mass-raw-nosplit-charex
DATA_DIR=/media/pipaek/wdusb/data/mass-raw-nosplit-charex
mkdir -p mono
for SPLIT in train valid test; do
    python encode.py \
        --inputs ${DATA_DIR}/${SPLIT}/raw_korean_corpus.${SPLIT}.txt \
        --outputs mono/${SPLIT}.txt \
        --workers 6; \
done
