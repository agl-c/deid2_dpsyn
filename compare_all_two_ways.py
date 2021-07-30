import copy
import multiprocessing
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from tqdm import tqdm
import os
from data.DataLoader import *
from data.RecordPostprocessor import RecordPostprocessor


import argparse
# this file serves to compare two metric designs, add this comment to test git
COLS = {
    "PUMA": "str",
    "YEAR": "uint32",
    "HHWT": "float",
    "GQ": "uint8",
    "PERWT": "float",
    "SEX": "uint8",
    "AGE": "uint8",
    "MARST": "uint8",
    "RACE": "uint8",
    "HISPAN": "uint8",
    "CITIZEN": "uint8",
    "SPEAKENG": "uint8",
    "HCOVANY": "uint8",
    "HCOVPRIV": "uint8",
    "HINSEMP": "uint8",
    "HINSCAID": "uint8",
    "HINSCARE": "uint8",
    "EDUC": "uint8",
    "EMPSTAT": "uint8",
    "EMPSTATD": "uint8",
    "LABFORCE": "uint8",
    "WRKLSTWK": "uint8",
    "ABSENT": "uint8",
    "LOOKING": "uint8",
    "AVAILBLE": "uint8",
    "WRKRECAL": "uint8",
    "WORKEDYR": "uint8",
    "INCTOT": "int32",
    "INCWAGE": "int32",
    "INCWELFR": "int32",
    "INCINVST": "int32",
    "INCEARN": "int32",
    "POVERTY": "uint32",
    "DEPARTS": "uint32",
    "ARRIVES": "uint32",
}

BINS = {
    "AGE": np.r_[-np.inf, np.arange(20, 105, 5), np.inf],
    "INCTOT": np.r_[-np.inf, np.arange(0, 105_000, 5_000), np.inf],
    "INCWAGE": np.r_[-np.inf, np.arange(0, 105_000, 5_000), np.inf],
    "INCWELFR": np.r_[-np.inf, np.arange(0, 105_000, 5_000), np.inf],
    "INCINVST": np.r_[-np.inf, np.arange(0, 105_000, 5_000), np.inf],
    "INCEARN": np.r_[-np.inf, np.arange(0, 105_000, 5_000), np.inf],
    "POVERTY": np.r_[-np.inf, np.arange(0, 520, 20), np.inf],
    "HHWT": np.r_[-np.inf, np.arange(0, 520, 20), np.inf],
    "PERWT": np.r_[-np.inf, np.arange(0, 520, 20), np.inf],
    "DEPARTS": np.r_[-np.inf, [h * 100 + m for h in range(24) for m in (0, 15, 30, 45)], np.inf],
    "ARRIVES": np.r_[-np.inf, [h * 100 + m for h in range(24) for m in (0, 15, 30, 45)], np.inf],
}


def _apply_metric(counts):
    if counts.shape[1] < 2:
        return 2.0
    sums = counts.sum(axis=0)
    if np.min(sums) < 1:
        return 2.0
    return (counts / sums).diff(axis=1).sum(axis=1).abs().sum()


def compare(grouped):
    grouped_ground_truth, grouped_data, cols = grouped
    # print("--->", cols)
    # pd.set_option('display.max_rows', None)
    ground_truth = grouped_ground_truth.size().to_frame('ground_count')
    ground_truth_PUMA_YEAR_sum = ground_truth.groupby(['PUMA', 'YEAR']).agg(puma_year_sum=('ground_count', 'sum'))
    ground_truth = pd.merge(ground_truth.reset_index(), ground_truth_PUMA_YEAR_sum.reset_index(),
                            on=['PUMA', 'YEAR'], how="left").set_index(['PUMA', 'YEAR'] + cols)
    ground_truth['ground_count'] /= ground_truth['puma_year_sum']

    syn_data = grouped_data.size().to_frame('syn_count')
    syn_data /= np.sum(syn_data.values)
    # force to have the same type
    type1, type2 = ground_truth.index.get_level_values(2).dtype, ground_truth.index.get_level_values(3).dtype
    a = syn_data.index.get_level_values(0).astype(type1)
    b = syn_data.index.get_level_values(1).astype(type2)
    syn_data.index = [a, b]
    # print(syn_data.index.get_level_values(0).dtype, syn_data.index.get_level_values(1).dtype)
    # print(syn_data)
    puma_year_combinations = ground_truth_PUMA_YEAR_sum.index.to_frame()
    # print(puma_year_combinations.shape, syn_data.shape)
    puma_year_combinations['key'] = 0
    syn_data['key'] = 0
    syn_data = pd.merge(syn_data.reset_index(), puma_year_combinations,  how='outer').set_index(['PUMA', 'YEAR'] + cols).drop('key', axis=1)
    # print(syn_data)
    # syn_data = dp.merge(puma_year_combinations, syn_data.reset_index())
    # syn_data = pd.concat(syn_data, keys=)


    merged_df = pd.merge(ground_truth, syn_data, on=['PUMA', 'YEAR'] + cols, how="outer")
    # print(merged_df.loc[['17-1001']].shape)
    merged_df['ground_count'].fillna(0, inplace=True)
    merged_df['syn_count'].fillna(0, inplace=True)
    # merged_df.fillna(0, inplace=True)
    # print(merged_df.loc[['17-1001']].shape)

    merged_df['diff'] = merged_df['ground_count'] - merged_df['syn_count']
    merged_df['diff'] = merged_df['diff'].abs()
    # print("---> check sum", np.sum(merged_df['ground_count']), np.sum(merged_df['syn_count']))
    # print(syn_data.index)

    result = merged_df.groupby(['PUMA', 'YEAR']).agg(l1_diff=('diff', 'sum'))
    # check = merged_df.groupby(['PUMA', 'YEAR']).agg(l1_diff=('ground_count', 'sum'))
    # print(np.max(check.values), np.min(check.values))
    result = result.rename(columns={"l1_diff": str(cols)})
    # print("----> ", result.shape)
    return result


