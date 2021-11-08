# pylint: disable = W0614, W0401, C0411
# the above errcodes correspond to unused wildcard import, wildcard import, wrong-import-order
# In fact, we can run pylint in cmd and set options like: pylint --disable=Cxxxx,Wxxxx yyyy.py zzzz.py
import argparse
from pathlib import Path

import numpy as np
from loguru import logger

parser = argparse.ArgumentParser()

parser.add_argument("--priv_data", type=str, default="./data/accidential_drug_deaths.csv",
                    help="specify the path of original data file in csv format")

parser.add_argument("--priv_data_name", type=str,
                    help="users must specify it to help mid-way naming and avoid possible mistakes")

parser.add_argument("--config", type=str, default="./config/data.yaml",
                    help="specify the path of config file in yaml format")

parser.add_argument("--n", type=int, default=0,
                    help="specify the number of records to generate")

parser.add_argument("--params", type=str, default="./data/parameters.json",
                    help="specify the path of parameters file in json format")

parser.add_argument("--datatype", type=str, default="./data/column_datatypes.json",
                    help="specify the path of datatype file in json format")

parser.add_argument("--marginal_config", type=str, default="./config/eps=10.0.yaml",
                    help="specify the path of marginal config file in yaml format")

parser.add_argument("--update_iterations", type=int, default=30,
                    help="specify the num of update iterations")

parser.add_argument("--target_path", type=str, default="out.csv",
                    help="specify the target path of the synthetic dataset")

args = parser.parse_args()
PRIV_DATA = args.priv_data
PRIV_DATA_NAME = args.priv_data_name
CONFIG_DATA = args.config
PARAMS = args.params
DATA_TYPE = args.datatype
MARGINAL_CONFIG = args.marginal_config
UPDATE_ITERATIONS = args.update_iterations
TARGET_PATH = args.target_path

from data.DataLoader import *
from data.RecordPostprocessor import RecordPostprocessor
from method.dpsyn import DPSyn


def main():
    np.random.seed(0)
    np.random.RandomState(0)
    with open(args.config, 'r', encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    # dataloader initialization
    dataloader = DataLoader()
    dataloader.load_data()

    # default method is dpsyn
    method = 'dpsyn'

    n = args.n
    priv_data = args.priv_data
    priv_data_name = args.priv_data_name

    syn_data = run_method(config, dataloader, n)
    if n != 0:
        print("------------------------> now we synthesize a dataset with ", n, "rows")
        syn_data.to_csv(Path(TARGET_PATH), index=False)
    else:
        syn_data.to_csv(Path(TARGET_PATH), index=False)


def run_method(config, dataloader, n):
    parameters = json.loads(Path(args.params).read_text())
    syn_data = None

    # each item in 'runs' specify one dp task with (eps, delta, sensitivity) 
    # as well as a possible 'max_records' value which bounds the dataset's size
    for r in parameters["runs"]:
        # 'max_records_per_individual' is the global sensitivity value of the designed function f
        #  here in the example f is the count, and you may change as you like
        eps, delta, sensitivity = r['epsilon'], r['delta'], r['max_records_per_individual']

        # we import logger in synthesizer.py
        # we import DPSyn which inherits synthesizer 
        logger.info(f'working on eps={eps}, delta={delta}, and sensitivity={sensitivity}')

        # we will use dpsyn to generate a dataset 
        synthesizer = DPSyn(dataloader, eps, delta, sensitivity)
        # tmp returns a DataFrame
        tmp = synthesizer.synthesize(fixed_n=n)

        # we add in the synthesized dataframe a new column which is 'epsilon'
        # so when do comparison, you should remove this column for consistence
        tmp['epsilon'] = eps

        # syn_data is a list, tmp is added in the list 
        if syn_data is None:
            syn_data = tmp
        else:
            syn_data = syn_data.append(tmp, ignore_index=True)

    # post-processing generated data, map records with grouped/binned attribute back to original attributes
    print("********************* START POSTPROCESSING ***********************")
    postprocessor = RecordPostprocessor()
    syn_data = postprocessor.post_process(syn_data, args.config, dataloader.decode_mapping)
    logger.info("------------------------>synthetic data post-processed:")
    print(syn_data)

    return syn_data


if __name__ == "__main__":
    main()
