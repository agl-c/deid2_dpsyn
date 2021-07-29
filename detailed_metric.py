import copy
import multiprocessing
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from tqdm import tqdm

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


def _marginalize(grouped):
    pd.set_option('display.max_rows', None)
    ground_truth = grouped[0].size().to_frame('ground_count')
    ground_truth_PUMA_YEAR_sum = ground_truth.groupby(['PUMA', 'YEAR']).agg(puma_year_sum=('ground_count', 'sum'))
    ground_truth = pd.merge(ground_truth.reset_index(), ground_truth_PUMA_YEAR_sum.reset_index(),
                            on=['PUMA', 'YEAR'], how="left").set_index(['PUMA', 'YEAR'] + grouped[2])
    ground_truth['ground_count'] /= ground_truth['puma_year_sum']
    # print(grouped[2])
    syn_data = grouped[1].size().to_frame('syn_count')
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
    syn_data = pd.merge(syn_data.reset_index(), puma_year_combinations, how='outer').set_index(
        ['PUMA', 'YEAR'] + grouped[2]).drop('key', axis=1)

    merged_df = pd.merge(ground_truth, syn_data, on=['PUMA', 'YEAR'] + grouped[2], how="outer")
    # print(merged_df.loc[['17-1001']].shape)
    merged_df['ground_count'].fillna(0, inplace=True)
    merged_df['syn_count'].fillna(0, inplace=True)
    # merged_df.fillna(0, inplace=True)
    # print(merged_df.loc[['17-1001']].shape)

    merged_df['diff'] = merged_df['ground_count'] - merged_df['syn_count']
    merged_df['diff'] = merged_df['diff'].abs()
    # print(merged_df)
    # print("---> check sum", np.sum(merged_df['ground_count']), np.sum(merged_df['syn_count']))
    # print("---> check diff", np.min(merged_df['diff']), np.max(merged_df['diff']))
    # print(syn_data.index)

    result = merged_df.groupby(['PUMA', 'YEAR']).agg(l1_diff=('diff', 'sum'))
    check = merged_df.groupby(['PUMA', 'YEAR']).agg(l1_diff=('ground_count', 'sum'))
    # print(np.max(check.values), np.min(check.values))
    result = result.rename(columns={"l1_diff": str(grouped[2])})
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
            processes=2,
    ):
        self.k = k
        self.n_permutations = n_permutations

        # combine the dataframes into one, groupable df
        # self.combined_df = (
        #     pd.concat([raw_actual_df.assign(actual=1), raw_submitted_df.assign(actual=0)]).set_index(["PUMA", "YEAR"])
        #         .sort_index()
        # )
        self.raw_actual_df = raw_actual_df
        self.raw_submitted_df = raw_submitted_df

        # convert any numeric columns to bins
        self.bins_for_numeric_cols = bins_for_numeric_cols or {}
        for col, bins in bins_for_numeric_cols.items():
            self.raw_actual_df[col] = pd.cut(self.raw_actual_df[col], bins).cat.codes
            self.raw_submitted_df[col] = pd.cut(self.raw_submitted_df[col], bins).cat.codes

        self.puma_year_index = self.raw_actual_df.groupby(["PUMA", "YEAR"]).size().index
        self.n_puma_years = len(self.puma_year_index)

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
            iters = pool.imap(_marginalize, permutations_to_score)
            if self.verbose:
                iters = tqdm(iters, total=self.n_permutations)
            scores = list(iters)
        scores = pd.concat(scores, axis=1)
        scores['avg'] = scores.mean(axis=1)
        mean_score = scores.mean()
        # print(scores)
        # exit()
        # print(((2.0 - mean_score) / 2.0) * 1_000)
        return scores


def puma_year_detailed_score(
        ground_truth_csv: Path,
        submission_df: pd.DataFrame,
        k: int = 2,
        n_permutations: int = 528,
        bias_penalty_cutoff: int = 250000,
        processes: int = 20,
        verbose: bool = True,
        data_name: str = '',
):
    """
    Given the ground truth and a valid submission, compute the k-marginal score which the user would receive.
    """

    logger.info(f"reading in ground truth from {ground_truth_csv}")
    ground_truth_df = pd.read_csv(ground_truth_csv, dtype=COLS)
    if 'PUMA' in submission_df.columns:
        submission_df = submission_df.drop(columns=['PUMA'], axis=1)
    if 'YEAR' in submission_df.columns:
        submission_df = submission_df.drop(columns=['YEAR'], axis=1)
    # print(submission_df.columns)
    # exit()
    metric = DetailedKMarginalMetric(
        raw_actual_df=ground_truth_df,
        raw_submitted_df=submission_df,
        k=k,
        n_permutations=n_permutations,
        bias_penalty_cutoff=bias_penalty_cutoff,
        bins_for_numeric_cols=BINS,
        verbose=verbose,
        processes=processes,
    )
    scores = metric.k_marginal_scores()
    print("avg of avg", scores['avg'].mean(axis=0))
    scores.to_csv(f'1-sample_detailed_error_n={submission_df.shape[0]}.csv')
    return scores


