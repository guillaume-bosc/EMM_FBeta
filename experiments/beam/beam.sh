#!/bin/bash


if [ "$#" -ne 7 ]; then
	echo "please call: "
	echo " run.sh <arff_filepath> <min_sup> <max_sup> <beam_width> <topK_count> <max_redundancy> <measure>"
	exit 1
fi

STARTING_POSITION=$(pwd)

ARFF_FILE=$(realpath $1)
ARRF_NAME="${ARFF_FILE##*/}"
ARRF_NAME="${ARRF_NAME%.*}"
MIN_SUP=$2
MAX_SUP=$3
BEAM_WIDTH=$4
TOPK_COUNT=$5
MAX_REDUNDANCY=$6
MEASURE_PARAM=$7

mkdir -p "results"
BASE_RESULT_FOLDER_NAME="results/""$ARRF_NAME""_""$MIN_SUP""_"$MAX_SUP"_""$BEAM_WIDTH""_""$TOPK_COUNT""_""$MAX_REDUNDANCY"
mkdir -p $BASE_RESULT_FOLDER_NAME
RESULT_FOLDER_NAME="$BASE_RESULT_FOLDER_NAME""/""$MEASURE_PARAM"
mkdir -p $RESULT_FOLDER_NAME
DESTINATION="$STARTING_POSITION/$RESULT_FOLDER_NAME/"


cd ../../jars/BEAM

./run.sh $ARFF_FILE $MIN_SUP $MAX_SUP $BEAM_WIDTH $TOPK_COUNT $MAX_REDUNDANCY $MEASURE_PARAM

mv result.log $DESTINATION
mv support.log $DESTINATION
mv conf.conf $DESTINATION
mv measures.csv $DESTINATION
mv XBeta.csv $DESTINATION
mv LBeta.csv $DESTINATION
