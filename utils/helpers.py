import pickle

import numpy as np
import pandas as pd
from loguru import logger

from config.path import *


###############################################################################
# Auxiliary Functions                                                         #
###############################################################################
def get_submission_format(submission_format: Path = DEFAULT_SUBMISSION_FORMAT):
    submission_format_pkl = DATA_DIRECTORY / 'submission_format.pkl'
    if not submission_format_pkl.exists():
        submission_format = pd.read_csv(submission_format, index_col=["epsilon", "neighborhood", "year", "month"])
        pickle.dump(submission_format, open(submission_format_pkl, 'wb'))

    return pd.read_pickle(submission_format_pkl)


def get_individual_contribution(incident_csv: Path = DEFAULT_INCIDENTS):
    incident_n_counts_pkl = DATA_DIRECTORY / f'incidents_n_counts.pkl'

    if incident_n_counts_pkl.exists():
        return pickle.load(open(incident_n_counts_pkl, 'rb'))

    incidents = pd.read_csv(incident_csv, index_col=0)

    appearances = incidents['sim_resident'].value_counts()
    n_counts = np.histogram(appearances, bins=range(1, 22))[0]

    pickle.dump(n_counts, open(incident_n_counts_pkl, 'wb'))
    return n_counts


def get_ground_truth_merge(truncates: list, incident_csv: Path = DEFAULT_INCIDENTS,
                           submission_format: Path = DEFAULT_SUBMISSION_FORMAT):
    submission_format = get_submission_format(submission_format)

    epsilons = submission_format.index.levels[0]
    ground_truth = submission_format.copy()
    for eps_i, eps in enumerate(epsilons):
        counts = get_ground_truth_individual(incident_csv, submission_format, truncates[eps_i])
        ground_truth.loc[eps] = counts.values
    return submission_format, ground_truth


def get_ground_truth(incident_csv: Path = DEFAULT_INCIDENTS, submission_format: Path = DEFAULT_SUBMISSION_FORMAT):
    return get_ground_truth_merge([20, 20, 20])


def create_table(incidents: pd.DataFrame, incident_pkl: Path, submission_format: pd.DataFrame = None):
    # get actual counts
    logger.debug("... creating pivot table")

    counts = incidents.pivot_table(
        index=["neighborhood", "year", "month"],
        columns="incident_type",
        values="n",
        aggfunc=np.sum,
        fill_value=0,
    )
    # when you pivot, you only gets rows and columns for things that were actually there --
    # the ground truth may not have all of the neighborhoods, periods, or codes we expected to see,
    # so we'll fix that by reindexing and then filling the missing values
    if submission_format is None:
        submission_format = get_submission_format()
    epsilons = submission_format.index.levels[0]
    index_for_one_epsilon = submission_format.loc[epsilons[0]].index
    columns = submission_format.columns.astype(counts.columns)
    counts = (counts.reindex(columns=columns, index=index_for_one_epsilon).fillna(0).astype(np.int32))

    pickle.dump(counts, open(incident_pkl, 'wb'))

    return counts


def get_incident_weights():
    weights_pkl = DATA_DIRECTORY / f'weights.pkl'

    if weights_pkl.exists():
        return pd.read_pickle(weights_pkl)

    incident_all_pkl = DATA_DIRECTORY / f'incidents_20.pkl'
    incidents_all = pd.read_pickle(incident_all_pkl)

    rows = incidents_all.values
    weights = count_five(rows)

    pickle.dump(weights, open(weights_pkl, 'wb'))

    return weights


def count_five(rows):
    weights = np.zeros(174, dtype=np.int)
    for row_i, row in enumerate(rows):
        weight = row > 0.05 * np.sum(row)
        weights += weight.astype(int)
    return weights


def get_incident_sum():
    sums_pkl = DATA_DIRECTORY / f'sum.pkl'

    # if weights_pkl.exists():
    #     return pd.read_pickle(weights_pkl)

    incident_all_pkl = DATA_DIRECTORY / f'incidents_20.pkl'
    incidents_all = pd.read_pickle(incident_all_pkl)

    rows = incidents_all.values
    sums = np.sum(rows, axis=0)

    pickle.dump(sums, open(sums_pkl, 'wb'))

    return sums


