#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from os.path import basename, splitext,abspath, dirname,isdir,join
from os import listdir

#------------------------------------------------------------------
FONTSIZE = 15
LINEWIDTH = 5
MEASURE_SIMPLE_NAMES={"RelativeF1":"RF1", "WeightedRelativeF1":"WRF1",
          "FBeta":"FBeta","RelativeFBeta":"RFBeta","WeightedRelativeFBeta":"WRFBeta"}
#------------------------------------------------------------------
def to_percent(x, pos=0):
    return '%1.f'%(100*x)+'%'

def plotQualitiesAndLabels(valuefiles, measureNames, output):
    formatter = FuncFormatter(to_percent)
    cmap = plt.get_cmap('nipy_spectral')
    colors = [cmap(i) for i in np.linspace(0, 1, len(measureNames))]
    plot = [] 
    fig, axarr = plt.subplots(1, 2,figsize=(12, 6))
    qualAx = axarr[0]
    qualAx.set_xlabel("TopK",fontsize=FONTSIZE)
    qualAx.set_ylabel("# label supspaces",fontsize=FONTSIZE)
    qualAx.tick_params(labelsize=FONTSIZE)
    for valuefile,label,color in zip(valuefiles, measureNames, colors) :
        label = MEASURE_SIMPLE_NAMES[label] if label in MEASURE_SIMPLE_NAMES else label
        data = pd.read_csv(valuefile,sep='\t',header=0, index_col = None)
        names = list(data)
        combinations = {}
        combinationCounts = []
        for combination in data[names[2]] :
            combinations[combination]=True
            combinationCounts.append(len(combinations))
        topk = range(1,len(data[names[1]])+1)
        qualAx.errorbar(topk,combinationCounts,fmt="-",linewidth=LINEWIDTH,label=label,color=color)

    qualAx = axarr[1]
    qualAx.set_xlabel("TopK",fontsize=FONTSIZE)
    qualAx.set_ylabel("quality/max",fontsize=FONTSIZE)
    qualAx.tick_params(labelsize=FONTSIZE)
    for valuefile,label,color in zip(valuefiles, measureNames, colors) :
        label = MEASURE_SIMPLE_NAMES[label] if label in MEASURE_SIMPLE_NAMES else label
        data = pd.read_csv(valuefile,sep='\t',header=0, index_col = None)
        names = list(data)
        qualities = sorted(np.array(data[names[3]]), reverse=True)
        topk = range(1,len(qualities)+1)
        qualAx.errorbar(topk,qualities/qualities[0],fmt="-",linewidth=LINEWIDTH,label=label,color=color)
    plt.gca().yaxis.set_major_formatter(formatter)
    legend = qualAx.legend(loc='upper right', shadow=False,fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(output+"/topqualitiesandcombinations.pdf",bbox_inches='tight')

def plotQualities(valuefiles, measureNames, output):
    formatter = FuncFormatter(to_percent)
    cmap = plt.get_cmap('nipy_spectral')
    colors = [cmap(i) for i in np.linspace(0, 1, len(measureNames))]
    plot = []
    fig, qualAx = plt.subplots()
    qualAx.set_xlabel("TopK",fontsize=FONTSIZE)
    qualAx.set_ylabel("quality/max",fontsize=FONTSIZE)
    qualAx.tick_params(labelsize=FONTSIZE)
    plt.gca().yaxis.set_major_formatter(formatter)
    for valuefile,label,color in zip(valuefiles, measureNames, colors) :
        label = MEASURE_SIMPLE_NAMES[label] if label in MEASURE_SIMPLE_NAMES else label
        data = pd.read_csv(valuefile,sep='\t',header=0, index_col = None)
        names = list(data)
        qualities = sorted(np.array(data[names[3]]), reverse=True)
        topk = range(1,len(qualities)+1)
        qualAx.errorbar(topk,qualities/qualities[0],fmt="-",linewidth=LINEWIDTH,label=label,color=color)
    legend = qualAx.legend(loc='upper right', shadow=False,fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(output+"/topqualities.pdf",bbox_inches='tight')

def plotLabels(valuefiles, measureNames, output):
    cmap = plt.get_cmap('nipy_spectral')
    colors = [cmap(i) for i in np.linspace(0, 1, len(measureNames))]
    plot = []
    fig, qualAx = plt.subplots()
    qualAx.set_xlabel("TopK",fontsize=FONTSIZE)
    qualAx.set_ylabel("# label supspaces",fontsize=FONTSIZE)
    qualAx.tick_params(labelsize=FONTSIZE)
    for valuefile,label,color in zip(valuefiles, measureNames, colors) :
        label = MEASURE_SIMPLE_NAMES[label] if label in MEASURE_SIMPLE_NAMES else label
        data = pd.read_csv(valuefile,sep='\t',header=0, index_col = None)
        names = list(data)
        combinations = {}
        combinationCounts = []
        for combination in data[names[2]] :
            combinations[combination]=True
            combinationCounts.append(len(combinations))
        topk = range(1,len(data[names[1]])+1)
        qualAx.errorbar(topk,combinationCounts,fmt="-",linewidth=LINEWIDTH,label=label,color=color)  
    legend = qualAx.legend(loc='upper left', shadow=False,fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(output+"/topcombinations.pdf",bbox_inches='tight')


def plot(BASE) :
    PATHS=[]
    measures = [ name for name in listdir(BASE) if isdir(join(BASE, name)) ]
    for measure in measures :
        PATH=BASE+"/"+measure+"/result.log"
        PATHS.append(PATH)
    plotQualities(PATHS,measures,BASE)
    plotLabels(PATHS,measures,BASE)
    plotQualitiesAndLabels(PATHS,measures,BASE)

plot(sys.argv[1])
