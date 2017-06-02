#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import basename, splitext,abspath, dirname
from math import sqrt

#------------------------------------------------------------------
FONTSIZE = 15
LINEWIDTH = 5
MEASURE_SIMPLE_NAMES={"RelativeF1":"RF1", "WeightedRelativeF1":"WRF1",
          "FBeta":"FBeta","RelativeFBeta":"RFBeta","WeightedRelativeFBeta":"WRFBeta"}
#------------------------------------------------------------------
def plot(logFile):
    parentname = abspath(dirname(logFile))
    measureName = basename(parentname)
    measureName = MEASURE_SIMPLE_NAMES[measureName] if measureName in MEASURE_SIMPLE_NAMES else measureName
    data = pd.read_csv(logFile,sep='\t',header=0, index_col = None)
    names = list(data)
    possiblesLabels = set(data[names[1]])
    maximum = data.iloc[0][names[2]]
    labels = []
    supports = []
    counts = []
    means=[]
    stds = []
    for label in possiblesLabels :
        rules  = data[data[names[1]]==label]
        support = rules.iloc[0][names[3]]+rules.iloc[0][names[5]]
        count = len(rules)
        qualityMean = np.amax(rules[names[2]])
        qualityStd = np.std(rules[names[2]])
        labels.append(label)
        supports.append(support)
        counts.append(count)
        means.append(qualityMean)
        stds.append(qualityStd)
    fig, proportions = plt.subplots()
    proportions.set_xlabel("Target subspace support",fontsize=FONTSIZE)
    proportions.set_ylabel("# Subgroups",fontsize=FONTSIZE)
    proportions.tick_params(labelsize=FONTSIZE)
    supports, counts, means = zip(*sorted(zip(supports, counts, means), key= lambda element : element[2]))
    plt.scatter(supports,counts,c=means,s=100,vmin = 0, vmax = maximum,cmap='jet')
    cbar=plt.colorbar()
    cbar.ax.tick_params(labelsize=FONTSIZE)
    cbar.set_label(measureName,fontsize=FONTSIZE)
    filename = logFile.split("_")[0]
    plt.title(filename+" - "+measureName+" - "+str(len(possiblesLabels))+" label subspaces", fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(parentname+"/topcardistribution.pdf",bbox_inches='tight')

plot(sys.argv[1])
