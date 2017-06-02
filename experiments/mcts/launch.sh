#!/bin/bash
DATA=$(realpath $1)
TAKE_ATTRIBUTE=$2
COMPARE_WITH_COMPLETE=${3:-0}
ITERATION_COUNT=10000

TOPK_COUNT=1000
MIN_SUP=6
MAX_REDUNDANCY=1.4
REDUNDANCY_MEASURE_PARAM=sumJaccard

ARRF_NAME="${DATA##*/}"
ARRF_NAME="${ARRF_NAME%.*}"

POSSIBLE_MEASURES=(Acc RAcc WRAcc F1 RelativeF1 WeightedRelativeF1 FBeta RelativeFBeta WeightedRelativeFBeta)
for MEASURE_PARAM in ${POSSIBLE_MEASURES[@]}; do
	./mcts.sh $DATA $TAKE_ATTRIBUTE $MIN_SUP $ITERATION_COUNT $TOPK_COUNT $MAX_REDUNDANCY $MEASURE_PARAM $REDUNDANCY_MEASURE_PARAM
	RESULT="results/""$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$REDUNDANCY_MEASURE_PARAM""/""$ITERATION_COUNT""/""$MEASURE_PARAM""/result.log"	
	./topcardistribution.py $RESULT
	./betaprecisionrecall.py $RESULT
	./supportprecisionrecall.py $RESULT
done

FOLDER="results/""$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$REDUNDANCY_MEASURE_PARAM""/""$ITERATION_COUNT"
./topcarqualities.py $FOLDER
./jaccard.py $FOLDER

# ----------------------------------------------
# Boxplots
# ----------------------------------------------
MEASURE_PARAM=RelativeFBeta
ITERATIONS=(1000 5000 50000)
MAX_REDUNDANCY=0.5
REDUNDANCY_MEASURE_PARAM=jaccardSupportDescription
TOPK_COUNT=200

for ITERATION in ${ITERATIONS[@]}; do
	./mcts.sh $DATA $TAKE_ATTRIBUTE $MIN_SUP $ITERATION $TOPK_COUNT $MAX_REDUNDANCY $MEASURE_PARAM $REDUNDANCY_MEASURE_PARAM
	echo -n ""
done

if [ "$COMPARE_WITH_COMPLETE" -eq "0" ]; then
   ./boxplot.py "results/""$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$REDUNDANCY_MEASURE_PARAM" "$MEASURE_PARAM" 1000
   echo -n ""
else
   COMPLETE_DIR="results/""$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$REDUNDANCY_MEASURE_PARAM""/""complete"
   COMPLETE_DIR="$COMPLETE_DIR""/""$MEASURE_PARAM"
   mkdir -p $COMPLETE_DIR
   java -jar ../../jars/COMPLETE/complete.jar $DATA --minsup $MIN_SUP --topK $TOPK_COUNT --maxSim $MAX_REDUNDANCY --measures $MEASURE_PARAM  > "$COMPLETE_DIR/measures.csv"
   ./boxplot.py "results/""$ARRF_NAME""_""$TAKE_ATTRIBUTE""_"$MIN_SUP"_""$TOPK_COUNT""_""$MAX_REDUNDANCY""_""$REDUNDANCY_MEASURE_PARAM" "$MEASURE_PARAM" 15
fi