def iteration_detailed_score(
        ground_truth_csv: Path,
        submission_df: pd.DataFrame,
        k: int = 2,
        n_permutations: int = 528,
        bias_penalty_cutoff: int = 250000,
        processes: int = 10,
        verbose: bool = True,
):
    """
    Given the ground truth and a valid submission, compute the k-marginal score which the user would receive.
    """

    logger.info(f"reading in ground truth from {ground_truth_csv}")
    ground_truth_df = pd.read_csv(ground_truth_csv, dtype=COLS)
    assert "iteration" in submission_df.columns
    # difference_results = {}
    final_scores = None
    for itr in submission_df['iteration'].unique():
        subset_df = copy.deepcopy(submission_df.loc[submission_df['iteration'] == itr])
        tmp_ground_truth_df = copy.deepcopy(ground_truth_df)
        metric = DetailedKMarginalMetric(
            raw_actual_df=tmp_ground_truth_df,
            raw_submitted_df=subset_df,
            k=k,
            n_permutations=n_permutations,
            bias_penalty_cutoff=bias_penalty_cutoff,
            bins_for_numeric_cols=BINS,
            verbose=verbose,
            processes=processes,
        )

        scores = metric.k_marginal_scores()
        scores['iteration'] = itr
        scores = scores.reset_index().set_index(['PUMA', 'YEAR', 'iteration'])
        print("---> iteration:", itr)
        print(scores[['avg']])
        # difference_results[itr] = scores[['avg']]
        if final_scores is None:
            final_scores = copy.deepcopy(scores[['avg']])
        else:
            final_scores = final_scores.append(scores[['avg']])
        del scores, subset_df, tmp_ground_truth_df

    final_scores.to_csv(f'dpsyn_detailed_error_n={submission_df.shape[0]}.csv')
    return final_scores

def puma_year_to_puma_year_score(
        ground_truth_csv: Path,
        syn_data: pd.DataFrame,
        k: int = 2,
        n_permutations: int = 500,
        bias_penalty_cutoff: int = 250000,
        processes: int = 20,
        verbose: bool = True,
        data_name: str = '',
):
    logger.info(f"reading in ground truth from {ground_truth_csv}")
    ground_truth_df = pd.read_csv(ground_truth_csv, dtype=COLS)
    final_scores = None
    combinations = len(syn_data['PUMA'].unique()) * len(syn_data['YEAR'].unique())
    print("combinations:", combinations)
    for puma in syn_data['PUMA'].unique():
        for year in syn_data['YEAR'].unique():
            sub_ground_truth = copy.deepcopy(ground_truth_df.loc[(ground_truth_df['PUMA'] == puma) & (ground_truth_df['YEAR'] == year)])
            sub_syn_data = copy.deepcopy(syn_data.loc[(syn_data['PUMA'] == puma) & (syn_data['YEAR'] == year)])
            # print(sub_ground_truth.iloc[:4])
            metric = DetailedKMarginalMetric(
                raw_actual_df=sub_ground_truth,
                raw_submitted_df=sub_syn_data,
                k=k,
                n_permutations=n_permutations,
                bias_penalty_cutoff=bias_penalty_cutoff,
                bins_for_numeric_cols=BINS,
                verbose=verbose,
                processes=processes,
            )
            puma_year_scores = metric.k_marginal_scores()
            puma_year_scores['syn_size'] = sub_syn_data.shape[0]
            # print(puma_year_scores)
            if final_scores is None:
                final_scores = copy.deepcopy(puma_year_scores)
            else:
                final_scores = final_scores.append(puma_year_scores)
            print(f"{puma} {year} avg of avg: {puma_year_scores['avg'].mean(axis=0)}, shape {puma_year_scores.shape}")
            print(f"{final_scores.shape} / {combinations}")
            # print(final_scores)
    resuls = copy.deepcopy(final_scores[['avg', 'syn_size']])
    resuls.to_csv(f'puma-year-2-puma-year_detailed_error.csv')
    return final_scores


if __name__ == "__main__":
    syn_data = pd.read_csv('./sample-0-state-22-data.csv')
    ground_truth_csv = './data/state-22-data.csv'
    puma_year_to_puma_year_score(ground_truth_csv, syn_data, )
    pass
