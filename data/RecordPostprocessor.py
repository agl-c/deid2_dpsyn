import numpy as np
import pandas as pd
import yaml
import json 


class RecordPostprocessor:
    def __init__(self):
        self.config = None
        pass

    def post_process(self, data: pd.DataFrame, config_file_path: str, grouping_mapping: dict):
        assert isinstance(data, pd.DataFrame)
        with open(config_file_path, 'r', encoding="utf-8") as f:
            self.config = yaml.load(f, Loader=yaml.BaseLoader)
        # add for debug
        # print(data)
        # print(grouping_mapping)
        # data = self.ungrouping_attributes(data, grouping_mapping)
        data = self.unbinning_attributes(data)
        # we desert this for now
        # data = self.add_determined_attrs(data)
        # data = self.decode_other_attributes(data, grouping_mapping)
        data = self.ensure_types(data)
        return data

    def unbinning_attributes(self, data: pd.DataFrame):
        """unbin the binned attributes
        
        """
        print("unbinning attributes --------------->")
        binning_info = self.config['numerical_binning']
        # print(binning_info)
        for att, spec_list in binning_info.items():
            [s, t, step] = spec_list
            bins = np.r_[-np.inf, np.arange(int(s), int(t), int(step)), np.inf]

            # remove np.inf
            bins[0] = bins[1] - 1
            bins[-1] = bins[-2] + 2

            values_map = {i: int((bins[i] + bins[i + 1]) / 2) for i in range(len(bins) - 1)}
            data[att] = data[att].map(values_map)
        return data

    def ungrouping_attributes(self, data: pd.DataFrame, decode_mapping: dict):
        """ungroup the grouped attributes for consistency consideration
        as for now, not used since we do not group attributes
        
        """
        print("ungroup attributes ----------------->  ")
        grouping_info = self.config['grouping_attributes']
        for grouping in grouping_info:
            grouped_attr = grouping['grouped_name']
            attributes = grouping['attributes']
            mapping = pd.Index(decode_mapping[grouped_attr])
            # why the program print error here?
            data[grouped_attr] = pd.MultiIndex.to_numpy(mapping[data[grouped_attr]])
            data[attributes] = pd.DataFrame(data[grouped_attr].tolist(), index=data.index)
            data = data.drop(grouped_attr, axis=1)
        return data

    def decode_other_attributes(self, data: pd.DataFrame, decode_mapping: dict):
        """decode the attributes aside from the grouped ones and binned ones
        as for now, it works for decoding the attributes aside from binned ones since we set grouping info NULL

        """
        print("decode other attributes --------------->")
        grouping_attr = [info["grouped_name"] for info in self.config['grouping_attributes']]
        binning_attr = [attr for attr in self.config['numerical_binning'].keys()]
        for attr, mapping in decode_mapping.items():
            if attr in grouping_attr or attr in binning_attr:
                continue
            else:
                mapping = pd.Index(mapping)
                data[attr] = mapping[data[attr]]
        return data

    def add_determined_attrs(self, data: pd.DataFrame):
        """
             Some dataset are determined by other attributes
        """
        determined_info = self.config['determined_attributes']
        for determined_attr in determined_info.keys():
            control_attr = determined_info[determined_attr]['by']
            mapping = determined_info[determined_attr]['mapping']
            default = determined_info[determined_attr]['default']
            # type = data[control_attr].dtype
            mapping = {int(k): int(v) for k, v in mapping.items()}
            data[determined_attr] = data.apply(lambda row: mapping.get(row[control_attr], default), axis=1)
        return data

    def ensure_types(self, data: pd.DataFrame):
        """refer to the schema file DATA_TYPE,
        to ensure that the generated dataset have valid data types
        
        """
        from experiment import DATA_TYPE
        with open(DATA_TYPE,'r') as f:
            content = json.load(f)
        COLS = content['dtype']
        for col, data_type in COLS.items():
            data[col] = data[col].astype(data_type)
        return data
