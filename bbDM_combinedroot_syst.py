import sys
import os
import optparse
import argparse
from array import array
from glob import glob
from ROOT import TFile, gROOT, kBlack,TH1F

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

parser.add_option("-D", "--pDir", type="string",
                  dest="rootFileDir", help="directory containing histogram")
parser.add_option("-S", "--sigDir", type="string", dest="SIGrootFileDir",
                  help="directory containing signal histogram")
parser.add_option("-t", "--tag", type="string",
                  dest="plot_tag", help="version of histogram")
parser.add_option("-e", "--era", type="string",
                  dest="era_year", help="year of histogram")

(options, args) = parser.parse_args()

runOn2016 = False
runOn2017 = False
runOn2018 = False

if options.era_year == '2016':
    runOn2016 = True
    rebin_ = True
elif options.era_year == '2017':
    runOn2017 = True
    rebin_ = False
elif options.era_year == '2018':
    runOn2018 = True
    rebin_ = False
else:
    print('Please provide on which year you want to run?')

if runOn2016:
    import sig_sample_xsec_2016 as xsec_dict
    luminosity = 35.82 * 1000
    era_name = 'bbDM2016_'
elif runOn2017:
    import sig_sample_xsec_2017 as xsec_dict
    luminosity = 41.5 * 1000
    era_name = 'bbDM2017_'
elif runOn2018:
    import sig_sample_xsec_2018 as xsec_dict
    luminosity = 59.64 * 1000
    era_name = 'bbDM2018_'

gROOT.SetBatch(True)

if options.rootFileDir == None:
    print('Please provide histogram directory name')
    sys.exit()
else:
    CRSRPath = options.rootFileDir

if options.SIGrootFileDir == None:
    print('Please provide signal histogram directory name')
    sys.exit()
else:
    SignalPath = options.SIGrootFileDir

if options.plot_tag == None:
    print('Please provide histogram directory name')
    sys.exit()
else:
    plot_tag = options.plot_tag

CRSRFiles = [CRSRPath+'/' +fl for fl in os.listdir(CRSRPath) if ('_Recoil' in fl and 'CR' in fl) or ('_MET' in fl and 'SR' in fl)]
SignalFiles = [SignalPath+'/' +fl for fl in os.listdir(SignalPath) if '.root' in fl and 'bbDM_2HDMa' in fl]

rebin_ = False

def setHistStyle(h_temp2, newname, rebin=False):
    if rebin:
        h_temp = h_temp2.Rebin(len(bins)-1, "h_temp", array('d', bins))
    else:
        h_temp = h_temp2
    h_temp.SetName(newname)
    h_temp.SetTitle(newname)
    h_temp.SetLineWidth(1)
    h_temp.SetMarkerColor(kBlack)
    h_temp.SetMarkerStyle(2)
    return h_temp
    
SRCRhistos=['bkgSum','DIBOSON','ZJets','GJets','QCD','SMH','STop','Top','WJets','DYJets','data_obs']

bins = [200,250,350,500,1000]
# binsv1 = [200, 240, 300, 400, 550, 1000]
# binsv2 = [200, 235, 290, 400, 550, 1000]
# binsv3 = [200, 230, 290, 410, 550, 1000]

f=TFile("DataCardRootFiles/AllMETHistos_"+plot_tag+".root","RECREATE")

