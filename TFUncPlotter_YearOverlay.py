import sys
import os
import ROOT
import optparse
ROOT.gROOT.SetBatch(True)
from ROOT import TFile, TH1F, TCanvas, TGraphAsymmErrors
from ROOT import TH1D, TH1, TH1I
from ROOT import gStyle
from ROOT import TLegend
from ROOT import TPaveText

usage = "usage: python TFUncPlotter_overlay.py -y 2016 -t v16_12-00-03_1bMET_2bCTS"
parser = optparse.OptionParser(usage)

parser.add_option("--t16", "--tag16", type="string", dest="plot_tag16", help="version of histogram")
parser.add_option("--t17", "--tag17", type="string", dest="plot_tag17", help="version of histogram")
parser.add_option("--t18", "--tag18", type="string", dest="plot_tag18", help="version of histogram")
(options, args) = parser.parse_args()

if options.plot_tag16 == None:
  print('Please provide histogram directory name')
  sys.exit()
else:
  plot_tag16 = options.plot_tag16

if options.plot_tag17 == None:
  print('Please provide histogram directory name')
  sys.exit()
else:
  plot_tag17 = options.plot_tag17

if options.plot_tag18 == None:
  print('Please provide histogram directory name')
  sys.exit()
else:
  plot_tag18 = options.plot_tag18


colors=[1,2,4,5,8,9,11,41,46,30,12,28,20,32]
markerStyleUp=[20,21,22,23,29,33,34,47,43,39,41,45,20,21,22,23,29,33,34,47,43,39,41,45]
markerStyleDown=[24,25,26,32,30,27,28,46,42,37,40,44,24,25,26,32,30,27,28,46,42,37,40,44]
linestyle=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


def DrawOverlap(fileVec, histVec, titleVec, legendtext, pngname, logstatus=[0, 0], xRange=[-99999, 99999, 1]):

    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gStyle.SetTitleOffset(1.1,"Y")
    #gStyle.SetTitleOffset(1.9,"X");
    gStyle.SetLineWidth(3)
    gStyle.SetFrameLineWidth(3)
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.02, "y")
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")


    i=0

    histList=[]
    histList1=[]
    legList = []
    maximum=[]
    minimum=[]

    ## Legend
    leg = TLegend(0.25, 0.70, 0.89, 0.89)#,NULL,"brNDC");
    leg.SetBorderSize(0)
    leg.SetNColumns(2)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(62)
    leg.SetTextSize(0.025)

    c = TCanvas("c1", "c1",0,0,650,600)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.20)
    c.SetRightMargin(0.05)
    c.SetLogy(logstatus[1])
    c.SetLogx(logstatus[0])
    # print ("you have provided "+str(len(fileVec))+" files and "+str(len(histVec))+" histograms to make a overlapping plot" )
    # print ("opening rootfiles")
    c.cd()

    ii=0
    inputfile={}

    for ifile_ in fileVec:
      # print ("opening file  "+fileVec[ifile_])
      inputfile[ifile_] = TFile( fileVec[ifile_] )
      # print ("fetching histograms")
      for ihisto_ in range(len(histVec[ifile_])):
        # print("printing histo "+str(histVec[ifile_][ihisto_]))
        histo = inputfile[ifile_].Get(histVec[ifile_][ihisto_])
        #status_ = type(histo) is TGraphAsymmErrors
        max_bin = max([abs(histo.GetBinContent(i)) for i in range(1, 5)])
        if '2018' in ifile_ and 'prefire' in histo.GetName(): continue
        # if max_bin > 0.005 and 'JEC' in histo.GetName() and 'Up' in histo.GetName():
        #     print(histo.GetName())
        legList.append(legendtext[ifile_][ihisto_])
        histList.append(histo)
        # for ratio plot as they should nt be normalize
        histList1.append(histo)
        #print histList[ii].Integral()
        #histList[ii].Rebin(xRange[2])
        #histList[ii].Scale(1.0/histList[ii].Integral())
        maximum.append(histList[ii].GetMaximum())
        minimum.append(histList[ii].GetMinimum())
        maximum.sort()
        ii=ii+1
    leg.Draw()
    # print ('histList',[hist.GetName() for hist in histList])
    # print (maximum, "  ", max(maximum))
    # print (minimum, "  ", min(minimum))
    mcol_up = 0
    mcol_down = 0
    for ih in range(len(histList)):
        tt = type(histList[ih])
        if logstatus[1] == 1 :
            histList[ih].SetMaximum(1.5) #1.4 for log
            histList[ih].SetMinimum(0.1) #1.4 for log
        if logstatus[1] == 0 :
            maxi=max(maximum)
            mini=min(minimum)
            if maxi==0.0:maxi=0.001
            if mini==0.0:mini=-0.001
            histList[ih].SetMaximum(maxi*6) #1.4 for log
            histList[ih].SetMinimum(mini*4) #1.4 for log
