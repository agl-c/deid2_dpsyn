import argparse
import copy

from data.DataLoader import *
from data.RecordPostprocessor import RecordPostprocessor
from method.dpsyn import DPSyn
from method.sample_parallel import Sample
from method.direct_sample import DirectSample
from metric import *
from detailed_metric import *
import numpy as np


def main():
    np.random.seed(0)
    np.random.RandomState(0)
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    print("------> load config, priv data", config['priv_dataset_path'])

    # dataloader initialization
    dataloader = DataLoader()
    dataloader.load_data()

    args.method = 'dpsyn'
    # args.method = 'direct_sample'
    # args.method = 'sample'
    # args.method = 'plain_pub'
    n = 0
    # n = 1000
    bias_penalty_cutoff = 2500000
    # bias_penalty_cutoff = 250

    syn_data = run_method(config, dataloader, n, bias_penalty_cutoff)

    syn_data.to_csv(f"{args.method}-{n}-{config['priv_dataset_path']}.csv", index=False)


def run_method(config, dataloader, n, bias_penalty_cutoff):
    parameters = json.loads(Path(config['parameter_spec']).read_text())
    syn_data = None

    for r in parameters["runs"]:
        eps, delta, sensitivity = r['epsilon'], r['delta'], r['max_records_per_individual']
        logger.info(f'working on eps={eps}, delta={delta}, and sensitivity={sensitivity}')
        if args.method == 'plain_pub':
            tmp = copy.deepcopy(dataloader.public_data)
        elif args.method == 'direct_sample':
            synthesizer = DirectSample(dataloader, eps, delta, sensitivity)
            tmp = synthesizer.synthesize(fixed_n=n)
        elif args.method == 'sample':
            synthesizer = Sample(dataloader, eps, delta, sensitivity)
            tmp = synthesizer.synthesize()
        elif args.method == 'dpsyn':
            synthesizer = DPSyn(dataloader, eps, delta, sensitivity)
            tmp = synthesizer.synthesize(fixed_n=n)
        else:
            raise NotImplementedError

        tmp['epsilon'] = eps
        if syn_data is None:
            syn_data = tmp
        else:
            syn_data = syn_data.append(tmp, ignore_index=True)

    # post-processing generated data, map records with grouped/binned attribute back to original attributes
    postprocessor = RecordPostprocessor()
    syn_data = postprocessor.post_process(syn_data, args.config, dataloader.decode_mapping)
    logger.info("post-processed synthetic data")

    if n == 0:
        score_online(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data, parameters_json=Path(config['parameter_spec']), bias_penalty_cutoff=bias_penalty_cutoff)
    else:
        if args.method == 'sample' or 'direct_sample':
            puma_year_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)
        else:
            iteration_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)

    return syn_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, default="./config/data.yaml",
                        help="specify the path of config file in yaml")
    parser.add_argument("--method", type=str, default='sample',
                        help="specify which method to use")

    args = parser.parse_args()
    main()

