import ROOT
import os, math
import sys
import numpy as np
from glob import glob
from root_pandas import read_root
import array

path = sys.argv[1]
files = glob(path+'/QCD*.root')
file_out = ROOT.TFile('out_QCD_bENriched.root', 'RECREATE')
# file_out.cd()
histo_list = []
for file_in in files:
  binx_ = np.linspace(0.0, 6.0, num = 121)
  biny_ = [0.0 , 0.25, 0.50 , 0.75, 1.0]
  qcdDphi = ROOT.TH2F(file_in.split('/')[-1].strip('.root'),file_in.split('/')[-1].strip('.root'),len(binx_)-1,array.array('d', binx_),len(biny_)-1,array.array('d', biny_))
   h_total_mcweight = TH1F('h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 'h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 2, 0, 2)

  hist_list = []
  for df in read_root(file_in, 'bbDM_QCDbCR_2b', columns=['dPhi_jetMET', 'dEtaJet12', 'weight'], chunksize=125000):
    for dPhi_jetMET, dEtaJet12, weight in zip(df.dPhi_jetMET, df.dEtaJet12, df.weight):
      if dPhi_jetMET == -9999: continue
      ctsValue = abs(math.tanh(dEtaJet12/2))
      #print(dPhi_jetMET,ctsValue,weight)
      hist_list.append([dPhi_jetMET,ctsValue,weight])
      #qcdDphi.Fill(dPhi_jetMET,ctsValue,weight)

  for df in read_root(file_in, 'bbDM_SR_2b', columns=['dPhi_jetMET', 'dEtaJet12', 'weight'], chunksize=125000):
    for dPhi_jetMET, dEtaJet12, weight in zip(df.dPhi_jetMET, df.dEtaJet12, df.weight):
      if dPhi_jetMET == -9999: continue
      ctsValue = abs(math.tanh(dEtaJet12/2))
      #print(dPhi_jetMET,ctsValue,weight)
      hist_list.append([dPhi_jetMET,ctsValue,weight])
      #qcdDphi.Fill(dPhi_jetMET,ctsValue,weight)

  #print(hist_list)
  for i in range(len(hist_list)):
    qcdDphi.Fill(hist_list[i][0],hist_list[i][1],hist_list[i][2])
  #qcdDphi.Write()
  h_total_mcweight.Add(file_in.Get('h_total_mcweight'))
  histo_list.append(qcdDphi)
  histo_list.append(h_total_mcweight)


#file_out.Write()
file_out.cd()
for hist in hist_list:
  hist.Write()
file_out.Close()
