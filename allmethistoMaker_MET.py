import sys
import os
import optparse
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
SignalFiles = [SignalPath+'/' + fl for fl in os.listdir(SignalPath) if '.root' in fl and ('bbDM_2HDMa' in fl or 'bbDM_DMSimp' in fl)]


def setHistBin(h_temp2, histname):
    rebin = True
    bins = [250,300,400,550,1000] ## baseline binning for MET
    # bins = [250, 275, 300, 350, 400, 475, 550, 775, 1000]
    # bins = [250, 280, 340, 460, 1000]
    # bins = [250, 275, 325, 400, 1000]
    # bins = [250, 265, 325, 425, 1000]
    # bins = [250,270,320,400,1000]
    # bins = [250, 300, 325, 375, 1000]
    # bins = [250, 260, 300, 350, 1000]
    # bins = [250, 300, 350, 400, 500]
    # bins = [250, 313, 375, 437, 500]
    # bins = [250,280,310,340,500]
    # bins = [250,260,270,280,1000]
    # bins = [250, 260, 270, 280, 300, 350, 400, 500, 1000]
    if rebin:
        h_temp = h_temp2.Rebin(len(bins)-1, histname, array('d', bins))
    else:
        h_temp = h_temp2
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
    # print ('checking code for ',infile)
    fin       =   TFile(infile,"READ")
    rootFile  = infile.split('/')[-1]
    reg       = rootFile.split('_')[3]+'_'+rootFile.split('_')[2]
    syst = ''
    if 'Up.root' in infile or 'Down.root' in infile:
        laststr = infile.split('/')[-1]
        #print('laststr',laststr)
        # syst = '_'+laststr.split("_")[-1]+'_'+laststr.split("_")[-1].replace('.root','')
        if '_MET_' in laststr:
            syst = laststr.partition('MET')[-1].replace('.root','')
        elif '_Recoil_' in laststr:
            syst = laststr.partition('Recoil')[-1].replace('.root', '')
        syst = syst.replace('year', options.era_year)
    if ('MET' in infile.split('/')[-1] and 'SR' not in infile.split('/')[-1]): continue# or ('Recoil' not in infile): continue
    # print ('running code for ',infile)
    reg = reg.replace('ZmumuCR', 'ZMUMU').replace('ZeeCR', 'ZEE').replace('WmunuCR', 'WMU').replace(
        'WenuCR', 'WE').replace('TopmunuCR', 'TOPMU').replace('TopenuCR', 'TOPE').replace('2j', '1b').replace('3j', '2b')

    for hist in SRCRhistos:
        temp = setHistBin(fin.Get(hist),hist)
        hist = hist.replace('DIBOSON', 'diboson').replace('ZJets', 'zjets').replace('GJets', 'gjets').replace('QCD', 'qcd').replace('STop', 'singlet').replace('Top', 'tt').replace('WJets', 'wjets').replace('DYJets', 'dyjets').replace('STop', 'singlet').replace('SMH','smh')
        newName   = era_name+reg+'_'+str(hist)+syst
        if not syst=='' and hist=='data_obs':continue
        if temp.Integral() == 0.0:
            HISTNAME=newName
            temp = TH1F(newName, newName, temp.GetXaxis().GetNbins(),250,1000)
            # temp = TH1F(newName, newName, temp.GetXaxis().GetNbins(),array('d', bins))
            # print ('=================',hist)
            # print ('=================',temp.GetXaxis().GetNbins())
            for bin in range(1,temp.GetXaxis().GetNbins()+1):
                temp.SetBinContent(bin,0.00001)
                if temp.GetBinError(bin)<0:
                    temp.SetBinError(bin, 0.0001)
        for bin in range(1,temp.GetXaxis().GetNbins()+1):
            if temp.GetBinContent(bin)==0:
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
                myHist_up = setHistStyle(temp_up, newName_up)
                myHist_down = setHistStyle(temp_down, newName_down)
                myHist_up.Write()
                myHist_down.Write()
            for bin in range(1,temp.GetXaxis().GetNbins()+1):
                temp_allbinUp.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                temp_allbinDown.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
            # print(newName)
            myHist = setHistStyle(temp, newName)
            myHist_allbinUp = setHistStyle(temp_allbinUp, newName_allbinUp)
            myHist_allbinDown = setHistStyle(temp_allbinDown, newName_allbinDown)
            #f.cd()
            myHist.Write()
            myHist_allbinUp.Write()
            myHist_allbinDown.Write()
