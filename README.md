# DPSyn: a quick-start guide 

- [DPSyn: a quick-start guide](#dpsyn--a-quick-start-guide)
  * [What is DPsyn?](#what-is-dpsyn-)
    + [Comparison with related work](#comparison-with-related-work)
  * [Install DPSyn](#install-dpsyn)
    + [Docker support](#docker-support)
    + [Run the python file](#run-the-python-file)
    + [How to configure?](#how-to-configure-)
      - [Depend on 2 schema files and 2 config files](#depend-on-2-schema-files-and-2-config-files)
      - [Differential privacy parameters (eps, delta, sensitivity)](#differential-privacy-parameters--eps--delta--sensitivity-)
      - [In data.yaml](#in-datayaml)
      - [Marginal selection config](#marginal-selection-config)
    + [Details in fine tuning](#details-in-fine-tuning)
    + [Unused currently](#unused-currently)
        * [grouping settings](#grouping-settings)
        * [value-determined attributes](#value-determined-attributes)
    + [Measurements](#measurements)
    + [One Run example](#one-run-example)
  * [Team Members & Affiliation(s):](#team-members---affiliation-s--)
  * [GitHub User(s) Serving as POC:](#github-user-s--serving-as-poc-)

## What is DPsyn?

We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy.

To facilitate your understanding, please refer to the paper [*PrivSyn: Differentially Private Data Synthesis*](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun). And we utilized the record synthesis method proposed in that paper, which is GUM ( Gradually Update Method ) .

### Comparison with related work

There are two similar and highly-related papers (both from competitors in the competition) . They are:
[PrivMRF](http://www.vldb.org/pvldb/vol14/p2190-cai.pdf), and
[PGM](https://arxiv.org/pdf/1901.09136.pdf).

The difference is that PrivSyn includes the whole data synthesis pipeline: (1) finding marginals and (2) synthesize dataset from the marginals. PGM only handles the second part, and PrivMRF only handles the first part (and uses PGM as the second part).  Since the PrivSyn and PrivMRF appear concurrently, there is no direct comparison between the two. Compared to PGM, PrivSyn shows its synthesizing method can handle *dense* graph.

In this repository, we only include the second part for now.

----

*For your convenience, with a dataset (whose privacy you want to protect), you can directly use DPSyn algorithm to generate a private dataset;*


## Install DPSyn 

### Docker support

We create a public image in docker.io [link](https://hub.docker.com/repository/docker/chenanqi18pku/dpsyn)

You can obtain it by

```
> docker pull chenanqi18pku/dpsyn:v1
```

Or you can directly create the image with the directory here, since the Dockerfile is already included.

```
> docker build -t dpsyn .
```

Then you can create a container to run the image.

We show one example below with target_path=syndata.csv and container named 'test'.

```
> docker run -it --name test dpsyn --target_path syndata.csv
```

Note that you can add parameters like when you run "python experiment.py" as below example shows.

And you can find the synthetic dataset **syndata.csv** in the container **test**, right in the directory **/DPSyn** as we declared in the Dockerfile.

### Run the python file

We use the tool argparse for users to customize the input parameters and the usage message is shown below.

To get a better understanding of the args' meanings, you can refer to the default values of them in experiment.py and the run example we provided in later part.

```
python experiment.py -h
usage: experiment.py [-h] [--priv_data PRIV_DATA] [--config CONFIG] [--n N] [--params PARAMS] [--datatype DATATYPE]
                     [--marginal_config MARGINAL_CONFIG] [--priv_data_name PRIV_DATA_NAME]
                     [--update_iterations UPDATE_ITERATIONS] [--target_path TARGET_PATH]

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
  --target_path TARGET_PATH
                        specify the target path of the synthetic dataset
```



----

### How to configure?

#### Determine differential privacy parameters (eps, delta, sensitivity)

You should set the **eps, delta, sensitivity value** in 'runs' in **parameters.json** according to their specific differential privacy requirements （refer to [The Algorithmic Foundations of Differential Privacy](http://dx.doi.org/10.1561/0400000042) if you are not familiar with DP）. 
Here we display an example where the sensitivity value equals to 'max_records_per_individual', which essentially means the global sensitivity value of a specified function f (here f is the counting function).

```json
  "runs": [
    {
      "epsilon": 10.0,
      "delta": 3.4498908254380166e-11,
      "max_records": 1350000,
      "max_records_per_individual": 1
    }
  ]
```

As the above example shows, you can specify the 'max_records' parameter to bound the number of rows in the synthesized dataset. 


#### Obtain 2 schema files ([data/parameters.json](data/parameters.json) and [data/column_datatypes.json](data/column_datatypes.json)) and 2 config files ([data.yaml](config/data.yaml) and [eps=xxx.yaml](config/eps=10.0.yaml))

The input dataset should be in format of filename.csv with its first row a header row.
You should first preprocess the dataset. A [tool]( https://github.com/hd23408/nist-schemagen ) is provided to generate 2 schema files: **(1) parameters.json** **(2) column_datatypes.json**  from the original dataset and actually our algorithm relies on them as input. 

Besides, you should specify parameters in "runs" in **parameters.json** as instructed later.

Refer to **parameters.json**, you can set the bin parts in the config file like  **data.yaml**

And you can specify marginal settings in marginal config file like **eps=xxx.yaml**.

----

##### data.yaml 

Set identifier attribute, bin value parameters.

You can specify the **identifier** attribute's name in data.yaml (we assume your dataset has the identifer attribute by default; obviously, in synthetic dataset the column should be removed to protect privacy).

You can specify **bin** settings in the format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. (Further, you can change more details in bin generation in binning_attributes() in DataLoader.py.)

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

##### Marginal selection config

Suppose epsilon parameter in "runs" of parameters.json is 10 now.  We will go to eps=10.0.yaml to find the marginal configuration. In this example, we use all the two way marginals, i.e., "priv_all_two_way":

```yaml
priv_all_two_way:
  total_eps: 10
```

----


### Details in fine tuning
Below we list several hyper parameters through our code. You can fine tune them when working on your own experiments.

| variable          | file                 | class/function)    | value |  semantics                     |
| :---------------: | :------------------: | :------------:     | :----:| :--------:                     |
| update_iterations | dpsyn.py             | DPSyn              | 30    | the number of update iterations                        |
| alpha = 1.0       | record_synthesizer.py| RecordSynthesizer  |  1.0  | update rate                               |
| update_alpha()    | record_synthesizer.py| RecordSynthesizer  | self.alpha = 1.0 * 0.84 ** (iteration // 20) |inspired by ML practice |

----

### Unused currently

Currently below functions are not used:

##### grouping settings

You can define attributes to be grouped in data.yaml (possibly based on analysis in possible existing public datasets).

**some intuitional grouping tips:**

   * group those with small domains
   * group those with embedded correlation
   * group those essitially the same (for instance, some attributes only differ in naming or one can be fully determined by another)

##### Value-determined attributes 

If your dataset includes some attributes that can be determined by other attributes (e.g., if age is <18, then weekly working hour is 0), you can specify them in data.yaml, but by default we exclude the part.

----

### Measurements

You can refer to [Synthpop](https://docs.google.com/document/d/17jSDoMcSbozjc8Ef8X42xPJXRb6g_Syt/edit#heading=h.gjdgxs) (a R package) as a tool to compare the synthesized dataset against the original one. 

----

### One Run example 

Below we offer the outputs in one run example:

You can find the default input files in the repository we offered here.

And you can find the synthetic dataset "out.csv" ( under default setting ) in your working directory after the program finishes.

```
python experiment.py
------------------------> config yaml file loaded in DataLoader, config file:  ./config/data.yaml
------------------------> parameter file loaded in DataLoader, parameter file:  ./data/parameters.json
************* start loading private data *************
           ID  Date  Age     Sex  ... CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  ...             NaN                  NaN              NaN               NaN
1     12-0258  2012   51    MALE  ...             NaN                  NaN              NaN               NaN
2     13-0146  2013   28    MALE  ...             NaN                  NaN              NaN               NaN
3     14-0150  2014   46    MALE  ...             NaN                  NaN              NaN               NaN
4     14-0183  2014   52    MALE  ...             NaN                  NaN              NaN               NaN
...       ...   ...  ...     ...  ...             ...                  ...              ...               ...
7629  14-0128  2014   25    MALE  ...             NaN                  NaN              NaN               NaN
7630  20-1217  2020   62  FEMALE  ...             NaN                  NaN              NaN               NaN
7631  20-1138  2020   50  FEMALE  ...             NaN                  NaN              NaN               NaN
7632  16-0640  2016   36    MALE  ...             NaN                  NaN              NaN               NaN
7633  19-0963  2019   33    MALE  ...               Y                  NaN              NaN               NaN

[7634 rows x 32 columns]
********** afer fillna ***********
           ID  Date  Age     Sex  ... CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  ...
1     12-0258  2012   51    MALE  ...
2     13-0146  2013   28    MALE  ...
3     14-0150  2014   46    MALE  ...
4     14-0183  2014   52    MALE  ...
...       ...   ...  ...     ...  ...             ...                  ...              ...               ...
7629  14-0128  2014   25    MALE  ...
7630  20-1217  2020   62  FEMALE  ...
7631  20-1138  2020   50  FEMALE  ...
7632  16-0640  2016   36    MALE  ...
7633  19-0963  2019   33    MALE  ...               Y

[7634 rows x 32 columns]
------------------------> private dataset:  ./data/accidential_drug_deaths.csv
binning attributes done in DataLoader
------------------------> remove identifier column: ID
identifier removed in DataLoader
------------------------> start encoding remaining single attributes
encode remain: Date
encode remain: Sex
encode remain: Race
encode remain: Residence State
encode remain: Death County
encode remain: Location
encode remain: Location if Other
encode remain: Injury County
encode remain: Injury State
encode remain: Heroin
encode remain: Cocaine
encode remain: Fentanyl
encode remain: Fentanyl Analogue
encode remain: Oxycodone
encode remain: Oxymorphone
encode remain: Ethanol
encode remain: Hydrocodone
encode remain: Benzodiazepine
encode remain: Methadone
encode remain: Amphet
encode remain: Tramad
encode remain: Morphine (Not Heroin)
encode remain: Hydromorphone
encode remain: Xylazine
encode remain: Opiate NOS
encode remain: Any Opioid
encode remain: CardioCondition
encode remain: RespiratoryCondition
encode remain: ObesityCondition
encode remain: DiabetesCondition
encoding remaining single attributes done in DataLoader
************* private data loaded and preprocessed in DataLoader ************
priv df's rows:------------------------>  7634
2021-10-14 19:22:16.657 | INFO     | __main__:run_method:107 - working on eps=10.0, delta=3.4498908254380166e-11, and 
sensitivity=1
------------------------> all two way marginals generated
**************** help debug ************** num of records averaged from all two-way marginals: 7633.419354838709
**************** help debug ************** num of records from marginal count before adding noise: 7633.419354838709  
------------------------> now we decide the noise type:
considering eps: 10.0 , delta: 3.4498908254380166e-11 , sensitivity: 1 , len of marginals: 465
------------------------> noise type: gauss
------------------------> noise parameter: 16.386725928253217
2021-10-14 19:22:23.912 | INFO     | method.synthesizer:anonymize:82 - marginal priv_all_two_way use eps=10.0, noise type:gauss, noise parameter=16.386725928253217, sensitivity:1
------------------------> now we get the estimate of records' num by averaging from nosiy marginals: 7630
2021-10-14 19:22:28.296 | DEBUG    | lib_dpsyn.consistent:consist_views:105 - dependency computed
2021-10-14 19:22:28.665 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:28.679 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:29.033 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:29.046 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:29.397 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:29.410 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:29.759 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:29.772 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:30.136 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:30.148 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:30.511 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:30.523 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:30.875 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:30.888 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:31.426 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:31.439 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:32.066 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:32.077 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:32.442 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:32.453 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:32.818 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:32.831 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:33.196 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:33.211 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:33.582 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:33.597 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:33.969 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:33.981 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:34.438 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:34.450 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:34.874 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:34.886 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:35.468 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:35.486 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:35.944 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:35.954 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:36.316 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:36.329 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:36.688 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:36.698 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:37.058 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:37.071 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:37.441 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:37.454 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:37.821 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:37.833 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:38.219 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:38.232 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:38.590 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:38.601 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:38.963 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:38.977 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:39.335 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:39.348 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:39.762 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:39.775 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:40.202 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:40.215 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-14 19:22:40.615 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-14 19:22:40.627 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
------------------------> attributes: 
['Date', 'Age', 'Sex', 'Race', 'Residence State', 'Death County', 'Location', 'Location if Other', 'Injury County', 'Injury State', 'Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl Analogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine (Not Heroin)', 'Hydromorphone', 'Xylazine', 'Opiate NOS', 'Any Opioid', 'CardioCondition', 'RespiratoryCondition', 'ObesityCondition', 'DiabetesCondition']
------------------------> domains:
[ 9  9  2  7 11  9  7 10 15  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2
  2  2  2  2  2  2  2]
------------------------> cluseters:
{('Date', 'Injury County', 'Opiate NOS', 'Hydromorphone', 'CardioCondition', 'Amphet', 'Heroin', 'ObesityCondition', 'Location', 'Death County', 'Hydrocodone', 'Xylazine', 'DiabetesCondition', 'Tramad', 'Oxycodone', 'Age', 'Fentanyl Analogue', 'Fentanyl', 'Injury State', 'Race', 'Location if Other', 'Any Opioid', 'Oxymorphone', 'Morphine (Not Heroin)', 'Sex', 'Cocaine', 'RespiratoryCondition', 'Methadone', 'Residence State', 'Ethanol', 'Benzodiazepine'): [frozenset({'Date', 'Age'}), frozenset({'Date', 'Sex'}), frozenset({'Date', 'Race'}), frozenset({'Date', 'Residence State'}), frozenset({'Date', 'Death County'}), frozenset({'Date', 'Location'}), frozenset({'Date', 'Location if Other'}), frozenset({'Date', 'Injury County'}), frozenset({'Date', 'Injury State'}), frozenset({'Date', 'Heroin'}), frozenset({'Date', 'Cocaine'}), frozenset({'Date', 'Fentanyl'}), frozenset({'Date', 'Fentanyl Analogue'}), frozenset({'Date', 'Oxycodone'}), 
frozenset({'Oxymorphone', 'Date'}), frozenset({'Date', 'Ethanol'}), frozenset({'Date', 'Hydrocodone'}), frozenset({'Date', 'Benzodiazepine'}), frozenset({'Date', 'Methadone'}), frozenset({'Date', 'Amphet'}), frozenset({'Date', 'Tramad'}), frozenset({'Date', 'Morphine (Not Heroin)'}), frozenset({'Date', 'Hydromorphone'}), frozenset({'Date', 'Xylazine'}), frozenset({'Opiate NOS', 'Date'}), frozenset({'Date', 'Any Opioid'}), frozenset({'Date', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Date'}), frozenset({'Date', 'ObesityCondition'}), frozenset({'Date', 'DiabetesCondition'}), frozenset({'Age', 'Sex'}), frozenset({'Age', 'Race'}), frozenset({'Age', 'Residence State'}), frozenset({'Age', 'Death County'}), frozenset({'Age', 'Location'}), frozenset({'Age', 'Location if Other'}), frozenset({'Age', 'Injury County'}), frozenset({'Age', 'Injury State'}), frozenset({'Age', 'Heroin'}), frozenset({'Age', 'Cocaine'}), frozenset({'Age', 'Fentanyl'}), frozenset({'Age', 'Fentanyl Analogue'}), frozenset({'Age', 'Oxycodone'}), frozenset({'Oxymorphone', 'Age'}), frozenset({'Age', 'Ethanol'}), frozenset({'Age', 'Hydrocodone'}), frozenset({'Age', 'Benzodiazepine'}), frozenset({'Age', 'Methadone'}), frozenset({'Age', 'Amphet'}), frozenset({'Age', 'Tramad'}), frozenset({'Age', 'Morphine (Not Heroin)'}), frozenset({'Age', 'Hydromorphone'}), frozenset({'Age', 'Xylazine'}), frozenset({'Opiate NOS', 'Age'}), frozenset({'Age', 'Any Opioid'}), frozenset({'Age', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Age'}), 
frozenset({'Age', 'ObesityCondition'}), frozenset({'Age', 'DiabetesCondition'}), frozenset({'Race', 'Sex'}), frozenset({'Sex', 'Residence State'}), frozenset({'Sex', 'Death County'}), frozenset({'Location', 'Sex'}), frozenset({'Sex', 'Location if Other'}), frozenset({'Injury County', 'Sex'}), frozenset({'Sex', 'Injury State'}), frozenset({'Heroin', 'Sex'}), frozenset({'Sex', 'Cocaine'}), frozenset({'Fentanyl', 'Sex'}), frozenset({'Fentanyl Analogue', 'Sex'}), frozenset({'Sex', 'Oxycodone'}), frozenset({'Oxymorphone', 'Sex'}), frozenset({'Ethanol', 'Sex'}), frozenset({'Sex', 'Hydrocodone'}), frozenset({'Sex', 'Benzodiazepine'}), frozenset({'Methadone', 'Sex'}), frozenset({'Sex', 'Amphet'}), frozenset({'Tramad', 'Sex'}), frozenset({'Morphine (Not Heroin)', 'Sex'}), frozenset({'Sex', 'Hydromorphone'}), frozenset({'Sex', 'Xylazine'}), frozenset({'Opiate NOS', 'Sex'}), frozenset({'Sex', 'Any Opioid'}), frozenset({'CardioCondition', 'Sex'}), frozenset({'RespiratoryCondition', 'Sex'}), frozenset({'ObesityCondition', 'Sex'}), frozenset({'DiabetesCondition', 'Sex'}), frozenset({'Race', 'Residence State'}), frozenset({'Race', 'Death County'}), frozenset({'Race', 'Location'}), frozenset({'Race', 'Location if Other'}), frozenset({'Injury County', 'Race'}), frozenset({'Race', 'Injury State'}), frozenset({'Heroin', 'Race'}), frozenset({'Race', 'Cocaine'}), frozenset({'Race', 'Fentanyl'}), frozenset({'Race', 'Fentanyl Analogue'}), frozenset({'Race', 'Oxycodone'}), frozenset({'Oxymorphone', 'Race'}), frozenset({'Ethanol', 'Race'}), frozenset({'Race', 'Hydrocodone'}), frozenset({'Race', 'Benzodiazepine'}), frozenset({'Methadone', 'Race'}), frozenset({'Race', 'Amphet'}), frozenset({'Race', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Race'}), frozenset({'Race', 'Hydromorphone'}), frozenset({'Race', 'Xylazine'}), frozenset({'Opiate NOS', 'Race'}), frozenset({'Race', 'Any Opioid'}), frozenset({'Race', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Race'}), frozenset({'ObesityCondition', 'Race'}), frozenset({'Race', 'DiabetesCondition'}), frozenset({'Death County', 'Residence State'}), frozenset({'Location', 'Residence State'}), frozenset({'Location if Other', 'Residence State'}), frozenset({'Injury County', 'Residence State'}), frozenset({'Injury State', 'Residence State'}), frozenset({'Heroin', 'Residence State'}), frozenset({'Cocaine', 'Residence State'}), frozenset({'Fentanyl', 'Residence State'}), frozenset({'Fentanyl Analogue', 'Residence State'}), frozenset({'Oxycodone', 'Residence State'}), frozenset({'Oxymorphone', 'Residence State'}), frozenset({'Ethanol', 'Residence State'}), frozenset({'Hydrocodone', 'Residence State'}), frozenset({'Benzodiazepine', 'Residence 
State'}), frozenset({'Methadone', 'Residence State'}), frozenset({'Amphet', 'Residence State'}), frozenset({'Tramad', 
'Residence State'}), frozenset({'Morphine (Not Heroin)', 'Residence State'}), frozenset({'Hydromorphone', 'Residence State'}), frozenset({'Xylazine', 'Residence State'}), frozenset({'Opiate NOS', 'Residence State'}), frozenset({'Any Opioid', 'Residence State'}), frozenset({'CardioCondition', 'Residence State'}), frozenset({'RespiratoryCondition', 'Residence State'}), frozenset({'ObesityCondition', 'Residence State'}), frozenset({'DiabetesCondition', 'Residence State'}), frozenset({'Location', 'Death County'}), frozenset({'Location if Other', 'Death County'}), frozenset({'Injury County', 'Death County'}), frozenset({'Death County', 'Injury State'}), frozenset({'Heroin', 'Death County'}), frozenset({'Death County', 'Cocaine'}), frozenset({'Fentanyl', 'Death County'}), frozenset({'Fentanyl Analogue', 'Death County'}), frozenset({'Death County', 'Oxycodone'}), frozenset({'Oxymorphone', 'Death County'}), frozenset({'Ethanol', 'Death County'}), frozenset({'Death County', 'Hydrocodone'}), frozenset({'Death County', 'Benzodiazepine'}), frozenset({'Methadone', 'Death County'}), frozenset({'Death County', 'Amphet'}), frozenset({'Tramad', 'Death County'}), frozenset({'Morphine (Not Heroin)', 'Death County'}), frozenset({'Hydromorphone', 'Death County'}), frozenset({'Death County', 'Xylazine'}), frozenset({'Opiate NOS', 'Death County'}), frozenset({'Death County', 'Any Opioid'}), frozenset({'CardioCondition', 'Death County'}), frozenset({'RespiratoryCondition', 'Death County'}), frozenset({'ObesityCondition', 'Death County'}), frozenset({'DiabetesCondition', 'Death County'}), frozenset({'Location', 'Location if Other'}), frozenset({'Injury County', 'Location'}), frozenset({'Location', 'Injury State'}), frozenset({'Heroin', 'Location'}), frozenset({'Location', 'Cocaine'}), frozenset({'Fentanyl', 'Location'}), frozenset({'Fentanyl Analogue', 'Location'}), frozenset({'Location', 'Oxycodone'}), frozenset({'Oxymorphone', 'Location'}), frozenset({'Ethanol', 'Location'}), frozenset({'Location', 'Hydrocodone'}), frozenset({'Location', 'Benzodiazepine'}), frozenset({'Methadone', 'Location'}), frozenset({'Location', 'Amphet'}), frozenset({'Tramad', 'Location'}), frozenset({'Morphine (Not Heroin)', 'Location'}), frozenset({'Location', 'Hydromorphone'}), frozenset({'Location', 'Xylazine'}), frozenset({'Opiate NOS', 'Location'}), frozenset({'Location', 'Any Opioid'}), frozenset({'CardioCondition', 'Location'}), frozenset({'RespiratoryCondition', 'Location'}), frozenset({'ObesityCondition', 'Location'}), frozenset({'DiabetesCondition', 'Location'}), frozenset({'Injury County', 'Location if Other'}), frozenset({'Location if Other', 'Injury State'}), frozenset({'Heroin', 'Location if Other'}), frozenset({'Location if Other', 'Cocaine'}), frozenset({'Fentanyl', 'Location if Other'}), frozenset({'Fentanyl Analogue', 'Location if Other'}), frozenset({'Location if Other', 'Oxycodone'}), frozenset({'Oxymorphone', 'Location if Other'}), frozenset({'Ethanol', 'Location if Other'}), frozenset({'Location if Other', 'Hydrocodone'}), frozenset({'Location if Other', 'Benzodiazepine'}), frozenset({'Methadone', 'Location if Other'}), frozenset({'Location if Other', 'Amphet'}), frozenset({'Tramad', 'Location if Other'}), frozenset({'Morphine (Not Heroin)', 'Location if Other'}), frozenset({'Hydromorphone', 'Location if Other'}), frozenset({'Location if Other', 'Xylazine'}), frozenset({'Opiate NOS', 'Location if Other'}), frozenset({'Location if Other', 'Any Opioid'}), frozenset({'CardioCondition', 'Location if Other'}), frozenset({'RespiratoryCondition', 'Location if Other'}), frozenset({'ObesityCondition', 'Location if Other'}), frozenset({'DiabetesCondition', 'Location if Other'}), frozenset({'Injury County', 'Injury State'}), frozenset({'Heroin', 'Injury County'}), frozenset({'Injury County', 'Cocaine'}), frozenset({'Injury County', 'Fentanyl'}), frozenset({'Injury County', 'Fentanyl Analogue'}), frozenset({'Injury County', 'Oxycodone'}), frozenset({'Oxymorphone', 'Injury County'}), frozenset({'Injury County', 'Ethanol'}), frozenset({'Injury County', 'Hydrocodone'}), frozenset({'Injury County', 'Benzodiazepine'}), frozenset({'Methadone', 'Injury County'}), frozenset({'Injury County', 'Amphet'}), frozenset({'Injury County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury County'}), frozenset({'Injury County', 'Hydromorphone'}), frozenset({'Injury County', 'Xylazine'}), frozenset({'Opiate NOS', 'Injury County'}), frozenset({'Injury County', 'Any Opioid'}), frozenset({'Injury County', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Injury County'}), frozenset({'Injury County', 'ObesityCondition'}), frozenset({'Injury County', 'DiabetesCondition'}), frozenset({'Heroin', 'Injury State'}), frozenset({'Cocaine', 'Injury State'}), frozenset({'Fentanyl', 'Injury State'}), frozenset({'Fentanyl Analogue', 'Injury State'}), frozenset({'Oxycodone', 'Injury State'}), frozenset({'Oxymorphone', 'Injury State'}), frozenset({'Ethanol', 'Injury State'}), frozenset({'Hydrocodone', 'Injury State'}), frozenset({'Benzodiazepine', 'Injury State'}), frozenset({'Methadone', 'Injury State'}), frozenset({'Amphet', 'Injury State'}), frozenset({'Tramad', 'Injury State'}), frozenset({'Morphine (Not Heroin)', 'Injury State'}), frozenset({'Hydromorphone', 'Injury State'}), frozenset({'Xylazine', 'Injury State'}), frozenset({'Opiate NOS', 'Injury State'}), frozenset({'Any Opioid', 'Injury State'}), frozenset({'CardioCondition', 'Injury State'}), frozenset({'RespiratoryCondition', 'Injury State'}), 
frozenset({'ObesityCondition', 'Injury State'}), frozenset({'DiabetesCondition', 'Injury State'}), frozenset({'Heroin', 'Cocaine'}), frozenset({'Heroin', 'Fentanyl'}), frozenset({'Heroin', 'Fentanyl Analogue'}), frozenset({'Heroin', 'Oxycodone'}), frozenset({'Oxymorphone', 'Heroin'}), frozenset({'Heroin', 'Ethanol'}), frozenset({'Heroin', 'Hydrocodone'}), frozenset({'Heroin', 'Benzodiazepine'}), frozenset({'Heroin', 'Methadone'}), frozenset({'Heroin', 'Amphet'}), frozenset({'Heroin', 'Tramad'}), frozenset({'Heroin', 'Morphine (Not Heroin)'}), frozenset({'Heroin', 'Hydromorphone'}), frozenset({'Heroin', 'Xylazine'}), frozenset({'Opiate NOS', 'Heroin'}), frozenset({'Heroin', 'Any Opioid'}), frozenset({'Heroin', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Heroin'}), frozenset({'Heroin', 'ObesityCondition'}), frozenset({'Heroin', 'DiabetesCondition'}), frozenset({'Fentanyl', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Cocaine'}), frozenset({'Oxycodone', 'Cocaine'}), frozenset({'Oxymorphone', 'Cocaine'}), frozenset({'Ethanol', 'Cocaine'}), frozenset({'Cocaine', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Cocaine'}), frozenset({'Methadone', 'Cocaine'}), frozenset({'Cocaine', 'Amphet'}), frozenset({'Tramad', 'Cocaine'}), frozenset({'Morphine (Not Heroin)', 'Cocaine'}), frozenset({'Hydromorphone', 'Cocaine'}), frozenset({'Xylazine', 'Cocaine'}), frozenset({'Opiate NOS', 'Cocaine'}), 
frozenset({'Cocaine', 'Any Opioid'}), frozenset({'CardioCondition', 'Cocaine'}), frozenset({'RespiratoryCondition', 'Cocaine'}), frozenset({'ObesityCondition', 'Cocaine'}), frozenset({'DiabetesCondition', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Fentanyl'}), frozenset({'Fentanyl', 'Oxycodone'}), frozenset({'Oxymorphone', 'Fentanyl'}), frozenset({'Ethanol', 'Fentanyl'}), frozenset({'Fentanyl', 'Hydrocodone'}), frozenset({'Fentanyl', 'Benzodiazepine'}), frozenset({'Methadone', 'Fentanyl'}), frozenset({'Fentanyl', 'Amphet'}), frozenset({'Tramad', 'Fentanyl'}), frozenset({'Morphine 
(Not Heroin)', 'Fentanyl'}), frozenset({'Fentanyl', 'Hydromorphone'}), frozenset({'Fentanyl', 'Xylazine'}), frozenset({'Opiate NOS', 'Fentanyl'}), frozenset({'Fentanyl', 'Any Opioid'}), frozenset({'CardioCondition', 'Fentanyl'}), frozenset({'RespiratoryCondition', 'Fentanyl'}), frozenset({'ObesityCondition', 'Fentanyl'}), frozenset({'DiabetesCondition', 'Fentanyl'}), frozenset({'Fentanyl Analogue', 'Oxycodone'}), frozenset({'Oxymorphone', 'Fentanyl Analogue'}), frozenset({'Ethanol', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Hydrocodone'}), frozenset({'Fentanyl Analogue', 'Benzodiazepine'}), frozenset({'Methadone', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Amphet'}), frozenset({'Fentanyl Analogue', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Hydromorphone'}), frozenset({'Fentanyl Analogue', 'Xylazine'}), frozenset({'Opiate NOS', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Any Opioid'}), frozenset({'Fentanyl Analogue', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Fentanyl Analogue'}), frozenset({'ObesityCondition', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'DiabetesCondition'}), frozenset({'Oxymorphone', 'Oxycodone'}), frozenset({'Ethanol', 'Oxycodone'}), frozenset({'Oxycodone', 'Hydrocodone'}), frozenset({'Oxycodone', 'Benzodiazepine'}), frozenset({'Methadone', 'Oxycodone'}), frozenset({'Oxycodone', 'Amphet'}), frozenset({'Tramad', 'Oxycodone'}), frozenset({'Morphine (Not Heroin)', 'Oxycodone'}), frozenset({'Hydromorphone', 'Oxycodone'}), frozenset({'Oxycodone', 'Xylazine'}), frozenset({'Opiate NOS', 'Oxycodone'}), frozenset({'Oxycodone', 'Any Opioid'}), frozenset({'CardioCondition', 'Oxycodone'}), frozenset({'RespiratoryCondition', 'Oxycodone'}), frozenset({'ObesityCondition', 'Oxycodone'}), frozenset({'DiabetesCondition', 'Oxycodone'}), frozenset({'Oxymorphone', 'Ethanol'}), frozenset({'Oxymorphone', 'Hydrocodone'}), frozenset({'Oxymorphone', 'Benzodiazepine'}), frozenset({'Oxymorphone', 'Methadone'}), frozenset({'Oxymorphone', 'Amphet'}), frozenset({'Oxymorphone', 'Tramad'}), frozenset({'Oxymorphone', 'Morphine (Not Heroin)'}), frozenset({'Oxymorphone', 'Hydromorphone'}), frozenset({'Oxymorphone', 'Xylazine'}), frozenset({'Oxymorphone', 'Opiate NOS'}), frozenset({'Oxymorphone', 'Any Opioid'}), 
frozenset({'Oxymorphone', 'CardioCondition'}), frozenset({'Oxymorphone', 'RespiratoryCondition'}), frozenset({'Oxymorphone', 'ObesityCondition'}), frozenset({'Oxymorphone', 'DiabetesCondition'}), frozenset({'Ethanol', 'Hydrocodone'}), frozenset({'Ethanol', 'Benzodiazepine'}), frozenset({'Methadone', 'Ethanol'}), frozenset({'Ethanol', 'Amphet'}), frozenset({'Ethanol', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Ethanol'}), frozenset({'Ethanol', 'Hydromorphone'}), 
frozenset({'Ethanol', 'Xylazine'}), frozenset({'Opiate NOS', 'Ethanol'}), frozenset({'Ethanol', 'Any Opioid'}), frozenset({'Ethanol', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Ethanol'}), frozenset({'ObesityCondition', 'Ethanol'}), frozenset({'Ethanol', 'DiabetesCondition'}), frozenset({'Benzodiazepine', 'Hydrocodone'}), frozenset({'Methadone', 'Hydrocodone'}), frozenset({'Hydrocodone', 'Amphet'}), frozenset({'Tramad', 'Hydrocodone'}), frozenset({'Morphine (Not Heroin)', 'Hydrocodone'}), frozenset({'Hydromorphone', 'Hydrocodone'}), frozenset({'Xylazine', 'Hydrocodone'}), frozenset({'Opiate NOS', 'Hydrocodone'}), frozenset({'Hydrocodone', 'Any Opioid'}), frozenset({'CardioCondition', 'Hydrocodone'}), frozenset({'RespiratoryCondition', 'Hydrocodone'}), frozenset({'ObesityCondition', 'Hydrocodone'}), frozenset({'DiabetesCondition', 'Hydrocodone'}), frozenset({'Methadone', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Amphet'}), frozenset({'Tramad', 'Benzodiazepine'}), frozenset({'Morphine (Not Heroin)', 'Benzodiazepine'}), frozenset({'Hydromorphone', 'Benzodiazepine'}), frozenset({'Xylazine', 'Benzodiazepine'}), frozenset({'Opiate NOS', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Any Opioid'}), frozenset({'CardioCondition', 'Benzodiazepine'}), frozenset({'RespiratoryCondition', 'Benzodiazepine'}), frozenset({'ObesityCondition', 'Benzodiazepine'}), frozenset({'DiabetesCondition', 'Benzodiazepine'}), frozenset({'Methadone', 'Amphet'}), frozenset({'Methadone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Methadone'}), frozenset({'Methadone', 'Hydromorphone'}), frozenset({'Methadone', 'Xylazine'}), frozenset({'Opiate NOS', 'Methadone'}), frozenset({'Methadone', 'Any Opioid'}), frozenset({'Methadone', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Methadone'}), frozenset({'Methadone', 'ObesityCondition'}), frozenset({'Methadone', 'DiabetesCondition'}), frozenset({'Tramad', 'Amphet'}), frozenset({'Morphine (Not Heroin)', 'Amphet'}), frozenset({'Hydromorphone', 'Amphet'}), frozenset({'Xylazine', 'Amphet'}), frozenset({'Opiate NOS', 'Amphet'}), frozenset({'Any Opioid', 'Amphet'}), frozenset({'CardioCondition', 'Amphet'}), frozenset({'RespiratoryCondition', 'Amphet'}), frozenset({'ObesityCondition', 'Amphet'}), frozenset({'DiabetesCondition', 'Amphet'}), frozenset({'Morphine (Not Heroin)', 'Tramad'}), frozenset({'Tramad', 'Hydromorphone'}), frozenset({'Tramad', 'Xylazine'}), frozenset({'Opiate NOS', 'Tramad'}), frozenset({'Tramad', 'Any Opioid'}), frozenset({'CardioCondition', 'Tramad'}), frozenset({'RespiratoryCondition', 
'Tramad'}), frozenset({'ObesityCondition', 'Tramad'}), frozenset({'DiabetesCondition', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Hydromorphone'}), frozenset({'Morphine (Not Heroin)', 'Xylazine'}), frozenset({'Opiate NOS', 'Morphine (Not Heroin)'}), frozenset({'Morphine (Not Heroin)', 'Any Opioid'}), frozenset({'Morphine (Not Heroin)', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Morphine (Not Heroin)'}), frozenset({'Morphine (Not Heroin)', 'ObesityCondition'}), frozenset({'Morphine (Not Heroin)', 'DiabetesCondition'}), frozenset({'Hydromorphone', 'Xylazine'}), frozenset({'Opiate NOS', 'Hydromorphone'}), frozenset({'Hydromorphone', 'Any Opioid'}), frozenset({'CardioCondition', 'Hydromorphone'}), frozenset({'RespiratoryCondition', 'Hydromorphone'}), frozenset({'ObesityCondition', 'Hydromorphone'}), frozenset({'DiabetesCondition', 'Hydromorphone'}), frozenset({'Opiate NOS', 'Xylazine'}), frozenset({'Xylazine', 'Any Opioid'}), frozenset({'CardioCondition', 'Xylazine'}), frozenset({'RespiratoryCondition', 'Xylazine'}), frozenset({'ObesityCondition', 'Xylazine'}), frozenset({'DiabetesCondition', 'Xylazine'}), frozenset({'Opiate NOS', 'Any Opioid'}), frozenset({'Opiate NOS', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Opiate NOS'}), frozenset({'Opiate NOS', 'ObesityCondition'}), frozenset({'Opiate NOS', 'DiabetesCondition'}), frozenset({'CardioCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'Any Opioid'}), frozenset({'ObesityCondition', 'Any Opioid'}), frozenset({'DiabetesCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 
'CardioCondition'}), frozenset({'CardioCondition', 'DiabetesCondition'}), frozenset({'RespiratoryCondition', 'ObesityCondition'}), frozenset({'RespiratoryCondition', 'DiabetesCondition'}), frozenset({'ObesityCondition', 'DiabetesCondition'})]}
********************* START SYNTHESIZING RECORDS ********************
------------------------> num of synthesized records:
7630
2021-10-14 19:22:40.684 | INFO     | method.dpsyn:synthesize_records:161 - synthesizing for ('Date', 'Injury County', 
'Opiate NOS', 'Hydromorphone', 'CardioCondition', 'Amphet', 'Heroin', 'ObesityCondition', 'Location', 'Death County', 
'Hydrocodone', 'Xylazine', 'DiabetesCondition', 'Tramad', 'Oxycodone', 'Age', 'Fentanyl Analogue', 'Fentanyl', 'Injury State', 'Race', 'Location if Other', 'Any Opioid', 'Oxymorphone', 'Morphine (Not Heroin)', 'Sex', 'Cocaine', 'RespiratoryCondition', 'Methadone', 'Residence State', 'Ethanol', 'Benzodiazepine')
2021-10-14 19:22:40.694 | INFO     | method.dpsyn:synthesize_records:177 - update round: 0
2021-10-14 19:22:41.429 | INFO     | method.dpsyn:synthesize_records:177 - update round: 1
2021-10-14 19:22:42.224 | INFO     | method.dpsyn:synthesize_records:177 - update round: 2
2021-10-14 19:22:42.986 | INFO     | method.dpsyn:synthesize_records:177 - update round: 3
2021-10-14 19:22:43.752 | INFO     | method.dpsyn:synthesize_records:177 - update round: 4
2021-10-14 19:22:44.516 | INFO     | method.dpsyn:synthesize_records:177 - update round: 5
2021-10-14 19:22:45.297 | INFO     | method.dpsyn:synthesize_records:177 - update round: 6
2021-10-14 19:22:46.090 | INFO     | method.dpsyn:synthesize_records:177 - update round: 7
2021-10-14 19:22:46.955 | INFO     | method.dpsyn:synthesize_records:177 - update round: 8
2021-10-14 19:22:47.915 | INFO     | method.dpsyn:synthesize_records:177 - update round: 9
2021-10-14 19:22:48.865 | INFO     | method.dpsyn:synthesize_records:177 - update round: 10
2021-10-14 19:22:49.766 | INFO     | method.dpsyn:synthesize_records:177 - update round: 11
2021-10-14 19:22:50.543 | INFO     | method.dpsyn:synthesize_records:177 - update round: 12
2021-10-14 19:22:51.403 | INFO     | method.dpsyn:synthesize_records:177 - update round: 13
2021-10-14 19:22:52.257 | INFO     | method.dpsyn:synthesize_records:177 - update round: 14
2021-10-14 19:22:53.042 | INFO     | method.dpsyn:synthesize_records:177 - update round: 15
2021-10-14 19:22:53.868 | INFO     | method.dpsyn:synthesize_records:177 - update round: 16
2021-10-14 19:22:54.875 | INFO     | method.dpsyn:synthesize_records:177 - update round: 17
2021-10-14 19:22:55.747 | INFO     | method.dpsyn:synthesize_records:177 - update round: 18
2021-10-14 19:22:56.512 | INFO     | method.dpsyn:synthesize_records:177 - update round: 19
2021-10-14 19:22:57.310 | INFO     | method.dpsyn:synthesize_records:177 - update round: 20
2021-10-14 19:22:58.177 | INFO     | method.dpsyn:synthesize_records:177 - update round: 21
2021-10-14 19:22:59.361 | INFO     | method.dpsyn:synthesize_records:177 - update round: 22
2021-10-14 19:23:00.234 | INFO     | method.dpsyn:synthesize_records:177 - update round: 23
2021-10-14 19:23:01.090 | INFO     | method.dpsyn:synthesize_records:177 - update round: 24
2021-10-14 19:23:02.010 | INFO     | method.dpsyn:synthesize_records:177 - update round: 25
2021-10-14 19:23:02.880 | INFO     | method.dpsyn:synthesize_records:177 - update round: 26
2021-10-14 19:23:03.662 | INFO     | method.dpsyn:synthesize_records:177 - update round: 27
2021-10-14 19:23:04.446 | INFO     | method.dpsyn:synthesize_records:177 - update round: 28
2021-10-14 19:23:05.256 | INFO     | method.dpsyn:synthesize_records:177 - update round: 29
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
2021-10-14 19:23:06.132 | INFO     | __main__:run_method:163 - ------------------------>synthetic data post-processed:      Date  Age     Sex             Race  ... RespiratoryCondition ObesityCondition DiabetesCondition epsilon
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



