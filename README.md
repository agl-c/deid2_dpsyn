# DPSyn: a quick-start guide 
## What is DPsyn?
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy.

To facilitate your understanding, please refer to the paper *PrivSyn: Differentially Private Data Synthesis* [link](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun). And the repository is actually based on it.

## Comparison with related work

There are two similar and highly-related papers (both from competitors in the competition) . They are:
[PrivMRF](http://www.vldb.org/pvldb/vol14/p2190-cai.pdf), and
[PGM](https://arxiv.org/pdf/1901.09136.pdf).

The difference is that PrivSyn includes the whole data synthesis pipeline: (1) finding marginals and (2) synthesize dataset from the marginals. PGM only handles the second part, and PrivMRF only handles the first part (and uses PGM as the second part).  Since the PrivSyn and PrivMRF appear concurrently, there is no direct comparison between the two. Compared to PGM, PrivSyn shows its synthesizing method can handle *dense* graph.

In this repository, we only include the second part for now.

----

*For your convenience, with a dataset (whose privacy you want to protect), you can directly use DPSyn algorithm to generate a private dataset;*


## Install DPSyn 

*(fill this part after packaging, easy)*

We use the tool argparse for users to customize the input parameters and the usage message is shown below.

```
C:\Users\陈安琪\Desktop\nist_comp\deid2_s2 - clean_refresh\deid2_dpsyn>python experiment.py -h
usage: experiment.py [-h] [--priv_data PRIV_DATA] [--config CONFIG] [--n N] [--params PARAMS] [--datatype DATATYPE]
                     [--marginal_config MARGINAL_CONFIG] [--priv_data_name PRIV_DATA_NAME]
                     [--update_iterations UPDATE_ITERATIONS]

optional arguments:
  -h, --help            show this help message and exit
  --priv_data PRIV_DATA
                        specify the path of original data file in csv format
  --config CONFIG       specify the path of config file in yaml format
  --n N                 specify the number of records to generate
  --params PARAMS       specify the path of parameters file in json format
  --datatype DATATYPE   specify the path of datatype file in json format
  --marginal_config MARGINAL_CONFIG
                        specify the path of marginal config file in yaml format
  --priv_data_name PRIV_DATA_NAME
                        specify the name of the private dataset
  --update_iterations UPDATE_ITERATIONS
                        specify the num of update iterations
```



----

### How to configure?

#### Depend on 2 schema files and 2 config files

The input dataset should be in format of filename.csv with its first row a header row.
You should first preprocess the dataset. A tool(https://github.com/hd23408/nist-schemagen) is provided to generate 2 schema files: **(1) parameters.json** **(2) column_datatypes.json**  from the original dataset and actually our algorithm relies on them as input. We both include example files in our reporsitory.

Besides, you should specify parameters in "runs" in **parameters.json** as instructed later.

Refer to **parameters.json**, you can set the bin parts in the config file like  **data.yaml**.

And you can specify marginal settings in marginal config file like **eps=xxx.yaml**. (e.g. eps=10.0.yaml)

----

#### Differential privacy parameters (eps, delta, sensitivity)

<font color=red>for naive users, instruct about dp understandings, and instruct them to design the sensitive functions ? </font> (Gary comments they might not know how to set this..........)

Users should set the eps, delta, sensitivity value in 'runs' in **parameters.json** according to their specific differential privacy requirements. 
Here we display an example where the sensitivity value equals to 'max_records_per_individual', which essentially means the global sensitivity value of a specified function f(here is the count).

```json
  "runs": [
    {
      "epsilon": 10.0,
      "delta": 3.4498908254380166e-11,
      "max_records": 1350000,
      "max_records_per_individual": 7
    }
  ]
```


Meanwhile, as the above example shows, you can specify the 'max_records' parameter to bound the number of rows in the synthesized dataset. 

#### In data.yaml 

Set identifier attribute, bin value parameters.

You can specify the **identifier** attribute's name in data.yaml (we assume your dataset has the identifer attribute by default and obviously, in synthetic dataset the column should be removed to protect privacy)

You can specify **bin** settings in format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. ( Further, you can change more details in bin generation in binning_attributes() in DataLoader.py )

```yaml
identifier: ID
# you can define the binning settings as you want
# the three line means [min,max,step] values for bin,
# referring to parameters1.json, we set as below 
numerical_binning:
  "Age":
    - 14
    - 87
    - 10
```

----

#### Marginal selection config

Refer to eps=10.0.yaml as an example where we manually restrict the marginal selection method to be all the two way marginals. <font color=red>(include automatic marginal selection and combination part as in PrivSyn? )</font>

And we also write in this file the epsilon parameter corresponding to the one set in parameters.json "runs".

e.g.

```yaml
priv_all_two_way:
  total_eps: 10
```

----


### Details in fine tuning
Below we list several hyper parameters through our code. You can fine tune them when working on your own experiments instead of our default setting.

| variable          | file                 | class/function)    | value |  semantics                     |
| :---------------: | :------------------: | :------------:     | :----:| :--------:                     |
| update_iterations | dpsyn.py             | DPSyn              | 30    | the num of update iterations                        |
| alpha = 1.0       | record_synthesizer.py| RecordSynthesizer  |  1.0  |                                |
| update_alpha()    | record_synthesizer.py| RecordSynthesizer  | self.alpha = 1.0 * 0.84 ** (iteration // 20) |inspired by ML practice |

----

### Unused currently

Currently below functions are commented sicne they are tailored for specific datasets and in practice tricks **for efficiency consideration**.

##### grouping settings

You can define attributes to be grouped in data.yaml ( possibly based on analysis in possible existing public datasets ), and we may give you some tips on deciding which attributes to group.

**some intuitional grouping tips:**

   * group those with small domains
   * group those with embedded correlation
   * group those essitially the same (for instance, some attributes only differ in naming or one can be fully determined by another)

##### value-determined attributes 

If the original dataset includes some attributes that can be determined by other attributes, you can specify them in data.yaml, but by default we exclude the part since they are a little tricky.

----

### Measurements

You can refer to Synthpop(a R package) as a tool to compare the synthesized dataset against the original one. And we offer a quick-start guide [Synthpop](https://docs.google.com/document/d/17jSDoMcSbozjc8Ef8X42xPJXRb6g_Syt/edit#heading=h.gjdgxs ) for you here. 

Besides, we offer simple metric modules to measure the L1, L2 distance between the original dataset and the synthetic one.

----

### One Run example 

Below we offer the outputs in one run example:

You can find the default input files in the repository we offered here.

```
C:\Users\陈安琪\Desktop\nist_comp\deid2_dpsyn>python experiment.py
------------------------> config yaml file loaded in DataLoader, config file:  ./config/data.yaml
------------------------> parameter file loaded in DataLoader, parameter file:  ./data/parameters1.json
********** load private data from pickle **************
------------------------> priv pickle path:  data\pkl\preprocessed_priv_accidential_drug_deaths.pkl
************* private data loaded and preprocessed in DataLoader ************
priv df's rows:------------------------>  7634
2021-10-12 16:34:33.351 | INFO     | __main__:run_method:102 - working on eps=10.0, delta=3.4498908254380166e-11, and 
sensitivity=1
------------------------> all two way marginals generated
**************** help debug ************** num of records averaged from all two-way marginals: 7633.419354838709    
**************** help debug ************** num of records from marginal count before adding noise: 7633.419354838709
------------------------> now we decide the noise type:
considering eps: 10.0 , delta: 3.4498908254380166e-11 , sensitivity: 1 , len of marginals: 465
------------------------> noise type: gauss
------------------------> noise parameter: 16.386725928253217
2021-10-12 16:34:39.682 | INFO     | method.synthesizer:anonymize:82 - marginal priv_all_two_way use eps=10.0, noise type:gauss, noise parameter=16.386725928253217, sensitivity:1
------------------------> now we get the estimate of records' num by averaging from nosiy marginals: 7630
2021-10-12 16:34:44.329 | DEBUG    | lib_dpsyn.consistent:consist_views:103 - dependency computed
2021-10-12 16:34:44.746 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:44.759 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:45.167 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:45.184 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:45.604 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:45.620 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:46.017 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:46.030 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:46.459 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:46.472 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:46.868 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:46.884 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:47.315 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:47.328 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:47.744 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:47.758 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:48.151 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:48.163 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:48.576 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:48.590 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:49.035 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:49.050 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:49.502 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:49.518 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:49.915 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:49.933 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:50.342 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:50.355 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:50.763 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:50.774 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:51.174 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:51.188 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:51.654 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:51.667 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:52.090 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:52.114 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:52.533 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:52.549 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:53.037 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:53.051 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:53.512 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:53.525 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:53.941 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:53.954 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:54.362 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:54.377 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:54.816 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:54.840 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:55.245 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:55.259 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:55.673 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:55.690 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:56.137 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:56.152 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:56.557 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:56.570 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:56.971 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:56.985 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
2021-10-12 16:34:57.376 | DEBUG    | lib_dpsyn.consistent:consist_views:129 - consist finish
2021-10-12 16:34:57.388 | DEBUG    | lib_dpsyn.consistent:consist_views:146 - non-negativity finish
------------------------> attributes:
['Date', 'Age', 'Sex', 'Race', 'Residence State', 'Death County', 'Location', 'Location if Other', 'Injury County', 'Injury State', 'Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl Analogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine (Not Heroin)', 'Hydromorphone', 'Xylazine', 'Opiate NOS', 'Any Opioid', 'CardioCondition', 'RespiratoryCondition', 'ObesityCondition', 'DiabetesCondition']
------------------------> domains:
[ 9  9  2  7 11  9  7 10 15  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2
  2  2  2  2  2  2  2]
------------------------> cluseters:
{('Any Opioid', 'Injury State', 'Race', 'Location', 'Fentanyl', 'Residence State', 'Methadone', 'Xylazine', 'RespiratoryCondition', 'Ethanol', 'Benzodiazepine', 'Fentanyl Analogue', 'Hydromorphone', 'Sex', 'Injury County', 'Death County', 'Amphet', 'Cocaine', 'Morphine (Not Heroin)', 'Oxymorphone', 'Location if Other', 'CardioCondition', 'Hydrocodone', 'ObesityCondition', 'Tramad', 'Heroin', 'Opiate NOS', 'Oxycodone', 'DiabetesCondition', 'Age', 'Date'): [frozenset({'Age', 'Date'}), frozenset({'Date', 'Sex'}), frozenset({'Date', 'Race'}), frozenset({'Residence State', 'Date'}), frozenset({'Death County', 'Date'}), frozenset({'Date', 'Location'}), frozenset({'Date', 'Location if Other'}), frozenset({'Injury County', 'Date'}), frozenset({'Injury State', 'Date'}), frozenset({'Date', 'Heroin'}), frozenset({'Date', 'Cocaine'}), frozenset({'Date', 'Fentanyl'}), frozenset({'Date', 'Fentanyl Analogue'}), frozenset({'Oxycodone', 'Date'}), 
frozenset({'Oxymorphone', 'Date'}), frozenset({'Ethanol', 'Date'}), frozenset({'Hydrocodone', 'Date'}), frozenset({'Date', 'Benzodiazepine'}), frozenset({'Methadone', 'Date'}), frozenset({'Date', 'Amphet'}), frozenset({'Date', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Date'}), frozenset({'Date', 'Hydromorphone'}), frozenset({'Xylazine', 'Date'}), frozenset({'Opiate NOS', 'Date'}), frozenset({'Any Opioid', 'Date'}), frozenset({'Date', 'CardioCondition'}), frozenset({'Date', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Date'}), frozenset({'DiabetesCondition', 'Date'}), frozenset({'Age', 'Sex'}), frozenset({'Age', 'Race'}), frozenset({'Age', 'Residence State'}), frozenset({'Age', 'Death County'}), frozenset({'Age', 'Location'}), frozenset({'Age', 'Location if Other'}), frozenset({'Age', 'Injury County'}), frozenset({'Age', 'Injury State'}), frozenset({'Age', 'Heroin'}), frozenset({'Age', 'Cocaine'}), frozenset({'Age', 'Fentanyl'}), frozenset({'Age', 'Fentanyl Analogue'}), frozenset({'Age', 'Oxycodone'}), frozenset({'Age', 'Oxymorphone'}), frozenset({'Age', 'Ethanol'}), frozenset({'Hydrocodone', 'Age'}), frozenset({'Age', 'Benzodiazepine'}), frozenset({'Age', 'Methadone'}), frozenset({'Age', 'Amphet'}), frozenset({'Age', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Age'}), frozenset({'Age', 'Hydromorphone'}), frozenset({'Age', 'Xylazine'}), frozenset({'Age', 'Opiate NOS'}), frozenset({'Age', 'Any Opioid'}), frozenset({'Age', 'CardioCondition'}), frozenset({'Age', 'RespiratoryCondition'}), 
frozenset({'ObesityCondition', 'Age'}), frozenset({'DiabetesCondition', 'Age'}), frozenset({'Race', 'Sex'}), frozenset({'Residence State', 'Sex'}), frozenset({'Death County', 'Sex'}), frozenset({'Location', 'Sex'}), frozenset({'Location if Other', 'Sex'}), frozenset({'Injury County', 'Sex'}), frozenset({'Injury State', 'Sex'}), frozenset({'Heroin', 'Sex'}), frozenset({'Cocaine', 'Sex'}), frozenset({'Fentanyl', 'Sex'}), frozenset({'Fentanyl Analogue', 'Sex'}), frozenset({'Oxycodone', 'Sex'}), frozenset({'Oxymorphone', 'Sex'}), frozenset({'Ethanol', 'Sex'}), frozenset({'Hydrocodone', 'Sex'}), frozenset({'Benzodiazepine', 'Sex'}), frozenset({'Methadone', 'Sex'}), frozenset({'Amphet', 'Sex'}), frozenset({'Tramad', 'Sex'}), frozenset({'Morphine (Not Heroin)', 'Sex'}), frozenset({'Hydromorphone', 'Sex'}), frozenset({'Xylazine', 'Sex'}), frozenset({'Opiate NOS', 'Sex'}), frozenset({'Any Opioid', 'Sex'}), frozenset({'CardioCondition', 'Sex'}), frozenset({'RespiratoryCondition', 'Sex'}), frozenset({'ObesityCondition', 'Sex'}), frozenset({'DiabetesCondition', 'Sex'}), frozenset({'Residence State', 'Race'}), frozenset({'Death County', 'Race'}), frozenset({'Race', 'Location'}), frozenset({'Race', 'Location if Other'}), frozenset({'Injury County', 'Race'}), frozenset({'Injury State', 'Race'}), frozenset({'Race', 'Heroin'}), frozenset({'Race', 'Cocaine'}), frozenset({'Race', 'Fentanyl'}), frozenset({'Race', 'Fentanyl Analogue'}), frozenset({'Oxycodone', 'Race'}), frozenset({'Oxymorphone', 'Race'}), frozenset({'Ethanol', 'Race'}), frozenset({'Hydrocodone', 'Race'}), frozenset({'Race', 'Benzodiazepine'}), frozenset({'Methadone', 'Race'}), frozenset({'Race', 'Amphet'}), frozenset({'Race', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Race'}), frozenset({'Race', 'Hydromorphone'}), frozenset({'Xylazine', 'Race'}), frozenset({'Opiate NOS', 'Race'}), frozenset({'Any Opioid', 'Race'}), frozenset({'Race', 'CardioCondition'}), frozenset({'Race', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Race'}), frozenset({'DiabetesCondition', 'Race'}), frozenset({'Residence State', 'Death County'}), frozenset({'Residence State', 'Location'}), frozenset({'Residence State', 'Location if Other'}), frozenset({'Injury County', 'Residence State'}), frozenset({'Residence State', 'Injury State'}), frozenset({'Residence State', 'Heroin'}), frozenset({'Residence State', 'Cocaine'}), frozenset({'Residence State', 'Fentanyl'}), frozenset({'Residence State', 'Fentanyl Analogue'}), frozenset({'Residence State', 'Oxycodone'}), frozenset({'Oxymorphone', 'Residence State'}), frozenset({'Ethanol', 'Residence State'}), frozenset({'Hydrocodone', 'Residence State'}), frozenset({'Residence State', 'Benzodiazepine'}), frozenset({'Residence State', 'Methadone'}), frozenset({'Residence State', 'Amphet'}), frozenset({'Residence State', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Residence State'}), frozenset({'Residence State', 'Hydromorphone'}), frozenset({'Residence State', 'Xylazine'}), frozenset({'Opiate NOS', 'Residence State'}), frozenset({'Any Opioid', 'Residence State'}), frozenset({'Residence State', 'CardioCondition'}), frozenset({'Residence State', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Residence State'}), frozenset({'DiabetesCondition', 'Residence State'}), frozenset({'Death County', 'Location'}), frozenset({'Death County', 'Location if Other'}), frozenset({'Injury County', 'Death County'}), frozenset({'Injury State', 'Death County'}), frozenset({'Death County', 'Heroin'}), frozenset({'Death County', 'Cocaine'}), frozenset({'Death County', 'Fentanyl'}), frozenset({'Death County', 'Fentanyl Analogue'}), frozenset({'Oxycodone', 'Death County'}), frozenset({'Oxymorphone', 'Death County'}), frozenset({'Ethanol', 'Death County'}), frozenset({'Hydrocodone', 'Death County'}), frozenset({'Death County', 'Benzodiazepine'}), frozenset({'Methadone', 'Death County'}), frozenset({'Death County', 'Amphet'}), frozenset({'Death County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Death County'}), frozenset({'Death County', 'Hydromorphone'}), frozenset({'Xylazine', 'Death County'}), frozenset({'Opiate NOS', 'Death County'}), frozenset({'Any Opioid', 'Death County'}), frozenset({'Death County', 'CardioCondition'}), frozenset({'Death County', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Death County'}), frozenset({'DiabetesCondition', 'Death County'}), frozenset({'Location', 'Location if Other'}), frozenset({'Injury County', 'Location'}), frozenset({'Injury State', 'Location'}), frozenset({'Location', 'Heroin'}), frozenset({'Location', 'Cocaine'}), frozenset({'Fentanyl', 'Location'}), frozenset({'Fentanyl Analogue', 'Location'}), frozenset({'Oxycodone', 'Location'}), frozenset({'Oxymorphone', 'Location'}), frozenset({'Ethanol', 'Location'}), frozenset({'Hydrocodone', 'Location'}), frozenset({'Benzodiazepine', 'Location'}), frozenset({'Methadone', 'Location'}), frozenset({'Amphet', 'Location'}), frozenset({'Tramad', 'Location'}), frozenset({'Morphine (Not Heroin)', 'Location'}), frozenset({'Hydromorphone', 'Location'}), frozenset({'Xylazine', 'Location'}), frozenset({'Opiate NOS', 'Location'}), frozenset({'Any Opioid', 'Location'}), frozenset({'Location', 'CardioCondition'}), frozenset({'Location', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Location'}), frozenset({'DiabetesCondition', 'Location'}), frozenset({'Injury County', 'Location if Other'}), frozenset({'Injury State', 'Location if Other'}), frozenset({'Location if Other', 'Heroin'}), frozenset({'Cocaine', 'Location if Other'}), frozenset({'Fentanyl', 'Location if Other'}), frozenset({'Fentanyl Analogue', 'Location if Other'}), frozenset({'Oxycodone', 'Location if Other'}), frozenset({'Oxymorphone', 'Location if Other'}), frozenset({'Ethanol', 'Location if Other'}), frozenset({'Hydrocodone', 'Location if Other'}), frozenset({'Benzodiazepine', 'Location if Other'}), frozenset({'Methadone', 'Location if Other'}), frozenset({'Amphet', 'Location if Other'}), frozenset({'Tramad', 'Location if Other'}), frozenset({'Morphine (Not Heroin)', 'Location if Other'}), frozenset({'Hydromorphone', 'Location if Other'}), frozenset({'Xylazine', 'Location if Other'}), frozenset({'Opiate NOS', 'Location if Other'}), frozenset({'Any Opioid', 'Location if Other'}), frozenset({'Location if Other', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Location if Other'}), frozenset({'ObesityCondition', 'Location if Other'}), frozenset({'DiabetesCondition', 'Location if Other'}), frozenset({'Injury County', 'Injury State'}), frozenset({'Injury County', 'Heroin'}), frozenset({'Injury County', 'Cocaine'}), frozenset({'Injury County', 'Fentanyl'}), frozenset({'Injury County', 'Fentanyl Analogue'}), frozenset({'Injury County', 'Oxycodone'}), frozenset({'Injury County', 'Oxymorphone'}), frozenset({'Injury County', 'Ethanol'}), frozenset({'Hydrocodone', 'Injury County'}), frozenset({'Injury County', 'Benzodiazepine'}), frozenset({'Injury County', 'Methadone'}), frozenset({'Injury County', 'Amphet'}), frozenset({'Injury County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury County'}), frozenset({'Injury County', 'Hydromorphone'}), frozenset({'Injury County', 'Xylazine'}), frozenset({'Injury County', 'Opiate NOS'}), frozenset({'Injury County', 'Any Opioid'}), frozenset({'Injury County', 'CardioCondition'}), frozenset({'Injury County', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Injury County'}), frozenset({'DiabetesCondition', 'Injury County'}), frozenset({'Injury State', 'Heroin'}), frozenset({'Injury State', 'Cocaine'}), frozenset({'Injury State', 'Fentanyl'}), frozenset({'Injury State', 'Fentanyl Analogue'}), frozenset({'Injury State', 'Oxycodone'}), frozenset({'Oxymorphone', 'Injury State'}), frozenset({'Ethanol', 'Injury State'}), frozenset({'Hydrocodone', 'Injury State'}), frozenset({'Injury State', 'Benzodiazepine'}), frozenset({'Injury State', 'Methadone'}), frozenset({'Injury State', 'Amphet'}), frozenset({'Injury State', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury State'}), frozenset({'Injury State', 'Hydromorphone'}), frozenset({'Injury State', 'Xylazine'}), frozenset({'Opiate NOS', 'Injury State'}), frozenset({'Any Opioid', 'Injury State'}), frozenset({'Injury State', 'CardioCondition'}), frozenset({'Injury State', 'RespiratoryCondition'}), 
frozenset({'ObesityCondition', 'Injury State'}), frozenset({'DiabetesCondition', 'Injury State'}), frozenset({'Cocaine', 'Heroin'}), frozenset({'Fentanyl', 'Heroin'}), frozenset({'Fentanyl Analogue', 'Heroin'}), frozenset({'Oxycodone', 
'Heroin'}), frozenset({'Oxymorphone', 'Heroin'}), frozenset({'Ethanol', 'Heroin'}), frozenset({'Hydrocodone', 'Heroin'}), frozenset({'Benzodiazepine', 'Heroin'}), frozenset({'Methadone', 'Heroin'}), frozenset({'Amphet', 'Heroin'}), frozenset({'Tramad', 'Heroin'}), frozenset({'Morphine (Not Heroin)', 'Heroin'}), frozenset({'Hydromorphone', 'Heroin'}), frozenset({'Xylazine', 'Heroin'}), frozenset({'Opiate NOS', 'Heroin'}), frozenset({'Any Opioid', 'Heroin'}), frozenset({'CardioCondition', 'Heroin'}), frozenset({'RespiratoryCondition', 'Heroin'}), frozenset({'ObesityCondition', 'Heroin'}), frozenset({'DiabetesCondition', 'Heroin'}), frozenset({'Fentanyl', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Cocaine'}), frozenset({'Oxycodone', 'Cocaine'}), frozenset({'Oxymorphone', 'Cocaine'}), frozenset({'Ethanol', 'Cocaine'}), frozenset({'Hydrocodone', 'Cocaine'}), frozenset({'Benzodiazepine', 'Cocaine'}), frozenset({'Methadone', 'Cocaine'}), frozenset({'Amphet', 'Cocaine'}), frozenset({'Tramad', 'Cocaine'}), frozenset({'Morphine (Not Heroin)', 'Cocaine'}), frozenset({'Hydromorphone', 'Cocaine'}), frozenset({'Xylazine', 'Cocaine'}), frozenset({'Opiate NOS', 'Cocaine'}), 
frozenset({'Any Opioid', 'Cocaine'}), frozenset({'Cocaine', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Cocaine'}), frozenset({'ObesityCondition', 'Cocaine'}), frozenset({'DiabetesCondition', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Fentanyl'}), frozenset({'Oxycodone', 'Fentanyl'}), frozenset({'Oxymorphone', 'Fentanyl'}), frozenset({'Ethanol', 'Fentanyl'}), frozenset({'Hydrocodone', 'Fentanyl'}), frozenset({'Benzodiazepine', 'Fentanyl'}), frozenset({'Methadone', 'Fentanyl'}), frozenset({'Amphet', 'Fentanyl'}), frozenset({'Tramad', 'Fentanyl'}), frozenset({'Morphine 
(Not Heroin)', 'Fentanyl'}), frozenset({'Hydromorphone', 'Fentanyl'}), frozenset({'Xylazine', 'Fentanyl'}), frozenset({'Opiate NOS', 'Fentanyl'}), frozenset({'Any Opioid', 'Fentanyl'}), frozenset({'Fentanyl', 'CardioCondition'}), frozenset({'Fentanyl', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Fentanyl'}), frozenset({'DiabetesCondition', 'Fentanyl'}), frozenset({'Oxycodone', 'Fentanyl Analogue'}), frozenset({'Oxymorphone', 'Fentanyl Analogue'}), frozenset({'Ethanol', 'Fentanyl Analogue'}), frozenset({'Hydrocodone', 'Fentanyl Analogue'}), frozenset({'Benzodiazepine', 'Fentanyl Analogue'}), frozenset({'Methadone', 'Fentanyl Analogue'}), frozenset({'Amphet', 'Fentanyl Analogue'}), frozenset({'Tramad', 'Fentanyl Analogue'}), frozenset({'Morphine (Not Heroin)', 'Fentanyl Analogue'}), frozenset({'Hydromorphone', 'Fentanyl Analogue'}), frozenset({'Xylazine', 'Fentanyl Analogue'}), frozenset({'Opiate NOS', 'Fentanyl Analogue'}), frozenset({'Any Opioid', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'CardioCondition'}), frozenset({'Fentanyl Analogue', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Fentanyl Analogue'}), frozenset({'DiabetesCondition', 'Fentanyl Analogue'}), frozenset({'Oxymorphone', 'Oxycodone'}), frozenset({'Ethanol', 'Oxycodone'}), frozenset({'Hydrocodone', 'Oxycodone'}), frozenset({'Oxycodone', 'Benzodiazepine'}), frozenset({'Methadone', 'Oxycodone'}), frozenset({'Oxycodone', 'Amphet'}), frozenset({'Oxycodone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Oxycodone'}), frozenset({'Oxycodone', 'Hydromorphone'}), frozenset({'Xylazine', 'Oxycodone'}), frozenset({'Opiate NOS', 'Oxycodone'}), frozenset({'Any Opioid', 'Oxycodone'}), frozenset({'Oxycodone', 'CardioCondition'}), frozenset({'Oxycodone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Oxycodone'}), frozenset({'DiabetesCondition', 'Oxycodone'}), frozenset({'Oxymorphone', 'Ethanol'}), frozenset({'Hydrocodone', 'Oxymorphone'}), frozenset({'Oxymorphone', 'Benzodiazepine'}), frozenset({'Oxymorphone', 'Methadone'}), frozenset({'Oxymorphone', 'Amphet'}), frozenset({'Oxymorphone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Oxymorphone'}), frozenset({'Oxymorphone', 'Hydromorphone'}), frozenset({'Oxymorphone', 'Xylazine'}), frozenset({'Oxymorphone', 'Opiate NOS'}), frozenset({'Oxymorphone', 'Any Opioid'}), 
frozenset({'Oxymorphone', 'CardioCondition'}), frozenset({'Oxymorphone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Oxymorphone'}), frozenset({'DiabetesCondition', 'Oxymorphone'}), frozenset({'Hydrocodone', 'Ethanol'}), frozenset({'Ethanol', 'Benzodiazepine'}), frozenset({'Ethanol', 'Methadone'}), frozenset({'Ethanol', 'Amphet'}), frozenset({'Ethanol', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Ethanol'}), frozenset({'Ethanol', 'Hydromorphone'}), 
frozenset({'Ethanol', 'Xylazine'}), frozenset({'Ethanol', 'Opiate NOS'}), frozenset({'Any Opioid', 'Ethanol'}), frozenset({'Ethanol', 'CardioCondition'}), frozenset({'Ethanol', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Ethanol'}), frozenset({'DiabetesCondition', 'Ethanol'}), frozenset({'Hydrocodone', 'Benzodiazepine'}), frozenset({'Hydrocodone', 'Methadone'}), frozenset({'Hydrocodone', 'Amphet'}), frozenset({'Hydrocodone', 'Tramad'}), frozenset({'Hydrocodone', 'Morphine (Not Heroin)'}), frozenset({'Hydrocodone', 'Hydromorphone'}), frozenset({'Hydrocodone', 'Xylazine'}), frozenset({'Hydrocodone', 'Opiate NOS'}), frozenset({'Hydrocodone', 'Any Opioid'}), frozenset({'Hydrocodone', 'CardioCondition'}), frozenset({'Hydrocodone', 'RespiratoryCondition'}), frozenset({'Hydrocodone', 'ObesityCondition'}), frozenset({'Hydrocodone', 'DiabetesCondition'}), frozenset({'Methadone', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Amphet'}), frozenset({'Benzodiazepine', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Hydromorphone'}), frozenset({'Xylazine', 'Benzodiazepine'}), frozenset({'Opiate NOS', 'Benzodiazepine'}), frozenset({'Any Opioid', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'CardioCondition'}), frozenset({'Benzodiazepine', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Benzodiazepine'}), frozenset({'DiabetesCondition', 'Benzodiazepine'}), frozenset({'Methadone', 'Amphet'}), frozenset({'Methadone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Methadone'}), frozenset({'Methadone', 'Hydromorphone'}), frozenset({'Xylazine', 'Methadone'}), frozenset({'Opiate NOS', 'Methadone'}), frozenset({'Any Opioid', 'Methadone'}), frozenset({'Methadone', 'CardioCondition'}), frozenset({'Methadone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Methadone'}), frozenset({'DiabetesCondition', 'Methadone'}), frozenset({'Amphet', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Amphet'}), frozenset({'Amphet', 'Hydromorphone'}), frozenset({'Xylazine', 'Amphet'}), frozenset({'Opiate NOS', 'Amphet'}), frozenset({'Any Opioid', 'Amphet'}), frozenset({'Amphet', 'CardioCondition'}), frozenset({'Amphet', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Amphet'}), frozenset({'DiabetesCondition', 'Amphet'}), frozenset({'Morphine (Not Heroin)', 'Tramad'}), frozenset({'Hydromorphone', 'Tramad'}), frozenset({'Xylazine', 'Tramad'}), frozenset({'Opiate NOS', 'Tramad'}), frozenset({'Any Opioid', 'Tramad'}), frozenset({'Tramad', 'CardioCondition'}), frozenset({'Tramad', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Tramad'}), frozenset({'DiabetesCondition', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Hydromorphone'}), frozenset({'Morphine (Not Heroin)', 'Xylazine'}), frozenset({'Morphine (Not Heroin)', 'Opiate NOS'}), frozenset({'Morphine (Not Heroin)', 'Any Opioid'}), frozenset({'Morphine (Not Heroin)', 'CardioCondition'}), frozenset({'Morphine (Not Heroin)', 'RespiratoryCondition'}), frozenset({'Morphine (Not Heroin)', 'ObesityCondition'}), frozenset({'Morphine (Not Heroin)', 'DiabetesCondition'}), frozenset({'Xylazine', 'Hydromorphone'}), frozenset({'Opiate NOS', 'Hydromorphone'}), frozenset({'Any Opioid', 'Hydromorphone'}), frozenset({'Hydromorphone', 'CardioCondition'}), frozenset({'Hydromorphone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Hydromorphone'}), frozenset({'DiabetesCondition', 'Hydromorphone'}), frozenset({'Opiate NOS', 'Xylazine'}), frozenset({'Any Opioid', 'Xylazine'}), frozenset({'Xylazine', 'CardioCondition'}), frozenset({'Xylazine', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Xylazine'}), frozenset({'DiabetesCondition', 'Xylazine'}), frozenset({'Any Opioid', 'Opiate NOS'}), frozenset({'Opiate NOS', 'CardioCondition'}), frozenset({'Opiate NOS', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Opiate NOS'}), frozenset({'DiabetesCondition', 'Opiate NOS'}), frozenset({'Any Opioid', 'CardioCondition'}), frozenset({'Any Opioid', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Any Opioid'}), frozenset({'DiabetesCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 
'CardioCondition'}), frozenset({'DiabetesCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 'RespiratoryCondition'}), frozenset({'DiabetesCondition', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'DiabetesCondition'})]}
********************* START SYNTHESIZING RECORDS ********************
------------------------> num of synthesized records:
7630
2021-10-12 16:34:57.432 | INFO     | method.dpsyn:synthesize_records:167 - synthesizing for ('Any Opioid', 'Injury State', 'Race', 'Location', 'Fentanyl', 'Residence State', 'Methadone', 'Xylazine', 'RespiratoryCondition', 'Ethanol', 'Benzodiazepine', 'Fentanyl Analogue', 'Hydromorphone', 'Sex', 'Injury County', 'Death County', 'Amphet', 'Cocaine', 'Morphine (Not Heroin)', 'Oxymorphone', 'Location if Other', 'CardioCondition', 'Hydrocodone', 'ObesityCondition', 'Tramad', 'Heroin', 'Opiate NOS', 'Oxycodone', 'DiabetesCondition', 'Age', 'Date')
2021-10-12 16:34:57.442 | INFO     | method.dpsyn:synthesize_records:183 - update round: 0
2021-10-12 16:34:58.292 | INFO     | method.dpsyn:synthesize_records:183 - update round: 1
2021-10-12 16:34:59.132 | INFO     | method.dpsyn:synthesize_records:183 - update round: 2
2021-10-12 16:35:00.010 | INFO     | method.dpsyn:synthesize_records:183 - update round: 3
2021-10-12 16:35:00.921 | INFO     | method.dpsyn:synthesize_records:183 - update round: 4
2021-10-12 16:35:01.754 | INFO     | method.dpsyn:synthesize_records:183 - update round: 5
2021-10-12 16:35:02.676 | INFO     | method.dpsyn:synthesize_records:183 - update round: 6
2021-10-12 16:35:03.531 | INFO     | method.dpsyn:synthesize_records:183 - update round: 7
2021-10-12 16:35:04.343 | INFO     | method.dpsyn:synthesize_records:183 - update round: 8
2021-10-12 16:35:05.264 | INFO     | method.dpsyn:synthesize_records:183 - update round: 9
2021-10-12 16:35:06.102 | INFO     | method.dpsyn:synthesize_records:183 - update round: 10
2021-10-12 16:35:06.951 | INFO     | method.dpsyn:synthesize_records:183 - update round: 11
2021-10-12 16:35:07.786 | INFO     | method.dpsyn:synthesize_records:183 - update round: 12
2021-10-12 16:35:08.611 | INFO     | method.dpsyn:synthesize_records:183 - update round: 13
2021-10-12 16:35:09.607 | INFO     | method.dpsyn:synthesize_records:183 - update round: 14
2021-10-12 16:35:10.504 | INFO     | method.dpsyn:synthesize_records:183 - update round: 15
2021-10-12 16:35:11.442 | INFO     | method.dpsyn:synthesize_records:183 - update round: 16
2021-10-12 16:35:12.260 | INFO     | method.dpsyn:synthesize_records:183 - update round: 17
2021-10-12 16:35:13.093 | INFO     | method.dpsyn:synthesize_records:183 - update round: 18
2021-10-12 16:35:14.075 | INFO     | method.dpsyn:synthesize_records:183 - update round: 19
2021-10-12 16:35:14.949 | INFO     | method.dpsyn:synthesize_records:183 - update round: 20
2021-10-12 16:35:15.796 | INFO     | method.dpsyn:synthesize_records:183 - update round: 21
2021-10-12 16:35:16.662 | INFO     | method.dpsyn:synthesize_records:183 - update round: 22
2021-10-12 16:35:17.512 | INFO     | method.dpsyn:synthesize_records:183 - update round: 23
2021-10-12 16:35:18.335 | INFO     | method.dpsyn:synthesize_records:183 - update round: 24
2021-10-12 16:35:19.165 | INFO     | method.dpsyn:synthesize_records:183 - update round: 25
2021-10-12 16:35:20.019 | INFO     | method.dpsyn:synthesize_records:183 - update round: 26
2021-10-12 16:35:20.858 | INFO     | method.dpsyn:synthesize_records:183 - update round: 27
2021-10-12 16:35:21.696 | INFO     | method.dpsyn:synthesize_records:183 - update round: 28
2021-10-12 16:35:22.558 | INFO     | method.dpsyn:synthesize_records:183 - update round: 29
------------------------> synthetic dataframe before postprocessing: 
      Date  Age  Sex  Race  ...  CardioCondition  RespiratoryCondition  ObesityCondition  DiabetesCondition
0        3    4    1     6  ...                1                     1                 1                  1
1        6    0    1     0  ...                0                     0                 0                  0
2        5    5    0     4  ...                0                     1                 1                  1
3        8    8    0     3  ...                1                     0                 1                  1
4        4    3    1     2  ...                1                     0                 1                  1
...    ...  ...  ...   ...  ...              ...                   ...               ...                ...
7625     6    4    1     1  ...                0                     1                 0                  0
7626     0    4    0     2  ...                0                     1                 0                  1
7627     3    2    1     3  ...                1                     1                 0                  1
7628     7    2    0     2  ...                0                     0                 1                  1
7629     0    1    1     6  ...                1                     0                 1                  1

[7630 rows x 31 columns]
********************* START POSTPROCESSING ***********************
unbinning attributes ------------------------>
decode other attributes ------------------------>
2021-10-12 16:35:23.511 | INFO     | __main__:run_method:158 - ------------------------>synthetic data post-processed:      Date  Age     Sex             Race  ... RespiratoryCondition ObesityCondition DiabetesCondition epsilon
0     2015   49    MALE            WHITE  ...                    Y                Y                 Y    10.0
1     2018   13    MALE                   ...                                                            10.0
2     2017   59  FEMALE  HISPANIC, WHITE  ...                    Y                Y                 Y    10.0
3     2020   85  FEMALE  HISPANIC, BLACK  ...                                     Y                 Y    10.0
4     2016   39    MALE            BLACK  ...                                     Y                 Y    10.0
...    ...  ...     ...              ...  ...                  ...              ...               ...     ...
7625  2018   49    MALE            ASIAN  ...                    Y                                       10.0
7626  2012   49  FEMALE            BLACK  ...                    Y                                  Y    10.0
7627  2015   29    MALE  HISPANIC, BLACK  ...                    Y                                  Y    10.0
7628  2019   29  FEMALE            BLACK  ...                                     Y                 Y    10.0
7629  2012   19    MALE            WHITE  ...                                     Y                 Y    10.0

[7630 rows x 32 columns]
```



## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



