# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:23:30 2021

Script to train a transformer model on ag_news dataset

@author: Abinaya Mahendiran
"""


# Import necessary libraries
import pandas as pd
from datasets import load_dataset


# Load data and convert it to dataframe
def load_data(dataset_name : str) -> object:
    """
    Load the data from datasets library and convert to dataframe

    Parameters
    ----------
    dataset_name : str
        name of the dataset to be downloaded.

    Returns
    -------
    object
        dataframe.

    """
    data = load_dataset(dataset_name)
    return data
