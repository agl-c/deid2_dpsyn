import pandas as pd
import numpy as np
from loguru import logger
from method.dpsyn import DPSyn
from lib_dpsyn.view import View


class Sample(DPSyn):

    def synthesize(self, fixed_n=0, sample_data=None, scoring=None) -> pd.DataFrame:
        assert sample_data in [None, 'pub', 'dpsyn']
        assert scoring in [None, 'pub', '1way', '2way']
        noisy_puma_year = self.obtain_consistent_marginals()

        '''
            generate data
            # TODO: eps switch point 
            1. when eps is large (eps=10), call the parent class (DPSyn)'s method with fixed_n=10000
            2. when eps is small (eps=0.1 or 1), sample from pub
            self.obtain_consistent_marginals() already got the noisy marginals and stored them in self.attrs_view_dict
            self.obtain_consistent_marginals() also built other data structures
        '''
        if sample_data == 'dpsyn':
            logger.info("DPsyn generate candidate samples")
            init_data = super().internal_synthesize(noisy_puma_year, fixed_n=10000)
            init_data = init_data.drop('iteration', axis=1)
            init_data = init_data.values
        else:
            logger.info(f'eps {self.eps}, sampling from pub data')
            init_data = self.data.public_data.sample(n=int(10000)).values

        attrs = self.data.obtain_attrs()

        '''
            calculate weights based on number of attributes in marginals
        '''
        weights = {}
        # generate weights for marginals
        for cur_attrs in self.attrs_view_dict.keys():
            attrs_info = self.data.get_marginal_grouping_info(cur_attrs)
            weight = 1
            for attr, sub_attrs in attrs_info.items():
                weight *= len(sub_attrs)
            weights[cur_attrs] = weight

        '''
            decide which marginals will be used in scoring in sampling
        '''
        if scoring is None or scoring == 'pub':
            logger.info("using pub 2-way as scoring marginals for sampling...")
            scoring_marginals = self.data.generate_all_two_way_marginals_except_PUMA_YEAR(self.data.public_data)
        elif scoring == '1way':
            # 1 way marginals are not consistent
            logger.info("using noisy 1-way as scoring marginals for sampling...")
            scoring_marginals = self.get_noisy_marginals()
            del scoring_marginals[frozenset(['PUMA', 'YEAR'])]
        elif scoring == '2way':
            # 2-way marginals are consistent
            logger.info("using consistent 2-way as scoring marginals for sampling...")
            scoring_marginals = self.attrs_view_dict
        else:
            raise NotImplementedError

        '''
            **** experiment use only *****
            generate target marginals
        '''
        if fixed_n > 0:
            tmp = self.sample(init_data, scoring_marginals, weights, n=fixed_n)
            tmp = pd.DataFrame(tmp, columns=attrs)
            tmp['YEAR'] = 0
            tmp['PUMA'] = 0
            return tmp

        '''
            only generate datasets for PUMA-YEAR with different size in 100s
        '''
        interval = 100
        rounded_puma_year = noisy_puma_year.round(-2).astype(np.int)
        cell_count_max = np.max(rounded_puma_year.values)
        cell_count_min = np.min(rounded_puma_year.values)
        logger.info(f'sampling for sizes {np.unique(rounded_puma_year)}')

        # syn_pd = pd.DataFrame()
        syn_data_count = {}
        for count_i, cell_count in enumerate(np.unique(rounded_puma_year)):
            logger.info(f'=========== ITER {count_i}, for count{cell_count} =================')
            tmp = self.sample(init_data, scoring_marginals, weights, n=cell_count)
            syn_data_count[cell_count] = tmp

        syn_df_list = []
        for puma, puma_row in rounded_puma_year.iterrows():
            for year_i, cell_count in enumerate(puma_row):
                tmp = np.copy(syn_data_count[cell_count])
                tmp = pd.DataFrame(tmp, columns=attrs)
                tmp['PUMA'] = puma
                tmp['YEAR'] = year_i
                syn_df_list.append(tmp)
        syn_pd = pd.concat(syn_df_list, ignore_index=True)
        return syn_pd

    def sample(self, init_data, target_marginals, weights, n) -> np.ndarray:
        D = np.copy(init_data[:n, :])
        R = np.copy(init_data[n:, :])
        T = int(n / 3)
        t = 1
        early_stopping_threshold = 0.001

        pre_l1_error = len(target_marginals) * 2
        for i in range(T):
            # T_M, T_S, M_S = self.calculate_l1_errors(init_data, target_marginals, self.attrs_view_dict)
            D_scores = np.zeros(D.shape[0])
            R_scores = np.zeros(R.shape[0])
            l1_error = 0
            for cur_attrs, target_marginal in target_marginals.items():
                view = self.attrs_view_dict[cur_attrs]
                syn_marginal = view.count_records_general(D)
                if isinstance(target_marginal, pd.DataFrame):
                    target_marginal = np.copy(target_marginal.values.flatten())
                elif isinstance(target_marginal, View):
                    target_marginal = np.copy(target_marginal.count)
                target_marginal = target_marginal / np.sum(target_marginal) * np.sum(syn_marginal)
                l1_error += self._simple_l1(syn_marginal, target_marginal)

                under_cell_indices = np.where(syn_marginal < target_marginal - 1)[0]
                over_cell_indices = np.where(syn_marginal > target_marginal + 1)[0]

                # compute D_score and R_score
                for data, scores in zip([D, R], [D_scores, R_scores]):
                    # for cell_indices in [over_cell_indices, under_cell_indices]:
                    encode_records = np.matmul(data[:, view.attributes_index], view.encode_num)
                    encode_records_sort_index = np.argsort(encode_records)
                    encode_records = encode_records[encode_records_sort_index]

                    # here encode_records are sorted ordinal values, e.g., [0,0,0,1,1,1,1,2,3]
                    # cell_indices is e.g., [0,1], meaning that value 0, 1 are over or under
                    # we want to get the indices pointing to the chunks for 0,1
                    # so we search for the left end and right end; anything in between is an index we want
                    record_index_left = np.searchsorted(encode_records, over_cell_indices, side="left")
                    record_index_right = np.searchsorted(encode_records, over_cell_indices, side="right")
                    for j, cell_index in enumerate(over_cell_indices):
                        over_record_indices = encode_records_sort_index[record_index_left[j]: record_index_right[j]]
                        scores[over_record_indices] += weights[cur_attrs]

                    record_index_left = np.searchsorted(encode_records, under_cell_indices, side="left")
                    record_index_right = np.searchsorted(encode_records, under_cell_indices, side="right")
                    for j, cell_index in enumerate(under_cell_indices):
                        under_record_indices = encode_records_sort_index[record_index_left[j]: record_index_right[j]]
                        scores[under_record_indices] -= weights[cur_attrs]

            # reverse R_score
            R_scores = -1 * R_scores

            D_scores_sort_index = np.argsort(D_scores)
            R_scores_sort_index = np.argsort(R_scores)
            # add randomness if multiple highest
            d_i = self._sampled_largest_if_tie(D_scores, D_scores_sort_index)
            r_i = self._sampled_largest_if_tie(R_scores, R_scores_sort_index)
            # logger.debug(f"same largest score {d_i} {r_i}")
            # logger.debug(f"replace largest score {d_i} {r_i}")

            tmp = np.copy(R[R_scores_sort_index[-r_i], :])
            R[R_scores_sort_index[-r_i], :] = np.copy(D[D_scores_sort_index[-d_i], :])
            D[D_scores_sort_index[-d_i], :] = tmp
            logger.info(f'round {i + 1}/{T}, prev round L1 error:{l1_error}/{len(target_marginals)} = {l1_error/len(target_marginals)}')
            # check early stop
            if pre_l1_error - l1_error < early_stopping_threshold:
                logger.info(f' ==== EARLY STOP at round {i + 1}/{T}, threshold: {early_stopping_threshold} ')
                break
            else:
                pre_l1_error = l1_error
        return D

    @staticmethod
    def _simple_l1(m1, m2):
        normalize_m1 = m1 / np.sum(m1)
        normalize_m2 = m2 / np.sum(m2)
        return np.sum(np.abs(normalize_m1 - normalize_m2))

    @staticmethod
    def _sampled_largest_if_tie(scores, scores_sort_index):
        i = 1
        while scores[scores_sort_index[-i]] == scores[scores_sort_index[-i - 1]] and i < len(scores):
            i += 1
        i = np.random.randint(low=1, high=i + 1)
        return i