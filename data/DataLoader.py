import json
import os
import pickle
from typing import Tuple, Dict

import numpy as np
import pandas as pd
import yaml

from config.path import PICKLE_DIRECTORY



class DataLoader:
    """Load data, bin some attributes, group some attributes,
    during which encode the attributes' values to categorical indexes,
    encode the remained single attributes likewise,
    remove the identifier attribute,
    (if existing) remove those attributes whose values can be determined by others.

    several marginal generation funtions are also included in the class for use.
    
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
        # we set pub_ref=False since the default case is not owning a public dataset to refer to
        self.pub_ref = False

    def load_data(self, pub_only=False):
    
        # TODO: I guess pub_only serves for sampling methods
        # load public data and get grouping mapping and filter values
        # CONFIG_DATA means data.yaml, which include some paths and value bins
        from experiment import PRIV_DATA, CONFIG_DATA, PARAMS, PRIV_DATA_NAME, DATA_TYPE
        with open(CONFIG_DATA, 'r', encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.config = config
        print("------------------------> config yaml file loaded in DataLoader, config file: ", CONFIG_DATA)

     
        # which include parameters for several runs and data schema
        with open(PARAMS,'r', encoding="utf-8") as f:
            parameter_spec = json.load(f)
            self.general_schema = parameter_spec['schema']
        print("------------------------> parameter file loaded in DataLoader, parameter file: ", PARAMS)

        # we use pickle to store the objects in files as binary flow
        priv_pickle_path = PICKLE_DIRECTORY / f"preprocessed_priv_{PRIV_DATA_NAME}.pkl"

        # load private data
        if os.path.isfile(priv_pickle_path) and not pub_only:
            print("********** load private data from pickle **************")
            print("------------------------> priv pickle path: ", priv_pickle_path)
            [self.private_data, self.encode_mapping] = pickle.load(open(priv_pickle_path, 'rb'))
            for attr, encode_mapping in self.encode_mapping.items():
                self.decode_mapping[attr] = sorted(encode_mapping, key=encode_mapping.get)
        
        elif not pub_only:
            print("************* start loading private data *************")
            print("------------------------> process and store with pkl file name: ", f"preprocessed_priv_{PRIV_DATA_NAME}.pkl")
            from experiment import DATA_TYPE

            with open(DATA_TYPE,'r', encoding="utf-8") as f:
                content = json.load(f)
            COLS = content['dtype']

            self.private_data = pd.read_csv(PRIV_DATA, dtype=COLS)
            print(self.private_data)

            self.private_data.fillna('',inplace=True)
            print("********** afer fillna ***********")
            print(self.private_data)
            print("------------------------> private dataset: ", PRIV_DATA)
            self.private_data = self.binning_attributes(config['numerical_binning'], self.private_data)
            # self.private_data = self.grouping_attributes(config['grouping_attributes'], self.private_data)
            self.private_data = self.remove_identifier(self.private_data)
            # self.private_data = self.remove_determined_attributes(config['determined_attributes'], self.private_data)
            self.private_data = self.encode_remain(self.general_schema, config, self.private_data, is_private=True)
            pickle.dump([self.private_data, self.encode_mapping], open(priv_pickle_path, 'wb'))

        for attr, encode_mapping in self.encode_mapping.items():
        # note that here schema means all the valid values of encoded ones
            self.encode_schema[attr] = sorted(encode_mapping.values())
        print("************* private data loaded and preprocessed in DataLoader ************")
        print("priv df's rows:------------------------> ", self.private_data.shape[0])


    def obtain_attrs(self):
        """return the list of all attributes' name  except the identifier attribute
        
        """
        if not self.all_attrs:

            all_attrs = list(self.private_data.columns)
            # here we use try: except: and all exceptions are caught in one ways
            try:
                all_attrs.remove(self.config['identifier'])
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
            # fit with the binning settings in format of [s,t,step]        
            # here we use np.r_ to connect the 1-dim arrays in row display
            [s, t, step] = spec_list
            # generate the bins
            # use np.arrange(s,t,step) to generate 1-dim array
            bins = np.r_[-np.inf, np.arange(s, t, step), np.inf]    
            # translate attribute original value to intervals and further translate to interval codes 
            data[attr] = pd.cut(data[attr], bins).cat.codes    
            # actually, the following 2 rows are based on agreed convention and serve not hard use
            # range(n) return [0,..,n-1]
            self.encode_mapping[attr] = {(bins[i], bins[i + 1]): i for i in range(len(bins) - 1)}
            # actually, the decode_maping is naive? just record the index array should suffice? I doubt...
            self.decode_mapping[attr] = [i for i in range(len(bins) - 1)]
        print("binning attributes done in DataLoader")
        return data

    def grouping_attributes(self, grouping_info, data):
        """Some attributes can be grouped  under settings in grouping_info

        """
        print("************* start grouping some attributes **************")
        for grouping in grouping_info:
            attributes = grouping['attributes']
            new_attr = grouping['grouped_name']

            # group attribute values into tuples
            data[new_attr] = data[attributes].apply(tuple, axis=1)

            # map tuples to new values in new columns
            encoding = {v: i for i, v in enumerate(grouping['combinations'])}
            # this row is verbous, data[new_attr] = data[attributes].apply(tuple, axis=1)
            # here we map them to codes again like we map intervals to interval indexes
            data[new_attr] = data[new_attr].map(encoding)
           
            self.encode_mapping[new_attr] = encoding
            # look at this, here decode_mapping is a dict which maps index to real tuple
            self.decode_mapping[new_attr] = grouping['combinations']

            # todo: do we still need filter?
            # EMP top 20 filter
            # if "filter" in grouping:
            #     data = data[~data[new_attr].isin(self.filter_values[new_attr])]

            # drop those already included in new_attr
            data = data.drop(attributes, axis=1)
            print("new attr:", new_attr, "<-", attributes)
            print("new uniques after encoding:", sorted(data[new_attr].unique()))
        # display after grouping
        print("columns after grouping:", data.columns)
        print("grouping attributes done in DataLoader")
    
        return data

    def remove_identifier(self, data):
        """remove the identifier attribute column
        
        """
        data = data.drop(self.config['identifier'], axis=1)
        print("------------------------> remove identifier column:", self.config['identifier'])
        print("identifier removed in DataLoader")
        return data
    
    # we declare the function as @staticmethod so that you can use it without instantiating an object
    # however, maybe determined_attributes are not so easy to be detected with a general dataset, so we mute the part
    @staticmethod
    def remove_determined_attributes(determined_info, data):
        """Some  attributes are determined by other attributes
        so why not first desert them and finally recover them 

        """
        for determined_attr in determined_info.keys():
            data = data.drop(determined_attr, axis=1)
        # desert the determined attributes and print the info
            print("remove", determined_attr)
        # desert the identifiers, but wait(why it seems to have appeared otherwhere?)
        # data = data.drop(self.config[identifier], axis=1) 
        # note that here rely on specific data setting claiming about determined attributes
        return data

    # encode the remaining single attributes to save storage
    #　i.e., all the attributes are encoded to save now
    def encode_remain(self, schema, config, data, is_private=False):
       
        # encoded_attr = list(config['numerical_binning'].keys()) + [grouping['grouped_name'] for grouping in config['grouping_attributes']]
        encoded_attr = list(config['numerical_binning'].keys()) 
        print("------------------------> start encoding remaining single attributes")
        for attr in data.columns:    
            if attr in [self.config['identifier']] or attr in encoded_attr:
                continue
            print("encode remain:", attr)
            assert attr in schema and 'values' in schema[attr]
            # below line serves for syhthesizing a dataset when fixing PUMA,YEAR 
            # data[].unique() returns an array which includes all the unique values in the column

            mapping = schema[attr]['values']
            encoding = {v: i for i, v in enumerate(mapping)}
            # we encode the remaining single attributes' original values to the categorical indexes
            data[attr] = data[attr].map(encoding)
            self.encode_mapping[attr] = encoding
            self.decode_mapping[attr] = mapping
        print("encoding remaining single attributes done in DataLoader")
        return data
   
    def generate_one_way_marginal(self, records: pd.DataFrame, index_attribute: list):
        """ generate marginal for one attribute
        (I guess the recommended arg should be in type of str)

        we first assign a new column 'n' and assign them as 1 for each record in orignal DataFrame
        note that aggfunc means aggrigation function 
        and we get counts for each candidate value for the specific index_attribute
        we set fill_value=0 for NaN
        
        """
        marginal = records.assign(n=1).pivot_table(values='n', index=index_attribute, aggfunc=np.sum, fill_value=0)
        # we create new indices which is in ascending order to help create a user-friendly pivot table
        indices = sorted([i for i in self.encode_mapping[index_attribute].values()])
        # and we reindex then fillna(0) means we will fill NaN with 0
        marginal = marginal.reindex(index=indices).fillna(0).astype(np.int32)
        return marginal

    def generate_two_way_marginal(self, records: pd.DataFrame, index_attribute: list, column_attribute: list):
        """generate marginal for a pair of attributes

        index_attribute corresponds to row index
        column_attribute corresponds to column index 
        
        """
        marginal = records.assign(n=1).pivot_table(values='n', index=index_attribute, columns=column_attribute,
                                                   aggfunc=np.sum, fill_value=0)
        # create a new ordered indices for row and column, just serving for a new display order
        indices = sorted([i for i in self.encode_mapping[index_attribute].values()])
        columns = sorted([i for i in self.encode_mapping[column_attribute].values()])
        marginal = marginal.reindex(index=indices, columns=columns).fillna(0).astype(np.int32)
       
        # print("*********** generating a two-way marginal *********** ")
        # print("*********** i ******* ", indices)
        # print("*********** j ******* ", columns)
        # print(marginal)
        # print("********** tmp count from the two-way marginal ****** ", np.sum(marginal.values))

        return marginal

    
    def generate_all_one_way_marginals(self, records: pd.DataFrame):
        """generate all the one-way marginals,
        which simply calls generate_one_way_marginal in every cycle round
        
        """
        all_attrs = self.obtain_attrs()
        marginals = {}
        for attr in all_attrs:
            marginals[frozenset([attr])] = self.generate_one_way_marginal(records, attr)
        print("------------------------> all one way marginals generated")
        return marginals
    
    def generate_all_two_way_marginals(self, records: pd.DataFrame):
        """generate all the two-way marginals,
        which simply builds a loop and calls generate_two_way_marginal in every cycle round
        
        """
        all_attrs = self.obtain_attrs()
        marginals = {}
        for i, attr in enumerate(all_attrs):
            for j in range(i + 1, len(all_attrs)):
                marginals[frozenset([attr, all_attrs[j]])] = self.generate_two_way_marginal(records, attr, all_attrs[j])
        
        print("------------------------> all two way marginals generated")
        # debug
        tmp_num = np.mean([np.sum(marginal.values) for marginal_att, marginal in marginals.items()])
        print("**************** help debug ************** num of records averaged from all two-way marginals:", tmp_num)

        return marginals
    

    def generate_marginal_by_config(self, records: pd.DataFrame, config: dict) -> Tuple[Dict, Dict]:
        """config means those marginals_xxxxx.yaml where define generation details
        1. users manually set config about marginal choosing
        2. automatic way of choosing which marginals TODO

        e.g.
        priv_all_two_way: 
          total_eps: 990
        e.g.
        priv_all_one_way: 
          total_eps: xxxxx

        """
        marginal_sets = {}
        epss = {}
        for marginal_key, marginal_dict in config.items():
            marginals = {}
        
            if marginal_key == 'priv_all_one_way':
                # merge the returned marginal dictionary
                marginals.update(self.generate_all_one_way_marginals(records))
            elif marginal_key == 'priv_all_two_way':
                # merge the returned marginal dictionary
                marginals.update(self.generate_all_two_way_marginals(records))
            else:
                # interestingly, the case 'else' only serves for privatizing for PUMA,YEAR attributes
                # i.e., return marginal for PUMA, YEAR, no use in general case
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


    def get_marginal_grouping_info(self, cur_attrs):
        """return a dictionary which map attr to a list of attr:
        if it's a single attribute, the list include itself,
        otherwise the list includes the attributes being grouped.

        """
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
