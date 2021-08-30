# DPSyn: a quick start tutorial 
## What is DPsyn?
<<<<<<< HEAD
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy. Besides, inspired by the access to a public dataset in the 20deID2 competition, in some cases (which is decided by specific method_decision algorithm), we turn to the public dataset instead of the dp-tackled private one to generate the query answer. 
### For your convenience, with a dataset (which you want to protect privacy), you can:
* directly choose to use the DPsyn algorithm to generate a private dataset;
### Further, with another public dataset for reference, you can:
* utilize our code to decide whether to use the public dataset or the DPSyned private one to answer queries;
### Moreover, with a private dataset generated not by DPSyn:
* you can also use the method_decision algorithm to decide whether turn to the public dataset or the private one for answering queires.
### As to measure the quality of generated datasets:
* we present 2 metric programes which you can run to test the quality of generated datasets: one is provided by the competition organizer and the other is drafted by ourselves.

## Install DPsyn (fill this part after packaging, easy)
## How to config?
### Preparation work to generate supporting files for specific dataset
FYI, you should firstly do a preprocession of the dataset to find the schema of the dataset before utilizing the package's implemented tools. 

For simplification, we require you to provide dataset in format of filename.csv(comma-separated file), which is a file format in general use for data storage, and we offer you tools to generate the parameters.json and read_csv_kwargs.json.

Q: how we get the data types of all the colums of the csv file? (to get read_csv_kwargs.json)
A: Refer to https://stackoverflow.com/questions/52369572/python-how-to-get-data-types-for-all-columns-in-csv-file,
it seems that we can get to extrapolate the value types by proprocession of DataFrame, like using:
for name, dtype in df.dtypes.iteritems():
    # note that we should store in json format, detailed coding needed 
    # besides, I worry about whether the deduction is correct about value types.

Q: how we set run parameters and get the all possible valid values of parameters? (parameters.json)
I guess that with the DataFrame, we get to know some features of the colums and set them in json file which is not that hard?
Confused: why YEAR and sim_individual_id are not included in parameters.json?😅
Why we restrict the maximum records per individual?　Concerned for too heavy data procession?

TODO: ask them for existing tools


As to data.yaml, where we specify:
(1) specified parameters of an experiment run (depend on specific design)
(2) the lowest-boundary-value, highest-boundary-value and step-value of some attributes, (depend on granuarity metric settings)
(3) some hard coded grouped attributes. (depend on analysis on possible existing public datasets and we may give you some tips about choosing to group what attributes)
Tips: 
* group those with small domains;
* group those with embedded correlation
* group those essitially the same attributes (for instance, one attribute differs with another only in naming or can be fully determined by the other)
In summary, in data.yaml we ask users to set appropriate bin value parameters, grouping settings, and value-determined attributes which are detected by users themselves.
(TODO: Or should we better implement the attribute selection and combination part of DPSyn paper?)



### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content, as well as define the bin values of attributes which also depends on pre analysis of the dataset
2. in config/data_type.py, write the value types of the attributes (which should be easy since we must get read_csv_kwargs.json)
3. in config/path.py,  write the paths of input dataset, the possible existing input public dataset, the parameters(attribute name,  value type, valid values, etc), etc
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and write more details in the yaml file which describes what you want to do in this run.
(Q: what does it mean? why all those xxxx.yaml cares about 'PUMA' and 'YEAR'?😅
A: it is because the metric is on how the synthesized dataset are close to the original one in a "PUMA YEAR" setting. 
)
<font color=red>
For instance, 
attributes:
    - 'PUMA'
    - 'YEAR'

To solve your confusion about how we generate a complete row with all the attributes, please refer to the paper *PrivSyn: Differentially Private Data Synthesis*, https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun


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
=======
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy. Besides, inspired by the access to a public dataset in the 20deID2 competition, in some cases (which is decided by specific method_decision algorithm), we turn to the public dataset instead of the privatized one to generate the query answer. 

To facilitate your understanding, please refer to the paper *PrivSyn: Differentially Private Data Synthesis* [link](https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun).

### Comparison with related work
There are two similar and highly-related papers (both from competitors in the competition) . They are:
[PrivMRF](http://www.vldb.org/pvldb/vol14/p2190-cai.pdf), and
[PGM](https://arxiv.org/pdf/1901.09136.pdf).

The difference is that PrivSyn includes the whole data synthesize pipeline: (1) finding marginals and (2) synthesize dataset from the marginals. PGM only handles the second part, and PrivMRF only handles the first part (and uses PGM as the second part).  Since the PrivSyn and PrivMRF appear concurrently, there is no direct comparison between the two. Compared to PGM, PrivSyn shows its synthesizing method can handle *dense* graph.

In this repository, we only include the second part for now.

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
1. You can specify the identifier attribute's name in data.yaml (we assume your dataset has the identifer attribute by default and obviously, in synthetic dataset the column should be removed to protect privacy)
2. You can specify bin values like [min, max, step] in numerical_binning in data.yaml (based on your granuarity likes)
3. Moreover, you can change more details in bin generation in binning_attributes() in DataLoader.py
4. You can define attributes to be grouped in data.yaml
 (based on analysis in possible existing public datasets and we may give you some tips on choosing to group which attributes)
*Basically, you can refer to some intuitional tips:* 
   * group those with small domains;
   * group those with embedded correlation;
   * group those essitially the same attributes (for instance, one attribute differs with another only in naming or can be fully determined by the other);
TODO:
1. consider including the code of  attribute selection and combination part in DPSyn paper. 😋
2. King seemed to mention one combination package which might help in instructing combining? (But I can not figure out how it works as we even cannot know the inner features of the to-protect dataset.)


4. If your dataset includes some attributes that can be determined by other attributes, you can specify them in data.yaml, but by default we exclude the part and you can find related code in comment
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


>>>>>>> 26522d7


 😅:
  pub_marginals = self.data.generate_all_pub_marginals()
  noise_type = priv_split_method[set_key]
  def lap_adv_comp(epsilon, delta, sensitivity, k):
  zcdp and zcdp2 and rdp perform the same
  with open(args.config, 'r') as f:
  if pub_only:
  def reload_priv(self, new_data_path):


### More configrations to fit our tool to your dataset
I guess more tip documentation are needed..... Since some hard code exist.
Or I need more experience or intelligence in tackling a general case. 😭

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



