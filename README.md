# DPSyn: a quick start tutorial 
## What is DPsyn?
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy. Besides, inspired by the access to a public dataset in the 20deID2 competition, in some cases (which is decided by specific method_decision algorithm), we turn to the public dataset instead of the privatized one to generate the query answer. 

To facilitate your understanding, please refer to the paper *PrivSyn: Differentially Private Data Synthesis*, https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun


### For your convenience, with a dataset (whose privacy you want to protect), you can:
* directly use DPsyn algorithm to generate a private dataset;
### (*for research*)Further, with another public dataset for reference, you can:
* decide whether to use the public one or the DPSyned dataset to answer queries, as to which problem we place some default intuitional settings (in practice, they could be researched deeper) and users can change as they want.
### As to measure the generated dataset:
*(In the competition's setting, we present 2 metric programes which you can run to test the quality of generated datasets: one is provided by the competition organizer and the other is drafted by ourselves.)
* generally, you can refer to Synthpop(a R package) as a tool to compare the synthesized dataset against the original one.


## Install DPsyn (fill this part after packaging, easy)








## How to configure to synthesize a dataset by DPsyn?
### Preparation work to generate supporting files for specific dataset
You should first preprocess the dataset. 
We require you to provide dataset in format of filename.csv(comma-separated file, and you can find ground_truth.csv as an example), and we offer you tools to generate the parameters.json and read_csv_kwargs.json(both we include example files in the repository) which include some schema of the dataset to help our algorithm run.
In data.yaml we ask users to set file paths, bin value parameters, grouping settings, and value-determined attributes which are detected by users themselves.

More details:
1. You can specify bin values like [min, max, step] in numerical_binning in data.yaml (based on your granuarity likes)
2. Moreover, you can change more details in bin generation in binning_attributes() in DataLoader.py
3. You can define attributes to be grouped in data.yaml ()
 (based on analysis in possible existing public datasets and we may give you some tips on choosing to group which attributes)
*Basically, you can refer to some intuitional tips:* 
   * group those with small domains;
   * group those with embedded correlation;
   * group those essitially the same attributes (for instance, one attribute differs with another only in naming or can be fully determined by the other);
TODO:
1. consider including the code of  attribute selection and combination part in DPSyn paper. 😋
2. King seemed to mention one combination package which might help in instructing combining? (But I can not figure out how it works as we even cannot know the inner features of the to-protect dataset.)


4. If your dataset include some attributes that can be determined by other attributes, you can specify them in data.yaml 🤔
5. If you have a public dataset to refer to, set pub_ref=True in load_data() in DataLoader.py
TODO:  🤣
there is a parameter called pub_only in load_data and I guess whether it is when we only input the public dataset?


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
🤔

### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content
2. in config/data_type.py, write the value types of the attributes (easy with read_csv_kwargs.json obtained)
TODO: find its use in the whole folder? 😅
3. in config/path.py,  write the paths of input original dataset file, the public dataset file(if there exists one to refer to), the parameters file (attribute name,  value type, valid values, etc), etc


(
### Below is related to generate a dataset with certain attributes fiexd (I think we'd better desert the part)
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and include more details in the yaml file which describes what you want to do in this run.
(For instance, to generate a dataset for each pair of  "PUMA" and "YEAR", which is motivated by the specific metric here, you can set in yaml things like below)
<font color=red>
attributes:
    - 'PUMA'
    - 'YEAR'
)

### More configrations to fit our algorithm to your dataset
Below we list several places in our code where you can set some magic values (instead of our rude default settings) when using the package to generate specific dataset.
Tips on how to design those values will be obtained in related places in code files. 

| variable          | file                 | class/function) | value |  
| update_iterations | dpsyn.py             | DPSyn           | 60    |
| n                 | experiment.py        | main()          | 0 ??? |
| d                 | dpsyn.py             | DPSyn           | 0??   |
| 




 😅:
  pub_marginals = self.data.generate_all_pub_marginals()
  noise_type = priv_split_method[set_key]
  def lap_adv_comp(epsilon, delta, sensitivity, k):






*Below is simply draft to help thinking:*
#### Interesting，as to the paper, I found myself memory-lost...
(1) what does it mean by constructing a graph with all the 2-way marginals? 
A：Each attribute is a node and the edge between them is a distribution describing the correlation between attributes. 
(2) In DPSyn paper, as to selecting marginals, it means choosing from all possible pairs to a selected set until the calculated error can not be decreased? (it is greedy algorithm, please refer to paper link for more details)
As to the project here, we skip the step of choosing marginals and simply do that manually by ourselves? 
TODO: You can start from using all the pairs or require people to designate what pairs to care about? 
TODO：Maybe we can include the greedy algorithm code on pair selection later.

1.what is the formal definition of the graphical model? refer to paper: *Graphical-model based estimation and inference for differential privacy*
TODO：I have not totally understand the example of 3-way marginal?
Why it means a triangle which just takes care of correlation between 2 attributes?
I supposed the "3-way marginal" implies a correlationship between all the 3 which however seems to be in paradox with the 3-edge-representation?


## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