def get_incident_weights_pub(year: int = 2013, mix_type: str = ''):
    weights_pkl = DATA_DIRECTORY / f'weights_{year}{mix_type}.pkl'

    if weights_pkl.exists():
        return pd.read_pickle(weights_pkl)

    if mix_type:
        incident_all_pkl = DATA_DIRECTORY / f'{year}{mix_type}.pkl'
        incidents_all = pd.read_pickle(incident_all_pkl)
        incidents_all['n'] = 1
        incidents_count_pkl = DATA_DIRECTORY / f'count_{year}{mix_type}.pkl'
        rows = create_table(incidents_all, incidents_count_pkl).values
    else:
        incident_all_pkl = DATA_DIRECTORY / f'pub_incidents_{year}.pkl'
        incidents_all = pd.read_pickle(incident_all_pkl)
        rows = incidents_all.values
    weights = count_five(rows)

    pickle.dump(weights, open(weights_pkl, 'wb'))

    return weights


def truncate_incidents(incidents, truncate):
    agg_incidents = incidents.groupby(['sim_resident'], sort=False, as_index=False).agg({'n': sum})
    agg_incidents = agg_incidents.rename(columns={"n": "agg_n"})
    agg_incidents['scale'] = 1
    agg_incidents.loc[agg_incidents['agg_n'] <= truncate, ['scale']] = 1
    agg_incidents.loc[agg_incidents['agg_n'] > truncate, ['scale']] = agg_incidents['agg_n'] / truncate
    incidents = incidents.merge(agg_incidents, on='sim_resident', how='left')
    incidents['n'] = incidents['n'] / incidents['scale']
    return incidents


###############################################################################
# Pre-Process Methods: Competition Data                                       #
###############################################################################
def get_ground_truth_individual(incident_csv: Path = DEFAULT_INCIDENTS, truncate: int = 20):
    incident_pkl = DATA_DIRECTORY / f'incidents_{truncate}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incidents = pd.read_csv(incident_csv, index_col=0)
    incidents['n'] = 1

    if truncate < 20:
        incidents_with_count = incidents.groupby(['sim_resident'], sort=False).size().reset_index(name='count')
        over_residents = incidents_with_count[incidents_with_count['count'] > truncate]

        drop_indices = []
        for _, res in over_residents.iterrows():
            drop_records = incidents[incidents['sim_resident'] == res['sim_resident']].index
            drop_indices.append(np.random.choice(drop_records, res['count'] - truncate, replace=False))
        logger.debug(f"... found indices to duplicate for truncation {truncate}")
        incidents = incidents.drop(np.concatenate(drop_indices, axis=None))

    return create_table(incidents, incident_pkl)


def frac_get_ground_truth_individual(incident_csv: Path = DEFAULT_INCIDENTS, truncate: int = 20):
    incident_pkl = DATA_DIRECTORY / f'frac_incidents_{truncate}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incidents = pd.read_csv(incident_csv, index_col=0)
    incidents['n'] = 1

    # truncate
    if truncate < 20:
        incidents_with_count = incidents.groupby(['sim_resident'], sort=False).size().reset_index(name='count')
        incidents_with_count.loc[incidents_with_count['count'] <= truncate, ['count']] = 1
        incidents_with_count.loc[incidents_with_count['count'] > truncate, ['count']] /= truncate
        incidents = incidents.merge(incidents_with_count, on='sim_resident', how='left')
        incidents['n'] = incidents['n'] / incidents['count']

    return create_table(incidents, incident_pkl)


def weight_get_ground_truth_individual(incident_csv: Path = DEFAULT_INCIDENTS, truncate: int = 20):
    incident_pkl = DATA_DIRECTORY / f'weight_incidents_{truncate}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incidents = pd.read_csv(incident_csv, index_col=0)
    weights = get_incident_weights()
    incidents['n'] = weights[incidents['incident_type']]

    incidents = truncate_incidents(incidents, truncate)

    return create_table(incidents, incident_pkl)


