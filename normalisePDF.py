import sys
from ROOT import TFile
file_in=sys.argv[1]
file_out = sys.argv[2]
tfile_in = TFile.Open(str(file_in), 'r')
tfile_out = TFile.Open(str(file_out), 'RECREATE')

allhistos = []
hist_dict = {}

for h in tfile_in.GetListOfKeys():
    h = h.ReadObj()
    hist_dict.update({str(h.GetName()): h})

# for key in hist_dict:
#   # if '_2HDMa_' in key and ('_pdf' in key or '_mu_scale' in key):
#   if ('_pdf' in key or '_mu_scale' in key):
#     central = hist_dict[key.partition('0p7')[0]+key.partition('0p7')[1]].Integral()
#     UpDown = hist_dict[key].Integral()
#     scaling_fac = central/UpDown
#     print(key.partition('0p7')[0]+key.partition('0p7')[1]+key.partition('0p7')[2], scaling_fac)
#     hist_dict[key].Scale(scaling_fac)
#     allhistos.append(hist_dict[key])
#   else:
#     allhistos.append(hist_dict[key])


for key in hist_dict:
  # if '_2HDMa_' in key and ('_pdf' in key or '_mu_scale' in key):
  if ('_mu_scale' in key or ('_pdf' in key)):
    central = hist_dict[key.partition('_CMS')[0]].Integral()
    UpDown = hist_dict[key].Integral()
    scaling_fac = central/UpDown
    # print(key.partition('0p7')[0]+key.partition('0p7')[1]+key.partition('0p7')[2], scaling_fac)
    hist_dict[key].Scale(scaling_fac)
    allhistos.append(hist_dict[key])
  else:
    allhistos.append(hist_dict[key])


tfile_out.cd()
for hist in allhistos:
  hist.Write()

tfile_out.Close()
tfile_in.Close()
