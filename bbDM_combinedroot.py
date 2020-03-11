import sys,os,array

from array import array
from glob import glob

from ROOT import TFile, gROOT, kBlack,TH1F

import signal_xsec_list as xsec_dict

gROOT.SetBatch(True)

#CRSRPath = '/Users/dekumar/MEGA/Fullwork/2017_Plotting/22102019/monoHROOT'
CRSRPath = '/Users/ptiwari/cernbox/plottingTools/plots_norm/14012020_2016/bbDMRoot/2016_bkg_rootFiles'
#SignalPath = '/Users/dekumar/MEGA/Fullwork/2017_Plotting/rootFiles_Signal'
SignalPath = '/Users/ptiwari/cernbox/plottingTools/Signal_Histo_2016_02022020_official'

CRSRFiles = [CRSRPath+'/'+fl for fl in os.listdir(CRSRPath) if 'Recoil' in fl or 'MET' in fl]
SignalFiles = [SignalPath+'/'+fl for fl in os.listdir(SignalPath) if '.root' in fl]

os.system('rm -rf DataCardRootFiles')
os.system('mkdir DataCardRootFiles')


def setHistStyle(h_temp,newname):

    #h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
    h_temp.SetName(newname)
    h_temp.SetTitle(newname)
    h_temp.SetLineWidth(1)
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    #h_temp.GetXaxis().SetRangeUser(200,1000)
    h_temp.SetMarkerColor(kBlack);
    h_temp.SetMarkerStyle(2);
    return h_temp


def reBin(h_temp,bins):

    h_temp=h_temp.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    # h_temp.GetXaxis().SetRangeUser(200,1000)
    #h_temp.SetMarkerColor(kBlack);
    #h_temp.SetMarkerStyle(2);
    return h_temp


#xsec_dict.CSList_150 = {'ma_150_mA_300':1.606,'ma_150_mA_400':0.987,'ma_150_mA_500':0.5074,'ma_150_mA_600':0.2984,'ma_150_mA_1000':0.0419,'ma_150_mA_1200':0.0106,'ma_150_mA_1600':0.07525}


print ('xsec_dict.CSList_0',xsec_dict.CSList_0)

SRCRhistos=['bkgSum','DIBOSON','ZJets','GJets','QCD','STop','Top','WJets','DYJets','data_obs']

bins= [200,250,350,500,1000]

f=TFile("DataCardRootFiles/AllMETHistos.root","RECREATE")

for infile in CRSRFiles:
    print ('checking code for ',infile)
    fin       =   TFile(infile,"READ")
    rootFile  = infile.split('/')[-1]
    reg       = rootFile.split('_')[3]+'_'+rootFile.split('_')[2]
    #print('reg', rootFile.split('_')[2]+'_'+rootFile.split('_')[3])

    if ('MET' in infile and 'SR' not in infile):continue# or ('Recoil' not in infile): continue
    print ('running code for ',infile)
    reg = reg.replace('Zmumu','ZMUMU').replace('Zee','ZEE').replace('Wmunu','WMUNU').replace('Wenu','WENU').replace('Topmunu','TOPMUNU').replace('Topenu','TOPENU')

    for hist in SRCRhistos:
        temp   = fin.Get(hist)
        hist=hist.replace('DIBOSON','diboson').replace('ZJets','zjets').replace('GJets','gjets').replace('QCD','qcd').replace('STop','singlet').replace('Top','tt').replace('WJets','wjets').replace('DYJets','dyjets')
        newName   = 'bbDM2016_'+reg+'_'+str(hist)

        if temp.Integral() == 0.0:
            HISTNAME=newName
            temp = TH1F(newName, newName, 4, array('d',bins))
            # print ('=================',hist)
            # print ('=================',temp.GetXaxis().GetNbins())
            for bin in range(4):
                temp.SetBinContent(bin+1,0.00001)

        myHist = setHistStyle(temp,newName)
        f.cd()
        myHist.Write()


lumi = 35.8*1000

BR = 0.588

for cat in ['1b','2b']:
    for infile in SignalFiles:
        #print ('infile',infile)
        fin       =   TFile(infile,"READ")
        rootFile = infile.split('/')[-1]
        #print ('rootFile', rootFile.split('_'))
        ma=rootFile.split('_')[6].strip('Ma')
        mA=rootFile.split('_')[8].strip('MA')

        if mA=='1400': continue

        sampStr = 'Ma'+ma+'_MChi1_MA'+mA
        #Ma250_MChi1_MA1200
        CS = xsec_dict.CSList_0[sampStr]
        temp = fin.Get('h_reg_SR_'+cat+'_MET')

        if  temp.Integral() == 0.0:
            for bin in range(temp.GetXaxis().GetNbins()):
                temp.SetBinContent(bin,0.00001)

        h_total = fin.Get('h_total_mcweight')
        totalEvents = h_total.Integral()
        temp.Scale((lumi*CS*BR)/(totalEvents))
        samp = 'bbDM2016_'+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7'
        if int(mA)==1200:
            print (ma)
        #samp = 'bbDM2016_'+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA

        myHist = setHistStyle(temp,samp)
        #print('myHist name  ',myHist.GetName())
        f.cd()
        myHist.Write()


f.Close()
