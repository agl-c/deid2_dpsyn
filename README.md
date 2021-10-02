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

----

### How to configure?

#### Generate supporting schema files 

The input dataset should be in format of filename.csv with its first row a header row.
And you should first preprocess the dataset. A tool(https://github.com/hd23408/nist-schemagen) is provided to generate the **parameters.json** and **column_datatypes.json** (both we include repository  example files ), which include some schema of the dataset to help our algorithm run.
Based on that,  **data_type.py** easily generate a dict COLS that record the columns' data types. 

----

#### Set paths

Set several paths in **config/path.py**, as the comments in the file instruct.

#### In data.yaml 

Set identifier attribute, bin value parameters.

+ You can specify the **identifier** attribute's name in data.yaml (we assume your dataset has the identifer attribute by default and obviously, in synthetic dataset the column should be removed to protect privacy)
+ You can specify **bin** settings in format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. ( Further, you can change more details in bin generation in binning_attributes() in DataLoader.py )

----

<font color=green> Currently below functions are commented sicne they are tailored for specific datasets and in practice tricks for efficiency consideration. </font>

<font color=green>(more) set and fix if you want: grouping settings</font>

+ You can define attributes to be grouped in data.yaml ( possibly based on analysis in possible existing public datasets ), and we may give you some tips on deciding which attributes to group.

**some intuitional grouping tips:**

   * group those with small domains
   * group those with embedded correlation
   * group those essitially the same (for instance, some attributes only differ in naming or one can be fully determined by another)

<font color=green>(more) set and fix if you want: value-determined attributes which you can detect by yourself. </font>

+ If the original dataset includes some attributes that can be determined by other attributes, you can specify them in data.yaml, but by default we exclude the part and you can find related code in comment.

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

### Measurements

You can refer to Synthpop(a R package) as a tool to compare the synthesized dataset against the original one. And we offer a quick-start guide [Synthpop](https://docs.google.com/document/d/17jSDoMcSbozjc8Ef8X42xPJXRb6g_Syt/edit#heading=h.gjdgxs ) for you here. 

## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



