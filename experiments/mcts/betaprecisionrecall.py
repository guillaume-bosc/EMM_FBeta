#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import basename, splitext,abspath, dirname
from math import sqrt, tanh

#------------------------------------------------------------------
FONTSIZE = 15
LINEWIDTH = 5
MARKERSIZE=8
TOP=500
#------------------------------------------------------------------

def beta(xbeta, lbeta, support):
    return 0.5*(1 + tanh((xbeta-float(support))/lbeta))
def plot(logFile):
    parentname = abspath(dirname(logFile))
    xbetaFile = parentname+"/XBeta.csv"
    lbetaFile = parentname+"/LBeta.csv"
    
    data = pd.read_csv(logFile,sep='\t',header=0, index_col = None) 
    xbeta = pd.read_csv(xbetaFile,sep='\t',header=None, index_col = None)[0][0]
    lbeta = pd.read_csv(lbetaFile,sep='\t',header=None, index_col = None)[0][0]
    
    names = list(data)
    NOWTOP = min(len(data[names[3]]),TOP)
    E11=np.array(data[names[3]][:NOWTOP])
    E10=np.array(data[names[4]][:NOWTOP])
    E01=np.array(data[names[5]][:NOWTOP])

    supports = E11 + E01 
    precisions = E11/(E11+E10)
    recalls = E11/supports

    absoluteSupports = np.arange(0,max(supports)+1,5.)
    betas = np.array([beta(xbeta,lbeta,support) for support in absoluteSupports])

    fig, proportions = plt.subplots()
    proportions.set_xlabel("label subspace support",fontsize=FONTSIZE)
    proportions.set_xscale("log")
    proportions.tick_params(labelsize=FONTSIZE)
    plt.errorbar(supports,precisions,fmt="^",color="r", label="Precision", markersize = MARKERSIZE)
    plt.errorbar(supports,recalls,fmt="x",color="b", label="Recall", markersize = MARKERSIZE)
    plt.errorbar(absoluteSupports,betas,fmt="-",color="black",label="Beta", linewidth=LINEWIDTH)
    legend = proportions.legend(loc='lower left', shadow=False,fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(parentname+"/betaprecisionrecall.pdf",bbox_inches='tight')

plot(sys.argv[1])
