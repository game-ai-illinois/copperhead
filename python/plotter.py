import pandas as pd
import numpy as np
from hist.intervals import poisson_interval
from python.workflow import parallelize
from python.io import load_histogram
from python.variable import Variable
from python.entry import Entry

import matplotlib.pyplot as plt
import mplhep as hep

style = hep.style.CMS
style["mathtext.fontset"] = "cm"
style["mathtext.default"] = "rm"
plt.style.use(style)

stat_err_opts = {
    "step": "post",
    "label": "Stat. unc.",
    "hatch": "//////",
    "facecolor": "none",
    "edgecolor": (0, 0, 0, 0.5),
    "linewidth": 0,
}
ratio_err_opts = {"step": "post", "facecolor": (0, 0, 0, 0.3), "linewidth": 0}


def plotter(client, parameters, hist_df=None, timer=None):

    if hist_df is None:
        arg_load = {
            "year": parameters["years"],
            "var_name": parameters["hist_vars"],
            "dataset": parameters["datasets"],
        }
        hist_rows = parallelize(load_histogram, arg_load, client, parameters)
        hist_df = pd.concat(hist_rows).reset_index(drop=True)

    arg_plot = {
        "year": parameters["years"],
        "region": parameters["regions"],
        "channel": parameters["channels"],
        "var_name": [
            v for v in hist_df.var_name.unique() if v in parameters["plot_vars"]
        ],
        "df": [hist_df],
    }

    yields = parallelize(plot, arg_plot, client, parameters)

    return yields


def plot(args, parameters={}):
    year = args["year"]
    region = args["region"]
    channel = args["channel"]
    var_name = args["var_name"]
    hist = args["df"].loc[(args["df"].var_name == var_name) & (args["df"].year == year)]

    if var_name in parameters["variables_lookup"].keys():
        var = parameters["variables_lookup"][var_name]
    else:
        var = Variable(var_name, var_name, 50, 0, 5)

    if hist.shape[0] == 0:
        return

    plotsize = 8
    ratio_plot_size = 0.25

    # temporary
    variation = "nominal"

    slicer = {"region": region, "channel": channel}
    if parameters["has_variations"]:
        slicer["variation"] = variation

    fig = plt.figure()

    if parameters["plot_ratio"]:
        fig.set_size_inches(plotsize * 1.2, plotsize * (1 + ratio_plot_size))
        gs = fig.add_gridspec(
            2, 1, height_ratios=[(1 - ratio_plot_size), ratio_plot_size], hspace=0.07
        )
        # Top panel: Data/MC
        ax1 = fig.add_subplot(gs[0])
    else:
        fig, ax1 = plt.subplots()
        fig.set_size_inches(plotsize, plotsize)

    # stack, step, and errorbar entries
    entries = {et: Entry(et, parameters) for et in parameters["plot_groups"].keys()}

    total_yield = 0
    for entry in entries.values():
        if len(entry.entry_list) == 0:
            continue

        plottables_df = entry.get_plottables(hist, year, var_name, slicer)
        plottables = plottables_df["hist"].values.tolist()
        sumw2 = plottables_df["sumw2"].values.tolist()
        labels = plottables_df["label"].values.tolist()
        total_yield += sum([p.sum() for p in plottables])

        if len(plottables) == 0:
            continue

        yerr = np.sqrt(sum(plottables).values()) if entry.yerr else None

        hep.histplot(
            plottables,
            label=labels,
            ax=ax1,
            yerr=yerr,
            stack=entry.stack,
            histtype=entry.histtype,
            **entry.plot_opts,
        )

        # MC errors
        if entry.entry_type == "stack":
            total_bkg = sum(plottables).values()
            total_sumw2 = sum(sumw2).values()
            if sum(total_bkg) > 0:
                err = poisson_interval(total_bkg, total_sumw2)
                ax1.fill_between(
                    x=plottables[0].axes[0].edges,
                    y1=np.r_[err[0, :], err[0, -1]],
                    y2=np.r_[err[1, :], err[1, -1]],
                    **stat_err_opts,
                )

    ax1.set_yscale("log")
    ax1.set_ylim(0.01, 1e9)
    ax1.legend(prop={"size": "x-small"})

    if parameters["plot_ratio"]:
        ax1.set_xlabel("")
        ax1.tick_params(axis="x", labelbottom=False)
    else:
        ax1.set_xlabel(var.caption, loc="right")

    if parameters["plot_ratio"]:

        # Bottom panel: Data/MC ratio plot
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        num = den = []

        if len(entries["errorbar"].entry_list) > 0:
            # get Data yields
            num_df = entries["errorbar"].get_plottables(hist, year, var.name, slicer)
            num = num_df["hist"].values.tolist()
            if len(num) > 0:
                num = sum(num).values()

        if len(entries["stack"].entry_list) > 0:
            # get MC yields and sumw2
            den_df = entries["stack"].get_plottables(hist, year, var.name, slicer)
            den = den_df["hist"].values.tolist()
            den_sumw2 = den_df["sumw2"].values.tolist()
            if len(den) > 0:
                edges = den[0].axes[0].edges
                den = sum(den).values()  # total MC
                den_sumw2 = sum(den_sumw2).values()

        if len(num) * len(den) > 0:
            # compute Data/MC ratio
            ratio = np.divide(num, den)
            yerr = np.zeros_like(num)
            yerr[den > 0] = np.sqrt(num[den > 0]) / den[den > 0]
            hep.histplot(
                ratio,
                bins=edges,
                ax=ax2,
                yerr=yerr,
                histtype="errorbar",
                **entries["errorbar"].plot_opts,
            )

        if sum(den) > 0:
            # compute MC uncertainty
            unity = np.ones_like(den)
            w2 = np.zeros_like(den)
            w2[den > 0] = den_sumw2[den > 0] / den[den > 0] ** 2
            den_unc = poisson_interval(unity, w2)
            ax2.fill_between(
                edges,
                np.r_[den_unc[0], den_unc[0, -1]],
                np.r_[den_unc[1], den_unc[1, -1]],
                label="Stat. unc.",
                **ratio_err_opts,
            )

        ax2.axhline(1, ls="--")
        ax2.set_ylim([0.5, 1.5])
        ax2.set_ylabel("Data/MC", loc="center")
        ax2.set_xlabel(var.caption, loc="right")
        ax2.legend(prop={"size": "x-small"})

    if parameters["14TeV_label"]:
        hep.cms.label(
            ax=ax1, data=False, label="Preliminary", year="HL-LHC", rlabel="14 TeV"
        )
    else:
        hep.cms.label(ax=ax1, data=True, label="Preliminary", year=year)

    if parameters["save_plots"]:
        path = parameters["plots_path"]
        out_name = f"{path}/{var.name}_{year}.png"
        fig.savefig(out_name)
        print(f"Saved: {out_name}")

    return total_yield
