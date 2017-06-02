#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import basename, splitext,abspath, dirname
from math import tanh
import argparse

# ------------------------------------------
FONTSIZE=15
# ------------------------------------------
def getDefaultXLbeta(counts):
    return (np.percentile(counts,85),np.percentile(counts,85)-np.percentile(counts,80))
    
def beta(xbeta, lbeta, support):
    return 0.5*(1 + tanh((xbeta-float(support))/lbeta))

def loadManualxlBetas(basefile): 
    data = pd.read_csv(basefile,sep=',',header=0, index_col = None)
    xlbetas = {}
    filename = list(data)[0]
    xbeta = list(data)[1]
    lbeta = list(data)[2]

    for _, row in data.iterrows() :
        xlbetas[row[filename]]=(row[xbeta],row[lbeta])

    return xlbetas

def getxlbeta(arffFile, manual):
    try :
        xlbeta = loadManualxlBetas(args.manual)[splitext(basename(args.arfffile))[0]]
    except Exception:
        names,values=getQualities(arffFile)
        counts = getQualityDistribution(names,values)
        xlbeta = getDefaultXLbeta(counts)
    return xlbeta
    
# ------------------------------------------
def getQualities(arffFile):
    qualityNames = []
    qualityValues = []
    with open(arffFile,'r') as f :
        qualityIds=[]
        attr_index = -1
        isData = False
        for line in f:
            line = line.strip()
            if not line : continue
            if line[0]=='%' : continue
            if isData :
                if line[0]=="{" and line[-1]=="}" :
                    elements = set([int(l.split(" ")[0]) for l in line[1:-2].split(",")])
                    line = ["1" if i in elements else "0" for i in range(attr_index+1)]
                else :
                    line = line.split(",")
                qualityValues.append([line[i] for i in qualityIds])
            if line[0]=="@" :
                line = line.split()
                if line[0] == "@relation" : continue
                elif line[0] == "@attribute" :
                    attr_index += 1
                    if line[2] == "label" :
                        qualityIds.append(attr_index)
                        qualityNames.append(line[1])
                    else : continue
                elif line[0] == "@data" :
                    isData = True
                else :
                    raise NameError("Incorrect token "+line[0])
    return qualityNames, qualityValues
    
def getAttributes(arffFile, attrTypes):
    attributeNames = []
    attributeValues = []
    with open(arffFile,'r') as f :
        attributeIds=[]
        attr_index = -1
        isData = False
        for line in f:
            line = line.strip()
            if not line : continue
            if line[0]=='%' : continue
            if isData :
                if line[0]=="{" and line[-1]=="}" :
                    elements = set([int(l.split(" ")[0]) for l in line[1:-2].split(",")])
                    line = ["1" if i in elements else "0" for i in range(attr_index+1)]
                else :
                    line = line.split(",")
                attributeValues.append([line[i] for i in attributeIds])
            if line[0]=="@" :
                line = line.split()
                if line[0] == "@relation" : continue
                elif line[0] == "@attribute" :
                    attr_index += 1
                    if line[2] in attrTypes :
                        attributeIds.append(attr_index)
                        attributeNames.append(line[1])
                    else : continue
                elif line[0] == "@data" :
                    isData = True
                else :
                    raise NameError("Incorrect token "+line[0])
    return attributeNames, attributeValues

# ------------------------------------------

def exportCSV(names, values, destination) :
    with open(destination,"w") as f :
        if names : f.write("\t".join(names)+"\n")
        for line in values:
            f.write("\t".join(line)+"\n")

def transform(arffFile, attrTypes) :
    qualityNames,qualityValues = getQualities(arffFile)
    attributeNames,attributeValues = getAttributes(arffFile, attrTypes)
    qualityDestination = "qualities.csv"
    attributeDestination = "attributes.csv"
    objectDestination = "objects.csv"
    print "Outputing qualities of %s in %s ..."%(arffFile, qualityDestination)
    exportCSV(qualityNames,qualityValues,qualityDestination)
    print "Outputing %s attributes of %s in %s ..."%(attrTypes, arffFile, attributeDestination)
    exportCSV(attributeNames,attributeValues,attributeDestination)
    print "Outputing objects names of %s in %s ..."%(arffFile, objectDestination)
    exportCSV(None,[[str(i+1)] for i in range(len(qualityValues))],objectDestination)
    

