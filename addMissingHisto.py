import os, sys
from ROOT import TFile
file17=sys.argv[1]
file16=sys.argv[2]
tfile17 = TFile.Open(str(file17),'r')
tfile16 = TFile.Open(str(file16), 'update')
bool_check = False

missing_hist = ['_DMSimp_MPhi10_MChi1', '_DMSimp_MPhi150_MChi1', '_DMSimp_MPhi250_MChi1', '_DMSimp_MPhi450_MChi1',
                '_DMSimp_MPhi700_MChi1', '_2HDMa_Ma100_MChi1_MA1200', '_2HDMa_Ma100_MChi1_MA600', '_2HDMa_Ma300_MChi1_MA1200']
for h in tfile17.GetListOfKeys():
    h = h.ReadObj()
    if any([bool(mh in h.GetName()) for mh in missing_hist]):
      h1 = h.Clone(str(h.GetName()))
      h1.SetName(str(h.GetName()).replace('2017', '2016'))
      h1.SetTitle(str(h.GetName()).replace('2017', '2016'))
      h1.Scale(35.82/41.5)
      tfile16.cd()
      h1.Write()

tfile17.Close()
tfile16.Close()
