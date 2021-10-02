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
And you should first preprocess the dataset. we offer you tools(https://github.com/hd23408/nist-schemagen) to generate the **parameters.json** and **column_datatypes.json** (both we include example files in the repository) which include some schema of the dataset to help our algorithm run.
Based on that, you can easily generate **data_type.py**, which simply include a dictionary called COLS that record the columns' data types. And you may add this part in data/RecordPostprocessor.py.

#### Set paths

Set several paths in **config/path.py**, instructed by the variables' names.  <font color=red>(we'd better keep all paths in only one place)</font>

<font color=blue> I want to : (1) make path all in path.py  </font>



#### In data.yaml 

<font color=red>(we can rename the config file?) </font>

<font color=blue> conside desert / rename some files </font>

You should set file paths, identifier attribute, bin value parameters, grouping settings, 

<font color=green>and possibly value-determined attributes which are detected by users themselves. (desert ? Y) </font>

#### Marginal selection config

Refer to eps=1000.0.yaml as an example where we manually restrict the marginal selection method to be all the two way marginals. <font color=red>(include automatic marginal selection and combination part as in PrivSyn? )</font>

+ You can specify the identifier attribute's name in data.yaml (we assume your dataset has the identifer attribute by default and obviously, in synthetic dataset the column should be removed to protect privacy)

+ You can specify bin settings in format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. Further, you can change more details in bin generation in binning_attributes() in DataLoader.py

+ You can define attributes to be grouped in data.yaml (possibly based on analysis in possible existing public datasets), and we may give you some tips on deciding which attributes to group.

**some intuitional grouping tips:**

   * group those with small domains
   * group those with embedded correlation
   * group those essitially the same (for instance, some attributes only differ in naming or one can be fully determined by another)

<font color=green> Discuss if desert below functions:</font>

+ If your dataset includes some attributes that can be determined by other attributes, you can specify them in data.yaml, but by default we exclude the part and you can find related code in comment

+ If you have a public dataset to refer to, set pub_ref=True in load_data() in DataLoader.py and fill the settings in data.yaml 

#### Differential privacy parameters (eps, delta, sensitivity)

<font color=red>for naive users, how to instruct design the sensitive functions </font> (Gary comments they might not know how to set this)

Users should set the eps, delta, sensitivity value in 'runs' in parameters.json according to their specific differential privacy requirements. 
Here we display an example where the sensitivity value equals to 'max_records_per_individual', which essentially means the global sensitivity value of a specified function f(here is the count).
    {
      "epsilon": 2.0,
      "delta": 3.4498908254380166e-11,
      "max_records": 1350000,
      "max_records_per_individual": 7
    }
Meanwhile, as the above example shows, you can specify the 'max_records' parameter to bound the number of rows in the synthesized dataset. 


### Details in fine tuning
Below we list several hyper parameters through our code. You can fine tune them when working on your own experiments instead of our default setting.

| variable          | file                 | class/function)    | value |  semantics                     |
| :---------------: | :------------------: | :------------:     | :----:| :--------:                     |
| update_iterations | dpsyn.py             | DPSyn              | 30    | the num of update iterations                        |
| alpha = 1.0       | record_synthesizer.py| RecordSynthesizer  |  1.0  |                                |
| update_alpha()    | record_synthesizer.py| RecordSynthesizer  | self.alpha = 1.0 * 0.84 ** (iteration // 20) |inspired by ML practice |



----

<font color=red>Challenging parts：</font>

1. how to set <font color=green>groupings</font> when a new dataset come, simply with schema we cannot decide how to group?

   Actually I'm unclear about what rules the grouping info in config should submit to? 

   Should the dataset include exactly all the possible combinations of grouping settings?  

   ( one attribute as a group? or no grouping )

2. include <font color=red>marginal selection and combination </font>(?)

3. <font color=red>dataset size n: as for now, we just input it when run, if automatically set by dp, </font>how? (I haven't figured it out)   

   ( some number calculation function )

4. as to metric, we need a small tool to produce a smaller sized dataset as inputs since the metric function consumes a lot of memory.  

   (refer to numpy or pandas)



I can work on:


1. clean unrelated code
2. explicit instructions and comments
3. add a catalog in README,  refer to https://github.com/cmla-psu/statdp, consider the format of code (add dark background), add a catalog
4. latest libraries, check then... (✅)
5. packaging, 



<font color=red> what arrived now</font>

After config (where we should think how users provide grouping info and design sensitivity function), we run with input n which denotes the num of records to synthesize, and we can synthesize a dataset with all-two-way marginals method.

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



