# from datetime import datetime
import argparse
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

from scripts.config import DATA_DIR

warnings.filterwarnings("ignore")


def get_sampling_method_map():
    return {
        "random": random_sampling,
        "least": least_confidence_sampling,
        "margin": margin_sampling,
        "entropy": entropy_sampling,
    }


def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def random_sampling(raw_data: pd.DataFrame, size: int = 1000, random_seed=100):
    raw_data = raw_data[raw_data["annotated_labels"].isna()].copy()
    all_idx = raw_data["idx"].values.tolist()
    np.random.seed(random_seed)
    idx = np.random.choice(all_idx, size=size, replace=False)
    return idx


def least_confidence_sampling(raw_data: pd.DataFrame, size: int = 1000):
    raw_data = raw_data.copy()
    raw_data = raw_data[raw_data["annotated_labels"].isna()].copy()
    raw_data.sort_values("max_prob", inplace=True)
    return raw_data.head(size).idx.values


def margin_sampling(raw_data: pd.DataFrame, size: int = 1000):
    raw_data = raw_data[raw_data["annotated_labels"].isna()].copy()

    prob_cols = ["prob_0", "prob_1", "prob_2", "prob_3"]
    prob_sorted = np.sort(raw_data[prob_cols], axis=1)
    margin = prob_sorted[:, -1] - prob_sorted[:, -2]
    raw_data["margin"] = margin
    raw_data.sort_values("margin", ascending=True, inplace=True)
    return raw_data.head(size).idx.values


def entropy_sampling(raw_data: pd.DataFrame, size: int = 1000):
    raw_data = raw_data[raw_data["annotated_labels"].isna()].copy()

    prob_cols = ["prob_0", "prob_1", "prob_2", "prob_3"]
    raw_data["entropy"] = -1 * np.sum(raw_data[prob_cols] * np.log(raw_data[prob_cols]), axis=1)
    raw_data.sort_values("entropy", ascending=False, inplace=True)
    return raw_data.head(size).idx.values


def annotation_message():
    annotation_instruction = (
        "Please provide input as per the instruction given in box to annotate \n"
    )
    annotation_instruction += "---------------------------------------\n"
    annotation_instruction += "| 1: World News                        |\n"
    annotation_instruction += "| 2: Sports                            |\n"
    annotation_instruction += "| 3: Business                          |\n"
    annotation_instruction += "| 4: Sci/Tech                          |\n"
    annotation_instruction += "| 0: Not Sure                          |\n"
    annotation_instruction += "---------------------------------------\n"
    annotation_instruction += "| save: to save the results            |\n"
    annotation_instruction += "| f: full instruction                  |\n"
    annotation_instruction += "| u: go back to last text (undo)       |\n"
    annotation_instruction += "---------------------------------------\n"

    full_instruction = "Please provide input as per the instruction given in box to see examples \n"
    full_instruction += "---------------------------------------------\n"
    full_instruction += "| u: go back to last text (undo)             |\n"
    full_instruction += "| w: World News examples                     |\n"
    full_instruction += "| s: Sports News examples                    |\n"
    full_instruction += "| b: Business News examples                  |\n"
    full_instruction += "| t: Science/ Technology News examples       |\n"
    full_instruction += "| f: full instruction                        |\n"
    full_instruction += "---------------------------------------------\n"
    full_instruction += annotation_instruction

    return full_instruction, annotation_instruction


def get_examples(exp_data, label=0):
    label_data = exp_data[exp_data["labels"] == label]
    return label_data.head(1)


def get_data(annotation_data_path, sampling_method, sample_size):

    df_for_annotation = pd.read_csv(annotation_data_path, index_col=False)
    df_for_annotation["sampling_method"].fillna("", inplace=True)
    sampling_method_in_data = df_for_annotation.sampling_method.unique()
    if len(sampling_method_in_data) > 1:
        if sampling_method not in sampling_method_in_data:
            raise ValueError(
                f"""Warning: data of other sampling {sampling_method_in_data} method is being used, when actual sampling method is {sampling_method}. This might corrupt data"""
            )
    sampling_method_map = get_sampling_method_map()
    sample_idx = sampling_method_map[sampling_method](df_for_annotation, size=sample_size)
    data = df_for_annotation[df_for_annotation["idx"].isin(sample_idx)]
    remaining_data = df_for_annotation[~(df_for_annotation["idx"].isin(sample_idx))]
    return (data, remaining_data)


def get_countdown():

    for i in range(5, 0, -1):
        sys.stdout.write(str(i) + " ")
        sys.stdout.flush()
        time.sleep(1)


