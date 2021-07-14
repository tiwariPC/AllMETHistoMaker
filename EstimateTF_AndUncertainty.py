import os
import sys
import optparse
import ROOT
from copy import copy

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

parser.add_option("-f", "--file", type="string", dest="rootFile", help="AllMETHistMaker File")
parser.add_option("-y", "--year", type="string", dest="year", help="year of histogram")
parser.add_option("-s", "--save", action="store_true", dest="savetoAllMET")
parser.add_option("-t", "--tag", type="string", dest="plot_tag", help="version of histogram")
(options, args) = parser.parse_args()

if options.rootFile == None:
    print('Please provide Allmethisto file')
    sys.exit()
else:
    inputAllMETHISTO = options.rootFile

if options.savetoAllMET == None:
    savetoAllMET = False
else:
    savetoAllMET = options.savetoAllMET

if options.plot_tag == None:
    print('Please provide histogram directory name')
    sys.exit()
else:
    plot_tag = options.plot_tag

fout = ROOT.TFile("bin/TF_"+plot_tag+".root", "RECREATE")
if savetoAllMET:
    fin = ROOT.TFile(inputAllMETHISTO, "UPDATE")
else:
    fin = ROOT.TFile(inputAllMETHISTO, "r")

## macro is setup for the inverted transfer factors.

def GetTF(sr_bkg, cr_bkg, postfix=""):
    print ("histogram used for TF are:", sr_bkg+postfix, cr_bkg+postfix)
    if postfix=="Prefire" or postfix=="JEC" or postfix=="allbin":h_sr_bkg = fin.Get(sr_bkg+postfix)
    else:h_sr_bkg = fin.Get(sr_bkg)
    h_cr_bkg = fin.Get(cr_bkg+postfix)
    tf_sr_cr = h_sr_bkg.Clone()
    tf_sr_cr.Divide(h_cr_bkg)
    print ([tf_sr_cr.GetBinContent(i) for i in range(1,tf_sr_cr.GetNbinsX()+1)])
    histname = ("tf_"+sr_bkg+"_to_"+cr_bkg+postfix).replace("bbDM2017_","").replace("bbDM2016_","").replace("bbDM2018_","")
    tf_sr_cr.SetName(histname)
    tf_sr_cr.SetTitle(histname)
    return tf_sr_cr

def GetFracUncertainty(tfs):
    tf= tfs[0].Clone()
    tf_up = tfs[1].Clone()
    tf_down = tfs[2].Clone()
    unc_up = tfs[1].Clone()    ## up - central
    unc_up.Add(tf,-1)
    unc_up.Divide(tf)
    name_up = "Unc_"+tf_up.GetName()
    unc_up.SetName(name_up)
    unc_down = tfs[2].Clone()  ## central - down
    unc_down.Add(tf,-1)
    unc_down.Divide(tf)
    name_down = "Unc_"+tf_down.GetName()
    unc_down.SetName(name_down)
    return [unc_up,unc_down]


''' mode can be all, up, down, central
syst: name of the systematics as in the AllMETHisto.root
sr_bkg: bkg histo in SR
cr_bkg: bkg histo in CR
'''
def GetAllTF(sr_bkg, cr_bkg,  syst="Prefire", mode="all",):
    postfix=[]
    if mode=="all": postfix = ["Up","Down"]
    if mode=="up": postfix = ["Up"]
    if mode=="down": postfix = ["Down"]
    postfix= ["_"+syst+i for i in postfix]
    central_ = GetTF(sr_bkg,cr_bkg)
    up_      = GetTF(sr_bkg,cr_bkg,postfix[0])
    down_    = GetTF(sr_bkg,cr_bkg,postfix[1])
    return ([central_,up_,down_] + GetFracUncertainty([central_,up_,down_]) )

def GetStatsUncTF(sr_bkg, cr_bkg, nbin=4):
    print ("reading histo: ",sr_bkg+"_binUp", cr_bkg+"_bin1Up")
    sr_bin1up = fin.Get(sr_bkg+"_bin1Up")
    cr_bin1up = fin.Get(cr_bkg+"_bin1Up")
    tf_sr_cr_bin1up  = sr_bin1up.Clone()
    tf_sr_cr_bin1up.Divide(cr_bin1up)
    sr_bin1down = fin.Get(sr_bkg+"_bin1Down")
    cr_bin1down = fin.Get(cr_bkg+"_bin1Down")
    tf_sr_cr_bin1down  = sr_bin1down.Clone()
    tf_sr_cr_bin1down.Divide(cr_bin1down)
    print ([tf_sr_cr_bin1up.GetBinContent(i) for i in range(1,tf_sr_cr_bin1up.GetNbinsX()+1)])
    return [tf_sr_cr_bin1up, tf_sr_cr_bin1down]


