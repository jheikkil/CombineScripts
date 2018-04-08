#!/usr/bin/env python
import ROOT
import re
from array import array
import argparse
from poisson import convert
from poisson import poisson_errors
from poisson import getTH1FfromTGraphAsymmErrors

parser = argparse.ArgumentParser(
    "Create pre/post-fit plots for SM HTT")
parser.add_argument(
    "--fs",
    action="store",
    dest="fs",
    default="emt",
    help="Which channel to run over? (emt, mmt, ett, mtt, whlep, whhad, wh, zh, eeem, eeet, eemt, eett, emmm, emmt, mmtt, mmmt, llem, llet, llmt, lltt)")
parser.add_argument(
    "--fit",
    action="store",
    dest="fit",
    default="postfit",
    help="Prefit or postfit? choose prefit or postfit")
parser.add_argument(
    "--unblind",
    action="store",
    dest="unblind",
    default=False,
    help="Ready to unblind? default is unblind=False, use --unblind=1 to unblind")
args = parser.parse_args()
fs=args.fs
fit=args.fit
unblind=args.unblind
assert( fit in ["prefit","postfit"] ), "Choice was not a valid fit argument: %s" % fit

if fit == "prefit" :
    prepend = "shapes_prefit/"
    output_dir = "prefit"
if fit == "postfit" :
    prepend = "shapes_fit_s/"
    output_dir = "postfit"

def print_yields( h, name ) :
    err = ROOT.Double(0.)
    #print h.IntegralAndError( 1, h.GetNbinsX() + 1, err )
    h.IntegralAndError( 1, h.GetNbinsX() + 1, err )
    #print h.Integral()
    print "%15s: %.3f \pm %.3f   &" % (name, h.Integral(), err)

def add_lumi():
    lowX=0.58
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
        #output = ROOT.TLegend(0.70, 0.40, 0.92, 0.84, "", "brNDC")
        output = ROOT.TLegend(0.45, 0.60, 0.95, 0.84, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetNColumns(2)
        output.SetTextFont(62)
        return output

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)

c=ROOT.TCanvas("canvas","",0,0,600,600)
c.cd()

file=ROOT.TFile("fitDiagnostics.root","r")
#print file

adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

wh_channels=["ch9","ch11","ch10","ch12"]
zh_channels=["ch1","ch5","ch2","ch6","ch3","ch7","ch4","ch8"]
channels=[]
set_max = 10
if fs=="emt":
  channels=["ch9"]
  cat_text = "e#mu#tau_{h}"
  set_max = 12
if fs=="mmt":
  channels=["ch11"]
  cat_text = "#mu#mu#tau_{h}"
  set_max = 12
if fs=="ett":
  channels=["ch10"]
  cat_text = "e#tau_{h}#tau_{h}"
  set_max = 12
if fs=="mtt":
  channels=["ch12"]
  cat_text = "#mu#tau_{h}#tau_{h}"
  set_max = 12
if fs=="eeem":
  channels=["ch1"]
  cat_text = "ee+e#mu"
  set_max = 7
if fs=="eeet":
  channels=["ch2"]
  cat_text = "ee+e#tau_{h}"
if fs=="eemt":
  channels=["ch3"]
  cat_text = "ee+#mu#tau_{h}"
if fs=="eett":
  channels=["ch4"]
  cat_text = "ee+#tau_{h}#tau_{h}"
if fs=="emmm":
  channels=["ch5"]
  cat_text = "#mu#mu+e#mu"
  set_max = 7
if fs=="emmt":
  channels=["ch6"]
  cat_text = "#mu#mu+e#tau_{h}"
if fs=="mmmt":
  channels=["ch7"]
  cat_text = "#mu#mu+#mu#tau_{h}"
if fs=="mmtt":
  channels=["ch8"]
  cat_text = "#mu#mu+#tau_{h}#tau_{h}"
if fs=="llem":
  channels=["ch1","ch5"]
  cat_text = "ll+e#mu"
if fs=="llet":
  channels=["ch2","ch6"]
  cat_text = "ll+e#tau_{h}"
if fs=="llmt":
  channels=["ch3","ch7"]
  cat_text = "ll+#mu#tau_{h}"
if fs=="lltt":
  channels=["ch4","ch8"]
  cat_text = "ll+#tau_{h}#tau_{h}"
if fs=="zh":
  channels=zh_channels
  cat_text = "ZH combined"
if fs=="whlep":
  channels=["ch9","ch11"]
  cat_text = "WH semi-leptonic"
if fs=="whhad":
  channels=["ch10","ch12"]
  cat_text = "WH hadronic"
