import sys
import os
import optparse
import numpy as np
from array import array
from ROOT import TFile, gROOT, kBlack,TH1F

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

parser.add_option("-D", "--pDir", type="string",
                  dest="rootFileDir", help="directory containing histogram")
parser.add_option("-S", "--sigDir", type="string", dest="SIGrootFileDir",
                  help="directory containing signal histogram")
parser.add_option("-t", "--tag", type="string",
                  dest="plot_tag", help="version of histogram")
parser.add_option("-y", "--year", type="string",
                  dest="era_year", help="year of histogram")

(options, args) = parser.parse_args()

runOn2016 = False
runOn2017 = False
runOn2018 = False

if options.era_year == '2016':
    runOn2016 = True
elif options.era_year == '2017':
    runOn2017 = True
elif options.era_year == '2018':
    runOn2018 = True
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


# limit_var  = 'bdtscore'
# minBin = -1
# maxBin = 1
# limit_var = 'ctsValue'
# minBin = 0
# maxBin = 1

# CRSRFiles = [CRSRPath+'/' +fl for fl in os.listdir(CRSRPath) if ('_'+limit_var in fl and 'CR' in fl) or ('_'+limit_var in fl and 'SR' in fl)]

CRSRFiles = [CRSRPath+'/' + fl for fl in os.listdir(CRSRPath) if (
    '_Recoil' in fl and 'CR' in fl) or ('_MET' in fl and 'SR' in fl) or ('_ctsValue' in fl)]

SignalFiles = [SignalPath+'/' + fl for fl in os.listdir(
    SignalPath) if '.root' in fl and ('bbDM_2HDMa' in fl or 'bbDM_DMSimp' in fl)]


def setHistBin(h_temp2, histname, limit_var, emptyHist=False):
    if 'ctsValue' in limit_var:
        bins = [0.0, 0.25, 0.50, 0.75, 1.0]
        # bins = [0.0 , 0.45, 0.80 , 0.95, 1.0] # binset_v2
        # bins = [0.0 , 0.40, 0.75 , 0.90, 1.0]  # binset_v3
        # bins = [0.0 , 0.35, 0.55 , 0.75, 1.0]  # binset_v4
        # bins = [0.0, 0.20, 0.50, 0.80, 1.0]  # binset_v5
        # bins = [0.0, 0.3, 0.5, 0.7, 0.85, 1.0] # binset_v6
        # bins = [0.0, 0.17, 0.34, 0.51, 0.68, 0.84,1.0] # binset_v7
        # bins = [0., 0.125, 0.25, 0.375, 0.5, 0.625 ,0.75, 0.875, 1.] # binset_v8
        # bins = [0., 0.15, 0.25, 0.35, 0.45, 0.55 ,0.65, 0.80, 1.] # binset_v9
        #bins = [0., 0.10, 0.25, 0.40, 0.45, 0.60 ,0.75, 0.90, 1.] # binset_v10
        # bins = [0., 0.15, 0.25, 0.35, 0.45, 0.57 ,0.65, 0.80, 1.] # binset_v11
    else:
        bins = [250, 300, 400, 550, 1000]
    # bins = np.linspace(-1.0, 1.0, num = 5)
    # bins = [-1, -0.3, 0.0, 0.3, 1]
    # bins = [-1, -0.1, 0.0, 0.1, 1.0]
    # bins = [-1, -0.1, -0.05, 0.0, 0.05, 0.1, 1.0]  # binset5
    # bins = [-1, -0.1, -0.01, 0.01, 0.1, 1.0]  # binset6
    # bins = [-1, -0.1, -0.03, 0.03, 0.1, 1.0]  # binset7
    # bins = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    if not emptyHist:
        h_temp = h_temp2.Rebin(len(bins)-1, histname, array('d', bins))
    else:
        h_temp = TH1F(histname, histname, len(bins)-1, array('d', bins))
    return h_temp

def setHistStyle(h_temp, newname):
    h_temp.SetName(newname)
    h_temp.SetTitle(newname)
    h_temp.SetLineWidth(1)
    h_temp.SetMarkerColor(kBlack)
    h_temp.SetMarkerStyle(2)
    return h_temp

