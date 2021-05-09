# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:23:30 2021

Script to train simpletransformer model

@author: Abinaya Mahendiran
"""


# Import necessary libraries
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from simpletransformers.classification import ClassificationModel
from scripts.config import logger
from scripts import config
from sklearn.metrics import accuracy_score

class NewsClassification():

    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.model_type = config.MODEL_TYPE
        self.train_data = pd.read_csv(Path(config.DATA_DIR, "train.csv"))
        self.test_data = pd.read_csv(Path(config.DATA_DIR, "test.csv"))
        self.cuda = torch.cuda.is_available()
        self.model_args = config.MODEL_ARGS
        self.labels = config.LABELS

    def preprocess_data(self, data: object, column_name: str) -> object:
        """
        Perform preprocessing on the text data

        Parameters
        ----------
        data : object
            dataframe.
        column_name : str
            name of the column in the dataframe

        Returns
        -------
        object
            pre-processed dataframe.

        """
        if column_name == 'text':
            data[column_name] = data[column_name].str.lower()
        if column_name == 'label':
            data[column_name] =  data[column_name].apply(int) - 1
        data.rename(columns={'label': 'labels'}, inplace = True)
        logger.info(str(data.columns))
        return data

    def split_data(self, data: object, random_seed: int) -> (object, object):
        """
        Split the dataset into train and eval

        Parameters
        ----------
        data : object
            dataframe containing training data.
        random_seed : int
            integer to set the random seed

        Returns
        -------
        (object, object)
            train split, eval split.

        """
        np.random.seed(random_seed)
        train_idx = np.random.choice(data.index,
                size=int(data.shape[0]*config.TEST_SPLIT), replace=False)
        valid_idx = set(data.index) - set(train_idx)

        train_data = data[data.index.isin(train_idx)]
        eval_data = data[data.index.isin(valid_idx)]
        return(train_data, eval_data)

    def train(self, train_data: object, eval_data: object) -> object:
        """
        Create and train the chosen model based on the args

        Parameters
        ----------
        train_data : object
            train split of the train_data.
        eval_data : object
            validation split of the train_data.

        Returns
        -------
        object
            model.

        """

        # Create a ClassificationModel
        model = ClassificationModel(self.model_name,
                                    self.model_type,
                                    args = self.model_args,
                                    use_cuda = self.cuda,
                                    num_labels = len(self.labels) - 1)
        # Train the model
        model.train_model(train_df = train_data,
                          eval_df = eval_data,
                          accuracy = accuracy_score)
        return model

    def load_model(self, model_type: str) -> object:
        """
        Load the specified model

        Parameters
        ----------
        model_type : str
            path or model type to be loaded.

        Returns
        -------
        object
            model.

        """
        model = ClassificationModel(self.model_name,
                                    model_type,
                                    args = self.model_args,
                                    use_cuda = self.cuda,
                                    num_labels = len(self.labels) - 1)
        return model

def main():
    """
    Run the news classification model

    Returns
    -------
    None.

    """
    # Create classification object
    news_model = NewsClassification()
    logger.info("News classification model instantiated")

    # Preprocess and split data
    data = news_model.preprocess_data(news_model.train_data, "text")
    logger.info("Datat is pre-processed")
    train_data, eval_data = news_model.split_data(data, config.RANDOM_SEED)
    logger.info("Data is split")

    # Train model
    train_model = news_model.train(train_data, eval_data)
    logger.info("Model is trained")

    # Load model
    loaded_model = news_model.load_model(config.BEST_MODEL_SPEC_DIR)
    logger.info("Model is loaded")

    # Eval model
    model_result, model_outputs, wrong_predictions = loaded_model.eval_model(eval_data,
                                                                     accuracy =
                                                                     accuracy_score)

    # Prediction
    predictions, raw_outputs = loaded_model.predict(news_model.test_data)
    

if __name__ == '__main__':
    main()
