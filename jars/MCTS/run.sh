#!/bin/bash

SCRIPTS=../../scripts/
SCRIPT_FILE="$SCRIPTS"script.py
XLBETA_FILE="$SCRIPTS"xlbetas.csv

if [ "$#" -ne 8 ]; then
	echo "please call: "
	echo " run.sh <arff_filepath> <[numeric|symbolic|boolean]> <min_sup> <iteration_count> <topK_count> <max_redundancy> <[F1|FBeta|WRacc|WKL]> <[ jaccardSupportDescription | jaccardSupportDescriptionTarget | sumJaccard ]>"
	exit 1
fi

ARFF_FILE=$1
ARRF_NAME="${ARFF_FILE##*/}"
ARRF_NAME="${ARRF_NAME%.*}"
TAKE_ATTRIBUTE=$2
MIN_SUP=$3
ITERATION_COUNT=$4
TOPK_COUNT=$5
MAX_REDUNDANCY=$6
MEASURE_PARAM=$7
REDUNDANCY_MEASURE_PARAM=$8
RESULT_FOLDER_NAME="$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$ITERATION_COUNT""_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$MEASURE_PARAM""_""$REDUNDANCY_MEASURE_PARAM"

if [ "$TAKE_ATTRIBUTE" == "numeric" ]; then
	ATTRIBUTE_TYPE=Numeric
elif [ "$TAKE_ATTRIBUTE" == "symbolic" ]; then
	ATTRIBUTE_TYPE=Nominal
elif [ "$TAKE_ATTRIBUTE" == "boolean" ]; then
	ATTRIBUTE_TYPE=Boolean
else
	echo "please call: "
	echo " run.sh <arff_filepath> <[numeric|symbolic|boolean]> <iteration_count> <topK_count> <max_redundancy> <[F1|FBeta|WRacc|WKL]>"
	exit 1
fi

./$SCRIPT_FILE transform $ARFF_FILE --types $TAKE_ATTRIBUTE

VALUES=$(echo $(./$SCRIPT_FILE xlbeta $ARFF_FILE --manual $XLBETA_FILE))
VALUES=($VALUES)

XBETA_PARAM=${VALUES[0]}
LBETA_PARAM=${VALUES[1]}

echo $XBETA_PARAM > XBeta.csv
echo $LBETA_PARAM > LBeta.csv 

cat conf.template | sed \
  -e "s|{{ATTRIBUTE_TYPE}}|${ATTRIBUTE_TYPE}|g" \
  -e "s|{{MIN_SUP}}|${MIN_SUP}|g" \
  -e "s|{{ITERATION_COUNT}}|${ITERATION_COUNT}|g" \
  -e "s|{{TOPK_COUNT}}|${TOPK_COUNT}|g" \
  -e "s|{{MAX_REDUNDANCY}}|${MAX_REDUNDANCY}|g" \
  -e "s|{{RESULT_FOLDER_NAME}}|${RESULT_FOLDER_NAME}|g" \
  -e "s|{{XBETA_PARAM}}|${XBETA_PARAM}|g" \
  -e "s|{{LBETA_PARAM}}|${LBETA_PARAM}|g" \
  -e "s|{{MEASURE_PARAM}}|${MEASURE_PARAM}|g" \
  -e "s|{{REDUNDANCY_MEASURE_PARAM}}|${REDUNDANCY_MEASURE_PARAM}|g" \
   > conf.conf

java -jar -Xms8G -Xmx8G MCTS4SD.jar conf.conf

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
MY_RESULT="mcts-$ITERATION_COUNT.csv"
while read line; do 
	MEASURE=$(echo "$line" | awk -F"\t" '{print $3}')
	echo $MEASURE >> $MY_RESULT
done < $RESULT_FILE_PATH

VAR=$(sed '27q;d' "results""/""$RESULT_FOLDER_NAME""/resXP"$MAX"/info.log" | awk -F" " '{print $3}')
echo "#runtime(ms) : $VAR" >> $MY_RESULT

rm -r results