#        print "graph_status =" ,(tt is TGraphAsymmErrors)
#        print "hist status =", (tt is TH1D) or (tt is TH1F)
        if ih == 0 :
            if tt is TGraphAsymmErrors :
                histList[ih].Draw("APL")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("P hist")
        if ih > 0 :
            #histList[ih].SetLineWidth(2)
            if tt is TGraphAsymmErrors :
                histList[ih].Draw("PL same")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("P hist same")

        if tt is TGraphAsymmErrors :
            histList[ih].SetMaximum(100)
            # histList[ih].SetMarkerColor(colors[ih])
            if 'Up' in str(histList[ih].GetName()):
                histList[ih].SetMarkerColor(2)
                histList[ih].SetMarkerStyle(markerStyleUp[mcol_up])
                mcol_up+=1
            elif 'Down' in str(histList[ih].GetName()):
                histList[ih].SetMarkerColor(4)
                histList[ih].SetMarkerStyle(markerStyleDown[mcol_down])
                mcol_down+=1
            histList[ih].SetLineColor(colors[ih])
            histList[ih].SetMarkerSize(2)
            histList[ih].SetLineWidth(2)
            leg.AddEntry(histList[ih], legList[ih], "PL")
        if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
            histList[ih].SetLineStyle(linestyle[ih])
            histList[ih].SetLineColor(colors[ih])
            # histList[ih].SetMarkerColor(colors[ih])
            if 'Up' in str(histList[ih].GetName()):
                histList[ih].SetMarkerColor(2)
                histList[ih].SetMarkerStyle(markerStyleUp[mcol_up])
                mcol_up+=1
            elif 'Down' in str(histList[ih].GetName()):
                histList[ih].SetMarkerColor(4)
                histList[ih].SetMarkerStyle(markerStyleDown[mcol_down])
                mcol_down+=1
            histList[ih].SetMarkerSize(2)
            histList[ih].SetLineWidth(3)
            leg.AddEntry(histList[ih],legList[ih],"P")
        histList[ih].GetYaxis().SetTitle(titleVec[1])
        histList[ih].GetYaxis().SetTitleSize(0.062)
        histList[ih].GetYaxis().SetTitleOffset(1.6)
        histList[ih].GetYaxis().CenterTitle(True)
        # histList[ih].GetYaxis().SetMaxDigits(2)
        histList[ih].GetYaxis().SetTitleFont(42)
        histList[ih].GetYaxis().SetLabelFont(42)
        histList[ih].GetYaxis().SetLabelSize(.052)
        histList[ih].GetXaxis().SetRangeUser(xRange[0],xRange[1])

        histList[ih].GetXaxis().SetTitle(titleVec[0])
        histList[ih].GetXaxis().SetLabelSize(0.052)
        histList[ih].GetXaxis().SetTitleSize(0.052)
        #histList[ih].GetXaxis().SetTitleOffset(1.14)
        histList[ih].GetXaxis().SetTitleFont(42)

        histList[ih].GetXaxis().SetLabelFont(42)
        histList[ih].GetYaxis().SetLabelFont(42)
        histList[ih].GetXaxis().SetNdivisions(507)
        #histList[ih].GetXaxis().SetMoreLogLabels();
        #histList[ih].GetXaxis().SetNoExponent();
        #histList[ih].GetTGaxis().SetMaxDigits(3);
        max_bin = max([abs(histList[ih].GetBinContent(i)) for i in range(1, 5)])
        if max_bin > 0.005 and 'JEC' in histList[ih].GetName() :
            print(histList[ih].GetName())

        i=i+1
    pt = TPaveText(0.01,0.92,0.95,0.96,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.046)
    pt.AddText(0.18,0.35,"#bf{CMS} #it{Internal}")
    pt.AddText(0.77, 0.35, "(13 TeV)")
    pt.Draw()
    c.Update()
    leg.Draw()
    outputdirname = 'TFUncPlots_YearOverlay/'+plot_tag16+'_'+plot_tag17+'_'+plot_tag18+'/'
    if not os.path.exists(outputdirname):
        os.makedirs(outputdirname)
    histname=outputdirname+pngname
    c.SaveAs(histname+'.png')
    c.SaveAs(histname+'.pdf')
    c.Close()