if fs=="wh":
  channels=wh_channels
  cat_text = "WH combined"

nchan=len(channels)
print fs
#print channels

#print file.Get(prepend+channels[0])
#print file.Get(prepend+channels[0]).Get("data")
data_graph=file.Get(prepend+channels[0]).Get("data")
Data=getTH1FfromTGraphAsymmErrors( data_graph, "data" )
Data.Sumw2(ROOT.kFALSE)
Data.SetBinErrorOption(ROOT.TH1.kPoisson)
#Data=file.Get(prepend+channels[0]).Get("data")
#print Data
ZZ=file.Get(prepend+channels[0]).Get("ZZ")
if file.Get(prepend+channels[0]).Get("ggZZ"):
  ZZ.Add(file.Get(prepend+channels[0]).Get("ggZZ"))
WZ=file.Get(prepend+channels[0]).Get("WZ")
#print file.Get(prepend+channels[0]).Get("WZ")
Rare=file.Get(prepend+channels[0]).Get("ttZ")
if file.Get(prepend+channels[0]).Get("TT"):
 Rare.Add(file.Get(prepend+channels[0]).Get("TT"))
if file.Get(prepend+channels[0]).Get("allFakes"):
  Fake=file.Get(prepend+channels[0]).Get("allFakes")
if file.Get(prepend+channels[0]).Get("RedBkg"):
  Fake=file.Get(prepend+channels[0]).Get("RedBkg")
if file.Get(prepend+channels[0]).Get("jetFakes"):
  Fake=file.Get(prepend+channels[0]).Get("jetFakes")
#print prepend+channels[0]
WH=file.Get(prepend+channels[0]).Get("WH_htt")
ZH=file.Get(prepend+channels[0]).Get("ZH_htt")
Total=file.Get(prepend+channels[0]).Get("total_background")
if file.Get(prepend+channels[0]).Get("DY"):
  Rare.Add(file.Get(prepend+channels[0]).Get("DY"))
if file.Get(prepend+channels[0]).Get("ttW"): 
  Rare.Add(file.Get(prepend+channels[0]).Get("ttW"))
if file.Get(prepend+channels[0]).Get("TriBoson"):
  Rare.Add(file.Get(prepend+channels[0]).Get("TriBoson"))
if file.Get(prepend+channels[0]).Get("WH_hww125"):
  Rare.Add(file.Get(prepend+channels[0]).Get("WH_hww125"))
if file.Get(prepend+channels[0]).Get("ZH_hww125"):
  Rare.Add(file.Get(prepend+channels[0]).Get("ZH_hww125"))
if file.Get(prepend+channels[0]).Get("ggH_hzz125"):
  Rare.Add(file.Get(prepend+channels[0]).Get("ggH_hzz125"))
if file.Get(prepend+channels[0]).Get("ttH_other125"):
  Rare.Add(file.Get(prepend+channels[0]).Get("ttH_other125"))
if file.Get(prepend+channels[0]).Get("ttHnonBB"):
  Rare.Add(file.Get(prepend+channels[0]).Get("ttHnonBB"))
if channels[0] not in wh_channels and file.Get(prepend+channels[0]).Get("WZ"):
  Rare.Add(file.Get(prepend+channels[0]).Get("WZ"))

