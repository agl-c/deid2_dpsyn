# DPSyn: a quick start tutorial 
## What is DPsyn?
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy.

To facilitate your understanding, please refer to the paper *PrivSyn: Differentially Private Data Synthesis* [link](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun).

### Comparison with related work
There are two similar and highly-related papers (both from competitors in the competition) . They are:
[PrivMRF](http://www.vldb.org/pvldb/vol14/p2190-cai.pdf), and
[PGM](https://arxiv.org/pdf/1901.09136.pdf).

The difference is that PrivSyn includes the whole data synthesis pipeline: (1) finding marginals and (2) synthesize dataset from the marginals. PGM only handles the second part, and PrivMRF only handles the first part (and uses PGM as the second part).  Since the PrivSyn and PrivMRF appear concurrently, there is no direct comparison between the two. Compared to PGM, PrivSyn shows its synthesizing method can handle *dense* graph.

In this repository, we only include the second part for now.

### For your convenience, with a dataset (whose privacy you want to protect), you can:
* directly use DPsyn algorithm to generate a private dataset;
### (*for research*)Further, with another public dataset for reference, you can:
* decide whether to use the public one or the DPSyned dataset to answer queries, as to which problem we place some default intuitional settings (in practice, they could be researched deeper) and users can change as they want.
### As to measure the generated dataset:
* (In the competition's setting, we present 2 metric programes which you can run to test the quality of generated datasets: one is provided by the competition organizer and the other is drafted by ourselves.)
* generally, you can refer to Synthpop(a R package) as a tool to compare the synthesized dataset against the original one.


## Install DPsyn (fill this part after packaging, easy)



## How to configure to synthesize a dataset by DPsyn?
### generate supporting files for specific dataset
You should first preprocess the dataset. 
We require you to provide dataset in format of filename.csv(comma-separated file, and you can find ground_truth.csv as an example).
And we offer you tools(https://github.com/hd23408/nist-schemagen) to generate the **parameters.json** and **column_datatypes.json**(both we include example files in the repository) which include some schema of the dataset to help our algorithm run.
Based on that, you can easily generate **data_type.py**, which simply include a dictionary called COLS that record the columns' data types. And you may add this part in data/RecordPostprocessor.py.

### set file paths
You should set several paths in **config/path.py**, instructed by the variables' names. 

### In data.yaml
You should set file paths, identifier attribute, bin value parameters, grouping settings, and possibly value-determined attributes which are detected by users themselves.

### Marginal selection method config
Refer to eps=1000.0.yaml as an example file where we manully restrict the marginal selection method to be all the two way marginals.


**More details**
1. You can specify the identifier attribute's name in data.yaml (we assume your dataset has the identifer attribute by default and obviously, in synthetic dataset the column should be removed to protect privacy)
2. You can specify bin settings in format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. Further, you can change more details in bin generation in binning_attributes() in DataLoader.py
3. You can define attributes to be grouped in data.yaml(possibly based on analysis in possible existing public datasets), and we may give you some tips on deciding which attributes to group.

*some intuitional grouping tips:* 
   * group those with small domains
   * group those with embedded correlation
   * group those essitially the same (for instance, some attributes only differ in naming or one can be fully determined by another)

TODO:
1. consider including the code of  attribute selection and combination part in DPSyn paper. 😋
2. King seemed to mention one combination package which might help in instructing combining? (But I can not figure out how it works as we even cannot know the inner features of the to-protect dataset.)
3. If your dataset includes some attributes that can be determined by other attributes, you can specify them in data.yaml, but by default we exclude the part and you can find related code in comment
4. If you have a public dataset to refer to, set pub_ref=True in load_data() in DataLoader.py and fill the settings in data.yaml


### As to dp parameters(eps, delta, sensitivity)
Users should set the eps, delta, sensitivity value in 'runs' in parameters.json according to their specific differential privacy requirements.
Here we display an example where the sensitivity value equals to 'max_records_per_individual', which essentially means the global sensitivity value of a specified function f(here is the count).
    {
      "epsilon": 2.0,
      "delta": 3.4498908254380166e-11,
      "max_records": 1350000,
      "max_records_per_individual": 7
    }
Meanwhile, as the above example shows, you can specify the 'max_records' parameter to bound the number of rows in the synthesized dataset.


### Below is related to generate a dataset with certain attributes fiexd (I think we'd better desert the part)
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and include more details in the yaml file which describes what you want to do in this run.
(For instance, to generate a dataset for each pair of  "PUMA" and "YEAR", which is motivated by the specific metric here, you can set in yaml things like below)
<font color=red>
attributes:
    - 'PUMA'
    - 'YEAR'


### More manual configrations to fit our algorithm to your dataset
Below we list several hyper parameters through our code which you can design by yourself to replace our default setting.

| variable          | file                 | class/function)    | value |  semantics                     |
| :---------------: | :------------------: | :------------:     | :----:| :--------:                     |
| update_iterations | dpsyn.py             | DPSyn              | 30    | the num of update iterations                        |
| alpha = 1.0       | record_synthesizer.py| RecordSynthesizer  |  1.0  |                                |
| update_alpha()    | record_synthesizer.py| RecordSynthesizer  | self.alpha = 1.0 * 0.84 ** (iteration // 20) |inspired by ML practice |

btw, you can manually set noise type in method/synthesizer.py anoymize() by hardcoding it.

2. dataset size n
(1) TODO: automaticly set by dp  A: not n=0, then how?
(2) user input
3. noise type? 
 (1) automatically
 refer to: synthesizer.py , synthesize()
 since the advanced_composition is a python module which provides related noise parameters
 noise_type, noise_param = advanced_composition.get_noise(eps, self.delta, self.sensitivity, len(marginals))
 we can fix this part as kind of improvement? 
 (2) users set




4. benchmark and improve, since the metric tool is not that convincing
5. clean the unrelated code to provide a well-organized code repository with explicit instructions and comments.
6. As to latest libraries, check then...
7. As to packacging, maybe we can transfer some settings to command line interactions.....

More:
1. I haven't read the lib code deeply
2. remind on sharing reviewing ( 90% bad-quality......)

*Below is simply draft to help thinking:*
#### Interesting，as to the paper, I found myself memory-lost...
(1) what does it mean by constructing a graph with all the 2-way marginals? 
A：Each attribute is a node and the edge between them is a distribution describing the correlation between attributes. 
(2) In DPSyn paper, as to selecting marginals, it means choosing from all possible pairs to a selected set until the calculated error can not be decreased? (it is greedy algorithm, please refer to paper link for more details)
As to the project here, we skip the step of choosing marginals and simply do that manually by ourselves? 
(I haven't found where we choose marginals)
Q: You can start from using all the pairs or require people to designate what pairs to care about? 
Q：Maybe we can include the greedy algorithm code on pair selection later.

1.what is the formal definition of the graphical model? refer to paper: *Graphical-model based estimation and inference for differential privacy*
Q：I have not totally understand the example of 3-way marginal?
Why it means a triangle which just takes care of correlation between 2 attributes?
I supposed the "3-way marginal" implies a correlationship between all the 3 which however seems to be in paradox with the 3-edge-representation?


## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