class DetailedKMarginalMetric:
    """
    Implementation of k-marginal scoring
    """

    def __init__(
            self,
            raw_actual_df,
            raw_submitted_df,
            k,
            n_permutations,
            bins_for_numeric_cols=None,
            random_seed=None,
            verbose=False,
            bias_penalty_cutoff=250,
            processes=1,
            encoded=False
    ):
        self.k = k
        self.n_permutations = n_permutations

        self.raw_actual_df = raw_actual_df
        self.raw_submitted_df = raw_submitted_df

        if not encoded:
            # convert any numeric columns to bins
            self.bins_for_numeric_cols = bins_for_numeric_cols or {}
            for col, bins in bins_for_numeric_cols.items():
                self.raw_actual_df[col] = pd.cut(self.raw_actual_df[col], bins).cat.codes
                self.raw_submitted_df[col] = pd.cut(self.raw_submitted_df[col], bins).cat.codes
        else:
            print("---> no binning...")

        self.puma_year_index = self.raw_actual_df.groupby(["PUMA", "YEAR"]).size().index
        self.n_puma_years = len(self.puma_year_index)
        print("====> n_puma_years", self.n_puma_years)

        self.bias_penalty_cutoff = bias_penalty_cutoff
        self.marginal_group_cols = list(sorted(set(COLS.keys()) - set(["PUMA", "YEAR"])))
        self.random_seed = random_seed or 123456
        self.verbose = verbose
        self.processes = processes

    def groupby_column_permutations(self):
        """
        Figure out which permutations of columns to use. Deterministic based on the random seed.
        """
        rand = np.random.RandomState(seed=self.random_seed)
        for _ in range(self.n_permutations):
            # grab the next set of K columns to marginalize
            features_i = rand.choice(self.marginal_group_cols, size=self.k, replace=False).tolist()
            # we are going to group by the columns we always group by and also the K columns
            yield features_i

    def all_groupby(self):
        all_attrs = list(self.raw_actual_df.columns)
        all_attrs.remove("sim_individual_id")
        all_attrs.remove("PUMA")
        all_attrs.remove("YEAR")
        # todo: generate all 2-way from
        for i, attr in enumerate(all_attrs):
            for j in range(i + 1, len(all_attrs)):
                yield [all_attrs[i], all_attrs[j]]

    def k_marginal_scores(self):
        # set up the columns we need to go through
        permutations_to_score = (
            (self.raw_actual_df.groupby(["PUMA", "YEAR"] + k_cols),
             self.raw_submitted_df.groupby(k_cols), k_cols)
            for k_cols in self.all_groupby()
        )
        with multiprocessing.Pool(processes=self.processes) as pool:
            iters = pool.imap(compare, permutations_to_score)
            if self.verbose:
                iters = tqdm(iters, total=self.n_permutations)
            scores = list(iters)
        print(len(scores))
        scores = pd.concat(scores, axis=1)
        scores['avg'] = scores.mean(axis=1)
        # print(scores)
        return scores


