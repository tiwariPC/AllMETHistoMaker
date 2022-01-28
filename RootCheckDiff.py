from ROOT import TFile

import os,traceback
import sys, optparse,argparse

import glob


usage = "python DataframeToHist.py -F -inDir directoryName -D outputDir "
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-f", "--firstfile",  dest="firstfile",default="myfiles.root")
parser.add_argument("-s", "--secondfile",  dest="secondfile",default="myfiles2.root")

args = parser.parse_args()

infilename1  = args.firstfile
infilename2  = args.secondfile

f = TFile.Open(infilename1, "READ")
f2 = TFile.Open(infilename2, "READ")

Keys = f.GetListOfKeys()

for key in Keys:
    if key.GetClassName() == 'TDirectory':
        td = key.ReadObj()
        dirName = td.GetName()
        dirs[dirName] = td

    elif key.GetClassName() == 'TH1F':
        hist = key.ReadObj()
        histName = hist.GetName()
        if '_B_' in histName:continue# or 'Up' in histName or 'Down' in histName:continue
        hist2 = f2.Get(histName)

        number1 = hist.Integral()
        number2 = hist2.Integral()

        if number1!=number2:
            print ("Difference in histogram:  ",histName)
            print ("integral from first file ", number1)
            print ("integral from second file ",number2)

    else:continue