# pylint: disable = W0614, W0401, C0411
# the above errcodes correspond to unused wildcard import, wildcard import, wrong-import-order
# In fact, we can run pylint in cmd and set options like: pylint --disable=Cxxxx,Wxxxx yyyy.py zzzz.py
import argparse
import copy

# import these when debuggging
from pathlib import Path
from loguru import logger
from data.DataLoader import *
from data.RecordPostprocessor import RecordPostprocessor
from method.dpsyn import DPSyn
# TODO: later we remove below two modules which serve no use for dpsyn 
# from method.sample_parallel import Sample
# from method.direct_sample import DirectSample
# from metric import *
# from detailed_metric import *
import numpy as np


def main():
    np.random.seed(0)
    np.random.RandomState(0)
    # by default, args.config is ./config/data.yaml, you may change it by typing --config=.....
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    print("------> load config, priv data", config['priv_dataset_path'])

    # dataloader initialization
    dataloader = DataLoader()
    dataloader.load_data()

    # default method is dpsyn
    args.method = 'dpsyn'
    # args.method = 'direct_sample'
    # args.method = 'sample'
    # args.method = 'plain_pub'
    n = 100
    # TODO: what do n and bias_penalty means 
    # bias_penalty_cutoff = 2500000
    # bias_penalty_cutoff = 250

    # check what is bias_penalty_cutoff
    # syn_data = run_method(config, dataloader, n, bias_penalty_cutoff)
    syn_data = run_method(config, dataloader, n)
    syn_data.to_csv(f"{args.method}-{n}-{config['priv_dataset_path']}.csv", index=False)


#def run_method(config, dataloader, n, bias_penalty_cutoff):
def run_method(config, dataloader, n):
    parameters = json.loads(Path(config['parameter_spec']).read_text())
    syn_data = None

    #　each item in 'runs' specify one dp task with (eps, delta, sensitivity) 
    # as well as a possible 'max_records' value which bounds the dataset's size
    for r in parameters["runs"]:
        # replace the below 'max_records_per_individual' with your own design
        # 'max_records_per_individual' is the global sensitivity value of the designed function f
        #  here in the example f is the count, and you may change as you like
        eps, delta, sensitivity = r['epsilon'], r['delta'], r['max_records_per_individual']
        # we import logger in synthesizer.py
        # we import DPSyn which inderitats synthesizer 
        # and I'm not sure whether it will import synthesizer.py too
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
            """I guess it help by displaying the runtime logic below
            1. DPSyn(Synthesizer)
            it got dataloader, eps, delta, sensitivity
            however, Synthesizer is so simple and crude(oh no it initializes the parameters in __init__)
            2. we call synthesizer.synthesize(fixed_n=n) which is written in dpsyn.py(but what fixed_n means?)


            3. look at synthesize then
                def synthesize(self, fixed_n=0) -> pd.DataFrame:
                # def obtain_consistent_marginals(self, priv_marginal_config, priv_split_method) -> Marginals:
                    noisy_marginals = self.obtain_consistent_marginals()
               it call obtain_consistent_marginals without input which introduces bugs
            4. it calls get_noisy_marginals() which is written in synthesizer.py
                # noisy_marginals = self.get_noisy_marginals(priv_marginal_config, priv_split_method)
            5. look at get_noisy_marginals()
                # we firstly generate punctual marginals
                priv_marginal_sets, epss = self.data.generate_marginal_by_config(self.data.private_data, priv_marginal_config)
                # todo: consider fine-tuned noise-adding methods for one-way and two-way respectively?
                # and now we add noises to get noisy marginals
                noisy_marginals = self.anonymize(priv_marginal_sets, epss, priv_split_method)


            6. look at generate_marginal_by_config() which is written in DataLoader.py
               we need config files like (but it seems quite weird?)
               how we manage these?
            e.g.3.
               priv_all_one_way: (or priv_all_two_way)
               total_eps: xxxxx


            7. look at anonymize() which is written in synthesizer.py 
             def anonymize(self, priv_marginal_sets: Dict, epss: Dict, priv_split_method: Dict) -> Marginals:
                noisy_marginals = {}
                for set_key, marginals in priv_marginal_sets.items():
                    eps = epss[set_key]
                # noise_type, noise_param = advanced_composition.get_noise(eps, self.delta, self.sensitivity, len(marginals))
                    noise_type = priv_split_method[set_key]
            actually, priv_split_method seems to be hard_coded in config files here 
            and in old code we tried to decide the noise type by advanced_compisition()?
            and I wonder which decision method to take?
            
            """
            # we will use dpsyn to generate a dataset 
            synthesizer = DPSyn(dataloader, eps, delta, sensitivity)
            # what fixed_n means?
            # tmp returns a DataFrame
            # it's a simple function having no relation to puma year things
            
            tmp = synthesizer.synthesize(fixed_n=n)
        else:
            raise NotImplementedError

        tmp['epsilon'] = eps
        # syn_data is a list 
        # tmp is added in the list 
        if syn_data is None:
            syn_data = tmp
        else:
            syn_data = syn_data.append(tmp, ignore_index=True)

    # post-processing generated data
    # map records with grouped/binned attribute back to original attributes
    # TODO: debug in postprocessing but I  doubt whether things have gone wrong in setting fixed_n=0?
    # btw, I　guess the mistake happens because of data structure problems
    postprocessor = RecordPostprocessor()
    syn_data = postprocessor.post_process(syn_data, args.config, dataloader.decode_mapping)
    logger.info("post-processed synthetic data")

    # sorry, but what the following part means
    # TODO: below the 'scorexxxx' functions' names are not found
    # but actually, for synthesis task, we do not resort to these metric functions
    # if n == 0:
    #     # here we encounter the use of bias_penalty_cutoff, but what does it mean?
    #     score_online(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data, parameters_json=Path(config['parameter_spec']), bias_penalty_cutoff=bias_penalty_cutoff)
    # else:
    #     if args.method == 'sample' or 'direct_sample':
    #         puma_year_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)
    #     else:
    #         iteration_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)

    return syn_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    #　we use the argparse 
    # add config file which include paths and so on
    parser.add_argument("--config", type=str, default="./config/data.yaml",
                        help="specify the path of config file in yaml")
    # actually now we only synthesize by dpsyn
    # parser.add_argument("--method", type=str, default='sample',
    #                    help="specify which method to use")

    args = parser.parse_args()
    main()