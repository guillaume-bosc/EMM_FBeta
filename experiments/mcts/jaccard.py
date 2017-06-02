#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import basename, splitext,abspath, dirname,isdir,join
from os import listdir

#------------------------------------------------------------------
FONTSIZE = 15
LINEWIDTH = 5
MEASURE_SIMPLE_NAMES={"RelativeF1":"RF1", "WeightedRelativeF1":"WRF1",
          "FBeta":"FBeta","RelativeFBeta":"RFBeta","WeightedRelativeFBeta":"WRFBeta"}
KEEP_ONLY_MEASURES = ["RAcc","WRAcc","RelativeF1","WeightedRelativeF1","RelativeFBeta","WeightedRelativeFBeta"]
TOP=50
#------------------------------------------------------------------
def jaccard(support1, support2) :
    return float(len(support1 & support2))/len(support1 | support2)


def getSimilarity(supports1, supports2) :
    len1 = float(len(supports1))
    len2 = float(len(supports2))
    return max(sum([max([jaccard(support1, support2) for support2 in supports2]) for support1 in supports1])/len1,
               sum([max([jaccard(support1, support2) for support1 in supports1]) for support2 in supports2])/len2)

def plotJaccards(valuefiles, measureNames, output):
    allSupports=[]
    fig, qualAx = plt.subplots(figsize=(12, 6))
    for valuefile in valuefiles :
        data = pd.read_csv(valuefile,sep='\t',header=None, index_col = None)
        supports = set(frozenset(s.strip().split(" ")) for s in data[0][0:min(TOP,len(data[0]))])
        allSupports.append(supports)

    toPlotMatrix=[]
    for i in range(len(measureNames)) :
        toPlotLine = []
        print measureNames[i]," with "
        for j in range(0, i+1) :
            if i == j : measure = 1
            else : measure = toPlotMatrix[j][i]
            toPlotLine.append(measure)
        for j in range(i+1,len(measureNames)) :
            print "  >>",measureNames[j]
            measure = getSimilarity(allSupports[i],allSupports[j])
            toPlotLine.append(measure)
        toPlotMatrix.append(toPlotLine)
    toPlotMatrix=[list(reversed(l)) for l in toPlotMatrix]
    heatmap = plt.pcolor(toPlotMatrix,vmin=0, vmax=1,cmap='RdYlGn')
    cbar=plt.colorbar(heatmap)
    cbar.ax.tick_params(labelsize=FONTSIZE)
    cbar.set_label("Jaccard",fontsize=FONTSIZE)
    for i in range(len(toPlotMatrix)) :
        values = toPlotMatrix[i]
        for j in range(len(values)) :
            percentage = values[j]*100
            plt.text(j + 0.5, i + 0.5, '%.2f' % percentage + '%',horizontalalignment='center',verticalalignment='center',fontsize=FONTSIZE)
    plt.xticks([.5+i for i in range(len(measureNames))],[(MEASURE_SIMPLE_NAMES[m] if m in MEASURE_SIMPLE_NAMES else m) for m in reversed(measureNames)],rotation=30)
    plt.yticks([.5+i for i in range(len(measureNames))],[(MEASURE_SIMPLE_NAMES[m] if m in MEASURE_SIMPLE_NAMES else m) for m in measureNames])
    plt.tick_params(labelsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(output+"/jaccards-"+str(TOP)+".pdf",bbox_inches='tight')

def plot(BASE):
    PATHS=[]
    measures = [ name for name in listdir(BASE) if isdir(join(BASE, name)) and name in KEEP_ONLY_MEASURES]
    for measure in measures :
        PATH=BASE+"/"+measure+"/support.log"
        PATHS.append(PATH)
    plotJaccards(PATHS, measures, BASE)

plot(sys.argv[1])

#plotJaccards(["olfactive_numeric_6_10_1.4_1000/mcts-WeightedRelativeFBeta.csv","olfactive_numeric_6_10_1.4_1000/mcts-WRAcc.csv"])