for i in range (1,nchan):
   data_graph=file.Get(prepend+channels[i]).Get("data")
   data_hist=getTH1FfromTGraphAsymmErrors( data_graph )
   data_hist.Sumw2(ROOT.kFALSE)
   data_hist.SetBinErrorOption(ROOT.TH1.kPoisson)
   Data.Add(data_hist)
   ZZ.Add(file.Get(prepend+channels[i]).Get("ZZ"))
   if file.Get(prepend+channels[i]).Get("ggZZ"):
     ZZ.Add(file.Get(prepend+channels[i]).Get("ggZZ"))
   if channels[i] in wh_channels :
     WZ.Add(file.Get(prepend+channels[i]).Get("WZ"))
   if file.Get(prepend+channels[i]).Get("DY"): 
     Rare.Add(file.Get(prepend+channels[i]).Get("DY"))
   if file.Get(prepend+channels[i]).Get("TT"): 
     Rare.Add(file.Get(prepend+channels[i]).Get("TT"))
   if file.Get(prepend+channels[i]).Get("allFakes"): 
     Fake.Add(file.Get(prepend+channels[i]).Get("allFakes"))
   if file.Get(prepend+channels[i]).Get("RedBkg"): 
     Fake.Add(file.Get(prepend+channels[i]).Get("RedBkg"))
   if file.Get(prepend+channels[i]).Get("jetFakes"): 
     Fake.Add(file.Get(prepend+channels[i]).Get("jetFakes"))
   WH.Add(file.Get(prepend+channels[i]).Get("WH_htt"))
   ZH.Add(file.Get(prepend+channels[i]).Get("ZH_htt"))
   if file.Get(prepend+channels[i]).Get("ttZ"):
     Rare.Add(file.Get(prepend+channels[i]).Get("ttZ"))
   if file.Get(prepend+channels[i]).Get("ttW"):
     Rare.Add(file.Get(prepend+channels[i]).Get("ttW"))
   if file.Get(prepend+channels[i]).Get("TriBoson"):
     Rare.Add(file.Get(prepend+channels[i]).Get("TriBoson"))
   if file.Get(prepend+channels[i]).Get("WH_hww125"):
     Rare.Add(file.Get(prepend+channels[i]).Get("WH_hww125"))
   if file.Get(prepend+channels[i]).Get("ZH_hww125"):
     Rare.Add(file.Get(prepend+channels[i]).Get("ZH_hww125"))
   if file.Get(prepend+channels[i]).Get("ggH_hzz125"): 
     Rare.Add(file.Get(prepend+channels[i]).Get("ggH_hzz125"))
   if file.Get(prepend+channels[0]).Get("ttH_other125"):
     Rare.Add(file.Get(prepend+channels[0]).Get("ttH_other125"))
   if file.Get(prepend+channels[0]).Get("ttHnonBB"):
     Rare.Add(file.Get(prepend+channels[0]).Get("ttHnonBB"))
   if channels[i] not in wh_channels and file.Get(prepend+channels[i]).Get("WZ"):
     Rare.Add(file.Get(prepend+channels[i]).Get("WZ"))

   Total.Add(file.Get(prepend+channels[i]).Get("total_background"))

#if fit == "prefit" :
#    WH.Scale(5./6.5 / 2.34)
#    ZH.Scale(5./6.5 / 2.34)
#if fit == "postfit" :
#    WH.Scale(5. / 2.34) # 2.34 is signal str
#    ZH.Scale(5. / 2.34)

WH.GetXaxis().SetTitle("")
WH.GetXaxis().SetTitleSize(0)
WH.GetXaxis().SetNdivisions(505)
WH.GetYaxis().SetLabelFont(42)
WH.GetYaxis().SetLabelOffset(0.01)
WH.GetYaxis().SetLabelSize(0.06)
WH.GetYaxis().SetTitleSize(0.075)
WH.GetYaxis().SetTitleOffset(1.04)
WH.SetTitle("")
WH.GetYaxis().SetTitle("Events/bin")
WH.SetMinimum(0)
WH.SetMarkerStyle(20)
WH.SetMarkerSize(1)
WH.GetXaxis().SetLabelSize(0)

Data.Sumw2(ROOT.kFALSE)
Data.SetBinErrorOption(ROOT.TH1.kPoisson)
Data.GetXaxis().SetTitle("")
Data.GetXaxis().SetTitleSize(0)
Data.GetXaxis().SetNdivisions(505)
Data.GetYaxis().SetLabelFont(42)
Data.GetYaxis().SetLabelOffset(0.01)
Data.GetYaxis().SetLabelSize(0.06)
Data.GetYaxis().SetTitleSize(0.075)
Data.GetYaxis().SetTitleOffset(1.04)
Data.SetTitle("")
Data.GetYaxis().SetTitle("Events/bin")

if channels[0] in wh_channels :
 WZ.SetFillColor(ROOT.TColor.GetColor("#efe7ae"))
ZZ.SetFillColor(ROOT.TColor.GetColor("#11e7ae"))
Fake.SetFillColor(ROOT.TColor.GetColor("#a278aa"))
Rare.SetFillColor(ROOT.TColor.GetColor("#3e125f"))
WH.SetLineWidth(4)
ZH.SetLineWidth(4)

Data.SetMarkerStyle(20)
Data.SetLineColor(1)
Data.SetMarkerSize(1)
Fake.SetLineColor(1)
if channels[0] in wh_channels :
  WZ.SetLineColor(1)
ZZ.SetLineColor(1)
Rare.SetLineColor(1)
Total.SetLineColor(1)
ZH.SetLineColor(2)
WH.SetLineColor(9)

errorBand=Total.Clone()

stack=ROOT.THStack("stack","stack")
if channels[0] in wh_channels :
  stack.Add(WZ)
stack.Add(ZZ)
stack.Add(Rare)
stack.Add(Fake)