SRCRhistos=['bkgSum','DIBOSON','ZJets','GJets','QCD','SMH','STop','Top','WJets','DYJets','data_obs']

f=TFile("DataCardRootFiles/AllMETHistos_"+plot_tag+".root","RECREATE")

for infile in CRSRFiles:
    # print ('checking code for ',infile.split('/')[-1])
    if 'ctsValue' in infile.split('/')[-1]:
        limit_var = 'ctsValue'
        minBin = 0; maxBin = 1
    elif '_MET'in infile.split('/')[-1]:
        limit_var = 'MET'
        minBin = 250; maxBin = 1000
    elif '_Recoil' in infile.split('/')[-1]:
        limit_var = 'Recoil'
        minBin = 250; maxBin = 1000
    fin       =   TFile(infile,"READ")
    rootFile  = infile.split('/')[-1]
    reg       = rootFile.split('_')[3]+'_'+rootFile.split('_')[2]
    syst = ''
    if 'Up.root' in infile or 'Down.root' in infile:
        laststr = infile.split('/')[-1]
        if '_'+limit_var+'_' in laststr:
            syst = laststr.partition(limit_var)[-1].replace('.root', '')
        syst = syst.replace('year', options.era_year)
    reg = reg.replace('ZmumuCR','ZMUMU').replace('ZeeCR','ZEE').replace('WmunuCR','WMU').replace('WenuCR','WE').replace('TopmunuCR','TOPMU').replace('TopenuCR','TOPE').replace('2j','1b').replace('3j','2b')
    for hist in SRCRhistos:
        temp = setHistBin(fin.Get(hist), hist, limit_var)
        hist = hist.replace('DIBOSON', 'diboson').replace('ZJets', 'zjets').replace('GJets', 'gjets').replace('QCD', 'qcd').replace('STop', 'singlet').replace('Top', 'tt').replace('WJets', 'wjets').replace('DYJets', 'dyjets').replace('STop', 'singlet').replace('SMH','smh')
        newName   = era_name+reg+'_'+str(hist)+syst
        if not syst=='' and hist=='data_obs':continue
        if temp.Integral() <= 0.0: #<=$
            # temp = TH1F(newName, newName, temp.GetXaxis().GetNbins(),minBin,maxBin)
            temp = setHistBin(temp, newName, limit_var, True)
            for bin in range(1,temp.GetXaxis().GetNbins()+1):
                temp.SetBinContent(bin,0.00001)
                if temp.GetBinError(bin)<0:
                    temp.SetBinError(bin, 0.0)
        for bin in range(1,temp.GetXaxis().GetNbins()+1):
            if temp.GetBinContent(bin)<= 0.0: #<=$
                temp.SetBinContent(bin,0.00001)
            if temp.GetBinError(bin)<0:
                temp.SetBinError(bin, 0.00)
        f.cd()
        if 'Up' in newName or 'Down' in newName:
            newName = era_name+reg+'_'+str(hist)+syst
            temp_syst = temp.Clone('temp_syst')
            myHist_syst = setHistStyle(temp_syst, newName)
            myHist_syst.Write()
        else:
            newName_allbinUp = era_name+reg+'_'+str(hist)+syst+'_allbinUp'
            newName_allbinDown = era_name+reg+'_'+str(hist)+syst+'_allbinDown'
            temp_allbinUp = temp.Clone('temp_allbinUp')
            temp_allbinDown = temp.Clone('temp_allbinDown')
            for bin in range(1,temp.GetXaxis().GetNbins()+1):
                newName_up = era_name+reg+'_'+str(hist)+syst+'_eff_bin'+str(bin)+'Up'
                newName_down = era_name+reg+'_'+str(hist)+syst+'_eff_bin'+str(bin)+'Down'
                temp_up = temp.Clone('temp_up'+str(bin))
                temp_down = temp.Clone('temp_down'+str(bin))
                temp_up.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                temp_down.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
                for bin in range(1, temp_up.GetXaxis().GetNbins()+1):
                    if temp_up.GetBinContent(bin) <= 0.0: #<=$
                        temp_up.SetBinContent(bin, 0.00001)
                    if temp_down.GetBinContent(bin) <= 0.0: #<=$
                        temp_down.SetBinContent(bin, 0.00001)
                myHist_up = setHistStyle(temp_up, newName_up)
                myHist_down = setHistStyle(temp_down, newName_down)
                myHist_up.Write()
                myHist_down.Write()
            for bin in range(1,temp.GetXaxis().GetNbins()+1):
                temp_allbinUp.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                temp_allbinDown.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
                for bin in range(1, temp_allbinUp.GetXaxis().GetNbins()+1):
                    if temp_allbinUp.GetBinContent(bin) <= 0.0: #<=$
                        temp_allbinUp.SetBinContent(bin, 0.00001)
                    if temp_allbinDown.GetBinContent(bin) <= 0.0: #<=$
                        temp_allbinDown.SetBinContent(bin, 0.00001)
            # print(newName)
            myHist = setHistStyle(temp, newName)
            myHist_allbinUp = setHistStyle(temp_allbinUp, newName_allbinUp)
            myHist_allbinDown = setHistStyle(temp_allbinDown, newName_allbinDown)
            myHist.Write()
            myHist_allbinUp.Write()
            myHist_allbinDown.Write()
