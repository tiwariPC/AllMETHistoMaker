# In this at the end of filevector I am putting the dirname
# so loop over n-1 files and n will give the name of the output dir.

# In legend also the n element will give the name for the ratio plot y axis label.
#edited by Monika Mittal
#Script for ratio plot
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

parser.add_option("-y", "--year", type="string", dest="year", help="year of histogram")
parser.add_option("-t", "--tag", type="string", dest="plot_tag", help="version of histogram")
(options, args) = parser.parse_args()

if options.plot_tag == None:
    print('Please provide histogram directory name')
    sys.exit()
else:
    plot_tag = options.plot_tag

colors=[1,2,4,5,8,9,11,41,46,30,12,28,20,32]
markerStyleUp=[20,21,22,23,29,33,34,47,43,39,41,45,20,21,22,23,29,33,34,47,43,39,41,45]
markerStyleDown=[24,25,26,32,30,27,28,46,42,37,40,44,24,25,26,32,30,27,28,46,42,37,40,44]
linestyle=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


def DrawOverlap(fileVec, histVec, titleVec,legendtext,pngname,logstatus=[0,0],xRange=[-99999,99999,1]):

    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gStyle.SetTitleOffset(1.1,"Y")
    #gStyle.SetTitleOffset(1.9,"X");
    gStyle.SetLineWidth(3)
    gStyle.SetFrameLineWidth(3)
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.02, "y")


    i=0

    histList_=[]
    histList=[]
    histList1=[]
    maximum=[]
    minimum=[]

    ## Legend
    leg = TLegend(0.4, 0.70, 0.89, 0.89)#,NULL,"brNDC");
    leg.SetBorderSize(0)
    leg.SetNColumns(2)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(62)
    leg.SetTextSize(0.035)

    c = TCanvas("c1", "c1",0,0,650,600)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.20)
    c.SetRightMargin(0.05)
    c.SetLogy(logstatus[1])
    c.SetLogx(logstatus[0])
    print ("you have provided "+str(len(fileVec))+" files and "+str(len(histVec))+" histograms to make a overlapping plot" )
    print ("opening rootfiles")
    c.cd()

    ii=0
    inputfile={}
    print (str(fileVec[(len(fileVec)-1)]))

    for ifile_ in range(len(fileVec)):
        print ("opening file  "+fileVec[ifile_])
        inputfile[ifile_] = TFile( fileVec[ifile_] )
        print ("fetching histograms")
        for ihisto_ in range(len(histVec)):
            print ("printing histo "+str(histVec[ihisto_]))
            histo = inputfile[ifile_].Get(histVec[ihisto_])
            #status_ = type(histo) is TGraphAsymmErrors
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

    print ('histList',[hist.GetName() for hist in histList])
    print (maximum, "  ", max(maximum))
    print (minimum, "  ", min(minimum))
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
            histList[ih].SetMaximum(maxi*3) #1.4 for log
            histList[ih].SetMinimum(mini*3) #1.4 for log
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
            leg.AddEntry(histList[ih],legendtext[ih],"PL")
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
            leg.AddEntry(histList[ih],legendtext[ih],"P")
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

        i=i+1
    pt = TPaveText(0.01,0.92,0.95,0.96,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.046)
    pt.AddText(0.18,0.35,"#bf{CMS} #it{Internal}")
    if options.year == '2016':
        pt.AddText(0.7, 0.35, "35.90fb^{-1}(13 TeV)")
    elif options.year == '2017':
        pt.AddText(0.7, 0.35, "41.50fb^{-1}(13 TeV)")
    elif options.year == '2018':
        pt.AddText(0.7, 0.35, "59.64fb^{-1}(13 TeV)")
    pt.Draw()

    leg.Draw()
    outputdirname = 'TFUncPlots_Overlay/'+plot_tag+'/'
    if not os.path.exists(outputdirname):
        os.makedirs(outputdirname)
    histname=outputdirname+pngname
    c.SaveAs(histname+'.png')
    c.SaveAs(histname+'.pdf')

print ("calling the plotter")

files = ['bin/TF_'+plot_tag+'.root']

#postfix= ['CMS2017_trig_ele', 'CMS2017_EleID', 'CMS2017_EleRECO','CMS2017_trig_met', 'CMS2017_MuID', 'CMS2017_MuISO', 'CMS2017_MuTRK']
postfix=['CMS'+options.year+'_trig_ele', 'CMS'+options.year+'_EleID', 'CMS'+options.year+'_EleRECO','CMS'+options.year+'_trig_met', 'CMS'+options.year+'_MuID', 'CMS'+options.year+'_MuISO','CMS'+options.year+'_eff_b']
legend_dict={'CMS'+options.year+'_trig_ele':'Ele Trig', 'CMS'+options.year+'_EleID':'Ele ID', 'CMS'+options.year+'_EleRECO':'Ele RECO','CMS'+options.year+'_trig_met':'MET Trig', 'CMS'+options.year+'_MuID':'Mu ID', 'CMS'+options.year+'_MuISO':'Mu ISO', 'CMS'+options.year+'_MuTRK':'Mu TRK','CMS'+options.year+'_eff_b':'b-tag'}
ytitle='relative unc'

cats   = ['1b','2b']

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
        hists = []
        legend = []
        for pf in postfix:
            uphist = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg+"_"+pf+"Up"
            downhist = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg+"_"+pf+"Down"
            if ("ZEE" in uphist or "WE" in uphist or "TOPE" in uphist) and ("Mu" in uphist or 'trig_met' in uphist):continue
            if ("ZMUMU" in uphist or "WMU" in uphist or "TOPMU" in uphist) and ("Ele" in uphist or 'trig_ele' in uphist):continue
            uphist_dict.update({pf:uphist})
            downhist_dict.update({pf:downhist})
            hists.append(uphist_dict[pf])
            hists.append(downhist_dict[pf])
            legend.append(legend_dict[pf]+" Up")
            legend.append(legend_dict[pf]+" Down")
        print ("hists",hists)
        pngname = "Unc_tf_"+cat+"_"+sr_bkg+"_to_"+cat+"_"+cr_bkg
        if '1b' in cat:
            DrawOverlap(files,hists,axistitle,legend,pngname,[0,0],[250,1000])
        elif '2b' in cat:
            DrawOverlap(files,hists,axistitle,legend,pngname,[0,0],[0,1])

