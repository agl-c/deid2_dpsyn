# DPSyn: a quick-start guide 
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


## Install DPSyn 

### Docker support

We created a public image in docker.io [link](https://hub.docker.com/repository/docker/chenanqi18pku/dpsyn). You can obtain it by

```
> docker pull chenanqi18pku/dpsyn:v1
```

Or you can directly create the image with the directory here, since the Dockerfile is already included.

```
> docker build -t dpsyn .
```

Then you can create a container to run the image. We show one example below with target_path=syndata.csv and container named 'test'.

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

First, you preprocess the input dataset (the input dataset should be in format of filename.csv with its first row a header row). A [tool]( https://github.com/hd23408/nist-schemagen ) is provided to generate schema files: **(1) [parameters.json](data/parameters.json)** **(2) [column_datatypes.json](data/column_datatypes.json)** from the original dataset.

##### 1. Determine differential privacy parameters (eps, delta, sensitivity)

You should set the **eps, delta, sensitivity value** in 'runs' in **parameters.json** according to their specific differential privacy requirements (refer to [The Algorithmic Foundations of Differential Privacy](http://dx.doi.org/10.1561/0400000042) if you are not familiar with DP). 
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
The next step is to specify marginal settings in marginal config file like **[eps=xxx.yaml](config/eps=10.0.yaml)** (each eps=xxx.yaml corresponds to each epsilon=xxx in parameters.json).

##### 2. Marginal selection config

Suppose epsilon parameter in "runs" of parameters.json is 10 now.  We will go to eps=10.0.yaml to find the marginal configuration. In this example, we use all the two way marginals, i.e., "priv_all_two_way":

```yaml
priv_all_two_way:
  total_eps: 10
```

##### 3. Data config

Finally, you need to config [data.yaml](config/data.yaml): You can specify the **identifier** attribute's name in data.yaml (we assume your dataset has the identifer attribute by default; obviously, in synthetic dataset the column should be removed to protect privacy). You can also specify **bin** settings in the format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. (Further, you can change more details in bin generation in binning_attributes() in DataLoader.py.)

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

Notice that the showed command input **--priv_data_name** as **testpkl**, which we require users to set so that the algorithm won't select a wrong pickled file to utilize.

You can find the default input files in the repository we offered here.

And you can find the synthetic dataset "out.csv" ( under default setting ) in your working directory after the program finishes.

```
>python experiment.py --priv_data_name testpkl 
------------------------> config yaml file loaded in DataLoader, config file:  ./config/data.yaml
------------------------> parameter file loaded in DataLoader, parameter file:  ./data/parameters.json
************* start loading private data *************
------------------------> process and store with pkl file name:  preprocessed_priv_testpkl.pkl
           ID  Date  Age     Sex   Race  ... Any Opioid CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
1     12-0258  2012   51    MALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
2     13-0146  2013   28    MALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
3     14-0150  2014   46    MALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
4     14-0183  2014   52    MALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
...       ...   ...  ...     ...    ...  ...        ...             ...                  ...              ...
 ...
7629  14-0128  2014   25    MALE  WHITE  ...        NaN             NaN                  NaN              NaN
 NaN
7630  20-1217  2020   62  FEMALE  WHITE  ...          Y             NaN                  NaN              NaN
 NaN
7631  20-1138  2020   50  FEMALE  WHITE  ...          Y             NaN                  NaN              NaN
 NaN
7632  16-0640  2016   36    MALE  WHITE  ...          Y             NaN                  NaN              NaN
 NaN
7633  19-0963  2019   33    MALE  WHITE  ...          Y               Y                  NaN              NaN
 NaN

[7634 rows x 32 columns]
********** afer fillna ***********
           ID  Date  Age     Sex   Race  ... Any Opioid CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  WHITE  ...

1     12-0258  2012   51    MALE  WHITE  ...

2     13-0146  2013   28    MALE  WHITE  ...

3     14-0150  2014   46    MALE  WHITE  ...

4     14-0183  2014   52    MALE  WHITE  ...

...       ...   ...  ...     ...    ...  ...        ...             ...                  ...              ...
 ...
7629  14-0128  2014   25    MALE  WHITE  ...

7630  20-1217  2020   62  FEMALE  WHITE  ...          Y

7631  20-1138  2020   50  FEMALE  WHITE  ...          Y

7632  16-0640  2016   36    MALE  WHITE  ...          Y

7633  19-0963  2019   33    MALE  WHITE  ...          Y               Y


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
2021-10-23 09:40:47.932 | INFO     | __main__:run_method:107 - working on eps=10.0, delta=3.4498908254380166e-11, and sensitivity=1
------------------------> all two way marginals generated
**************** help debug ************** num of records averaged from all two-way marginals: 7633.419354838709    
**************** help debug ************** num of records from marginal count before adding noise: 7633.419354838709
------------------------> now we decide the noise type:
considering eps: 10.0 , delta: 3.4498908254380166e-11 , sensitivity: 1 , len of marginals: 465
------------------------> noise type: gauss
------------------------> noise parameter: 16.386725928253217
2021-10-23 09:40:55.373 | INFO     | method.synthesizer:anonymize:79 - marginal priv_all_two_way use eps=10.0, noise type:gauss, noise parameter=16.386725928253217, sensitivity:1
------------------------> now we get the estimate of records' num by averaging from nosiy marginals: 7630
h                                                                                          mputed
2021-10-23 09:41:02.726 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativithy finish                                                                                   y finish
2021-10-23 09:41:03.158 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finishh                                                                                          y finish
2021-10-23 09:41:03.171 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativithy finish                                                                                   y finish
2021-10-23 09:41:03.624 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finishh                                                                                          y finish
2021-10-23 09:41:03.642 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativithy finish                                                                                   y finish
2021-10-23 09:41:04.068 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finishh                                                                                          y finish
2021-10-23 09:41:04.080 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativithy finish                                                                                   y finish
2021-10-23 09:41:04.494 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finishh
2021-10-23 09:41:04.506 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:04.883 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:04.899 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:05.338 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:05.353 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:05.928 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:05.942 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:06.345 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:06.357 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:06.783 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:06.797 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:07.243 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:07.265 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:07.887 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:07.902 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:08.406 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:08.419 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:08.963 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish       
2021-10-23 09:41:08.975 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:09.432 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish       
2021-10-23 09:41:09.447 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:09.843 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish       
2021-10-23 09:41:09.858 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:10.233 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:10.247 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:10.656 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish       
2021-10-23 09:41:10.669 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:11.036 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:11.049 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:11.481 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:11.496 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:11.896 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:11.910 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:12.316 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:12.331 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:12.726 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:12.739 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-23 09:41:13.128 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-23 09:41:13.142 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
------------------------> attributes: 
['Date', 'Age', 'Sex', 'Race', 'Residence State', 'Death County', 'Location', 'Location if Other', 'Injury County', 'Injury State', 'Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl Analogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine (Not Heroin)', 'Hydromorphone', 'Xylazine', 'Opiate NOS', 'Any Opioid', 'CardioCondition', 'RespiratoryCondition', 'ObesityCondition', 'DiabetesCondition']
------------------------> domains:
[ 9  9  2  7 11  9  7 10 15  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2
  2  2  2  2  2  2  2]
------------------------> cluseters:
{('Cocaine', 'Location if Other', 'Age', 'Hydromorphone', 'Tramad', 'Morphine (Not Heroin)', 'RespiratoryCondition', 'Date', 'Heroin', 'Oxymorphone', 'Hydrocodone', 'Injury State', 'Opiate NOS', 'Location', 'Sex', 'Benzodiazepine', 'Oxycodone', 'Fentanyl Analogue', 'Death County', 'Fentanyl', 'DiabetesCondition', 'Ethanol', 'Residence State', 'Methadone', 'Xylazine', 'ObesityCondition', 'CardioCondition', 'Any Opioid', 'Race', 'Amphet', 'Injury County'): [frozenset({'Age', 'Date'}), frozenset({'Date', 'Sex'}), frozenset({'Race', 'Date'}), frozenset({'Residence State', 'Date'}), frozenset({'Death County', 'Date'}), frozenset({'Location', 'Date'}), frozenset({'Location if Other', 'Date'}), frozenset({'Date', 'Injury County'}), frozenset({'Injury State', 'Date'}), frozenset({'Heroin', 'Date'}), frozenset({'Cocaine', 'Date'}), frozenset({'Fentanyl', 'Date'}), frozenset({'Fentanyl Analogue', 'Date'}), frozenset({'Date', 'Oxycodone'}), frozenset({'Date', 'Oxymorphone'}), frozenset({'Ethanol', 'Date'}), frozenset({'Hydrocodone', 'Date'}), frozenset({'Benzodiazepine', 'Date'}), frozenset({'Date', 'Methadone'}), frozenset({'Amphet', 'Date'}), frozenset({'Date', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Date'}), frozenset({'Hydromorphone', 'Date'}), frozenset({'Date', 'Xylazine'}), frozenset({'Date', 'Opiate NOS'}), frozenset({'Any Opioid', 'Date'}), frozenset({'CardioCondition', 'Date'}), frozenset({'RespiratoryCondition', 'Date'}), frozenset({'ObesityCondition', 'Date'}), frozenset({'DiabetesCondition', 'Date'}), frozenset({'Age', 'Sex'}), frozenset({'Race', 'Age'}), frozenset({'Age', 'Residence State'}), frozenset({'Death County', 'Age'}), frozenset({'Location', 'Age'}), frozenset({'Location if Other', 'Age'}), frozenset({'Age', 'Injury County'}), frozenset({'Age', 'Injury State'}), frozenset({'Age', 'Heroin'}), frozenset({'Cocaine', 'Age'}), frozenset({'Fentanyl', 'Age'}), frozenset({'Age', 'Fentanyl Analogue'}), frozenset({'Age', 'Oxycodone'}), frozenset({'Age', 'Oxymorphone'}), frozenset({'Age', 
'Ethanol'}), frozenset({'Hydrocodone', 'Age'}), frozenset({'Age', 'Benzodiazepine'}), frozenset({'Age', 'Methadone'}), frozenset({'Age', 'Amphet'}), frozenset({'Age', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Age'}), frozenset({'Age', 'Hydromorphone'}), frozenset({'Age', 'Xylazine'}), frozenset({'Age', 'Opiate NOS'}), frozenset({'Age', 'Any Opioid'}), frozenset({'Age', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Age'}), frozenset({'ObesityCondition', 'Age'}), frozenset({'DiabetesCondition', 'Age'}), frozenset({'Race', 'Sex'}), frozenset({'Residence State', 'Sex'}), frozenset({'Death County', 'Sex'}), frozenset({'Location', 'Sex'}), frozenset({'Location if Other', 'Sex'}), frozenset({'Sex', 'Injury County'}), frozenset({'Injury State', 'Sex'}), frozenset({'Heroin', 'Sex'}), frozenset({'Cocaine', 'Sex'}), frozenset({'Fentanyl', 'Sex'}), frozenset({'Fentanyl Analogue', 'Sex'}), frozenset({'Sex', 'Oxycodone'}), frozenset({'Sex', 'Oxymorphone'}), frozenset({'Ethanol', 'Sex'}), frozenset({'Hydrocodone', 'Sex'}), frozenset({'Benzodiazepine', 'Sex'}), frozenset({'Sex', 'Methadone'}), frozenset({'Amphet', 'Sex'}), frozenset({'Sex', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Sex'}), frozenset({'Hydromorphone', 'Sex'}), frozenset({'Sex', 'Xylazine'}), frozenset({'Sex', 'Opiate NOS'}), frozenset({'Any Opioid', 'Sex'}), frozenset({'CardioCondition', 'Sex'}), frozenset({'RespiratoryCondition', 'Sex'}), frozenset({'ObesityCondition', 
'Sex'}), frozenset({'DiabetesCondition', 'Sex'}), frozenset({'Race', 'Residence State'}), frozenset({'Death County', 'Race'}), frozenset({'Location', 'Race'}), frozenset({'Race', 'Location if Other'}), frozenset({'Race', 'Injury County'}), frozenset({'Race', 'Injury State'}), frozenset({'Race', 'Heroin'}), frozenset({'Cocaine', 'Race'}), frozenset({'Fentanyl', 'Race'}), frozenset({'Race', 'Fentanyl Analogue'}), frozenset({'Race', 'Oxycodone'}), frozenset({'Race', 'Oxymorphone'}), frozenset({'Race', 'Ethanol'}), frozenset({'Race', 'Hydrocodone'}), frozenset({'Race', 'Benzodiazepine'}), frozenset({'Race', 'Methadone'}), frozenset({'Race', 'Amphet'}), frozenset({'Race', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Race'}), frozenset({'Race', 'Hydromorphone'}), frozenset({'Race', 
'Xylazine'}), frozenset({'Race', 'Opiate NOS'}), frozenset({'Race', 'Any Opioid'}), frozenset({'Race', 'CardioCondition'}), frozenset({'Race', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Race'}), frozenset({'Race', 'DiabetesCondition'}), frozenset({'Death County', 'Residence State'}), frozenset({'Location', 'Residence State'}), frozenset({'Location if Other', 'Residence State'}), frozenset({'Residence State', 'Injury County'}), frozenset({'Injury State', 'Residence State'}), frozenset({'Residence State', 'Heroin'}), frozenset({'Cocaine', 'Residence State'}), frozenset({'Fentanyl', 'Residence State'}), frozenset({'Residence State', 'Fentanyl Analogue'}), frozenset({'Residence State', 'Oxycodone'}), frozenset({'Residence State', 'Oxymorphone'}), frozenset({'Ethanol', 'Residence State'}), frozenset({'Hydrocodone', 'Residence State'}), frozenset({'Residence State', 'Benzodiazepine'}), frozenset({'Residence State', 'Methadone'}), frozenset({'Amphet', 'Residence State'}), frozenset({'Residence 
State', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Residence State'}), frozenset({'Hydromorphone', 'Residence State'}), frozenset({'Residence State', 'Xylazine'}), frozenset({'Residence State', 'Opiate NOS'}), frozenset({'Any Opioid', 'Residence State'}), frozenset({'CardioCondition', 'Residence State'}), frozenset({'RespiratoryCondition', 'Residence State'}), frozenset({'ObesityCondition', 'Residence State'}), frozenset({'DiabetesCondition', 'Residence State'}), frozenset({'Death County', 'Location'}), frozenset({'Death County', 'Location if Other'}), 
frozenset({'Death County', 'Injury County'}), frozenset({'Death County', 'Injury State'}), frozenset({'Death County', 'Heroin'}), frozenset({'Death County', 'Cocaine'}), frozenset({'Death County', 'Fentanyl'}), frozenset({'Death County', 'Fentanyl Analogue'}), frozenset({'Death County', 'Oxycodone'}), frozenset({'Death County', 'Oxymorphone'}), frozenset({'Death County', 'Ethanol'}), frozenset({'Death County', 'Hydrocodone'}), frozenset({'Death County', 'Benzodiazepine'}), frozenset({'Death County', 'Methadone'}), frozenset({'Death County', 'Amphet'}), frozenset({'Death County', 'Tramad'}), frozenset({'Death County', 'Morphine (Not Heroin)'}), frozenset({'Death County', 'Hydromorphone'}), frozenset({'Death County', 'Xylazine'}), frozenset({'Death County', 'Opiate NOS'}), frozenset({'Death County', 'Any Opioid'}), frozenset({'Death County', 'CardioCondition'}), frozenset({'Death County', 'RespiratoryCondition'}), frozenset({'Death County', 'ObesityCondition'}), frozenset({'Death County', 'DiabetesCondition'}), frozenset({'Location', 'Location if Other'}), frozenset({'Location', 'Injury County'}), frozenset({'Location', 'Injury State'}), frozenset({'Location', 'Heroin'}), frozenset({'Cocaine', 'Location'}), frozenset({'Fentanyl', 'Location'}), frozenset({'Location', 'Fentanyl Analogue'}), frozenset({'Location', 'Oxycodone'}), frozenset({'Location', 'Oxymorphone'}), frozenset({'Location', 'Ethanol'}), frozenset({'Location', 'Hydrocodone'}), frozenset({'Location', 'Benzodiazepine'}), frozenset({'Location', 'Methadone'}), frozenset({'Location', 'Amphet'}), frozenset({'Location', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Location'}), frozenset({'Location', 'Hydromorphone'}), frozenset({'Location', 'Xylazine'}), frozenset({'Location', 'Opiate NOS'}), frozenset({'Location', 'Any Opioid'}), frozenset({'Location', 'CardioCondition'}), frozenset({'Location', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Location'}), frozenset({'Location', 'DiabetesCondition'}), frozenset({'Location if Other', 'Injury County'}), frozenset({'Location if Other', 'Injury State'}), frozenset({'Location if Other', 'Heroin'}), frozenset({'Cocaine', 'Location if Other'}), frozenset({'Fentanyl', 'Location if Other'}), frozenset({'Location if Other', 'Fentanyl Analogue'}), frozenset({'Location if Other', 'Oxycodone'}), frozenset({'Location if Other', 'Oxymorphone'}), frozenset({'Location if Other', 'Ethanol'}), frozenset({'Hydrocodone', 'Location if Other'}), frozenset({'Location if Other', 'Benzodiazepine'}), frozenset({'Location if Other', 'Methadone'}), frozenset({'Location if Other', 'Amphet'}), frozenset({'Location if Other', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Location if Other'}), frozenset({'Location if Other', 'Hydromorphone'}), frozenset({'Location if Other', 'Xylazine'}), frozenset({'Location if Other', 'Opiate NOS'}), frozenset({'Location if Other', 'Any Opioid'}), frozenset({'Location if Other', 'CardioCondition'}), frozenset({'Location if Other', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Location if Other'}), frozenset({'DiabetesCondition', 'Location if Other'}), frozenset({'Injury State', 'Injury County'}), frozenset({'Heroin', 'Injury County'}), frozenset({'Cocaine', 'Injury County'}), frozenset({'Fentanyl', 'Injury County'}), frozenset({'Fentanyl Analogue', 'Injury County'}), frozenset({'Injury County', 'Oxycodone'}), frozenset({'Oxymorphone', 'Injury County'}), frozenset({'Ethanol', 'Injury County'}), frozenset({'Hydrocodone', 'Injury County'}), frozenset({'Benzodiazepine', 'Injury County'}), frozenset({'Methadone', 'Injury County'}), frozenset({'Amphet', 'Injury County'}), frozenset({'Injury County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury County'}), frozenset({'Hydromorphone', 'Injury County'}), frozenset({'Xylazine', 'Injury 
County'}), frozenset({'Injury County', 'Opiate NOS'}), frozenset({'Any Opioid', 'Injury County'}), frozenset({'CardioCondition', 'Injury County'}), frozenset({'RespiratoryCondition', 'Injury County'}), frozenset({'ObesityCondition', 'Injury County'}), frozenset({'DiabetesCondition', 'Injury County'}), frozenset({'Injury State', 'Heroin'}), frozenset({'Cocaine', 'Injury State'}), frozenset({'Fentanyl', 'Injury State'}), frozenset({'Injury State', 'Fentanyl Analogue'}), frozenset({'Injury State', 'Oxycodone'}), frozenset({'Injury State', 'Oxymorphone'}), frozenset({'Injury State', 'Ethanol'}), frozenset({'Hydrocodone', 'Injury State'}), frozenset({'Injury State', 'Benzodiazepine'}), frozenset({'Injury State', 'Methadone'}), frozenset({'Injury State', 'Amphet'}), frozenset({'Injury State', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury State'}), frozenset({'Injury State', 'Hydromorphone'}), frozenset({'Injury State', 'Xylazine'}), frozenset({'Injury State', 'Opiate NOS'}), frozenset({'Injury State', 'Any Opioid'}), frozenset({'Injury State', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Injury State'}), frozenset({'ObesityCondition', 'Injury State'}), frozenset({'DiabetesCondition', 'Injury State'}), frozenset({'Cocaine', 'Heroin'}), frozenset({'Fentanyl', 'Heroin'}), frozenset({'Fentanyl Analogue', 'Heroin'}), frozenset({'Heroin', 'Oxycodone'}), frozenset({'Heroin', 'Oxymorphone'}), frozenset({'Ethanol', 'Heroin'}), frozenset({'Hydrocodone', 'Heroin'}), frozenset({'Benzodiazepine', 'Heroin'}), frozenset({'Heroin', 'Methadone'}), frozenset({'Amphet', 'Heroin'}), frozenset({'Heroin', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Heroin'}), frozenset({'Hydromorphone', 'Heroin'}), frozenset({'Heroin', 'Xylazine'}), frozenset({'Heroin', 'Opiate NOS'}), frozenset({'Any Opioid', 'Heroin'}), frozenset({'CardioCondition', 'Heroin'}), frozenset({'RespiratoryCondition', 'Heroin'}), frozenset({'ObesityCondition', 'Heroin'}), frozenset({'DiabetesCondition', 'Heroin'}), frozenset({'Fentanyl', 'Cocaine'}), frozenset({'Cocaine', 'Fentanyl Analogue'}), frozenset({'Cocaine', 'Oxycodone'}), frozenset({'Cocaine', 'Oxymorphone'}), frozenset({'Cocaine', 'Ethanol'}), frozenset({'Cocaine', 'Hydrocodone'}), frozenset({'Cocaine', 'Benzodiazepine'}), frozenset({'Cocaine', 'Methadone'}), frozenset({'Cocaine', 'Amphet'}), frozenset({'Cocaine', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Cocaine'}), frozenset({'Cocaine', 'Hydromorphone'}), frozenset({'Cocaine', 'Xylazine'}), frozenset({'Cocaine', 'Opiate NOS'}), frozenset({'Cocaine', 'Any Opioid'}), frozenset({'Cocaine', 'CardioCondition'}), frozenset({'Cocaine', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Cocaine'}), frozenset({'Cocaine', 'DiabetesCondition'}), frozenset({'Fentanyl', 'Fentanyl Analogue'}), frozenset({'Fentanyl', 'Oxycodone'}), frozenset({'Fentanyl', 'Oxymorphone'}), frozenset({'Fentanyl', 'Ethanol'}), frozenset({'Fentanyl', 'Hydrocodone'}), frozenset({'Fentanyl', 'Benzodiazepine'}), frozenset({'Fentanyl', 'Methadone'}), frozenset({'Fentanyl', 'Amphet'}), frozenset({'Fentanyl', 'Tramad'}), frozenset({'Fentanyl', 'Morphine (Not Heroin)'}), frozenset({'Fentanyl', 'Hydromorphone'}), frozenset({'Fentanyl', 'Xylazine'}), frozenset({'Fentanyl', 'Opiate NOS'}), frozenset({'Fentanyl', 'Any Opioid'}), frozenset({'Fentanyl', 'CardioCondition'}), frozenset({'Fentanyl', 'RespiratoryCondition'}), frozenset({'Fentanyl', 'ObesityCondition'}), frozenset({'Fentanyl', 'DiabetesCondition'}), frozenset({'Fentanyl Analogue', 'Oxycodone'}), frozenset({'Fentanyl Analogue', 'Oxymorphone'}), frozenset({'Ethanol', 'Fentanyl Analogue'}), frozenset({'Hydrocodone', 'Fentanyl Analogue'}), frozenset({'Benzodiazepine', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Methadone'}), frozenset({'Amphet', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Fentanyl Analogue'}), frozenset({'Hydromorphone', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Xylazine'}), frozenset({'Fentanyl 
Analogue', 'Opiate NOS'}), frozenset({'Any Opioid', 'Fentanyl Analogue'}), frozenset({'CardioCondition', 'Fentanyl Analogue'}), frozenset({'RespiratoryCondition', 'Fentanyl Analogue'}), frozenset({'ObesityCondition', 'Fentanyl Analogue'}), frozenset({'DiabetesCondition', 'Fentanyl Analogue'}), frozenset({'Oxymorphone', 'Oxycodone'}), frozenset({'Ethanol', 'Oxycodone'}), frozenset({'Hydrocodone', 'Oxycodone'}), frozenset({'Benzodiazepine', 'Oxycodone'}), frozenset({'Methadone', 'Oxycodone'}), frozenset({'Amphet', 'Oxycodone'}), frozenset({'Tramad', 'Oxycodone'}), frozenset({'Morphine (Not Heroin)', 'Oxycodone'}), frozenset({'Hydromorphone', 'Oxycodone'}), frozenset({'Xylazine', 'Oxycodone'}), frozenset({'Opiate NOS', 'Oxycodone'}), frozenset({'Any Opioid', 'Oxycodone'}), frozenset({'CardioCondition', 'Oxycodone'}), frozenset({'RespiratoryCondition', 'Oxycodone'}), frozenset({'ObesityCondition', 'Oxycodone'}), frozenset({'DiabetesCondition', 'Oxycodone'}), frozenset({'Ethanol', 'Oxymorphone'}), frozenset({'Hydrocodone', 'Oxymorphone'}), frozenset({'Benzodiazepine', 'Oxymorphone'}), frozenset({'Methadone', 'Oxymorphone'}), frozenset({'Amphet', 'Oxymorphone'}), frozenset({'Oxymorphone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Oxymorphone'}), frozenset({'Hydromorphone', 'Oxymorphone'}), frozenset({'Xylazine', 'Oxymorphone'}), frozenset({'Oxymorphone', 'Opiate NOS'}), frozenset({'Any Opioid', 'Oxymorphone'}), frozenset({'CardioCondition', 'Oxymorphone'}), frozenset({'RespiratoryCondition', 'Oxymorphone'}), frozenset({'ObesityCondition', 'Oxymorphone'}), frozenset({'DiabetesCondition', 'Oxymorphone'}), frozenset({'Hydrocodone', 'Ethanol'}), frozenset({'Ethanol', 'Benzodiazepine'}), frozenset({'Ethanol', 'Methadone'}), frozenset({'Ethanol', 'Amphet'}), frozenset({'Ethanol', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Ethanol'}), frozenset({'Ethanol', 'Hydromorphone'}), frozenset({'Ethanol', 'Xylazine'}), frozenset({'Ethanol', 'Opiate NOS'}), frozenset({'Ethanol', 'Any Opioid'}), frozenset({'Ethanol', 'CardioCondition'}), frozenset({'RespiratoryCondition', 'Ethanol'}), frozenset({'ObesityCondition', 'Ethanol'}), frozenset({'DiabetesCondition', 'Ethanol'}), frozenset({'Hydrocodone', 'Benzodiazepine'}), frozenset({'Hydrocodone', 'Methadone'}), frozenset({'Hydrocodone', 'Amphet'}), frozenset({'Hydrocodone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Hydrocodone'}), frozenset({'Hydrocodone', 'Hydromorphone'}), frozenset({'Hydrocodone', 'Xylazine'}), frozenset({'Hydrocodone', 'Opiate NOS'}), frozenset({'Hydrocodone', 'Any Opioid'}), frozenset({'Hydrocodone', 'CardioCondition'}), frozenset({'Hydrocodone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Hydrocodone'}), frozenset({'DiabetesCondition', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Methadone'}), 
frozenset({'Amphet', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Benzodiazepine'}), frozenset({'Hydromorphone', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Xylazine'}), frozenset({'Benzodiazepine', 'Opiate NOS'}), frozenset({'Any Opioid', 'Benzodiazepine'}), frozenset({'CardioCondition', 'Benzodiazepine'}), frozenset({'RespiratoryCondition', 'Benzodiazepine'}), frozenset({'ObesityCondition', 'Benzodiazepine'}), frozenset({'DiabetesCondition', 'Benzodiazepine'}), frozenset({'Amphet', 'Methadone'}), frozenset({'Methadone', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Methadone'}), frozenset({'Hydromorphone', 
'Methadone'}), frozenset({'Xylazine', 'Methadone'}), frozenset({'Methadone', 'Opiate NOS'}), frozenset({'Any Opioid', 'Methadone'}), frozenset({'CardioCondition', 'Methadone'}), frozenset({'RespiratoryCondition', 'Methadone'}), frozenset({'ObesityCondition', 'Methadone'}), frozenset({'DiabetesCondition', 'Methadone'}), frozenset({'Amphet', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Amphet'}), frozenset({'Hydromorphone', 'Amphet'}), frozenset({'Amphet', 'Xylazine'}), frozenset({'Amphet', 'Opiate NOS'}), frozenset({'Any Opioid', 'Amphet'}), frozenset({'CardioCondition', 'Amphet'}), frozenset({'RespiratoryCondition', 'Amphet'}), frozenset({'ObesityCondition', 'Amphet'}), frozenset({'DiabetesCondition', 'Amphet'}), frozenset({'Morphine (Not Heroin)', 'Tramad'}), frozenset({'Hydromorphone', 'Tramad'}), frozenset({'Xylazine', 'Tramad'}), frozenset({'Opiate NOS', 'Tramad'}), frozenset({'Any Opioid', 'Tramad'}), frozenset({'CardioCondition', 'Tramad'}), frozenset({'RespiratoryCondition', 'Tramad'}), frozenset({'ObesityCondition', 'Tramad'}), frozenset({'DiabetesCondition', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Hydromorphone'}), frozenset({'Morphine (Not Heroin)', 'Xylazine'}), frozenset({'Morphine (Not Heroin)', 'Opiate NOS'}), frozenset({'Morphine (Not Heroin)', 'Any Opioid'}), frozenset({'Morphine (Not Heroin)', 'CardioCondition'}), frozenset({'Morphine (Not Heroin)', 'RespiratoryCondition'}), frozenset({'Morphine (Not Heroin)', 'ObesityCondition'}), frozenset({'Morphine (Not Heroin)', 'DiabetesCondition'}), frozenset({'Hydromorphone', 'Xylazine'}), frozenset({'Hydromorphone', 'Opiate NOS'}), frozenset({'Any Opioid', 'Hydromorphone'}), frozenset({'CardioCondition', 'Hydromorphone'}), frozenset({'RespiratoryCondition', 'Hydromorphone'}), frozenset({'ObesityCondition', 'Hydromorphone'}), frozenset({'DiabetesCondition', 'Hydromorphone'}), frozenset({'Xylazine', 'Opiate NOS'}), frozenset({'Any Opioid', 'Xylazine'}), frozenset({'CardioCondition', 'Xylazine'}), frozenset({'RespiratoryCondition', 'Xylazine'}), frozenset({'ObesityCondition', 'Xylazine'}), frozenset({'DiabetesCondition', 'Xylazine'}), frozenset({'Any Opioid', 'Opiate NOS'}), frozenset({'CardioCondition', 'Opiate NOS'}), frozenset({'RespiratoryCondition', 'Opiate NOS'}), frozenset({'ObesityCondition', 'Opiate NOS'}), frozenset({'DiabetesCondition', 'Opiate NOS'}), frozenset({'CardioCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'Any Opioid'}), frozenset({'ObesityCondition', 'Any Opioid'}), frozenset({'DiabetesCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 'CardioCondition'}), frozenset({'DiabetesCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 'RespiratoryCondition'}), frozenset({'DiabetesCondition', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'DiabetesCondition'})]}
********************* START SYNTHESIZING RECORDS ********************
------------------------> num of synthesized records:
7630
2021-10-23 09:41:13.192 | INFO     | method.dpsyn:synthesize_records:155 - synthesizing for ('Cocaine', 'Location if Other', 'Age', 'Hydromorphone', 'Tramad', 'Morphine (Not Heroin)', 'RespiratoryCondition', 'Date', 'Heroin', 
'Oxymorphone', 'Hydrocodone', 'Injury State', 'Opiate NOS', 'Location', 'Sex', 'Benzodiazepine', 'Oxycodone', 'Fentanyl Analogue', 'Death County', 'Fentanyl', 'DiabetesCondition', 'Ethanol', 'Residence State', 'Methadone', 'Xylazine', 'ObesityCondition', 'CardioCondition', 'Any Opioid', 'Race', 'Amphet', 'Injury County')
2021-10-23 09:41:13.207 | INFO     | method.dpsyn:synthesize_records:171 - update round: 0
2021-10-23 09:41:13.978 | INFO     | method.dpsyn:synthesize_records:171 - update round: 1
2021-10-23 09:41:14.809 | INFO     | method.dpsyn:synthesize_records:171 - update round: 2
2021-10-23 09:41:15.631 | INFO     | method.dpsyn:synthesize_records:171 - update round: 3
2021-10-23 09:41:16.566 | INFO     | method.dpsyn:synthesize_records:171 - update round: 4
2021-10-23 09:41:17.392 | INFO     | method.dpsyn:synthesize_records:171 - update round: 5
2021-10-23 09:41:18.199 | INFO     | method.dpsyn:synthesize_records:171 - update round: 6
2021-10-23 09:41:19.040 | INFO     | method.dpsyn:synthesize_records:171 - update round: 7
2021-10-23 09:41:19.828 | INFO     | method.dpsyn:synthesize_records:171 - update round: 8
2021-10-23 09:41:20.614 | INFO     | method.dpsyn:synthesize_records:171 - update round: 9
2021-10-23 09:41:21.416 | INFO     | method.dpsyn:synthesize_records:171 - update round: 10
2021-10-23 09:41:22.196 | INFO     | method.dpsyn:synthesize_records:171 - update round: 11
2021-10-23 09:41:22.981 | INFO     | method.dpsyn:synthesize_records:171 - update round: 12
2021-10-23 09:41:23.759 | INFO     | method.dpsyn:synthesize_records:171 - update round: 13
2021-10-23 09:41:24.544 | INFO     | method.dpsyn:synthesize_records:171 - update round: 14
2021-10-23 09:41:25.316 | INFO     | method.dpsyn:synthesize_records:171 - update round: 15
2021-10-23 09:41:26.115 | INFO     | method.dpsyn:synthesize_records:171 - update round: 16
2021-10-23 09:41:26.915 | INFO     | method.dpsyn:synthesize_records:171 - update round: 17
2021-10-23 09:41:27.702 | INFO     | method.dpsyn:synthesize_records:171 - update round: 18
2021-10-23 09:41:28.499 | INFO     | method.dpsyn:synthesize_records:171 - update round: 19
2021-10-23 09:41:29.311 | INFO     | method.dpsyn:synthesize_records:171 - update round: 20
2021-10-23 09:41:30.121 | INFO     | method.dpsyn:synthesize_records:171 - update round: 21
2021-10-23 09:41:30.952 | INFO     | method.dpsyn:synthesize_records:171 - update round: 22
2021-10-23 09:41:31.774 | INFO     | method.dpsyn:synthesize_records:171 - update round: 23
2021-10-23 09:41:32.603 | INFO     | method.dpsyn:synthesize_records:171 - update round: 24
2021-10-23 09:41:33.431 | INFO     | method.dpsyn:synthesize_records:171 - update round: 25
2021-10-23 09:41:34.252 | INFO     | method.dpsyn:synthesize_records:171 - update round: 26
2021-10-23 09:41:35.062 | INFO     | method.dpsyn:synthesize_records:171 - update round: 27
2021-10-23 09:41:35.879 | INFO     | method.dpsyn:synthesize_records:171 - update round: 28
2021-10-23 09:41:36.708 | INFO     | method.dpsyn:synthesize_records:171 - update round: 29
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
2021-10-23 09:41:37.618 | INFO     | __main__:run_method:163 - ------------------------>synthetic data post-processed:
      Date  Age     Sex             Race  ... RespiratoryCondition ObesityCondition DiabetesCondition epsilon
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

[7630 rows x 32 columns]v
```



## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



