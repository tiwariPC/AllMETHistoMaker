from ROOT import TFile
tfile = TFile.Open(
    "DataCardRootFiles/AllMETHistos_v17_07_04_00_11012020.root")
tfile.cd()
bool_check = False
for h in tfile.GetListOfKeys():
    h = h.ReadObj()
    if h.GetNbinsX() != 4:  # the number of bins you want
        bool_check = True
        if h.Integral()==0:
            print(h.GetName(), h.GetNbinsX(), h.Integral(), )
    for i in range(1, h.GetNbinsX()+1):
        if h.GetBinContent(i) == 0:
            print(h.GetName(),' bin'+str(i)+' ', h.GetBinContent(i))
            

if bool_check:
    print('INCORRECT BINNING')
else:
    print('CORRECT BINNING')   
print('Done')
