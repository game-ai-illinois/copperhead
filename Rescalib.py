import pandas as pd
import ROOT as rt
rt.gSystem.Load("stage3/lib/RooDoubleCB/RooDoubleCB_cxx")


#___---------_--___---____--Calibration_____---_______---____#
for i in range(0,30):
    cat_name  = f"Calibration_cat{i}"
    massResPE = pd.read_csv(f"/depot/cms/hmm/vscheure/Calib/stage2_output/2017/data_x/data_x_{cat_name}.csv")["dimuon_ebe_mass_res"].median()

    
    if i<=11:
        massResFit_ws_BW = rt.TFile.Open(f"fits/calib_fits/BWxDCBexp/2017/workspace_ggh_All_Zfit_Calib_calib_cat{i}.root").Get("w")
        massResFit = massResFit_ws_BW.var(f"sigma").getVal()
        massResFitErr = massResFit_ws_BW.var(f"sigma").getError()
        #massResFitVo = massResFit_ws_Vo.var(f"sigma_ggh_All").getVal()
        #massResFitErrVo = massResFit_ws_Vo.var(f"sigma_ggh_All").getError()
        Chi2BW = massResFit_ws_BW.var(f"chi2BWxDCB_ggh_All").getVal()
        #Chi2BVo= massResFit_ws_Vo.var(f"chi2VoigtianxErf_ggh_All").getVal()
    else:
        massResFit_ws_Vo = rt.TFile.Open(f"fits/calib_fits/Voigtian/2017/workspace_ggh_All_Zfit_Calib_calib_cat{i}.root").Get("w")
        massResFit = massResFit_ws_Vo.var(f"sigma_ggh_All").getVal()
        massResFitErr = massResFit_ws_Vo.var(f"sigma_ggh_All").getError()
    Factor = massResFit/massResPE
    print(f"Category {i}:  massResPE: {massResPE}, massResFit: {massResFit}, Fit unc. {massResFitErr}, Factor: {Factor}")
    #print(Factor)

    #print(f"Category {i}:  massResBW: {massResFit}, Fit unc. {massResFitErr}, Chi2: {Chi2BW}, massResFitVo: {massResFitVo}, Fit unc. {massResFitErrVo}, Chi2: {Chi2BVo}")
#exit()

#___---------_--___---____--ClosureTest_____---_______---____#

x_values=[]
y_values=[]
x_values2=[]
for i in [1,3,4,5,6,7,8,9,10]:
    
    cat_name  = f"Closure_cat{i}"
    massResPE = pd.read_csv(f"/depot/cms/hmm/vscheure/Calib/stage2_output/2017/data_x/data_x_{cat_name}.csv")["dimuon_ebe_mass_res_calib"].median()
    massResRaw = pd.read_csv(f"/depot/cms/hmm/vscheure/Calib/stage2_output/2017/data_x/data_x_{cat_name}.csv")["dimuon_ebe_mass_res"].median()
    massResFit_ws = rt.TFile.Open(f"fits/calib_fits/BWxDCBexp/2017/workspace_ggh_All_Zfit_Calib_closure_cat{i}.root").Get("w")

    massResFit = massResFit_ws.var(f"sigma").getVal()
    massResFitErr = massResFit_ws.var(f"sigma").getError()
    Chi2BW = massResFit_ws.var(f"chi2BWxDCB_ggh_All").getVal()
    x_values.append(massResPE)
    x_values2.append(massResRaw)
    y_values.append(massResFit)
    print(f"Closure category {i}: massResCalibrated: {massResPE}, massResFit: {massResFit}, Fit unc. {massResFitErr}, Chi2: {Chi2BW}")
import matplotlib.pyplot as plt
import numpy as np
# Create scatter plot
plt.scatter(x_values, y_values, label='Calibrated')
plt.scatter(x_values2, y_values, label='Non-calibrated')

min_val = min(min(x_values), min(y_values))
max_val = max(max(x_values), max(y_values))
# Calculate ±10% values
# Calculate the distance of ±10% from the line
line_x = [min_val, max_val]
ten_percent_distance =  0.1 * np.array(line_x)

# Define the coordinates for shading area
shading_x = np.linspace(min_val, max_val, 100)
shading_y1 = line_x + ten_percent_distance
shading_y2 = line_x - ten_percent_distance
# Add line for identical x and y values

plt.plot([min_val, max_val], [min_val, max_val], color='black')
plt.fill_between(line_x, shading_y1, shading_y2, color='lightblue', alpha=0.3, label='±10%')
# Add labels and title
plt.legend()
plt.xlabel('Calibrated resolution')
plt.ylabel('True resolution')
plt.title('Closure test 2017')
plt.savefig("Closuretest2017.png")
# Add legend
