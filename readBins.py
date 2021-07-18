import os, sys
from ROOT import TFile
file=sys.argv[1]
tfile = TFile.Open(str(file))
tfile.cd()
bool_check = False
reg_name = ['1b_SR', '2b_SR', '1b_ZMUMU', '2b_ZMUMU', '1b_TOPMU', '2b_TOPMU', '1b_WMU', '2b_WMU', '1b_ZEE', '2b_ZEE', '1b_TOPE', '2b_TOPE', '1b_WE', '2b_WE']
for h in tfile.GetListOfKeys():
    h = h.ReadObj()
    bin_list = []
    val_list = []
    for i in range(1, h.GetNbinsX()+1):
        # bin_list.append(h.GetXaxis().GetBinLabel(i))
        bin_list.append(h.GetBinWidth(i))
        val_list.append(h.GetBinContent(i))
    # print([i < 0.0 for i in val_list], any([i < 0.0 for i in val_list]))
    if any([i<=0.0 for i in val_list]):
        print(h.GetName(),bin_list, val_list)
        bool_check=True
    # if h.GetNbinsX() != 4:  # the number of bins you want
    #     bool_check = True
    #     if h.Integral()==0:
    #         print(h.GetName(), h.GetNbinsX(), h.Integral(), )
    # for i in range(1, h.GetNbinsX()+1):
    #     if h.GetBinContent(i) == 0:
    #         print(h.GetName(),' bin'+str(i)+' ', h.GetBinContent(i))

if bool_check:
    print('INCORRECT BINNING or Negative Elements')
else:
    print('CORRECT BINNING')
print('Done')


