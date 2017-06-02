#!/bin/bash

SCRIPTS=../../scripts/
SCRIPT_FILE="$SCRIPTS"script.py
XLBETA_FILE="$SCRIPTS"xlbetas.csv

if [ "$#" -ne 7 ]; then
	echo "please call: "
	echo " run.sh <arff_filepath> <min_sup> <max_sup> <beam_width> <topK_count> <max_redundancy> <measure_param> "
	exit 1
fi

ARFF_FILE=$1
ARRF_NAME="${ARFF_FILE##*/}"
ARRF_NAME="${ARRF_NAME%.*}"
MIN_SUP=$2
MAX_SUP=$3
BEAM_WIDTH=$4
TOPK_COUNT=$5
MAX_REDUNDANCY=$6
MEASURE_PARAM=$7
RESULT_FOLDER_NAME="$ARRF_NAME""_""$MIN_SUP""_"$MAX_SUP"_""$BEAM_WIDTH""_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$MEASURE_PARAM"

./$SCRIPT_FILE transform $ARFF_FILE --types numeric

VALUES=$(echo $(./$SCRIPT_FILE xlbeta $ARFF_FILE --manual $XLBETA_FILE))
VALUES=($VALUES)

XBETA_PARAM=${VALUES[0]}
LBETA_PARAM=${VALUES[1]}

echo $XBETA_PARAM > XBeta.csv
echo $LBETA_PARAM > LBeta.csv 

cat conf.template | sed \
  -e "s|{{ATTRIBUTE_TYPE}}|${ATTRIBUTE_TYPE}|g" \
  -e "s|{{MIN_SUP}}|${MIN_SUP}|g" \
  -e "s|{{MAX_SUP}}|${MAX_SUP}|g" \
  -e "s|{{BEAM_WIDTH}}|${BEAM_WIDTH}|g" \
  -e "s|{{TOPK_COUNT}}|${TOPK_COUNT}|g" \
  -e "s|{{MAX_REDUNDANCY}}|${MAX_REDUNDANCY}|g" \
  -e "s|{{RESULT_FOLDER_NAME}}|${RESULT_FOLDER_NAME}|g" \
  -e "s|{{XBETA_PARAM}}|${XBETA_PARAM}|g" \
  -e "s|{{LBETA_PARAM}}|${LBETA_PARAM}|g" \
  -e "s|{{MEASURE_PARAM}}|${MEASURE_PARAM}|g" \
   > conf.conf

java -jar ELMMut.jar conf.conf

rm attributes.csv
rm qualities.csv
rm objects.csv

RESULT_DIR_PATH="results""/""$RESULT_FOLDER_NAME"
MAX=-1
for RESULT in $(ls $RESULT_DIR_PATH); do
	TIME=${RESULT:5:${#RESULT} - 5}
	((TIME > MAX)) && MAX=$TIME
done
RESULT_FILE_PATH="$RESULT_DIR_PATH""/resXP"$MAX"/result.log"
SUPPORT_FILE_PATH="$RESULT_DIR_PATH""/resXP"$MAX"/support.log"
cp $RESULT_FILE_PATH .
cp $SUPPORT_FILE_PATH .
MY_RESULT="measures.csv"
while read line; do 
	MEASURE=$(echo "$line" | awk -F"\t" '{print $4}')
	echo $MEASURE >> $MY_RESULT
done < $RESULT_FILE_PATH

VAR=$(sed '23q;d' "results""/""$RESULT_FOLDER_NAME""/resXP"$MAX"/info.log" | awk -F" " '{print $1}')
echo "#runtime(ms) : $VAR""000" >> $MY_RESULT

rm -r results
