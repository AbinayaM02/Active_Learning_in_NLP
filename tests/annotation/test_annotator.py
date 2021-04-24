import os
import sys

import numpy as np
import pandas as pd
import pytest

from scripts.annotator import (  # random_sampling,
    entropy_sampling,
    least_confidence_sampling,
    margin_sampling,
)

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


@pytest.fixture
def test_data():
    return pd.DataFrame(
        {
            "idx": [1, 2, 3],
            "prob_0": [0.1, 0, 0.25],
            "prob_1": [0.2, 0.1, 0.25],
            "prob_2": [0.2, 0.1, 0.25],
            "prob_3": [0.5, 0.8, 0.25],
            "max_prob": [0.5, 0.6, 0.2],
            "annotated_labels": [np.nan, np.nan, np.nan],
        }
    )


def test_least_confidence_sampling(test_data):
    actual_idx = least_confidence_sampling(test_data, 1)
    expected_idx = 3
    assert expected_idx == actual_idx


def test_margin_sampling(test_data):
    actual_idx = margin_sampling(test_data, 2)
    expected_idx = np.array([3, 1])
    assert (expected_idx == actual_idx).all()


def test_entropy_sampling(test_data):
    actual_idx = entropy_sampling(test_data, 1)
    expected_idx = 3
    assert expected_idx == actual_idx
