#!/bin/bash
DATA=$1
SCRIPTS=../../scripts/
SCRIPT_FILE="$SCRIPTS"script.py
XLBETA_FILE="$SCRIPTS"xlbetas.csv

./$SCRIPT_FILE boxplot $DATA --manual $XLBETA_FILE

