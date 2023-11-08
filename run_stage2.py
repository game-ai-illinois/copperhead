import glob
import tqdm
import argparse
import dask
from dask.distributed import Client
import dask.dataframe as dd

from python.io import load_dataframe
from stage2.postprocessor import process_partitions
from stage3.fitter import run_fits

from config.mva_bins import mva_bins
from config.variables import variables_lookup

__all__ = ["dask"]


parser = argparse.ArgumentParser()
parser.add_argument(
    "-y", "--year", nargs="+", help="Years to process", default=["2018"]
)
parser.add_argument(
    "-sl",
    "--slurm",
    dest="slurm_port",
    default=None,
    action="store",
    help="Slurm cluster port (if not specified, will create a local cluster)",
)
parser.add_argument(
    "-l",
    "--label",
    dest="label",
    default="test",
    action="store",
    help="Unique run label (to create output path)",
)
args = parser.parse_args()

# Dask client settings
use_local_cluster = args.slurm_port is None
node_ip = "128.211.149.133"
node_ip = "128.211.149.140"

if use_local_cluster:
    ncpus_local = 4
    slurm_cluster_ip = ""
    dashboard_address = f"{node_ip}:34875"
else:
    slurm_cluster_ip = f"{node_ip}:{args.slurm_port}"
    dashboard_address = f"{node_ip}:8787"

# global parameters
parameters = {
    # < general settings >
    "slurm_cluster_ip": slurm_cluster_ip,
    "global_path": "/depot/cms/hmm/vscheure",
    "years": args.year,
    "label": args.label,
    #"channels": ["ggh_0jets","ggh_1jet","ggh_2orMoreJets","vbf"],
    #"channels": ["ggh"],
    "channels": ["ggh"],
    "mva_channels": ["ggh"],
    "cats_by_score": True,
    #"regions": ["h-sidebands","h-peak"],
    "regions": ["h-peak"],
    
    "syst_variations": ["nominal"],
    # "custom_npartitions": {
    #     "vbf_powheg_dipole": 1,
    # },
    #
    # < settings for histograms >
    "hist_vars":  ["dimuon_mass","dimuon_pt","dimuon_ebe_mass_res","dimuon_cos_theta_cs","zeppenfeld","jj_dEta","dimuon_phi_cs","jj_mass","dimuon_dR","njets","mu1_pt","dimuon_mass_res","mu1_eta","jet1_pt","njets","mmj_min_dEta","mmj2_dPhi","jet1_eta", "jet1_phi",],
    "variables_lookup": variables_lookup,
    "save_hists": True,
    #
    # < settings for unbinned output>
    "tosave_unbinned": {
        "vbf": ["dimuon_mass", "event", "wgt_nominal", "mu1_pt", "score_pytorch_test"],
        "none": ["dimuon_mass", "event", "wgt_nominal", "mu1_pt", "score_pytorch_test"],
        "ggh_0jets": ["dimuon_mass", "wgt_nominal"],
        "ggh_1jet": ["dimuon_mass", "wgt_nominal"],
        "ggh_2orMoreJets": ["dimuon_mass", "wgt_nominal"],
    },
    "save_unbinned": True,
    #
    # < MVA settings >
    "models_path": "/depot/cms/hmm/vscheure/data/trained_models/",
    "dnn_models": {
        #"vbf": ["ValerieDNNtest2","ValerieDNNtest3"],
        "ggh": ["ggHtest2"]
        #"vbf": ["ValerieDNNtest3"]
        # "vbf": ["pytorch_test"],
        # "vbf": ["pytorch_jun27"],
        #"vbf": ["pytorch_jun27"],
        #"vbf": ["pytorch_jul12"],  # jun27 is best
        # "vbf": ["pytorch_aug7"],
         #"vbf": [
             #"ValerieDNNtest2",
             #"pytorch_jun27",
        #    #"pytorch_sep4",
        #    #"pytorch_sep2_vbf_vs_dy",
        #    #"pytorch_sep2_vbf_vs_ewk",
        #    #"pytorch_sep2_vbf_vs_dy+ewk",
        #    #"pytorch_sep2_ggh_vs_dy",
        #    #"pytorch_sep2_ggh_vs_ewk",
        #    #"pytorch_sep2_ggh_vs_dy+ewk",
        #    #"pytorch_sep2_vbf+ggh_vs_dy",
        #    #"pytorch_sep2_vbf+ggh_vs_ewk",
        #    #"pytorch_sep2_vbf+ggh_vs_dy+ewk",
         #],
        # "vbf": ["pytorch_may24_pisa"],
    },
    # "mva_categorizer": "3layers_64_32_16_all_feat",
    # "vbf_mva_cutoff": 0.5,
   # "bdt_models": {
        # "vbf": ["bdt_sep13"],
    #},
    "mva_bins_original": mva_bins,
}