for cat in ['1b','2b']:
    for infile in SignalFiles:
        if '1b' in cat: limit_var = 'MET'
        elif '2b' in cat: limit_var = 'ctsValue'
        if '2HDMa' in infile: whichSig = 1
        elif 'DMSimp' in infile: whichSig = 0
        fin = TFile(infile,"READ")
        rootFile = infile.split('/')[-1]
        if runOn2016:
            if '2HDMa' in infile:
                ma=rootFile.split('_')[4].strip('Ma')
                mA=rootFile.split('_')[6].strip('MA')
            elif 'DMSimp' in infile:
                ma = rootFile.split('_')[7]
                mA = rootFile.split('_')[9].strip('.root')
        else:
            ma = rootFile.split('_')[9]
            mA = rootFile.split('_')[11].strip('.root')

        if runOn2016:
            if whichSig == 1:
                sampStr = 'Ma'+ma+'_MChi1_MA'+mA
                CS = xsec_dict.hdma_xsList_0[sampStr]
                # CS = xsec_dict.hdma_xsList_150[sampStr]
            elif whichSig == 0:
                sampStr = 'mphi_'+ma+'_mchi_'+mA
                CS = xsec_dict.dmsimp_xsList[sampStr]
        else:
            if whichSig == 1:
                sampStr = 'ma_'+ma+'_mA_'+mA
                CS = xsec_dict.hdma_xsList_150[sampStr]
            elif whichSig == 0:
                sampStr = 'mphi_'+ma+'_mchi_'+mA
                CS = xsec_dict.dmsimp_xsList_150[sampStr]
        for syst in [limit_var,'CMSyear_eff_b','CMSyear_fake_b','EWK','CMSyear_Top','CMSyear_trig_met','CMSyear_trig_ele', 'CMSyear_EleID', 'CMSyear_EleRECO', 'CMSyear_MuID','CMSyear_MuISO', 'CMSyear_MuTRK','CMSyear_PU','En','CMSyear_mu_scale','CMSyear_pdf','CMSyear_prefire','JECAbsolute','JECAbsolute_year','JECBBEC1','JECBBEC1_year','JECEC2','JECEC2_year','JECFlavorQCD','JECHF','JECHF_year','JECRelativeBal','JECRelativeSample_year'] :
            if syst == limit_var:
                temp = setHistBin(fin.Get('h_reg_SR_'+cat+'_'+limit_var), 'h_reg_SR_'+cat+'_'+limit_var, limit_var)
                if  temp.Integral() <= 0.0: #<=$
                    for bin in range(1,temp.GetXaxis().GetNbins()+1):
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                for bin in range(1,temp.GetXaxis().GetNbins()+1):
                    if temp.GetBinContent(bin) <= 0.0: #<=$
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                h_total = fin.Get('h_total_mcweight')
                totalEvents = h_total.Integral()
                temp.Scale((luminosity*CS)/(totalEvents))
                if whichSig==1:
                    samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7'
                elif whichSig <= 0:
                    samp = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1'
                myHist = setHistStyle(temp, samp)
                f.cd()
                myHist.Write()
                temp.Sumw2()
                ## up and down
                temp_allbinUp = temp.Clone('temp_allbinUp')
                temp_allbinDown = temp.Clone('temp_allbinDown')
                if whichSig == 1:
                    samp_allbinUp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_allbinUp'
                    samp_allbinDown = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_allbinDown'
                elif whichSig <= 0:
                    samp_allbinUp = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_allbinUp'
                    samp_allbinDown = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_allbinDown'
                for bin in range(1,temp.GetXaxis().GetNbins()+1):
                    temp_allbinUp.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                    temp_allbinDown.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
                    for bin in range(1, temp_allbinUp.GetXaxis().GetNbins()+1):
                        if temp_allbinUp.GetBinContent(bin) <= 0.0: #<=$
                            temp_allbinUp.SetBinContent(bin, 0.00001)
                        if temp_allbinDown.GetBinContent(bin) <= 0.0: #<=$
                            temp_allbinDown.SetBinContent(bin, 0.00001)
                myHist_allbinUp = setHistStyle(temp_allbinUp, samp_allbinUp)
                myHist_allbinDown = setHistStyle(temp_allbinDown, samp_allbinDown)
                myHist_allbinUp.Write()
                myHist_allbinDown.Write()
                for bin in range(1,temp.GetXaxis().GetNbins()+1):
                    temp_up = temp.Clone('temp_up'+str(bin))
                    temp_down = temp.Clone('temp_down'+str(bin))
                    if whichSig == 1:
                        samp_up = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_eff_bin'+str(bin)+'Up'
                        samp_down = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_eff_bin'+str(bin)+'Down'
                    elif whichSig <= 0:
                        samp_up = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_eff_bin'+str(bin)+'Up'
                        samp_down = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_eff_bin'+str(bin)+'Down'
                    temp_up.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                    temp_down.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
                    for bin in range(1,temp_up.GetXaxis().GetNbins()+1):
                        if temp_up.GetBinContent(bin) <= 0.0: #<=$
                            temp_up.SetBinContent(bin, 0.00001)
                        if temp_down.GetBinContent(bin) <= 0.0:  # <=$
                            temp_down.SetBinContent(bin, 0.00001)
                    myHist_up = setHistStyle(temp_up, samp_up)
                    myHist_down = setHistStyle(temp_down, samp_down)
                    myHist_up.Write()
                    myHist_down.Write()
            else:
                for ud in ['Up','Down']:
                    temp = setHistBin(fin.Get('h_reg_SR_'+cat+'_'+limit_var+'_'+syst+ud), 'h_reg_SR_'+cat+'_'+limit_var+'_'+syst+ud, limit_var)
                    if '_mu_scale' in syst:
                        print(ma,mA, temp.Integral())
                    if  temp.Integral() <= 0.0: #<=$
                        for bin in range(1,temp.GetXaxis().GetNbins()+1):
                            temp.SetBinContent(bin,0.00001)
                            if temp.GetBinError(bin)<0:
                                temp.SetBinError(bin,0.0)
                    for bin in range(1,temp.GetXaxis().GetNbins()+1):
                        if temp.GetBinContent(bin) == 0.0:  # <=$
                            temp.SetBinContent(bin,0.00001)
                        if temp.GetBinError(bin)<0:
                            temp.SetBinError(bin,0.0)
                    h_total = fin.Get('h_total_mcweight')
                    totalEvents = h_total.Integral()
                    temp.Scale((luminosity*CS)/(totalEvents))

                    if whichSig == 1:
                        samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_'+syst+ud
                    elif whichSig <= 0:
                        samp = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_'+syst+ud
                    samp = samp.replace('year', options.era_year)
                    myHist = setHistStyle(temp, samp)
                    f.cd()
                    myHist.Write()
print('*************DONE*************')
print("Saved histograms in DataCardRootFiles/AllMETHistos_"+plot_tag+".root file")
print('******************************')
f.Close()
