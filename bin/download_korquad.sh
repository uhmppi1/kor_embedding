#!/usr/bin/env bash

KORQUAD_DIR=raw/korquad

cd ..   # BASEDIR 디렉토리에서 실행한다.
BASEDIR=$(pwd)
echo BASEDIR

echo "download KorQuAD data..."
wget https://korquad.github.io/dataset/KorQuAD_v1.0_train.json -P $KORQUAD_DIR
wget https://korquad.github.io/dataset/KorQuAD_v1.0_dev.json -P $KORQUAD_DIR
mkdir -p $BASEDIR/processed