parameters["datasets"] = [
    "data_A",
    "data_B",
    "data_C",
    "data_D",
    "data_E",
    "data_F",
    "data_G",
    "data_H",
    "dy_M-50",
    "dy_M-50_nocut",
    "dy_M-100To200",
    #"dy_1j",
    #"dy_2j",
    #"dy_m105_160_amc",
    #"dy_m105_160_vbf_amc",
    #"ewk_lljj_mll105_160_py_dipole",
    "ewk_lljj_mll50_mjj120",
    "ttjets_dl",
    "ttjets_sl",
    #"ttw",
    #"ttz",
    "st_tw_top",
    "st_tw_antitop",
    "ww_2l2nu",
    "wz_2l2q",
    "wz_1l1nu2q",
    "wz_3lnu",
    "zz",
    #"www",
    #"wwz",
    #wzz",
    #"zzz",
    "ggh_powheg",
    "vbf_powheg",
]
# using one small dataset for debugging
#parameters["datasets"] = ["ggh_localTest"]

if __name__ == "__main__":
    # prepare Dask client
    if use_local_cluster:
        print(
            f"Creating local cluster with {ncpus_local} workers."
            f" Dashboard address: {dashboard_address}"
        )
        client = Client(
            processes=True,
            #dashboard_address=dashboard_address,
            n_workers=ncpus_local,
            threads_per_worker=1,
            memory_limit="8GB",
        )
    else:
        print(
            f"Connecting to Slurm cluster at {slurm_cluster_ip}."
            f" Dashboard address: {dashboard_address}"
        )
        client = Client(parameters["slurm_cluster_ip"])
    parameters["ncpus"] = len(client.scheduler_info()["workers"])
    print(f"Connected to cluster! #CPUs = {parameters['ncpus']}")

    # add MVA scores to the list of variables to create histograms from
    dnn_models = list(parameters["dnn_models"].values())
    bdt_models =[]
    #bdt_models = list(parameters["bdt_models"].values())
    for models in dnn_models + bdt_models:
       for model in models:
            parameters["hist_vars"] += ["score_" + model]
    
    # prepare lists of paths to parquet files (stage1 output) for each year and dataset
    #client = None
    all_paths = {}
    for year in parameters["years"]:
        all_paths[year] = {}
        for dataset in parameters["datasets"]:
            paths = glob.glob(
                f"{parameters['global_path']}/"
                f"{parameters['label']}/stage1_output/{year}/"
                f"{dataset}/*.parquet"
            )
            #print(f"{parameters['global_path']}/"
               #f"{parameters['label']}/stage1_output/{year}/"
                #f"{dataset}/")
            all_paths[year][dataset] = paths
            #print(all_paths)
    # run postprocessing
    for year in parameters["years"]:
        print(f"Processing {year}")
        
        for dataset, path in tqdm.tqdm(all_paths[year].items()):
            #print(path)
            if len(path) == 0:
                continue

            # read stage1 outputs
            df = load_dataframe(client, parameters, inputs=[path], dataset=dataset)
            print("have df, starting to compute")
            print(df.compute())
            if not isinstance(df, dd.DataFrame):
                print("Dataframe not in correct format")
                continue
            # run processing sequence (categorization, mva, histograms)
            info, df = process_partitions(client, parameters, df)
            #print(info)
            run_fits(client, parameters, df)