systematic_source = ['allbin','CMS'+options.year+'_eff_b','CMS'+options.year+'_fake_b','EWK','CMS'+options.year+'_Top','CMS'+options.year+'_trig_met','CMS'+options.year+'_trig_ele', 'CMS'+options.year+'_EleID', 'CMS'+options.year+'_EleRECO', 'CMS'+options.year+'_MuID','CMS'+options.year+'_MuISO', 'CMS'+options.year+'_MuTRK','CMS'+options.year+'_PU','En','CMS'+options.year+'_mu_scale','CMS'+options.year+'_pdf','CMS'+options.year+'_prefire','JECAbsolute','JECAbsolute_'+options.year,'JECBBEC1','JECBBEC1_'+options.year,'JECEC2','JECEC2_'+options.year,'JECFlavorQCD','JECHF','JECHF_'+options.year,'JECRelativeBal','JECRelativeSample_'+options.year]
analysis='bbDM'+options.year
alltfhists=[]
for icat in ["1b", "2b"]:
    for isyst in systematic_source:
        gen_ = any([i for i in ['allbin', 'JECRelativeSample_'+options.year, 'JECFlavorQCD', 'En', 'CMS'+options.year+'_mu_scale', 'CMS'+options.year+'_pdf', 'JECAbsolute', 'JECRelativeBal', 'JECHF_'+options.year, 'CMS'+options.year+'_eff_b', 'CMS'+options.year+'_fake_b', 'JECEC2_'+options.year, 'JECHF', 'JECBBEC1_'+options.year, 'JECAbsolute_'+options.year, 'EWK', 'JECEC2', 'CMS'+options.year+'_prefire', 'JECBBEC1', 'CMS'+options.year+'_PU'] if isyst==i])
        for_ele = any([i for i in ['CMS'+options.year+'_trig_ele', 'CMS'+options.year+'_EleID', 'CMS'+options.year+'_EleRECO'] if isyst==i])
        for_mu = any([i for i in ['CMS'+options.year+'_trig_met', 'CMS'+options.year+'_MuID', 'CMS'+options.year+'_MuISO', 'CMS'+options.year+'_MuTRK'] if isyst==i])
        if for_mu or gen_:
            if icat=='1b':
                tf_wmunu_wjets = GetAllTF(analysis+"_"+icat+"_SR_wjets",  analysis+"_"+icat+"_WMU_wjets", isyst);      alltfhists.append(tf_wmunu_wjets)
            if icat=='2b':
                tf_topmu_top   = GetAllTF(analysis+"_"+icat+"_SR_tt"   ,  analysis+"_"+icat+"_TOPMU_tt" , isyst);      alltfhists.append(tf_topmu_top)
            tf_zmumu_zj    = GetAllTF(analysis+"_"+icat+"_SR_zjets"   ,  analysis+"_"+icat+"_ZMUMU_dyjets" , isyst);      alltfhists.append(tf_zmumu_zj)
        if for_ele or gen_:
            if icat=='1b':
                tf_wenu_wjets  = GetAllTF(analysis+"_"+icat+"_SR_wjets",  analysis+"_"+icat+"_WE_wjets" , isyst);      alltfhists.append(tf_wenu_wjets)
            if icat=='2b':
                tf_topen_top   = GetAllTF(analysis+"_"+icat+"_SR_tt"   ,  analysis+"_"+icat+"_TOPE_tt"  , isyst);      alltfhists.append(tf_topen_top)
            tf_zee_zj      = GetAllTF(analysis+"_"+icat+"_SR_zjets"   ,  analysis+"_"+icat+"_ZEE_dyjets"  , isyst);      alltfhists.append(tf_zee_zj)

fout.cd()
for isyst in alltfhists:
    for ihist in isyst:
        ihist.Write()
print("Histograms are added to bin/TF_"+plot_tag+".root")

## close the file outside of loop
fout.Close()
if savetoAllMET:
    fin.cd()
    ROOT.gDirectory.mkdir("1b")
    fin.cd("1b")
    ROOT.gDirectory.mkdir("ZMUMU")
    ROOT.gDirectory.mkdir("ZEE")
    ROOT.gDirectory.mkdir("WMU")
    ROOT.gDirectory.mkdir("WE")

    fin.cd()
    ROOT.gDirectory.mkdir("2b")
    fin.cd("2b")
    ROOT.gDirectory.mkdir("ZMUMU")
    ROOT.gDirectory.mkdir("ZEE")
    ROOT.gDirectory.mkdir("TOPMU")
    ROOT.gDirectory.mkdir("TOPE")
    fin.cd()

    for isyst in alltfhists:
        up_list = {}
        down_list = {}
        for ihist in isyst:
            if 'Unc_' in ihist.GetName():
                if 'Up' in ihist.GetName():
                    up_list.update({'_'.join(ihist.GetName().split('_')[9:]).replace('Up',''):ihist})
                if 'Down' in ihist.GetName():
                    down_list.update({'_'.join(ihist.GetName().split('_')[9:]).replace('Down',''):ihist})

        fin.cd(up_list[list(up_list.keys())[0]].GetName().split('_')[2]+'/'+up_list[list(up_list.keys())[0]].GetName().split('_')[7])

        for key in up_list:
            h_hist = up_list[key].Clone(key)
            h_hist.SetName(key)
            h_hist.SetTitle(key)
            for i in range(1,h_hist.GetNbinsX()+1):
                max_unc = max(abs(up_list[key].GetBinContent(i)),abs(down_list[key].GetBinContent(i)))
                h_hist.SetBinContent(i, max_unc)
            h_hist.Write()
fin.Close()