print_yields( ZZ, 'ZZ' )
if channels[0] in wh_channels :
  print_yields( WZ, 'WZ' )
print_yields( Rare, 'Rare' )
print_yields( Fake, 'Fake' )
print_yields( WH, 'WH' )
print_yields( ZH, 'ZH' )
print_yields( Data, 'Data' )

errorBand.SetMarkerSize(0)
errorBand.SetFillColor(new_idx)
errorBand.SetFillStyle(3001)
errorBand.SetLineWidth(1)

pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
pad1.Draw()
pad1.cd()
pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetBorderSize(10)
pad1.SetTickx(1)
pad1.SetTicky(1)
pad1.SetLeftMargin(0.18)
pad1.SetRightMargin(0.05)
pad1.SetTopMargin(0.122)
pad1.SetBottomMargin(0.026)
pad1.SetFrameFillStyle(0)
pad1.SetFrameLineStyle(0)
pad1.SetFrameLineWidth(3)
pad1.SetFrameBorderMode(0)
pad1.SetFrameBorderSize(10)

Data.GetXaxis().SetLabelSize(0)

# Blinding
if not unblind :
    for k in range(1,Data.GetSize()-1):
         s=WH.GetBinContent(k)+ZH.GetBinContent(k)
         b=ZZ.GetBinContent(k)+Fake.GetBinContent(k)
         if channels[0] in wh_channels :
           b=ZZ.GetBinContent(k)+Fake.GetBinContent(k)+WZ.GetBinContent(k)
         if (b<0):
             b=0.000001
         if (0.2*s/(0.00001+0.05*s+b)**0.5 > 0.15):
             Data.SetBinContent(k,-10)
             Data.SetBinError(k,0)
         # blind ZH on mass peak for high LT always
         if channels[0] in zh_channels and (k == 15 or k == 16) :
             Data.SetBinContent(k,-10)
             Data.SetBinError(k,0)
Data.SetMinimum(0)

Poisson=convert(Data)
Poisson.GetXaxis().SetTitle("")
Poisson.GetXaxis().SetTitleSize(0)
Poisson.GetXaxis().SetNdivisions(505)
Poisson.GetYaxis().SetLabelFont(42)
Poisson.GetYaxis().SetLabelOffset(0.01)
Poisson.GetYaxis().SetLabelSize(0.06)
Poisson.GetYaxis().SetTitleSize(0.075)
Poisson.GetYaxis().SetTitleOffset(1.04)
Poisson.SetTitle("")
Poisson.GetYaxis().SetTitle("Events/bin")
Poisson.SetMinimum(0)
Poisson.SetMarkerStyle(20)
Poisson.SetLineColor(1)
Poisson.SetMarkerSize(1)
Poisson.GetXaxis().SetLabelSize(0)

# Poisson errors are large, make max 10 or greater
WH.SetMaximum( 
    max( Poisson.GetMaximum()*2.0, stack.GetMaximum()*2.0,
    Data.GetMaximum()*2.0,stack.GetMaximum()*2.0, set_max) )

# Check all bins to see if bin yield is zero (this is happening
# to WH postfit for some reason...) and limit range if so
emptyBins = []
for b in range(1, Total.GetXaxis().GetNbins()+ 1 ) :
    if Total.GetBinContent(b) == 0 and Data.GetBinContent(b) == 0 :
        print "both equal zero. skip bin",b
        emptyBins.append( b )
print "To skip:",emptyBins

if len( emptyBins ) > 0 :
    WH.GetXaxis().SetRange(1,emptyBins[0]-1)
    print "Limiting range from bins: %i - %i" % (1, emptyBins[0]-1 )

#Poisson.Draw("AP")
#Data.Draw("e0")
WH.Draw("hist")
stack.Draw("histsame")
errorBand.Draw("e2same")
WH.Draw("histsame")
ZH.Draw("histsame")
#Data.Draw("e0same")
Poisson.Draw("P")

legende=make_legend()
legende.AddEntry(Data,"Observed","elp")
if channels[0] in wh_channels :
  legende.AddEntry(WZ,"WZ#rightarrow 3l#nu","f")
legende.AddEntry(ZZ,"ZZ#rightarrow 4l","f")
legende.AddEntry(Rare,"Rare","f")
legende.AddEntry(Fake,"Reducible","f")
legende.AddEntry(WH,"WH, H#rightarrow#tau#tau (x5)","l")
legende.AddEntry(ZH,"ZH, H#rightarrow#tau#tau (x5)","l")
legende.AddEntry(errorBand,"Uncertainty","f")
legende.Draw()

