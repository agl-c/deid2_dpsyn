# this file includes the paths of several important files
from pathlib import Path

ROOT_DIRECTORY = Path("./")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
CONFIG_DIRECTORY = ROOT_DIRECTORY / "config"
PICKLE_DIRECTORY = DATA_DIRECTORY / "pkl"

# SUBMISSION_FORMAT = DATA_DIRECTORY / "submission_format.csv"
# INPUT = DATA_DIRECTORY / "ground_truth.csv"
# PUBLIC_INPUT = DATA_DIRECTORY / "ground_truth.csv"
# PUB_PKL = PICKLE_DIRECTORY / "preprocessed_ground_truth.pkl"
# PRIV_PKL = PICKLE_DIRECTORY / "preprocessed_private.pkl"
# PUB_MAR_PKL = PICKLE_DIRECTORY / "pub_marginals.csv"
# PRIV_MAR_PKL = PICKLE_DIRECTORY / "priv_marginals.csv"
PARAMS = DATA_DIRECTORY / "parameters1.json"
DATA_TYPE = DATA_DIRECTORY / "column_datatypes.json"
CONFIG_DATA = CONFIG_DIRECTORY / "data.yaml"
MARGINAL_CONFIG = CONFIG_DIRECTORY / "eps=10.0.yaml"


# OUTPUT = ROOT_DIRECTORY / "submission.csv"
