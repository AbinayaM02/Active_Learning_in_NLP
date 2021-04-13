from numpy.core.defchararray import index
from numpy.core.numeric import full
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
import argparse
import ipdb

# annotatation_data = "annotate_data/annotate.csv.gz"
# data_info = ".data_tracking/data_info.txt"


def get_annotate_idx(size=100, type="random"):
    with open(data_info) as in_file:
        annotate_idx = json.load(in_file)["annotate_idx"]
    return np.random.choice(annotate_idx, size=size, replace=False)


def random_sampling(
    raw_data: pd.DataFrame, annotate_data: pd.DataFrame = None, size: int = 1000
):
    ipdb.set_trace()
    all_idx = raw_data["idx"].values.tolist()
    if annotate_data is not None:
        annotated_idx = annotate_data["idx"].values.tolist()
        all_idx = list(set(all_idx) - set(annotated_idx))
    idx = np.random.choice(all_idx, size=size, replace=False)
    return idx


def least_confidence_sampling(
    raw_data: pd.DataFrame, annotate_data: pd.DataFrame = None, size: int = 1000
):
    raw_data = raw_data.copy()
    if annotate_data is not None:
        raw_data = raw_data[~(raw_data.idx.isin(annotate_data.idx))]
    raw_data.sort_values("max_prob", inplace=True)
    return raw_data.head(size).idx.values


def margin_sampling(
    raw_data: pd.DataFrame, annotate_data: pd.DataFrame = None, size: int = 1000
):
    raw_data = raw_data.copy()
    if annotate_data is not None:
        raw_data = raw_data[~(raw_data.idx.isin(annotate_data.idx))]
    prob_cols = ["prob_0", "prob_1", "prob_2", "prob_3"]
    prob_sorted = np.sort(raw_data[prob_cols], axis=1)
    margin = prob_sorted[:, -1] - prob_sorted[:, -2]
    raw_data["margin"] = margin
    raw_data.sort_values("margin", ascending=True, inplace=True)
    return raw_data.head(size).idx.values


def entropy_sampling(
    raw_data: pd.DataFrame, annotate_data: pd.DataFrame = None, size: int = 1000
):
    raw_data = raw_data.copy()
    if annotate_data is not None:
        raw_data = raw_data[~(raw_data.idx.isin(annotate_data.idx))]

    prob_cols = ["prob_0", "prob_1", "prob_2", "prob_3"]
    raw_data["entropy"] = -1 * np.sum(
        raw_data[prob_cols] * np.log(raw_data[prob_cols]), axis=1
    )
    raw_data.sort_values("entropy", ascending=False, inplace=True)
    return raw_data.head(size).idx


def annotation_message():
    annotation_instruction = (
        "Please provide input as per the instruction given in box to annotate \n"
    )
    annotation_instruction += "-----------------------------\n"
    annotation_instruction += "| 1: World News             | \n"
    annotation_instruction += "| 2: Sports                 |\n"
    annotation_instruction += "| 3: Business               |\n"
    annotation_instruction += "| 4: Sci/Tech               |\n"
    annotation_instruction += "| 0: Not Sure               |\n"
    annotation_instruction += "-----------------------------\n"
    annotation_instruction += "save: to save the results\n"
    annotation_instruction += "-----------------------------\n"

    full_instruction = annotation_instruction
    full_instruction += (
        "Please provide input as per the instruction given in box to see examples \n"
    )
    full_instruction += "----------------------------------------\n"
    full_instruction += "| b: go back to last text              |\n"
    full_instruction += "| w: World News examples               |\n"
    full_instruction += "| s: Sports News examples              |\n"
    full_instruction += "| b: Business News examples            |\n"
    full_instruction += "| t: Science/ Technology News examples |\n"
    full_instruction += "| f: full instruction                  |\n"
    full_instruction += "----------------------------------------\n"

    return full_instruction, annotation_instruction


def get_examples(exp_data, label=0):
    label_data = exp_data[exp_data["label"] == label]
    return label_data.head(1)


def get_annotation(data, exp_data):
    label_map = {"w": 0, "s": 1, "b": 2, "t": 3}
    label_desc_map = {
        "w": "World News examples",
        "s": "Sports News examples",
        "b": "Business News example",
        "t": "Science/Tech example",
    }
    data.reset_index(drop=True, inplace=True)
    data["labels"] = -1
    num_ex = data.shape[0]
    print(f"Number of examples to annotate are {num_ex}")
    full_instruction, annotation_instruction = annotation_message()
    print(full_instruction)
    ind = 0
    while ind < num_ex:
        if ind < 0:
            ind = 0

        textId = data.loc[ind, "idx"]
        title = data.loc[ind, "title"]
        description = data.loc[ind, "description"]

        print(annotation_instruction)
        print("*" * 80)
        print(f"{ind + 1}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        label = str(input("> "))
        if label in ["0", "1", "2", "3", "4"]:
            data.loc[ind, "labels"] = int(label) - 1
            ind += 1
        elif label == "b":
            ind -= 1
        elif label in ["w", "s", "b", "t"]:
            exp = get_examples(exp_data, label_map.get(label, 0))
            print(label_desc_map.get(label, "w"))
            print(f"\n Title: {exp['Title'].values[0]}")
            print(f"\n Description: {exp['Description'].values[0]}")
        elif label == "f":
            print(full_instruction)
        elif label == "save":
            print("saving all data and exiting")
            return data


def main():
    parser = argparse.ArgumentParser(
        description="Annotate data using uncertainty sampling methods"
    )
    parser.add_argument("annotation_data", help="data to be annotated")
    parser.add_argument(
        "sampling_method",
        default="random",
        help="method to use to sample data for annotation, options are `random`, `least`, `margin`, `entropy`",
    )
    parser.add_argument(
        "sample_size", default=100, help="Number of samples to be annotated"
    )
    parser.add_argument("output_location", help="location to write annotated data")
    parser.add_argument(
        "--annotated_data", help="path to the data which has already been annotated"
    )
    parser.add_argument(
        "--example_data", help="data from which we pick example for each class"
    )
    args = parser.parse_args()
    annotation_data_path = args.annotation_data
    sampling_method = args.sampling_method
    sample_size = int(args.sample_size)
    output_location = args.output_location
    annotated_data_path = args.annotated_data
    example_data_path = args.example_data
    if example_data_path is None:
        example_data_path = "../../data/exp_data.csv.gz"

    annotation_data = pd.read_csv(annotation_data_path, index_col=False)
    if annotated_data_path is not None:
        annotated_data = pd.read_csv(annotated_data_path)
    else:
        annotated_data = None
    exp_data = pd.read_csv(example_data_path)
    sampling_method_map = {
        "random": random_sampling,
        "least": least_confidence_sampling,
        "margin": margin_sampling,
        "entropy": entropy_sampling,
    }
    if sampling_method not in list(sampling_method_map.keys()):
        raise ValueError(
            "Sampling method has to be one of `random`, `least`, `margin`, `entropy` "
        )
    sample_idx = sampling_method_map[sampling_method](
        annotation_data, annotated_data, size=sample_size
    )

    data = annotation_data[annotation_data["idx"].isin(sample_idx)]

    annotated_data_1 = get_annotation(data, exp_data)
    if not os.path.exists(output_location):
        os.mkdir(
            output_location,
        )
    today = datetime.today().strftime("%Y%m%d")
    out_file = os.path.join(
        output_location, f"annotated_data_{sampling_method}_{today}.csv.gz"
    )
    annotated_data_1.to_csv(out_file, index=False, compression="gzip")


if __name__ == "__main__":
    main()