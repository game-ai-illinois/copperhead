#bin/bash
combineCards.py datacard_cat0.txt datacard_cat1-bkg.txt datacard_cat2-bkg.txt datacard_cat3-bkg.txt datacard_cat4-bkg.txt >  datacard_comb_sig_cat0.txt
combineCards.py datacard_cat0-bkg.txt datacard_cat1.txt datacard_cat2-bkg.txt datacard_cat3-bkg.txt datacard_cat4-bkg.txt >  datacard_comb_sig_cat1.txt
combineCards.py datacard_cat0-bkg.txt datacard_cat1-bkg.txt datacard_cat2.txt datacard_cat3-bkg.txt datacard_cat4-bkg.txt >  datacard_comb_sig_cat2.txt
combineCards.py datacard_cat0-bkg.txt datacard_cat1-bkg.txt datacard_cat2-bkg.txt datacard_cat3.txt datacard_cat4-bkg.txt >  datacard_comb_sig_cat3.txt
combineCards.py datacard_cat0-bkg.txt datacard_cat1-bkg.txt datacard_cat2-bkg.txt datacard_cat3-bkg.txt datacard_cat4.txt >  datacard_comb_sig_cat4.txt
combineCards.py datacard_cat0.txt datacard_cat1.txt datacard_cat2.txt datacard_cat3.txt datacard_cat4.txt >  datacard_comb_sig_all.txt
