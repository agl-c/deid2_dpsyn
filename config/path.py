# this file includes the paths of several important files
from pathlib import Path

ROOT_DIRECTORY = Path("./")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
CONFIG_DIRECTORY = ROOT_DIRECTORY / "config"
PICKLE_DIRECTORY = DATA_DIRECTORY / "pkl"

# PRIV_DATA is the path for the original dataset
PRIV_DATA = DATA_DIRECTORY / "accidential_drug_deaths.csv"
# save the name for use when naming synthesized files
PRIV_DATA_NAME = "accidential_drug_deaths"

# data.yaml defines some config settings, including identifier and bin...
CONFIG_DATA = CONFIG_DIRECTORY / "data.yaml"

# below two file include some schema of the dataset
PARAMS = DATA_DIRECTORY / "parameters1.json"
DATA_TYPE = DATA_DIRECTORY / "column_datatypes.json"

# MARGINAL_CONFIG currently defines the method of marginal selection to be priv_all_two_way
# which means the algorithm will generate records using all the two-way marginals  
MARGINAL_CONFIG = CONFIG_DIRECTORY / "eps=10.0.yaml"



# below is unused
# SUBMISSION_FORMAT = DATA_DIRECTORY / "submission_format.csv"
# INPUT = DATA_DIRECTORY / "ground_truth.csv"
# PUBLIC_INPUT = DATA_DIRECTORY / "ground_truth.csv"
# PUB_PKL = PICKLE_DIRECTORY / "preprocessed_ground_truth.pkl"
# PRIV_PKL = PICKLE_DIRECTORY / "preprocessed_private.pkl"
# PUB_MAR_PKL = PICKLE_DIRECTORY / "pub_marginals.csv"
# PRIV_MAR_PKL = PICKLE_DIRECTORY / "priv_marginals.csv"
# OUTPUT = ROOT_DIRECTORY / "submission.csv"