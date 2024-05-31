# Instructions

## Running Calibration Fits: `run_fits.py`

- `is_Z` flag needs to be set to `True`
- `do_calib` Flag `True`: Does BWxDCB fits (calibration categories 1-12)
- `do_calib` Flag `False`, `do_closure` flag `True`: Runs closure test fits (also BWxDCB)
- Both need categorised `.csv` files with minimal necessary data (examples for 2017 can be found in `/depot/cms/hmm/vscheure/Calib/stage2_output`)

`run_fitsCopy1.py`: Runs Voigtian fits for calibration - same as `run_fits.py` otherwise

## Stage 1

- `run_stage1.py` runs main analysis. Takes NanoAOD input, outputs `.parquet` files with all variables necessary for the ggh and vbf analyses, with all weights and variations applied
- `run_stage2.py`: Does Categorisation and MVAs (BDT for ggh, DNN for vbf). Needs to be run separately for ggh and vbf due to incompatibility. Also makes `stage2_output` csv files for calibration and ggh fitting if the respective flags are set to true

## Stage 3

- `run_stage3.py` Makes plots for ggh and vbf. For vbf it also produces templates and datacards for combine

## Combine Fitting

### vbf

1. First combine the SR and SB datacards produced by stage3:
    ```
    CombineCards.py cardA.txt cardB.txt combined_datacard.txt
    ```

2. Produces prefit significance:
    ```
    combine -d combined_datacard.txt -M Significance -m 125 --expectSignal=1 -t -1 --rMin -2 --rMax 5
    ```

3. Does postfit:
    ```
    combine -d combined_datacard.txt -M Significance -m 125 --expectSignal=1 -t -1 --rMin -2 --rMax 5 --toysFreq
    ```

### ggh

- `run_fits.py` (flags `is_Z`, `do_calib`, and `do_closure` need to be False). Run on data and ggh_powheg. This will run the full CorePdf fits on signal and background and save plots and workspaces. Example of the latest ggh results can be found in `fits/fit_ggh_all` (initial bkg fit) and `fits/fits_ggh_phifixedBDT__cat*/` for the final fits in the BDT categories.
- Datacards for combine to run on the fit results can also be found in `fits/` for running on the categories separate or total.

#### Category Significance


	 ```
	combine -M Significance -d datacard_cat0_multi.root -m 125 -n _signif_cat0_ggh -t -1  --expectSignal 1  --setParameters pdf_index=0 --setParameterRanges r=-10,10 --cminDefaultMinimizerTolerance 0.1
	 ```
  
#### Total significance:
 
   ```
	combine -M Significance -d datacard_All_multiwithvbf.root -m 125 -n _signif_comb  --cminDefaultMinimizerStrategy 1   -t -1  --toysFrequentist --expectSignal 1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminRunAllDiscreteCombinations --setParameterRanges r=-10,10 --X-rtd MINIMIZER_freezeDisassociatedParam --cminDefaultMinimizerTolerance 0.01 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd FAST_VERTICAL_MORPH
   ```
All combine comands as well as the CorePDF fits need the conda env in /depot/cms/kernels/combine to work !
