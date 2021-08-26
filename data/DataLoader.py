import json
import os
import pickle
from typing import Tuple, Dict

import numpy as np
import pandas as pd
import yaml

from config.path import CONFIG_DATA, PICKLE_DIRECTORY, DATA_DIRECTORY
from config.data_type import COLS


class DataLoader:
    """Load data, attributes' processing, marginal generation funtions
    
    """
    def __init__(self):
        self.public_data = None
        self.private_data = None
        self.all_attrs = []

        self.encode_mapping = {}
        self.decode_mapping = {}

        self.pub_marginals = {}
        self.priv_marginals = {}

        self.encode_schema = {}

        self.general_schema = {}
        self.filter_values = {}

        self.config = None

    def load_data(self, pub_only=False, pub_ref=False):
        # we set pub_ref=False since the default case is not owning a public dataset to refer to
        # load public data and get grouping mapping and filter values
        # CONFIG_DATA means data.yaml, which include some paths and value bins
        with open(CONFIG_DATA, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.config = config
        
        # config['parameter_spec'] means parameters.json, which include parameters for several runs and data schema
        with open(config['parameter_spec']) as f:
            parameter_spec = json.load(f)
            self.general_schema = parameter_spec['schema']

        public_pickle_path = PICKLE_DIRECTORY / f"preprocessed_pub_{config['pub_dataset_path']}.pkl"
        priv_pickle_path = PICKLE_DIRECTORY / f"preprocessed_priv_{config['priv_dataset_path']}.pkl"

        # load public data
        if pub_ref:
            if os.path.isfile(public_pickle_path):
                [self.public_data, self.encode_mapping] = pickle.load(open(public_pickle_path, 'rb'))
                if pub_only:
                    for attr, encode_mapping in self.encode_mapping.items():
                        self.decode_mapping[attr] = sorted(encode_mapping, key=encode_mapping.get)
            else:
                # COLS is claimed to be config.data_type, meaning we should read the csv with restricted datatypes
                # pd.read_csv returns a 2-dimensional DataFrame
                # note that the basic silent setting is that the first row is the table header, so no need to config

                self.public_data = pd.read_csv(DATA_DIRECTORY / f"{config['pub_dataset_path']}.csv", dtype=COLS)
                self.public_data = self.binning_attributes(config['numerical_binning'], self.public_data)
                self.public_data = self.grouping_attributes(config['grouping_attributes'], self.public_data)
                self.public_data = self.remove_determined_attributes(config['determined_attributes'], self.public_data)
                self.public_data = self.recode_remain(self.general_schema, config, self.public_data)
                pickle.dump([self.public_data, self.encode_mapping], open(public_pickle_path, 'wb'))

        # load private data
        if os.path.isfile(priv_pickle_path) and not pub_only:
            [self.private_data, self.encode_mapping] = pickle.load(open(priv_pickle_path, 'rb'))
            for attr, encode_mapping in self.encode_mapping.items():
                self.decode_mapping[attr] = sorted(encode_mapping, key=encode_mapping.get)
        elif not pub_only:
            self.private_data = pd.read_csv(DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", dtype=COLS)
            self.private_data = self.binning_attributes(config['numerical_binning'], self.private_data)
            self.private_data = self.grouping_attributes(config['grouping_attributes'], self.private_data)
            self.private_data = self.remove_determined_attributes(config['determined_attributes'], self.private_data)
            self.private_data = self.recode_remain(self.general_schema, config, self.private_data, is_private=True)
            pickle.dump([self.private_data, self.encode_mapping], open(priv_pickle_path, 'wb'))

        for attr, encode_mapping in self.encode_mapping.items():
            self.encode_schema[attr] = sorted(encode_mapping.values())

    def obtain_attrs(self):
        if not self.all_attrs:
            all_attrs = list(self.public_data.columns)
            try:
            # why we remove this?
                all_attrs.remove("sim_individual_id")
            except:
                pass
            self.all_attrs = all_attrs
        return self.all_attrs

    def binning_attributes(self, binning_info, data):
        """Numerical attributes can be binned,
        As data.yaml only claims the min, max, step value for an attribute,
        we write this function to materially bin the detailed values for each attribute.
        You can change details according to your specific needs.



        """
        for attr, spec_list in binning_info.items():
            # if attr == "DEPARTS" or attr == "ARRIVES":
            # why we hard code it like this? why h times 100? it should be *60?
            # here we use np.r_ to connect the 1-dim arrays in row display
            #    bins = np.r_[-np.inf, [h * 100 + m for h in range(24) for m in spec_list], np.inf]
            # else:
            [s, t, step] = spec_list
            bins = np.r_[-np.inf, np.arange(s, t, step), np.inf]    # use np.arrange(s,t,step) to generate 1-dim array
            data[attr] = pd.cut(data[attr], bins).cat.codes    # translate attribute original value to bin codes 
            # actually, the following 2 rows are based on agreed convention and serve not hard use
            self.encode_mapping[attr] = {(bins[i], bins[i + 1]): i for i in range(len(bins) - 1)}
            self.decode_mapping[attr] = [i for i in range(len(bins) - 1)]
        return data

    def grouping_attributes(self, grouping_info, data):
        """
            Some attributes can be grouped
        """
        for grouping in grouping_info:
            attributes = grouping['attributes']
            new_attr = grouping['grouped_name']

            # group attribute values into tuples
            data[new_attr] = data[attributes].apply(tuple, axis=1)

            # map tuples to new values in new columns
            encoding = {v: i for i, v in enumerate(grouping['combinations'])}
            data[new_attr] = data[attributes].apply(tuple, axis=1)
            data[new_attr] = data[new_attr].map(encoding)
            # here we map using the same logic like dealing with above single attribute
            self.encode_mapping[new_attr] = encoding
            self.decode_mapping[new_attr] = grouping['combinations']

            # todo: do we still need filter?
            # EMP top 20 filter
            # if "filter" in grouping:
            #     data = data[~data[new_attr].isin(self.filter_values[new_attr])]

            # drop grouped columns
            # we drop those included in grouping attributes to ensure the data schema
            # and we print the detailed information to help understanding
            data = data.drop(attributes, axis=1)
            print("new attr:", new_attr, "<-", attributes)
            print("new uniques", sorted(data[new_attr].unique()))

        print("columns after grouping:", data.columns)
        # here is mapped and grouped data on display 
        return data

    @staticmethod
    def remove_determined_attributes(determined_info, data):
        """Some  attributes are determined by other attributes so why not first desert them

        """
        for determined_attr in determined_info.keys():
            data = data.drop(determined_attr, axis=1)
            print("remove", determined_attr)
        data = data.drop('sim_individual_id', axis=1) 
        # note that here rely on specific data setting claiming about determined attributes
        return data

    # recode the remaining single attributes to save storage
    def recode_remain(self, schema, config, data, is_private=False):
        encoded_attr = list(config['numerical_binning'].keys()) + [grouping['grouped_name'] for grouping in config['grouping_attributes']]
        for attr in data.columns:
            if attr in ['sim_individual_id'] or attr in encoded_attr:
                continue
            print("encode remain:", attr)
            assert attr in schema and 'values' in schema[attr]
            if is_private and attr == 'PUMA':
                mapping = data[attr].unique()
            else:
                mapping = schema[attr]['values']
            encoding = {v: i for i, v in enumerate(mapping)}
            data[attr] = data[attr].map(encoding)
            self.encode_mapping[attr] = encoding
            self.decode_mapping[attr] = mapping
        return data

    def generate_all_pub_marginals(self):
        with open(CONFIG_DATA, 'r') as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
        pub_marginal_pickle = PICKLE_DIRECTORY / f"pub_all_marginals_{config['pub_dataset_path']}.pkl"

        if pub_marginal_pickle is not None and os.path.isfile(pub_marginal_pickle):
            self.pub_marginals = pickle.load(open(pub_marginal_pickle, 'rb'))
            return self.pub_marginals

        all_attrs = list(self.public_data.columns)
        # all_attrs.remove("sim_individual_id")
        # one-way marginals except PUMA and YEAR
        for attr in all_attrs:
            if attr == 'PUMA' or attr == 'YEAR':
                continue
            self.pub_marginals[frozenset([attr])] = self.generate_one_way_marginal(self.public_data, attr)
        # two_way marginals except PUMA and YEAR
        for i, attr in enumerate(all_attrs):
            if attr == 'PUMA' or attr == 'YEAR':
                continue
            for j in range(i + 1, len(all_attrs)):
                if all_attrs[j] == 'PUMA' or all_attrs[j] == 'YEAR':
                    continue
                self.pub_marginals[frozenset([all_attrs[i], all_attrs[j]])] = self.generate_two_way_marginal(
                    self.public_data, all_attrs[i], all_attrs[j])

        if pub_marginal_pickle is not None:
            pickle.dump(self.pub_marginals, open(pub_marginal_pickle, 'wb'))

        return self.pub_marginals

    def generate_one_way_marginal(self, records: pd.DataFrame, index_attribute: list):
        marginal = records.assign(n=1).pivot_table(values='n', index=index_attribute, aggfunc=np.sum, fill_value=0)
        indices = sorted([i for i in self.encode_mapping[index_attribute].values()])
        marginal = marginal.reindex(index=indices).fillna(0).astype(np.int32)
        return marginal

    def generate_two_way_marginal(self, records: pd.DataFrame, index_attribute: list, column_attribute: list):
        marginal = records.assign(n=1).pivot_table(values='n', index=index_attribute, columns=column_attribute,
                                                   aggfunc=np.sum, fill_value=0)
        indices = sorted([i for i in self.encode_mapping[index_attribute].values()])
        columns = sorted([i for i in self.encode_mapping[column_attribute].values()])
        marginal = marginal.reindex(index=indices, columns=columns).fillna(0).astype(np.int32)
        return marginal

    def generate_all_one_way_marginals_except_PUMA_YEAR(self, records: pd.DataFrame):
        all_attrs = self.obtain_attrs()
        marginals = {}
        for attr in all_attrs:
            if attr == 'PUMA' or attr == 'YEAR':
                continue
            marginals[frozenset([attr])] = self.generate_one_way_marginal(records, attr)
        return marginals

    def generate_all_two_way_marginals_except_PUMA_YEAR(self, records: pd.DataFrame):
        all_attrs = self.obtain_attrs()
        marginals = {}
        for i, attr in enumerate(all_attrs):
            if attr == 'PUMA' or attr == 'YEAR':
                continue
            for j in range(i + 1, len(all_attrs)):
                if all_attrs[j] == 'PUMA' or all_attrs[j] == 'YEAR':
                    continue
                marginals[frozenset([attr, all_attrs[j]])] = self.generate_two_way_marginal(records, attr, all_attrs[j])
        return marginals

    def generate_marginal_by_config(self, records: pd.DataFrame, config: dict) -> Tuple[Dict, Dict]:
        marginal_sets = {}
        epss = {}
        for marginal_key, marginal_dict in config.items():
            marginals = {}
            if marginal_key == 'priv_all_one_way':
                # merge the returned marginal dictionary
                marginals.update(self.generate_all_one_way_marginals_except_PUMA_YEAR(records))
            elif marginal_key == 'priv_all_two_way':
                # merge the returned marginal dictionary
                marginals.update(self.generate_all_two_way_marginals_except_PUMA_YEAR(records))
            else:
                attrs = marginal_dict['attributes']
                if len(attrs) == 1:
                    marginals[frozenset(attrs)] = self.generate_one_way_marginal(records, attrs[0])
                elif len(attrs) == 2:
                    marginals[frozenset(attrs)] = self.generate_two_way_marginal(records, attrs[0], attrs[1])
                else:
                    raise NotImplementedError
            epss[marginal_key] = marginal_dict['total_eps']
            marginal_sets[marginal_key] = marginals
        return marginal_sets, epss

    '''
    '''
    def reload_priv(self, new_data_path):
        with open(CONFIG_DATA, 'r') as f:
            config = yaml.load(f)

        self.private_data = pd.read_csv(new_data_path)
        self.private_data = self.binning_attributes(config['numerical_binning'], self.private_data)
        self.private_data = self.grouping_attributes(config['grouping_attributes'], self.private_data)
        self.private_data = self.remove_determined_attributes(config['determined_attributes'], self.private_data)
        self.private_data = self.recode_remain(self.general_schema, config, self.private_data, is_private=True)
        for attr, encode_mapping in self.encode_mapping.items():
            self.encode_schema[attr] = sorted(encode_mapping.values())
        print(f"reload private {new_data_path} done...")

    def get_marginal_grouping_info(self, cur_attrs):
        info = {}
        grouping_info = self.config['grouping_attributes']
        for attr in cur_attrs:
            for grouping in grouping_info:
                new_attr = grouping['grouped_name']
                if new_attr == attr:
                    info[new_attr] = grouping['attributes']
                    break
            if attr not in info:
                info[attr] = [attr]
        return info


if __name__ == "__main__":
    loader = DataLoader()
    loader.load_data()
    # loader.load_data('../config/data.yaml', './pkl/preprocessed_ground_truth.pkl', './pkl/preprocessed_private.pkl')
    # loader.generate_all_pub_marginals('./pub_marginals.pkl')
    # print(loader.generate_marginal_by_yaml(loader.public_data, '../config/marginals_2.yaml'))