# print ("calling the plotter")
# postfix = ['CMSYEAR_eff_b',]#'CMSYEAR_trig_ele',]# 'CMSYEAR_EleID']
# postfix=['CMSYEAR_trig_ele', 'CMSYEAR_EleID', 'CMSYEAR_EleRECO','CMSYEAR_trig_met', 'CMSYEAR_MuID', 'CMSYEAR_MuISO','CMSYEAR_eff_b','CMSYEAR_prefire', 'JECAbsolute', 'JECAbsolute_YEAR', 'JECBBEC1', 'JECBBEC1_YEAR', 'JECEC2', 'JECEC2_YEAR','JECFlavorQCD', 'JECHF' , 'JECHF_YEAR', 'JECRelativeBal', 'JECRelativeSample_YEAR']

# postfix = {'CMSYEAR_eff_b': 'CMSYEAR_eff_b'}

postfix={'CMSYEAR_trig_ele':'CMSYEAR_trig_ele', 'CMSYEAR_EleID':'CMSYEAR_EleID', 'CMSYEAR_EleRECO':'CMSYEAR_EleRECO','CMSYEAR_trig_met':'CMSYEAR_trig_met', 'CMSYEAR_MuID':'CMSYEAR_MuID', 'CMSYEAR_MuISO':'CMSYEAR_MuISO','CMSYEAR_eff_b':'CMSYEAR_eff_b','CMSYEAR_prefire':'CMSYEAR_prefire', 'JECAbsolute':'JECAbsolute', 'JECAbsolute_YEAR':'JECAbsolute_YEAR', 'JECBBEC1':'JECBBEC1', 'JECBBEC1_YEAR':'JECBBEC1_YEAR', 'JECEC2':'JECEC2', 'JECEC2_YEAR':'JECEC2_YEAR' , 'JECFlavorQCD':'JECFlavorQCD', 'JECHF':'JECHF' , 'JECHF_YEAR':'JECHF_YEAR', 'JECRelativeBal':'JECRelativeBal', 'JECRelativeSample_YEAR':'JECRelativeSample_YEAR','CMSYEAR_mu_scale':'CMSYEAR_mu_scale', 'CMSYEAR_pdf':'CMSYEAR_pdf'}

legend_dict = {'CMSYEAR_trig_ele': 'Ele Trig YEAR', 'CMSYEAR_EleID': 'Ele ID YEAR', 'CMSYEAR_EleRECO': 'Ele RECO YEAR', 'CMSYEAR_trig_met': 'MET Trig YEAR', 'CMSYEAR_MuID': 'Mu ID YEAR', 'CMSYEAR_MuISO': 'Mu ISO YEAR', 'CMSYEAR_eff_b': 'b-tag YEAR', 'CMSYEAR_prefire': 'prefire YEAR', 'JECAbsolute': 'JECAbsolute', 'JECAbsolute_YEAR': 'JECAbsolute_YEAR', 'JECBBEC1': 'JECBBEC1', 'JECBBEC1_YEAR': 'JECBBEC1_YEAR', 'JECEC2': 'JECEC2', 'JECEC2_YEAR': 'JECEC2_YEAR', 'JECFlavorQCD': 'JECFlavorQCD', 'JECHF': 'JECHF', 'JECHF_YEAR': 'JECHF_YEAR', 'JECRelativeBal': 'JECRelativeBal', 'JECRelativeSample_YEAR': 'JECRelativeSample_YEAR','CMSYEAR_mu_scale':'mu_scale YEAR', 'CMSYEAR_pdf':'pdf YEAR'}