for cat in ['1b','2b']:
    for infile in SignalFiles:
        # print ('infile',infile)
        if '2HDMa' in infile: whichSig = 1
        elif 'DMSimp': whichSig = 0
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
            CS = xsec_dict.hdma_xsList_0[sampStr]
        else:
            if whichSig == 1:
                sampStr = 'ma_'+ma+'_mA_'+mA
                CS = xsec_dict.hdma_xsList_150[sampStr]
            elif whichSig == 0:
                sampStr = 'mphi_'+ma+'_mchi_'+mA
                CS = xsec_dict.dmsimp_xsList_150[sampStr]

        for syst in ['MET','CMSyear_eff_b','CMSyear_fake_b','EWK','CMSyear_Top','CMSyear_trig_met','CMSyear_trig_ele', 'CMSyear_EleID', 'CMSyear_EleRECO', 'CMSyear_MuID','CMSyear_MuISO', 'CMSyear_MuTRK','CMSyear_PU','En','CMSyear_mu_scale','CMSyear_pdf','CMSyear_prefire','JECAbsolute','JECAbsolute_year','JECBBEC1','JECBBEC1_year','JECEC2','JECEC2_year','JECFlavorQCD','JECHF','JECHF_year','JECRelativeBal','JECRelativeSample_year'] :
            if syst=='MET':
                temp = setHistBin(fin.Get('h_reg_SR_'+cat+'_MET'), 'h_reg_SR_'+cat+'_MET')
                if  temp.Integral() == 0.0:
                    for bin in range(1,temp.GetXaxis().GetNbins()+1):
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                for bin in range(1,temp.GetXaxis().GetNbins()+1):
                    if temp.GetBinContent(bin)==0:
                        temp.SetBinContent(bin,0.00001)
                    if temp.GetBinError(bin)<0:
                        temp.SetBinError(bin,0.0)
                h_total = fin.Get('h_total_mcweight')
                totalEvents = h_total.Integral()
                temp.Scale((luminosity*CS)/(totalEvents))
                if whichSig==1:
                    samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7'
                elif whichSig == 0:
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
                elif whichSig == 0:
                    samp_allbinUp = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_allbinUp'
                    samp_allbinDown = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_allbinDown'
                for bin in range(1,temp_up.GetXaxis().GetNbins()+1):
                    temp_allbinUp.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                    temp_allbinDown.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
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
                    elif whichSig == 0:
                        samp_up = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_eff_bin'+str(bin)+'Up'
                        samp_down = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_eff_bin'+str(bin)+'Down'
                    temp_up.SetBinContent(bin, temp.GetBinContent(bin)+temp.GetBinError(bin))
                    temp_down.SetBinContent(bin, temp.GetBinContent(bin)-temp.GetBinError(bin))
                    for bin in range(1,temp_up.GetXaxis().GetNbins()+1):
                        if temp_up.GetBinContent(bin) == 0:
                            temp_up.SetBinContent(bin, 0.00001)
                        if temp_down.GetBinContent(bin) == 0:
                            temp_down.SetBinContent(bin, 0.00001)
                    myHist_up = setHistStyle(temp_up, samp_up)
                    myHist_down = setHistStyle(temp_down, samp_down)
                    myHist_up.Write()
                    myHist_down.Write()
            else:
                for ud in ['Up','Down']:
                    temp = setHistBin(fin.Get('h_reg_SR_'+cat+'_MET_'+syst+ud), 'h_reg_SR_'+cat+'_MET_'+syst+ud)
                    if  temp.Integral() == 0.0:
                        for bin in range(1,temp.GetXaxis().GetNbins()+1):
                            temp.SetBinContent(bin,0.00001)
                            if temp.GetBinError(bin)<0:
                                temp.SetBinError(bin,0.0)
                    for bin in range(1,temp.GetXaxis().GetNbins()+1):
                        if temp.GetBinContent(bin)==0:
                            temp.SetBinContent(bin,0.00001)
                        if temp.GetBinError(bin)<0:
                            temp.SetBinError(bin,0.0)
                    h_total = fin.Get('h_total_mcweight')
                    totalEvents = h_total.Integral()
                    temp.Scale((luminosity*CS)/(totalEvents))
                    if whichSig == 1:
                        samp = era_name+cat+'_SR_2HDMa_Ma'+ma+'_MChi1_MA'+mA+'_tb35_st_0p7_'+syst+ud
                    elif whichSig == 0:
                        samp = era_name+cat+'_SR_DMSimp_MPhi'+ma+'_MChi1_'+syst+ud
                    samp = samp.replace('year', options.era_year)
                    myHist = setHistStyle(temp, samp)
                    f.cd()
                    myHist.Write()
print('*************DONE*************')
print("Saved histograms in DataCardRootFiles/AllMETHistos_"+plot_tag+".root file")
print('******************************')
f.Close()