l1=add_lumi()
l1.Draw("same")
l2=add_CMS()
l2.Draw("same")
l3=add_Preliminary()
l3.Draw("same")

pad1.RedrawAxis()

categ  = ROOT.TPaveText(0.21, 0.45+0.013, 0.38, 0.70+0.155, "NDC")
categ.SetBorderSize(   0 )
categ.SetFillStyle(    0 )
categ.SetTextAlign(   12 )
categ.SetTextSize ( 0.05 )
categ.SetTextColor(    1 )
categ.SetTextFont (   42 )
categ.AddText( cat_text )

categ.Draw()

c.cd()
pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.35);
pad2.SetLeftMargin(0.18);
pad2.SetRightMargin(0.05);
pad2.SetTickx(1)
pad2.SetTicky(1)
pad2.SetFrameLineWidth(3)
pad2.SetGridx()
pad2.SetGridy()
pad2.Draw()
pad2.cd()
h1=Data.Clone()
hp=Poisson.Clone()
#hp.SetMaximum(2.0)#FIXME(1.5)
#hp.SetMinimum(0.0)#FIXME(0.5)
hp.SetMarkerStyle(20)
#h1.SetMaximum(2.0)#FIXME(1.5)
#h1.SetMinimum(0.0)#FIXME(0.5)
h1.SetMarkerStyle(20)
h3=errorBand.Clone()
hwoE=errorBand.Clone()
p_x=hp.GetX()
p_y=hp.GetY()
#print p_x[0],p_x[1],hwoE.GetBinContent(1)
for iii in range (0,hwoE.GetSize()-2):
  hwoE.SetBinError(iii+1,0)
  #print iii,p_x[iii],p_y[iii],p_y[iii]/max(hwoE.GetBinContent(iii+1),1e-5),h3.GetBinContent(iii+1)
  hp.SetPoint(iii,p_x[iii],p_y[iii]/max(hwoE.GetBinContent(iii+1),1e-5))
  hp.SetPointEYhigh(iii,hp.GetErrorYhigh(iii)/max(hwoE.GetBinContent(iii+1),1e-5))
  hp.SetPointEYlow(iii,hp.GetErrorYlow(iii)/max(hwoE.GetBinContent(iii+1),1e-5))
h1.SetStats(0)
h1.Divide(hwoE)
h3.Divide(hwoE)
h1.GetXaxis().SetTitle("m_{vis} (GeV)")
if channels[0] not in wh_channels :
   h1.GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
h1.GetYaxis().SetTitle("Obs./Exp.")
h1.GetXaxis().SetNdivisions(505)
h1.GetYaxis().SetNdivisions(5)

h3.GetXaxis().SetTitle("m_{vis} (GeV)")
if channels[0] not in wh_channels :
   h3.GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
h3.GetYaxis().SetTitle("Obs./Exp.")
h3.GetXaxis().SetNdivisions(505)
h3.GetYaxis().SetNdivisions(5)
h3.SetTitle("")
h3.GetXaxis().SetTitleSize(0.12)
h3.GetYaxis().SetTitleSize(0.12)
h3.GetYaxis().SetTitleOffset(0.56)
h3.GetXaxis().SetTitleOffset(1.06)
h3.GetXaxis().SetLabelSize(0.09)
h3.GetYaxis().SetLabelSize(0.11)
for b in range( 1, Data.GetXaxis().GetNbins()+1 ) :
    if channels[0] in wh_channels :
        text = "%i - %i" % ( ((b+1) * 10), (b+2) * 10)
    else : # ZH
        if b < 11 :
            text = "%i - %i" % ( ((b) * 20), (( (b+1)) * 20) )
        else :
            text = "%i - %i" % ( ((b) * 20)-200, (( (b+1)) * 20)-200 )
    h3.GetXaxis().SetBinLabel( b, text ) 
#h3.GetXaxis().SetBit( ROOT.TAxis.kLabelsVert )
h3.GetXaxis().SetLabelOffset(0.02)
h3.GetXaxis().SetTitleFont(42)
h3.GetYaxis().SetTitleFont(42)

h3.SetMaximum(3.0)#FIXME(1.5)
h3.SetMinimum(0.0)#FIXME(0.5)

if len( emptyBins ) > 0 :
    h3.GetXaxis().SetRange(1,emptyBins[0]-1 )
    print "Limiting range from bins: %i - %i" % (1, emptyBins[0]-1 )

h3.Draw("e2")
hp.Draw("P")

c.cd()
pad1.Draw()

ROOT.gPad.RedrawAxis()

c.Modified()
c.SaveAs(output_dir+"/"+fs+"_"+fit+".pdf")