def thres_get_ground_truth_individual(incident_csv: Path = DEFAULT_INCIDENTS, truncate: int = 20):
    incident_pkl = DATA_DIRECTORY / f'thres_incidents_{truncate}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incidents = pd.read_csv(incident_csv, index_col=0)
    incidents['n'] = 1

    weights = get_incident_weights()
    eps = 1
    weights[weights < 100 / eps] = 0
    weights[weights >= 100 / eps] = 10 / eps

    incidents = truncate_incidents(incidents, truncate)

    return create_table(incidents, incident_pkl)


def sqrt_get_ground_truth_individual(incident_csv: Path = DEFAULT_INCIDENTS, truncate: int = 20):
    incident_pkl = DATA_DIRECTORY / f'sqrt_incidents_{truncate}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incidents = pd.read_csv(incident_csv, index_col=0)
    incidents['n'] = 1

    weights = get_incident_weights()
    weights[weights < 100] = 100
    weights = np.sqrt(weights)

    incidents = truncate_incidents(incidents, truncate)

    return create_table(incidents, incident_pkl)


###############################################################################
# Pre-Process Methods: Public Data                                            #
###############################################################################
def get_ground_truth_pub(year: int = 2013):
    incident_pkl = DATA_DIRECTORY / f'pub_incidents_{year}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incident_data_npy = DATA_DIRECTORY / f'pub_incidents_all_{year}.npy'

    incidents = np.load(incident_data_npy)
    incidents = pd.DataFrame(incidents, columns=["neighborhood", "year", "month", "incident_type"])

    incidents['n'] = 1

    return create_table(incidents, incident_pkl)


def weight_get_ground_truth_pub(year: int = 2013):
    incident_pkl = DATA_DIRECTORY / f'pub_weight_incidents_{year}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incident_data_npy = DATA_DIRECTORY / f'pub_incidents_all_{year}.npy'

    incidents = np.load(incident_data_npy)
    incidents = pd.DataFrame(incidents, columns=["neighborhood", "year", "month", "incident_type"])

    weights = get_incident_weights()

    incidents['n'] = weights[incidents['incident_type']]

    return create_table(incidents, incident_pkl)


def priv_weight_get_ground_truth_pub(year: int = 2013):
    incident_pkl = DATA_DIRECTORY / f'pub_pub_weight_incidents_{year}.pkl'

    if incident_pkl.exists():
        return pd.read_pickle(incident_pkl)

    incident_data_npy = DATA_DIRECTORY / f'pub_incidents_all_{year}.npy'

    incidents = np.load(incident_data_npy)
    incidents = pd.DataFrame(incidents, columns=["neighborhood", "year", "month", "incident_type"])

    weights = get_incident_weights_pub(year)

    incidents['n'] = weights[incidents['incident_type']]

    return create_table(incidents, incident_pkl)


def thres_weight_get_ground_truth_pub(year: int = 2013, eps: float = 0.1):
    incident_pkl = DATA_DIRECTORY / f'pub_thres_weight_incidents_{year}_{eps}.pkl'

    # if incident_pkl.exists():
    #     return pd.read_pickle(incident_pkl)

    incident_data_npy = DATA_DIRECTORY / f'pub_incidents_all_{year}.npy'

    incidents = np.load(incident_data_npy)
    incidents = pd.DataFrame(incidents, columns=["neighborhood", "year", "month", "incident_type"])

    sums = get_incident_sum()
    weights = np.zeros_like(sums)
    weights[sums >= 800] = 10 / min(eps, 2)
    # weights[sums >= 800] = 1

    incidents['n'] = weights[incidents['incident_type']]

    return create_table(incidents, incident_pkl)