def get_annotation(data, exp_data, sample_size):
    label_map = {"w": 0, "s": 1, "b": 2, "t": 3}
    label_desc_map = {
        "w": "World News examples",
        "s": "Sports News examples",
        "b": "Business News example",
        "t": "Science/Tech example",
    }
    data.reset_index(drop=True, inplace=True)
    data["annotated_labels"] = np.nan
    num_ex = data.shape[0]
    clear()
    print(f"Number of examples to annotate are {num_ex}")
    full_instruction, annotation_instruction = annotation_message()
    print(full_instruction)
    input("Press enter to start annotation >")
    clear()
    ind = 0
    while ind < num_ex:
        if ind < 0:
            ind = 0
        if ind > 0:
            clear()
        # textId = data.loc[ind, "idx"]
        title = data.loc[ind, "title"]
        description = data.loc[ind, "description"]

        print(annotation_instruction)
        print("*" * 100)
        print(f"{ind + 1} / {sample_size}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        label = str(input("> "))
        if label in ["0", "1", "2", "3", "4"]:
            data.loc[ind, "annotated_labels"] = int(label) - 1
            ind += 1
        elif label == "u":
            ind -= 1 if ind > 0 else 0
        elif label in ["w", "s", "b", "t"]:
            clear()
            exp = get_examples(exp_data, label_map.get(label, 0))
            print("*" * 100)
            print(label_desc_map.get(label, "w"))
            print(f"\n Title: {exp['Title'].values[0]}")
            print(f"\n Description: {exp['Description'].values[0]}")
            print("*" * 100)
            print("Continue annotation [y/n]")
            instruction = str(input(">"))
            if instruction == "n":
                print("saving all data and exiting in")
                get_countdown()
                clear()
                # time.sleep(10)
                return data
            elif instruction == "y":
                print("continuing in")
                get_countdown()
                clear()
                # time.sleep(10)
                continue
            else:
                print("invalid response, continuing annotation in")
                get_countdown()
                clear()
                # time.sleep(10)
        elif label == "f":
            print(full_instruction)
            get_countdown()
            clear()
        elif label == "save":
            print("saving all data and exiting")
            return data
    print("-" * 100)
    print("Done with presentation set of annotation")
    return data


def main():
    parser = argparse.ArgumentParser(description="Annotate data using uncertainty sampling methods")
    parser.add_argument("annotation_data", help="data to be annotated")
    parser.add_argument(
        "sampling_method",
        default="random",
        help="method to use to sample data for annotation, options are `random`, `least`, `margin`, `entropy`",
    )
    parser.add_argument("sample_size", default=100, help="Number of samples to be annotated")
    parser.add_argument("output_location", help="location to write annotated data")
    parser.add_argument("--example_data", help="data from which we pick example for each class")
    args = parser.parse_args()
    annotation_data_path = args.annotation_data
    sampling_method = args.sampling_method
    sample_size = int(args.sample_size)
    output_location = args.output_location
    example_data_path = args.example_data
    if example_data_path is None:
        example_data_path = DATA_DIR / "exp_data.csv.gz"

    df_for_annotation = pd.read_csv(annotation_data_path, index_col=False)
    df_for_annotation["sampling_method"].fillna("", inplace=True)
    sampling_method_in_data = df_for_annotation.sampling_method.unique()
    if len(sampling_method_in_data) > 1:
        if sampling_method not in sampling_method_in_data:
            raise ValueError(
                f"""Warning: data of other sampling {sampling_method_in_data} method is being used, when actual sampling method is {sampling_method}. This might corrupt data"""
            )

    exp_data = pd.read_csv(example_data_path)
    sampling_method_map = {
        "random": random_sampling,
        "least": least_confidence_sampling,
        "margin": margin_sampling,
        "entropy": entropy_sampling,
    }
    if sampling_method not in list(sampling_method_map.keys()):
        raise ValueError("Sampling method has to be one of `random`, `least`, `margin`, `entropy` ")
    sample_idx = sampling_method_map[sampling_method](df_for_annotation, size=sample_size)

    data = df_for_annotation[df_for_annotation["idx"].isin(sample_idx)]
    reamining_data = df_for_annotation[~(df_for_annotation["idx"].isin(sample_idx))]

    annotated_data = get_annotation(data, exp_data, sample_size)
    if not os.path.exists(output_location):
        os.mkdir(
            output_location,
        )
    annotated_data.loc[
        ~(annotated_data["annotated_labels"].isna()), "sampling_method"
    ] = sampling_method
    tot_annotated = annotated_data[~(annotated_data.annotated_labels.isna())].shape[0]
    clear()
    print(f"Total annotation required {sample_size}, total annotated {tot_annotated}")
    annotated_data = pd.concat((annotated_data, reamining_data), axis=0)
    # today = datetime.today().strftime("%Y%m%d")
    out_file = os.path.join(output_location, f"annotated_data_{sampling_method}.csv.gz")
    print(f"Writing file to {out_file}")
    annotated_data.to_csv(out_file, index=False, compression="gzip")


if __name__ == "__main__":
    main()
