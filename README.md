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
C:\Users\陈安琪\Desktop\nist_comp\deid2_dpsyn>python experiment.py -h
usage: experiment.py [-h] [--priv_data PRIV_DATA] [--config CONFIG] [--n N] [--params PARAMS]
                     [--datatype DATATYPE] [--marginal_config MARGINAL_CONFIG]
                     [--priv_data_name PRIV_DATA_NAME]

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

## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