###############################################################################
# Pre-Process Methods: Mixed Data from Competition Data and Public Data       #
###############################################################################
def weight_get_ground_truth_mix(truncate: int = 20, year: int = 2013, type: str = 'base'):
    incident_pkl = DATA_DIRECTORY / f'pub_weight_incidents_{year}_{truncate}-{type}.pkl'
    incidents = DATA_DIRECTORY / f'{year}{type}.pkl'

    if incident_pkl.exists():
        return pickle.load(open(incident_pkl, 'rb'))

    incidents = pd.read_pickle(incidents)
    weights = get_incident_weights()
    incidents['n'] = weights[incidents['incident_type']]

    cur_incidents = truncate_incidents(incidents, truncate)
    return create_table(cur_incidents, incident_pkl)


def get_ground_truth_mix(truncate: int = 20, year: int = 2013, mix_type: str = '-base'):
    incident_pkl = DATA_DIRECTORY / f'incidents_{year}_{truncate}{mix_type}.pkl'
    incidents = DATA_DIRECTORY / f'{year}{mix_type}.pkl'

    if incident_pkl.exists():
        return pickle.load(open(incident_pkl, 'rb'))

    incidents = pd.read_pickle(incidents)
    incidents['n'] = 1

    cur_incidents = truncate_incidents(incidents, truncate)
    return create_table(cur_incidents, incident_pkl)


def get_ground_truth_reverse(truncate: int = 20, year: int = 2019, eps: float = 0.1, incident_csv: Path = DEFAULT_INCIDENTS):
    if truncate == 20:
        incident_pkl = DATA_DIRECTORY / f'incident_all_20.pkl'

        if incident_pkl.exists():
            return pickle.load(open(incident_pkl, 'rb'))

        incidents = pd.read_csv(incident_csv, index_col=0)
        incidents['n'] = 1

        incidents = truncate_incidents(incidents, truncate)

        return create_table(incidents, incident_pkl)
    else:
        incident_pkl = DATA_DIRECTORY / f'{year}-dpsyn-{eps}-{truncate}.pkl'
        return pickle.load(open(incident_pkl, 'rb'))


def priv_weight_get_ground_truth_mix(truncate: int = 20, year: int = 2013, mix_type: str = '-base'):
    incident_pkl = DATA_DIRECTORY / f'priv_weight_incidents_{year}_{truncate}{mix_type}.pkl'
    incidents = DATA_DIRECTORY / f'{year}{mix_type}.pkl'

    if incident_pkl.exists():
        return pickle.load(open(incident_pkl, 'rb'))

    incidents = pd.read_pickle(incidents)
    weights = get_incident_weights_pub(year, mix_type)
    incidents['n'] = weights[incidents['incident_type']]

    cur_incidents = truncate_incidents(incidents, truncate)
    return create_table(cur_incidents, incident_pkl)


def thres_get_ground_truth_mix(truncate: int = 20, eps: float = 1.0, year: int = 2013, mix_type: str = '-base'):
    incident_pkl = DATA_DIRECTORY / f'thres0_incidents_{year}_{truncate}-{eps}{mix_type}.pkl'
    incidents = DATA_DIRECTORY / f'{year}{mix_type}.pkl'

    if incident_pkl.exists():
        return pickle.load(open(incident_pkl, 'rb'))

    incidents = pd.read_pickle(incidents)
    sums = get_incident_sum()
    weights = np.zeros_like(sums)
    weights[sums >= 800] = 2 / min(eps, 2)
    incidents['n'] = weights[incidents['incident_type']]

    cur_incidents = truncate_incidents(incidents, truncate)
    return create_table(cur_incidents, incident_pkl)


def thres1_get_ground_truth_mix(truncate: int = 20, eps: float = 1.0, year: int = 2013, mix_type: str = '-base'):
    incident_pkl = DATA_DIRECTORY / f'thres01_incidents_{year}_{truncate}-{eps}{mix_type}.pkl'
    incidents = DATA_DIRECTORY / f'{year}{mix_type}.pkl'

    if incident_pkl.exists():
        return pickle.load(open(incident_pkl, 'rb'))

    incidents = pd.read_pickle(incidents)
    sums = get_incident_sum()
    weights = np.zeros_like(sums)
    weights[sums >= 800] = 1
    incidents['n'] = weights[incidents['incident_type']]

    cur_incidents = truncate_incidents(incidents, truncate)
    return create_table(cur_incidents, incident_pkl)
