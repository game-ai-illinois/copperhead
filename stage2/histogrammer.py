import itertools
import pandas as pd
import numpy as np

from hist import Hist
from python.variable import Variable
from python.io import save_stage2_output_hists


def make_histograms(df, var_name, year, dataset, regions, channels, categories, npart, parameters):
    # try to get binning from config
    #if "BDT" in var_name:
        #var_name = f"{var_name}_{year}"
    if var_name in parameters["variables_lookup"].keys():
        var = parameters["variables_lookup"][var_name]
    else:
        var = Variable(var_name, var_name, 40, 0, 1)
    #print(var_name)

    # prepare list of systematic variations
    do_variations = True
    if do_variations:
        wgt_variations = [w for w in df.columns if (("wgt_" in w) and ("nominal" not in w))]
    else: 
        wgt_variations = []
    wgt_variations.append("wgt_nominal")
    syst_variations = parameters.get("syst_variations", ["nominal"])
    variations = []
    for w in wgt_variations:
        #print(w)
        for v in syst_variations:
            variation = get_variation(w, v)
            if variation:
                variations.append(variation)

    # prepare multidimensional histogram
    # add axes for (1) mass region, (2) channel, (3) value or sumw2
    hist = (
        Hist.new.StrCat(regions, name="region")
        .StrCat(channels, name="channel")
        .StrCat(categories, name="category")
        .StrCat(["value", "sumw2"], name="val_sumw2")
    )

    # add axis for observable variable
    if "score" in var.name:
        #print(var.name)
        if "ggH" in var.name: 
            model_name = var.name.replace("score_", "").replace("_nominal", "")
            #model_name = f"{model_name}_{year}"
        else:
            model_name = var.name.replace("score_", "").replace("_nominal", "")
            #print(model_name)
        if "mva_bins" in parameters.keys():
            if model_name in parameters["mva_bins"].keys():
                #print(parameters["mva_bins"][model_name])
                bins = parameters["mva_bins"][model_name][f"{year}"]
                #print(bins)
            else:
                bins = np.arange(41) / 40.0
                #print( model_name)
        else:
            bins = np.arange(41) / 40.0
        hist = hist.Var(bins, name=var.name)
    else:
        hist = hist.Reg(var.nbins, var.xmin, var.xmax, flow = True, name=var.name, label=var.caption)

    # add axis for systematic variation
    hist = hist.StrCat(variations, name="variation")

    # specify container type
    hist = hist.Double()

    # loop over configurations and fill the histogram
    loop_args = {
        "region": regions,
        "w": wgt_variations,
        "v": syst_variations,
        "channel": channels,
        "category": categories,
    }
    loop_args = [
        dict(zip(loop_args.keys(), values))
        for values in itertools.product(*loop_args.values())
    ]
    hist_info_rows = []
    total_yield = 0
    for loop_arg in loop_args:
        region = loop_arg["region"]
        channel = loop_arg["channel"]
        category = loop_arg["category"]
        w = loop_arg["w"]
        v = loop_arg["v"]
        #print("w")
        #print("v")
        variation = get_variation(w, v)
        if not variation:
            continue

        var_name = f"{var.name}_{v}"
        if var_name not in df.columns:
            if var.name in df.columns:
                var_name = var.name
            elif f"{var.name}_{year}" in df.columns:
                var_name = f"{var.name}_{year}"
            else:
                continue

        slicer = (
            (df.dataset == dataset)
            & (df.region == region)
            & (df.year == year)
            & (df[f"channel_{v}"] == channel)
            & (df["category"] == category)
        )
        data = df.loc[slicer, var_name]
        weight = df.loc[slicer, w]

        to_fill = {var.name: data, "region": region, "channel": channel, "category": category}

        to_fill_value = to_fill.copy()
        to_fill_value["val_sumw2"] = "value"
        to_fill_value["variation"] = variation
        hist.fill(**to_fill_value, weight=weight)

        to_fill_sumw2 = to_fill.copy()
        to_fill_sumw2["val_sumw2"] = "sumw2"
        to_fill_sumw2["variation"] = variation
        hist.fill(**to_fill_sumw2, weight=weight * weight)

        hist_info_row = {
            "year": year,
            "var_name": var.name,
            "dataset": dataset,
            "variation": variation,
            "region": region,
            "channel": channel,
            "category": category,
            "yield": weight.sum(),
        }
        if weight.sum() == 0:
            continue
        total_yield += weight.sum()
        if "return_hist" in parameters:
            if parameters["return_hist"]:
                hist_info_row["hist"] = hist
        hist_info_rows.append(hist_info_row)

    if total_yield == 0:
        return None

    # save histogram for this partition to disk
    # (partitions will be joined in stage3)
    save_hists = parameters.get("save_hists", False)
    if save_hists:
        #if "score" in var.name:
            #print(var.name)
        save_stage2_output_hists(hist, var.name, dataset, year, parameters, npart)

    # return info for debugging
    hist_info_rows = pd.DataFrame(hist_info_rows)
    #print(hist_info_rows)
    return hist_info_rows


def get_variation(wgt_variation, sys_variation):
    #if "nominal" in wgt_variation:
    if wgt_variation == "wgt_nominal":
        if "nominal" in sys_variation:
            return "nominal"
        else:
            return sys_variation
    else:
        if "nominal" in sys_variation:
            return wgt_variation
        else:
            return None