# ------------------------------------------

def getQualityDistribution(qualityNames, qualityValues):
    qualitiesMap={qualityNames[i]:[int(qualityValues[j][i]) for j in range(len(qualityValues))] for i in range(len(qualityNames))}
    counts = np.array([sum(np.array(qualitiesMap[name])) for name in qualityNames])
    return counts

def printQualityStats(qualityNames, qualityValues):
    cardinality = float(sum([sum([int(i) for i in line]) for line in qualityValues]))/len(qualityValues)
    counts = getQualityDistribution(qualityNames, qualityValues)
    combinations = len(set([tuple(line) for line in qualityValues]))
    print "#instances:",len(qualityValues)
    print "#labels:",len(qualityNames)
    print "#combinations:",combinations
    print "cardinality:",cardinality
    print "density:",cardinality/len(qualityNames)
    print "min label support:",np.amin(counts)
    print "median label support:",np.percentile(counts,50)
    print "mean label support:",np.mean(counts)
    print "max label support:",np.amax(counts)


def boxplotWithBeta(arffFile, xlbeta = None) :
    names,values=getQualities(arffFile)
    parentname = abspath(dirname(arffFile))
    filename=splitext(basename(arffFile))[0]
    counts = getQualityDistribution(names,values)
    if not xlbeta :
        xlbeta=getDefaultXLbeta(counts)
    fig, ax = plt.subplots()
    xbeta,lbeta = xlbeta
    supports = range(0,max(counts),1)
    betas = np.array([beta(xbeta,lbeta,support) for support in supports])
    label="beta(%.2f,%.2f)"%(xbeta,lbeta)
    ax.plot(supports,betas, label = label)
    ax.text(0,0,filename,fontsize = FONTSIZE)
    ax2 = ax.twinx()
    ax2.boxplot(counts, vert=False)
    ax2.yaxis.set_visible(False)
    ax.set_xticks(([0] if min(counts) > 100 else [])+[min(counts),(max(counts)+min(counts))/2.,max(counts)])
    legend = ax.legend(loc='upper right', shadow=False,fontsize=FONTSIZE)
    ax.tick_params(labelsize=FONTSIZE)
    ax2.tick_params(labelsize=FONTSIZE)
    fig.tight_layout()
    destination=parentname+"/"+filename+".pdf"
    print "Outputing Figure in %s ..."%destination
    plt.savefig(destination,bbox_inches='tight')

# ------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='base')
    subparsers = parser.add_subparsers(help='sub-commands',dest="subparser_name")

    ptransform = subparsers.add_parser('transform', help='transform')
    ptransform.add_argument('arfffile', type=str, help='.arff file')
    ptransform.add_argument('--types', type=str, choices=["numeric","symbolic","boolean"], nargs='+', help='type to extract',required=True)

    pplot = subparsers.add_parser('boxplot', help='boxplot')
    pplot.add_argument('arfffile', type=str, help='.arff file')
    pplot.add_argument('--xbeta', type=float, help='xbeta')
    pplot.add_argument('--lbeta', type=float, help='lbeta')
    pplot.add_argument('--manual', type=str, help='manual xbeta and lbeta source file')

    pxlbeta = subparsers.add_parser('xlbeta', help='print xbeta and lbeta')
    pxlbeta.add_argument('arfffile', type=str, help='.arff file')
    pxlbeta.add_argument('--manual', type=str, help='manual xbeta and lbeta source file')

    args = parser.parse_args()
    if args.subparser_name=="transform" :
        transform(args.arfffile,args.types)
    elif args.subparser_name=="boxplot" :
        if args.manual :
            try :
                xlbeta = loadManualxlBetas(args.manual)[splitext(basename(args.arfffile))[0]]
                args.xbeta = xlbeta[0]
                args.lbeta = xlbeta[1]
            except Exception:
                pass
        boxplotWithBeta(args.arfffile,(args.xbeta,args.lbeta) if args.xbeta and args.lbeta else None)
    elif args.subparser_name=="xlbeta" :
        result = getxlbeta(args.arfffile,args.manual)
        print result[0],result[1]

# ------------------------------------------
