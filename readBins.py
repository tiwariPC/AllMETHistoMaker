from ROOT import TFile
tfile = TFile.Open("DataCardRootFiles/AllMETHistos_v16_07_04_01.root")
tfile.cd()
bool_check = False
for h in tfile.GetListOfKeys():
    h = h.ReadObj()
    if h.GetNbinsX() != 4:  # the number of bins you want
        bool_check = True
        if h.Integral()==0:
            print(h.GetName(), h.GetNbinsX(), h.Integral(), )

if bool_check:
    print('INCORRECT BINNING')
else:
    print('CORRECT BINNING')   
print('Done')
