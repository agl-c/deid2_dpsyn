from pathlib import Path

ROOT_DIRECTORY = Path("./")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
CONFIG_DIRECTORY = ROOT_DIRECTORY / "config"
PICKLE_DIRECTORY = DATA_DIRECTORY / "pkl"

SUBMISSION_FORMAT = DATA_DIRECTORY / "submission_format.csv"
INPUT = DATA_DIRECTORY / "ground_truth.csv"
PUBLIC_INPUT = DATA_DIRECTORY / "ground_truth.csv"
# PUB_PKL = PICKLE_DIRECTORY / "preprocessed_ground_truth.pkl"
# PRIV_PKL = PICKLE_DIRECTORY / "preprocessed_private.pkl"
# PUB_MAR_PKL = PICKLE_DIRECTORY / "pub_marginals.csv"
# PRIV_MAR_PKL = PICKLE_DIRECTORY / "priv_marginals.csv"
PARAMS = DATA_DIRECTORY / "parameters.json"
CONFIG_DATA = CONFIG_DIRECTORY / "data.yaml"
# CONFIG_DATA = CONFIG_DIRECTORY / "data_no_encode.yaml"
OUTPUT = ROOT_DIRECTORY / "submission.csv"

DETAILED_SCORES_DIR = ROOT_DIRECTORY / "detail_scores"
