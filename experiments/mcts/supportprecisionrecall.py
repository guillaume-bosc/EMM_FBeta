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
TOP=500
#------------------------------------------------------------------

def plot(logFile):
    parentname = abspath(dirname(logFile))
    data = pd.read_csv(logFile,sep='\t',header=0, index_col = None)
    
    names = list(data)
    NOWTOP = min(len(data[names[3]]),TOP)
    E11=np.array(data[names[3]][:NOWTOP])
    E10=np.array(data[names[4]][:NOWTOP])
    E01=np.array(data[names[5]][:NOWTOP])

    supports = E11 + E01 
    precisions = E11/(E11+E10)
    recalls = E11/supports

    fig, proportions = plt.subplots()
    proportions.set_xlabel("Precision",fontsize=FONTSIZE)
    proportions.set_ylabel("Recall",fontsize=FONTSIZE)
    proportions.tick_params(labelsize=FONTSIZE)
    plt.scatter(precisions,recalls,c=supports,s=100,vmin = 0, vmax = max(supports), cmap="jet")
    cbar=plt.colorbar()
    cbar.ax.tick_params(labelsize=FONTSIZE)
    cbar.set_label("# label subspace support",fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(parentname+"/supportprecisionrecall.pdf",bbox_inches='tight')

plot(sys.argv[1])
