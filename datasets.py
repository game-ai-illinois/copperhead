datasets = {
    "2016": {
        "data_B": "/store/data/Run2016B_ver2/SingleMuon/NANOAOD/Nano25Oct2019_ver2-v1/",    
        "data_C": "/store/data/Run2016C/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_D": "/store/data/Run2016D/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_E": "/store/data/Run2016E/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_F": "/store/data/Run2016F/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_G": "/store/data/Run2016G/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_H": "/store/data/Run2016H/SingleMuon/NANOAOD/Nano25Oct2019-v1/",

        #"dy": "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
        "dy": "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/",
        "dy_0j" : "/store/mc/RunIISummer16NanoAODv6/DYToLL_0J_13TeV-amcatnloFXFX-pythia8/",
        "dy_1j" : "/store/mc/RunIISummer16NanoAODv6/DYToLL_1J_13TeV-amcatnloFXFX-pythia8/",
        "dy_2j" : "/store/mc/RunIISummer16NanoAODv6/DYToLL_2J_13TeV-amcatnloFXFX-pythia8/",
        
        "dy_m105_160_amc": "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/",
        "dy_m105_160_vbf_amc" : "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-105To160_VBFFilter_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/",
        "dy_m105_160_mg" : "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/",
        
        "dy_m105_160_vbf_mg" : "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-105To160_VBFFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
        
        "ttjets_dl": "/store/mc/RunIISummer16NanoAODv6/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
        "ttjets_sl": "/store/mc/RunIISummer16NanoAODv6/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/",
        "ttw" : "/store/mc/RunIISummer16NanoAODv6/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/",
        "ttz" : "/store/mc/RunIISummer16NanoAODv6/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/",
        
        
        "ewk_lljj_mll50_mjj120": "/store/mc/RunIISummer16NanoAODv6/EWK_LLJJ_MLL-50_MJJ-120_13TeV-madgraph-herwigpp/",
        "ewk_lljj_mll105_160": "/store/mc/RunIISummer16NanoAODv6/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneEEC5_13TeV-madgraph-herwigpp/",
        
        "st_t_top": "",
        "st_t_antitop": "",
        "st_tw_top": "/store/mc/RunIISummer16NanoAODv6/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/",
        "st_tw_antitop": "/store/mc/RunIISummer16NanoAODv6/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/",

        "ww_2l2nu": "/store/mc/RunIISummer16NanoAODv6/WWTo2L2Nu_13TeV-powheg/",
        "wz_3lnu" : "/store/mc/RunIISummer16NanoAODv6/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/",
        "wz_2l2q" : "/store/mc/RunIISummer16NanoAODv6/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/",
        "wz_1l1nu2q" : "/store/mc/RunIISummer16NanoAODv6/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/",
        "zz" : "/store/mc/RunIISummer16NanoAODv6/ZZ_TuneCUETP8M1_13TeV-pythia8/",
        
        "www": "/store/mc/RunIISummer16NanoAODv6/WWW_4F_DiLeptonFilter_TuneCUETP8M1_13TeV-amcatnlo-pythia8/",
        "wwz": "/store/mc/RunIISummer16NanoAODv6/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/",
        "wzz": "/store/mc/RunIISummer16NanoAODv6/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/",
        "zzz": "/store/mc/RunIISummer16NanoAODv6/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/",

        "ggh_amcPS": "/store/mc/RunIISummer16NanoAODv6/GluGluHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "ggh_amcPS_TuneCP5down" : "/store/mc/RunIISummer16NanoAODv6/GluGluHToMuMu_M125_TuneCP5down_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "ggh_amcPS_TuneCP5up" : "/store/mc/RunIISummer16NanoAODv6/GluGluHToMuMu_M125_TuneCP5up_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "ggh_powheg" : "/store/mc/RunIISummer16NanoAODv6/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/",
        "ggh_powhegPS" : "/store/mc/RunIISummer16NanoAODv6/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/",        
        
        "vbf_amcPS": "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "vbf_amcPS_TuneCP5down" : "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M125_TuneCP5down_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "vbf_amcPS_TuneCP5up" : "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M125_TuneCP5up_PSweights_13TeV_amcatnloFXFX_pythia8/",
        "vbf_powheg" : "/store/mc/RunIISummer16NanoAODv6/VBF_HToMuMu_M125_13TeV_powheg_pythia8/",
        "vbf_powhegPS" : "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/",        
        "vbf_amc_herwig" :  "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M-125_TuneEEC5_13TeV-amcatnlo-herwigpp/",
        "vbf_powheg_herwig" : "/store/mc/RunIISummer16NanoAODv6/VBFHToMuMu_M-125_TuneEEC5_13TeV-powheg-herwigpp/",      
    
        "wmh" : "/store/mc/RunIISummer16NanoAODv6/WminusH_HToMuMu_WToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/",
        "wph" : "/store/mc/RunIISummer16NanoAODv6/WplusH_HToMuMu_WToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/",
        "tth" : "/store/mc/RunIISummer16NanoAODv6/ttHToMuMu_M125_TuneCP5_PSweights_13TeV-powheg-pythia8/",
        "zh" : "/store/mc/RunIISummer16NanoAODv6/ZH_HToMuMu_ZToAll_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/",
    },

    "2017": {
        "data_B": "/store/data/Run2017B/SingleMuon/NANOAOD/Nano25Oct2019-v1/",    
        "data_C": "/store/data/Run2017C/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_D": "/store/data/Run2017D/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_E": "/store/data/Run2017E/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_F": "/store/data/Run2017F/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
    
    },

    "2018": {
        "data_A": "/store/data/Run2018A/SingleMuon/NANOAOD/Nano25Oct2019-v1/",    
        "data_B": "/store/data/Run2018B/SingleMuon/NANOAOD/Nano25Oct2019-v1/",    
        "data_C": "/store/data/Run2018C/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
        "data_D": "/store/data/Run2018D/SingleMuon/NANOAOD/Nano25Oct2019-v1/",
    }
}


lumi_data = {
    "2016": {'lumi': 35860., 'events': 804026710}, # to be verified
    "2017": {'lumi': 41900., 'events': 769080716}, # to be verified
    "2018": {'lumi': 59900., 'events': 985425574} # to be verified
}