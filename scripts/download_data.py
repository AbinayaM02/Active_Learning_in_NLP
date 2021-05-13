# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:23:30 2021

Script to download ag_news dataset

@author: Abinaya Mahendiran
"""

from pathlib import Path

# Import necessary libraries
from datasets import load_dataset

from config import DATA_DIR, logger


# Load data and convert it to dataframe
def load_data(dataset_name: str, split: str) -> object:
    """
    Load the data from datasets library and convert to dataframe

    Parameters
    ----------
    dataset_name : str
        name of the dataset to be downloaded.
    split : str
        type of split (train or test).
    Returns
    -------
    object
        dataframe.

    """
    data = load_dataset(dataset_name, split=split)
    logger.info(split + " dataset downloaded!")
    return data


# Save teh data locally
def save_data(path: str, dataframe: object) -> None:
    """
    Save the dataframe to a local folder

    Parameters
    ----------
    path : str
        path of the folder.
    dataframe : object
        dataframe object.

    Returns
    -------
    None
        None.

    """
    dataframe.to_csv(path, index=False)
    logger.info("dataset saved!")


if __name__ == "__main__":
    train_data = load_data("ag_news", "train")
    save_data(Path(DATA_DIR, "train.csv"), train_data)
    test_data = load_data("ag_news", "test")
    save_data(Path(DATA_DIR, "test.csv"), test_data)
