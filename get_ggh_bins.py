import glob
from stage2.categorizer import split_into_channels, categorize_dnn_output_ggh
from stage2.mva_evaluators import evaluate_bdt
from python.io import load_dataframe
import argparse

parameters = {
    "global_path": "/depot/cms/hmm/vscheure/",
    "label": "phifixed",
    "channels": ["ggh"],
    "custom_npartitions": {
        "ggh_powheg": 1,
    },
    "models_path": "/depot/cms/hmm/vscheure/data/trained_models/",
}

dataset = "ggh_powheg"
#model_name = "pytorch_may18"
#model_name = "pytorch_may24_pisa"


channel = "ggh"
region = "h-peak"
label = parameters["label"]
parser = argparse.ArgumentParser()
parser.add_argument(
    "--BDT",
    dest="BDTname",
    default="ggHnew",
    action="store",
    help="Name of BDT model",
)
args = parser.parse_args()
BDTname = args.BDTname
#for year in ["2016", "2017", "2018"]:
for year in ["2016"]:
    print(year)
    if year == "2016":
        yearstr = "2016postVFP"
    else:
        yearstr = year
    model_name = f"{BDTname}_{yearstr}"
    score_name = f"score_{model_name}_nominal"
    #paths = glob.glob(f"/depot/cms/hmm/coffea/{year}_2022apr6/{dataset}/*.parquet")
    paths = glob.glob(f"/depot/cms/hmm/vscheure/{label}/stage1_output/{yearstr}/{dataset}/*.parquet")

    df = load_dataframe(None, parameters, inputs=paths, dataset=dataset)
    df = df.compute()
    df.jet1_has_matched_gen_nominal.fillna(False, inplace=True)
    df.jet2_has_matched_gen_nominal.fillna(False, inplace=True)
    df.fillna(-99.0, inplace=True)
    split_into_channels(df, v="nominal", ggHsplit=False)
    print(df)
    df.loc[df[f"channel_nominal"] == channel, score_name] = evaluate_bdt(
        df[df[f"channel_nominal"] == channel],
        "nominal",
        model_name,
        parameters,
        score_name,
    )
    #print(df.loc[df[f"channel_nominal"] == channel, score_name].describe())
    #import numpy as np
    #df["new"] = df[score_name].apply(np.tanh)
    #for i in range(4):
    #    print(df.loc[(df[f"channel_nominal"] == channel)&(df.event.mod(4)==i), score_name].value_counts())
    #print(df.loc[(df[f"channel_nominal"] == channel)&(df[score_name]>2.0421700477600098), "wgt_nominal"].sum())
    #print(df.loc[(df[f"channel_nominal"] == channel)&(df[score_name]>2.1076695919036865), "wgt_nominal"].sum())

    """
    df.loc[df[f"channel_nominal"] == channel, score_name] = evaluate_pytorch_dnn_pisa(
        df[df[f"channel_nominal"] == channel],
        "nominal",
        model_name,
        parameters,
        score_name,
        channel,
    )
    """

    categorize_dnn_output_ggh(df, score_name, channel, region, str(year),yearstr)


