from ROOT import TFile
tfile = TFile.Open("DataCardRootFiles/AllMETHistos_v16_07_04_01_SR_1p5.root ")
tfile.cd()
bool_check = False
for h in tfile.GetListOfKeys():
    h = h.ReadObj()
    if h.GetSize() !=6: ## the number of bins you want + 2 (for overflow and underflow)
        bool_check = True
        # print(h.ClassName(), h.GetName(), h.GetSize())

if bool_check:
    print('INCORRECT BINNING')
else:
    print('CORRECT BINNING')   
print('Done')