ytitle = 'relative unc'
cats = ['1b', '2b']
files = {'2016':'bin/TF_'+plot_tag16+'.root','2017':'bin/TF_'+plot_tag17+'.root','2018':'bin/TF_'+plot_tag18+'.root'}
hists = {}
for cat in cats:
  if '1b' in cat:
      SR_BKG = ['SR_zjets', 'SR_zjets', 'SR_wjets', 'SR_wjets']
      CR_BKG = ['ZEE_dyjets', 'ZMUMU_dyjets', 'WE_wjets', 'WMU_wjets']
      xtitle = 'Recoil [GeV]'
  elif '2b' in cat:
      SR_BKG = ['SR_zjets', 'SR_zjets', 'SR_tt', 'SR_tt']
      CR_BKG = ['ZEE_dyjets', 'ZMUMU_dyjets', 'TOPE_tt', 'TOPMU_tt']
      xtitle = 'cos(#theta)*'
  axistitle = [xtitle, ytitle]
  for sr_bkg, cr_bkg in zip(SR_BKG,CR_BKG):
    uphist_dict = {}
    downhist_dict = {}
    hists = {}
    legend = {}
    for pf in postfix:
      for year in ['2016','2017','2018']:
        postfix[pf] = postfix[pf].replace('YEAR', year)
        uphist = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg+"_"+postfix[pf]+"Up"
        downhist = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg+"_"+postfix[pf]+"Down"
        # print(uphist, downhist)
        # if ("ZEE" in uphist or "WE" in uphist or "TOPE" in uphist) and ("Mu" in uphist): continue
        # if ("ZMUMU" in uphist or "WMU" in uphist or "TOPMU" in uphist) and ("Ele" in uphist or 'trig_ele' in uphist or 'trig_met' in uphist ): continue
        # if ("WMU" in uphist or "TOPMU" in uphist or "WE" in uphist or "TOPE" in uphist) and ('eff_b' in uphist): continue
        # print(uphist, downhist)
        hists.update({year: [uphist, downhist]})
        postfix[pf] = postfix[pf].replace(year, 'YEAR')
        if ('JEC' in postfix[pf]) and ('YEAR' not in postfix[pf]):
          legend.update({year:[legend_dict[pf]+'('+year+')'+" Up", legend_dict[pf]+'('+year+')'+" Down"]})
        else:
          legend.update({year:[legend_dict[pf].replace('YEAR',year)+" Up", legend_dict[pf].replace('YEAR',year)+" Down"]})

      if ("ZEE" in hists['2016'][0] or "WE" in hists['2016'][0] or "TOPE" in hists['2016'][0]) and ("Mu" in hists['2016'][0]): continue
      # if ("ZMUMU" in hists['2016'][0] or "WMU" in hists['2016'][0] or "TOPMU" in hists['2016'][0]) and ("Ele" in hists['2016'][0] or 'trig_ele' in hists['2016'][0] or 'trig_met' in hists['2016'][0]): continue
      if ("ZMUMU" in hists['2016'][0] or "WMU" in hists['2016'][0] or "TOPMU" in hists['2016'][0]) and ("Ele" in hists['2016'][0] or 'trig_ele' in hists['2016'][0]) : continue
      # if ("WMU" in hists['2016'][0] or "TOPMU" in hists['2016'][0] or "WE" in hists['2016'][0] or "TOPE" in hists['2016'][0]) and ('eff_b' in hists['2016'][0]): continue

      # print(hists)
      pngname = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg+"_"+postfix[pf]
      if bool(hists):
        # print(files, hists)
        if '1b' in cat:
          DrawOverlap(files,hists,axistitle,legend,pngname,[0,0],[250,1000])
        elif '2b' in cat:
          DrawOverlap(files,hists,axistitle,legend,pngname,[0,0],[0,1])
