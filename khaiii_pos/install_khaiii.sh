#!/usr/bin/env bash

CUR_DIR=$(pwd)

REF_DIR=$HOME/reference
KHAIII_DIR=$REF_DIR/khaiii/

KHAIII_LARGE_RESOURCE=true

mkdir -p $REF_DIR
cd $REF_DIR


CMAKE=$(which cmake)
if [ -z "$CMAKE" ]; then
    echo "ERROR : cmake not installed!!"
    echo "sudo apt install cmake , and try install again.."
    exit
fi
PIP=$(which pip)
if [ -z "$PIP" ]; then
    echo "ERROR : pip not installed!!"
    echo "activate your virtualenv. or sudo apt install python-pip"
    exit
fi
TORCH=$(pip show torch)
if [ -z "$TORCH" ]; then
    echo "ERROR : pytorch not installed!!"
    echo "pip install torch , and try install again.."
    exit
fi


echo "======================================="
echo "KHAIII INSTALLATION START.."
echo "======================================="
if [ ! -d "$KHAIII_DIR" ]; then
    echo "khaiii project dir not found.."
    echo "git clone https://github.com/kakao/khaiii.git"
    git clone https://github.com/kakao/khaiii.git
else
# It's a directory!
# Directory command goes here.
    echo "khaiii project dir already exist.."
    echo "if you choose y, current khaiii dir will be removed."

    read -r -p "Are you sure to remove current khaiii dir and git clone again (y/N)? " response
    response=${response,,} # tolower
    #if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
    if [[ $response =~ ^(yes|y| ) ]]; then
        rm -rf $KHAIII_DIR
        echo "git clone https://github.com/kakao/khaiii.git"
        git clone https://github.com/kakao/khaiii.git
    else
        read -r -p "Keep going installation without git clone (y/N)? " response
        response=${response,,} # tolower
        #if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
        if [[ $response =~ ^(yes|y| ) ]]; then
            echo "you choose Y. Continue Khaiii building.."
        else
            echo "you choose N. installation aborted!!"
            exit
        fi
    fi
fi

echo "======================================="
echo "KHAIII MAIN MODULE BUILD.."
echo "======================================="
echo "if cmake not exist, sudo apt install cmake , and try install again.."
cd $KHAIII_DIR
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$KHAIII_DIR/install ..
make all
echo "khaiii main build OK!!"

echo "======================================="
echo "KHAIII RESOURCE BUILD.."
echo "======================================="
if [ "$KHAIII_LARGE_RESOURCE" = true ] ; then
    echo 'KHAIII Large resource build!'
    make large_resource
else
    echo 'KHAIII Normal resource build!'
    make resource
fi
echo "khaiii resource build OK!!"

echo "======================================="
echo "KHAIII INSTALL TO PYTHON"
echo "======================================="
make install
make package_python
cd package_python
pip install .

echo "======================================="
echo "KHAIII TEST"
echo "======================================="
cd $CUR_DIR
python test_khaiii.py

