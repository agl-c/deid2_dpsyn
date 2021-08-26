import abc

import numpy as np
import pandas as pd
from loguru import logger

from data.DataLoader import DataLoader
from utils import advanced_composition
from typing import Dict, Tuple


class Synthesizer(object):
    """the class include functions to synthesize noisy marginals
    note that some functions just own a draft which yet to be used in practice
    
    
    """
    # every class can inherit the base class object;
    # abc means Abstract Base Class
    __metaclass__ = abc.ABCMeta
    Marginals = Dict[Tuple[str], np.array]

    def __init__(self, data: DataLoader, eps: float, delta: float, sensitivity: int):
        self.data = data
        self.eps = eps
        self.delta = delta
        self.sensitivity = sensitivity

    @abc.abstractmethod
    def synthesize(self, fixed_n: int) -> pd.DataFrame:
        pass

    # make sure the synthetic data size does not exceed the max allowed size
    # currently not used
    def synthesize_cutoff(self, submit_data: pd.DataFrame) -> pd.DataFrame:
        if submit_data.shape > 0:
            submit_data.sample()
        return submit_data

    def anonymize(self, priv_marginal_sets: Dict, epss: Dict, priv_split_method: Dict) -> Marginals:
        """the function serves for adding noises
        priv_marginal_sets: Dict[set_key,marginals] where set_key is an key for eps and noise_type
        priv_split_method serves for mapping set_key to noise_type

        """
        noisy_marginals = {}
        for set_key, marginals in priv_marginal_sets.items():
            eps = epss[set_key]
            # noise_type, noise_param = advanced_composition.get_noise(eps, self.delta, self.sensitivity, len(marginals))
            noise_type = priv_split_method[set_key]
            # we use laplace or guass noise?
            # the advanced_composition is a python module which provides related noise parameters
            # for instance, as to laplace noises, it computes the reciprocal of laplace scale
            
            if noise_type == 'lap':
                noise_param = 1 / advanced_composition.lap_comp(eps, self.delta, self.sensitivity, len(marginals))
                for marginal_att, marginal in marginals.items():
                    marginal += np.random.laplace(scale=noise_param, size=marginal.shape)
                    noisy_marginals[marginal_att] = marginal
            else:
            # interestingly, I want to specify how advanced_composition works
            # is it used for determine the scale parameter to input?
            # marginal.shape should return the shape of this np.array (should it be 1-dim int number or can it be multi-dim?)
            # oh it never minds since it just matches the marginal's shape in output, that works well then    
                noise_param = advanced_composition.gauss_zcdp(eps, self.delta, self.sensitivity, len(marginals))
                for marginal_att, marginal in marginals.items():
                    noise = np.random.normal(scale=noise_param, size=marginal.shape) 
                    marginal += noise
                    noisy_marginals[marginal_att] = marginal 
            logger.info(f"marginal {set_key} use eps={eps}, noise type:{noise_type}, noise parameter={noise_param}, sensitivity:{self.sensitivity}")
        return noisy_marginals

    # below function currently is not filled or used
    def get_noisy_marginals(self, priv_marginal_config, priv_split_method):
        priv_marginal_sets, epss = self.data.generate_marginal_by_config(self.data.private_data, priv_marginal_config)
        # todo: fix noise calculation method for each?
        # means what?
        noisy_marginals = self.anonymize(priv_marginal_sets, epss, priv_split_method)
        del priv_marginal_sets
        return noisy_marginals