for infile in CRSRFiles:
    # print ('checking code for ',infile)
    fin       =   TFile(infile,"READ")
    rootFile  = infile.split('/')[-1]
    reg       = rootFile.split('_')[3]+'_'+rootFile.split('_')[2]
    syst = ''
    if '_up.root' in infile or '_down.root' in infile:
        laststr = infile.split('/')[-1]
        syst    = '_'+laststr.split("_")[-2]+'_'+laststr.split("_")[-1].replace('.root','')
    if ('MET' in infile and 'SR' not in infile): continue# or ('Recoil' not in infile): continue
    # print ('running code for ',infile)
    reg = reg.replace('ZmumuCR','ZMUMU').replace('ZeeCR','ZEE').replace('WmunuCR','WMU').replace('WenuCR','WE').replace('TopmunuCR','TOPMU').replace('TopenuCR','TOPE')

    for hist in SRCRhistos:
        temp   = fin.Get(hist)
        hist = hist.replace('DIBOSON', 'diboson').replace('ZJets', 'zjets').replace('GJets', 'gjets').replace('QCD', 'qcd').replace('STop', 'singlet').replace('Top', 'tt').replace('WJets', 'wjets').replace('DYJets', 'dyjets').replace('STop', 'singlet').replace('SMH','smh')
        newName   = era_name+reg+'_'+str(hist)+syst
        if not syst=='' and hist=='data_obs':continue
        if temp.Integral() == 0.0:
            HISTNAME=newName
            temp = TH1F(newName, newName, temp.GetXaxis().GetNbins(),200,1000)
            # temp = TH1F(newName, newName, temp.GetXaxis().GetNbins(),array('d', bins))
            # print ('=================',hist)
            # print ('=================',temp.GetXaxis().GetNbins())
            for bin in range(temp.GetXaxis().GetNbins()):
                temp.SetBinContent(bin+1,0.00001)
                if temp.GetBinError(bin)<0:
                    temp.SetBinError(bin,0.0)
        for bin in range(temp.GetXaxis().GetNbins()):
            if temp.GetBinContent(bin+1)==0:
                temp.SetBinContent(bin+1,0.00001)
            if temp.GetBinError(bin)<0:
                temp.SetBinError(bin,0.0)
        myHist = setHistStyle(temp, newName, rebin_)
        f.cd()
        myHist.Write()

for cat in ['1b','2b']:
    for infile in SignalFiles:
        # print ('infile',infile)
        fin = TFile(infile,"READ")
        rootFile = infile.split('/')[-1]
        if runOn2016:
            ma=rootFile.split('_')[4].strip('Ma')
            mA=rootFile.split('_')[6].strip('MA')       
        else:
            ma = rootFile.split('_')[9]
            mA = rootFile.split('_')[11].strip('.root')

        if runOn2016:
            sampStr = 'Ma'+ma+'_MChi1_MA'+mA
            CS = xsec_dict.CSList_0[sampStr]
        else:
            sampStr = 'ma_'+ma+'_mA_'+mA
            CS = xsec_dict.CSList_150[sampStr]

        for syst in ['MET','weightB','weightEWK','weightTop','weightMET','weightEle','weightMu','weightPU','weightJEC','Res','En'] :
            if syst=='MET':
                temp = fin.Get('h_reg_SR_'+cat+'_MET')
                if  temp.Integral() == 0.0:
                    for bin in range(temp.GetXaxis().GetNbins()):
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                for bin in range(temp.GetXaxis().GetNbins()):
                    if temp.GetBinContent(bin)==0:
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                h_total = fin.Get('h_total_mcweight')
                totalEvents = h_total.Integral()
                temp.Scale((luminosity*CS)/(totalEvents))
                samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7'
                myHist = setHistStyle(temp, samp, rebin_)
                f.cd()
                myHist.Write()
            else:
                for ud in ['up','down']:
                    temp = fin.Get('h_reg_SR_'+cat+'_MET_'+syst+'_'+ud)
                    if  temp.Integral() == 0.0:
                        for bin in range(temp.GetXaxis().GetNbins()):
                            temp.SetBinContent(bin,0.00001)
                            if temp.GetBinError(bin)<0:
                                temp.SetBinError(bin,0.0)
                    for bin in range(temp.GetXaxis().GetNbins()):
                        if temp.GetBinContent(bin)==0:
                            temp.SetBinContent(bin,0.00001)
                        if temp.GetBinError(bin)<0:
                            temp.SetBinError(bin,0.0)
                    h_total = fin.Get('h_total_mcweight')
                    totalEvents = h_total.Integral()
                    temp.Scale((luminosity*CS)/(totalEvents))
                    samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_'+syst+'_'+ud
                    myHist = setHistStyle(temp, samp, rebin_)
                    f.cd()
                    myHist.Write()
print('*************DONE*************')
print("Saved histograms in DataCardRootFiles/AllMETHistos_"+plot_tag+".root file")
print('******************************')
f.Close()
