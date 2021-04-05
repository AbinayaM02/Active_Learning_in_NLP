import pandas as pd
import numpy as np
import os
import datetime
import json

annotatation_data = "annotate_data/annotate.csv.gz"
data_info = ".data_tracking/data_info.txt"


def get_annotate_idx(size=100, type="random"):
    with open(data_info) as in_file:
        annotate_idx = json.load(in_file)["annotate_idx"]
    return np.random.choice(annotate_idx, size=size, replace=False)


annotation_insrtuction = "Please type, "
annotation_insrtuction += (
    "1 for World News, 2 for Sports, 3 for Business and 4 for Sci/Tech. "
)
annotation_insrtuction += "Type b to fo to back to last message. "
annotation_insrtuction += "Type w to get World News examples. "
annotation_insrtuction += "Type s to get Sports News examples. "
annotation_insrtuction += "Type b to get Business News examples. "
annotation_insrtuction += "Type t to get Science/ Technology News examples. "
annotation_insrtuction += "Type save to save the results"

train_data = pd.read_csv("train_data/train.csv.gz", index_col=False)


def get_annotation(data):
    data.reset_index(drop=True, inplace=True)
    data["labels"] = -1
    num_ex = data.shape[0]
    print(f"Number of examples to annotate are {num_ex}")

    ind = 0
    while ind < num_ex:
        if ind < 0:
            ind = 0

        textId = data.loc[ind, "id"]
        title = data.loc[ind, "Title"]
        description = data.loc[ind, "Description"]

        print(annotation_insrtuction)
        print("*" * 80)
        print(f"{ind + 1}")
        print(f"Title: \n {title}")
        print(f"Description: \n {description}")
        label = str(input("> "))
        if label in ["1", "2", "3", "4"]:
            data.loc[ind, "labels"] = label
        ind += 1
    data.to_csv("annotate_data/annotation_v1.csv.gz", index=False)


annotation_size = 5
annotation_idx = get_annotate_idx(annotation_size)
annotation_df = pd.read_csv(annotatation_data, index_col=False)
annotation_df = annotation_df[annotation_df["id"].isin(annotation_idx)]

get_annotation(annotation_df)
