""" Data creation for Active Learning
From original training data, get
i. training data: random sample of 20% of the original training data
ii. validation data: random sample of 10% of the original training data or 12.5% of data remaining after getting training data
iii. data for annotation: 70% of the data
"""

import json
import os

import numpy as np
import pandas as pd

# import logging
# import datetime

__author__ = "Pawan Kumar Singh"


def prepare_data(file_path, file_name, out_file_name):
    """Simple function to
       i. Read in data
       ii. change title and description to lower case
       iii. concatenate title and description to create text
       iv. add index[summary]

    Parameters
    ----------
    file_path : [type]
        [description]
    file_name : [type]
        [description]
    out_file_name : [type]
        [description]
    """
    data = pd.read_csv(os.path.join(file_path, file_name), index_col=False)
    data["Title"] = data["Title"].str.lower()
    data["Description"] = data["Description"].str.lower()
    data["text"] = data["Title"] + " " + data["Description"]
    data["labels"] = data["Class Index"]
    data.drop("Class Index", axis=1, inplace=True)

    data["id"] = data.index
    if "gz" not in out_file_name:
        out_file_name += ".gz"
    print(out_file_name)
    data.to_csv(os.path.join(file_path, out_file_name), index=False, compression="gzip")


def split_data(
    file_path,
    train_file_name,
    test_file_name,
    train_size=0.2,
    valid_size=0.1,
    random_seed=100,
):
    """Split original training data into training data and annotation data and
       save them in `train` and `annotation` directory in `file_path`

    Parameters
    ----------
    file_path : [type]
        [description]
    train_file_name : [type]
        [description]
    test_file_name : [type]
        [description]
    train_size : float, optional
        [description], by default 0.2
    valid_size : float, optional
        [description], by default 0.1
    random_seed : int, optional
        [description], by default 100
    """
    data = pd.read_csv(os.path.join(file_path, train_file_name), index_col=False)
    test_data = pd.read_csv(os.path.join(file_path, test_file_name), index_col=False)
    train_size = int(data.shape[0] * train_size)
    valid_size = int(data.shape[0] * valid_size)
    np.random.seed(100)
    all_idx = data["id"]
    train_idx = np.random.choice(all_idx, size=train_size, replace=False)
    remain_idx = list(set(all_idx.tolist()) - set(train_idx.tolist()))
    valid_idx = np.random.choice(remain_idx, size=valid_size, replace=False)
    annotate_idx = list(set(remain_idx) - set(valid_idx))

    data_track_dict = {}
    data_track_dict["train_idx"] = train_idx.tolist()
    data_track_dict["valid_idx"] = valid_idx.tolist()
    data_track_dict["annotate_idx"] = annotate_idx

    check_and_create_dir(".data_tracking")
    print(data_track_dict.keys())
    with open(os.path.join(".data_tracking", "data_info.txt"), "w") as outfile:
        json.dump(data_track_dict, outfile, indent=4)
    # json.dumps(data_track_dict, ".data_tracking")

    train_data = data[data["id"].isin(train_idx)]
    valid_data = data[data["id"].isin(valid_idx)]
    annotate_data = data[data["id"].isin(annotate_idx)]
    annotate_data.drop("labels", axis=1, inplace=True)

    print(f"Size of train data {train_data.shape[0] / data.shape[0]}")
    print(f"Size of valid data {valid_data.shape[0] / data.shape[0]}")
    print(f"Size of annotate data {annotate_data.shape[0] / data.shape[0]}")

    check_and_create_dir("train_data")
    write_csv(train_data, "train_data", "train.csv")
    check_and_create_dir("test_data")
    write_csv(test_data, "test_data", "test.csv")
    check_and_create_dir("annotate_data")
    write_csv(annotate_data, "annotate_data", "annotate.csv")
    check_and_create_dir("valid_data")
    write_csv(valid_data, "valid_data", "valid.csv")


def write_csv(data, out_path, file_name):
    if "gz" not in file_name:
        file_name += ".gz"
    data.to_csv(os.path.join(out_path, file_name))


def check_and_create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
