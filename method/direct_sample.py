import pandas as pd
import numpy as np
from method.synthesizer import Synthesizer


class DirectSample(Synthesizer):

    def synthesize(self, fixed_n=0):
        if fixed_n > 0:
            tmp = self.data.public_data.sample(n=fixed_n)
            tmp['YEAR'] = 0
            tmp['PUMA'] = 0
            return tmp

        noisy_marginals = self.get_noisy_marginals()
        noisy_marginal_puma_year = np.clip(noisy_marginals[frozenset(['YEAR', 'PUMA'])], a_min=0, a_max=np.inf)
        noisy_marginal_puma_year = noisy_marginal_puma_year.round().astype(np.int)

        syn_pd = pd.DataFrame()
        for puma, row in noisy_marginal_puma_year.iterrows():
            for year in noisy_marginal_puma_year:
                tmp = self.data.public_data.sample(n=row[year])
                tmp['YEAR'] = year
                tmp['PUMA'] = puma
                syn_pd = pd.concat([syn_pd, tmp])
        return syn_pd
