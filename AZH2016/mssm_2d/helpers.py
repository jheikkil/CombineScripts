import ROOT

def add_lumi():
    lowX=0.63
    lowY=0.82
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    lumi.AddText("35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.15
    lowY=0.73
    cms  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    cms.SetTextFont(61)
    cms.SetTextSize(0.06)
    cms.SetBorderSize(   0 )
    cms.SetFillStyle(    0 )
    cms.SetTextAlign(   12 )
    cms.SetTextColor(    1 )
    cms.AddText("CMS")
    return cms

def add_Preliminary():
    lowX=0.15
    lowY=0.66
    prelim  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    prelim.SetTextFont(52)
    prelim.SetTextSize(0.05)
    prelim.SetBorderSize(   0 )
    prelim.SetFillStyle(    0 )
    prelim.SetTextAlign(   12 )
    prelim.SetTextColor(    1 )
    prelim.AddText("Preliminary")
    return prelim

def add_Scenario( text ):
    lowX=0.25
    lowY=0.82
    scenario  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    scenario.SetTextFont(42)
    scenario.SetTextSize(0.05)
    scenario.SetBorderSize(   0 )
    scenario.SetFillStyle(    0 )
    scenario.SetTextColor(    1 )
    scenario.AddText( text )
    return scenario