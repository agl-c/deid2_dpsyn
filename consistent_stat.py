from method.dpsyn import DPSyn
from lib_dpsyn.consistent import Consistenter
from data.DataLoader import *
from lib_dpsyn.view import View
import numpy as np
import copy

from data.DataLoader import *
from lib_dpsyn.consistent import Consistenter
from method.dpsyn import DPSyn

states_data_dir = './other_data/other_states/'


def construct_views(attr_index_map, domain_list, marginals):
    onehot_view_dict = {}
    attr_view_dict = {}

    for marginal_att, marginal_value in marginals.items():
        view_onehot = DPSyn.one_hot(marginal_att, attr_index_map)
        view = View(view_onehot, domain_list)
        view.count = marginal_value.values.flatten().astype('float64')

        onehot_view_dict[tuple(view_onehot)] = view
        attr_view_dict[marginal_att] = view

        if not len(view.count) == view.domain_size:
            raise Exception('no match')

    return onehot_view_dict, attr_view_dict

def consistent_marginals(public_two_ways, target_one_ways, dataloader):
    num_synthesize_records = np.mean([np.sum(x.values) for _, x in target_one_ways.items()]).round().astype(np.int)
    print("-->", num_synthesize_records, dataloader.private_data.shape)
    attr_list = dataloader.obtain_attrs()
    domain_list = np.array([len(dataloader.encode_schema[att]) for att in attr_list])
    attr_index_map = {att: att_i for att_i, att in enumerate(attr_list)}

    # views are wrappers of marginals with additional functions for consistency
    # pub_marginals = {}
    # noisy_marginals = {frozenset(['PUMA', 'YEAR']): noisy_marginals[frozenset(['PUMA', 'YEAR'])]}
    pub_onehot_view_dict, pub_attr_view_dict = construct_views(attr_index_map, domain_list, public_two_ways)
    target_onehot_view_dict, target_attr_view_dict = construct_views(attr_index_map, domain_list, target_one_ways)
    # for key, view in target_attr_view_dict.items():
    #     print(key, np.sum(view.count))
    # for key, view in pub_attr_view_dict.items():
    #     print(key, np.sum(view.count))

    # all_views is one-hot to view dict, views_dict is attribute to view dict
    # they have different format to satisfy the needs of consistenter and synthesiser
    onehot_view_dict, attrs_view_dict = DPSyn.normalize_views(
        pub_onehot_view_dict,
        pub_attr_view_dict,
        target_attr_view_dict,
        attr_index_map,
        num_synthesize_records)

    # for key, view in onehot_view_dict.items():
    #     print(key, np.sum(view.count))
    # exit()

    consistenter = Consistenter(onehot_view_dict, domain_list)
    consistenter.consist_views()
    # todo: change views back to two way marginals
    consistent_two_ways = {}
    for one_hot, view in consistenter.views.items():
        attrs = [attr_list[i] for i, v in enumerate(one_hot) if v == 1]
        # print("decoding", attrs)
        if len(attrs) > 1:
            consistent_two_ways[frozenset(attrs)] = view.count
    return consistent_two_ways


def compute_l1_for_each_puma_year(dataloader, consistent_two_ways):
    priv_data = dataloader.private_data
    l1_diffs = {}
    for puma in priv_data['PUMA'].unique():
        for year in priv_data['YEAR'].unique():
            l1_diffs[str(puma) + str(year)] = 0
            sub_dataset = copy.deepcopy(priv_data.loc[(priv_data['PUMA'] == puma) & (priv_data['YEAR'] == year)])
            all_two_ways = dataloader.generate_all_two_way_marginals_except_PUMA_YEAR(sub_dataset)
            valid_count = 0
            # print(sub_dataset)
            # print(all_two_ways.keys())
            for attrs in consistent_two_ways.keys():
                # print(all_two_ways[attrs].values)
                # print(consistent_two_ways[attrs])
                m1 = all_two_ways[attrs].values.flatten() / np.sum(all_two_ways[attrs].values.flatten())
                m2 = consistent_two_ways[attrs] / np.sum(consistent_two_ways[attrs])
                # print(m1)
                # print(m2)
                # print(np.sum(m1), np.sum(m2))
                # exit()
                if np.isnan(np.sum(m2)) or np.sum(m2) == 0:
                    continue
                else:
                    l1_diffs[str(puma) + str(year)] += np.sum(np.abs(m1 - m2))
                    valid_count += 1
                # print(attrs, np.sum(m1), np.sum(m2), m1.shape, m2.shape)
                # if np.isnan(np.sum(m2)):
                #     print(m2)
            l1_diffs[str(puma) + str(year)] /= valid_count
            print(puma, year, l1_diffs[str(puma) + str(year)], valid_count)
            # exit()
    return l1_diffs


def main():
    # dataloader initialization
    dataloader = DataLoader()
    dataloader.load_data(pub_only=True)

    public_two_ways = dataloader.generate_all_two_way_marginals_except_PUMA_YEAR(dataloader.public_data)

    # todo: iterate all states
    l1_diffs = pd.DataFrame(columns=['diff after consist'])
    for filename in os.listdir(states_data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(states_data_dir, filename)
        else:
            continue
        dataloader.reload_priv(file_path)
        print(dataloader.private_data['PUMA'].unique(), dataloader.private_data['YEAR'].unique())
        target_one_ways = dataloader.generate_all_one_way_marginals_except_PUMA_YEAR(dataloader.private_data)
        # TODO: get consistented two way marginals
        consistent_two_ways = consistent_marginals(public_two_ways, target_one_ways, dataloader)
        # TODO: compute L1 distance for each puma year two ways
        l1_diff = compute_l1_for_each_puma_year(dataloader, consistent_two_ways)
        print(l1_diff)
        l1_diffs.loc[filename.replace('.csv', '')] = sum(v for v in l1_diff.values()) / len(l1_diff)
        l1_diffs.to_csv(f"./other_data/stats/consistent_new.csv")


if __name__ == "__main__":
    main()