def puma_year_detailed_score_compare(
        target_csv: Path,
        no_puma_year_csv: Path,
        k: int = 2,
        n_permutations: int = 50,
        bias_penalty_cutoff: int = 250000,
        processes: int = 10,
        verbose: bool = True,
        data_name: str = '',
):
    """
    Given the ground truth and a valid submission, compute the k-marginal score which the user would receive.
    """

    logger.info(f"reading in ground truth from {target_csv}")
    if args.mode == 'state' or args.mode == 'pub-state':
        target_df = pd.read_csv(target_csv, dtype=COLS)
        # no_puma_year_df is the one no puma-year
        no_puma_year_df = pd.read_csv(no_puma_year_csv, dtype=COLS)
        encoded = False
    elif args.mode == 'enc_dec_pub_state':
        dataloader = DataLoader()
        dataloader.load_data(pub_only=True)
        postprocessor = RecordPostprocessor()
        syn_data = postprocessor.post_process(dataloader.public_data, args.config, dataloader.decode_mapping)
        ## debug decode
        no_puma_year_df = pd.read_csv(no_puma_year_csv, dtype=COLS)
        pd.set_option('display.max_columns', None)
        # print(no_puma_year_df.iloc[:5])
        # print(syn_data.iloc[:5])
        no_puma_year_df = syn_data
        target_df = pd.read_csv(target_csv, dtype=COLS)
        encoded = False
    elif args.mode == 'enc_pub_enc_state':
        dataloader = DataLoader()
        dataloader.load_data(pub_only=True)
        dataloader.reload_priv(target_csv)
        target_df = dataloader.private_data
        no_puma_year_df = dataloader.public_data
        encoded = True
    elif args.mode == 'pub_enc_dec_state':
        dataloader = DataLoader()
        dataloader.load_data(pub_only=True)
        dataloader.reload_priv(target_csv)
        postprocessor = RecordPostprocessor()
        syn_data = postprocessor.post_process(dataloader.private_data, args.config, dataloader.decode_mapping)
        no_puma_year_df = pd.read_csv(no_puma_year_csv, dtype=COLS)
        target_df = copy.deepcopy(syn_data)
        encoded = False
    elif args.mode == 'enc_state_enc_state':
        dataloader = DataLoader()
        dataloader.load_data(pub_only=True)
        dataloader.reload_priv(no_puma_year_csv)
        target_df = copy.deepcopy(dataloader.private_data)
        no_puma_year_df = copy.deepcopy(dataloader.private_data)
        print(dataloader.encode_mapping)
        print(dataloader.private_data[['RACE', 'CITIZEN']].iloc[:10])
        encoded = True
    elif args.mode == 'enc_dec_state_state':
        dataloader = DataLoader()
        dataloader.load_data(pub_only=True)
        dataloader.reload_priv(no_puma_year_csv)
        postprocessor = RecordPostprocessor()
        syn_data = postprocessor.post_process(dataloader.private_data, args.config, dataloader.decode_mapping)
        target_df = pd.read_csv(target_csv, dtype=COLS)
        no_puma_year_df = copy.deepcopy(syn_data)
        encoded = False

    scores = None

    # TODO: use dataloader
    # target_df =

    # for puma in target_df['PUMA'].unique():
    #     for year in target_df['YEAR'].unique():
            # puma_year_df = copy.deepcopy(target_df.loc[(target_df['PUMA'] == puma) & (target_df['YEAR'] == year)])
    metric = DetailedKMarginalMetric(
        raw_actual_df=target_df,
        raw_submitted_df=no_puma_year_df,
        k=k,
        n_permutations=528,
        bias_penalty_cutoff=bias_penalty_cutoff,
        bins_for_numeric_cols=BINS,
        verbose=verbose,
        processes=processes,
        encoded=encoded
    )
    # if scores is None:
    scores = metric.k_marginal_scores()

    print("final avg:", scores['avg'].mean(axis=0))
    scores.to_csv(f"./other_data/stats/{args.mode}-{os.path.split(target_csv)[-1].replace('.csv','')}.csv")
    return scores['avg'].mean(axis=0)


def main():
    l1_diffs = pd.DataFrame(columns=['all margina avg l1 diff'])
    for filename in os.listdir(args.states_data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(args.states_data_dir, filename)
        else:
            continue
        print("====> file", filename)
        if args.mode == 'state' or args.mode == 'enc_state_enc_state' or args.mode == 'enc_dec_state_state':
            print("---> state to state compare")
            l1_diffs.loc[filename.replace('.csv','')] = [puma_year_detailed_score_compare(Path(file_path), Path(file_path))]
        else:
            l1_diffs.loc[filename.replace('.csv','')] = [puma_year_detailed_score_compare(Path(file_path), Path('./ground_truth.csv'))]
    l1_diffs.to_csv(f"./other_data/stats/final-{args.mode}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", type=str, default='state', choices=['state', 'pub-state', 'enc_dec_pub_state',
                                                                      'enc_pub_enc_state',
                                                                      'pub_enc_dec_state', 'enc_state_enc_state',
                                                                      'enc_dec_state_state'],
                        help="")
    parser.add_argument("--states_data_dir", type=str, default='./other_data/other_states/',
                        help="specify the path of data file in csv format")
    parser.add_argument("--config", type=str, default='./config/data.yaml',
                        help="config file")
    args = parser.parse_args()
    main()
    # public = Path("./ground_truth.csv")
    # puma_year_detailed_score_compare(public, public)

