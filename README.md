# DPSyn: a quick start tutorial 
## What is DPsyn?
We present DPSyn, an algorithm for synthesizing microdata for data analysis while satisfying differential privacy. Besides, inspired by the access to a public dataset in the 20deID2 competition, in some cases (which is decided by specific method_decision algorithm), we turn to the public dataset instead of the privatized one to generate the query answer. 

### For your convenience, with a dataset (whose privacy you want to protect), you can:
* directly choose to use the DPsyn algorithm to generate a private dataset;
### Further, with another public dataset for reference, you can:
* utilize our code to decide whether to use the public dataset or the DPSyned private one to answer queries;
### Moreover, with a private dataset generated not by DPSyn:
* you can also use the method_decision algorithm to decide whether turn to the public dataset or the private one for answering queires.
### As to measure the quality of generated datasets:
* we present 2 metric programes which you can run to test the quality of generated datasets: one is provided by the competition organizer and the other is drafted by ourselves.
* generally, for convincing performance measure, we also evaluate the synthesized datasets using the well-known packet synthpop.

## Install DPsyn (fill this part after packaging, easy)
## How to config?
### Preparation work to generate supporting files for specific dataset
You should first preprocess the dataset. We require you to provide dataset in format of filename.csv(comma-separated file, and you can find ground_truth.csv as an example), and we offer you tools to generate the parameters.json and read_csv_kwargs.json(both we include example files in the repository).


Q: how we set run parameters like epsilon? (parameters.json)
It is dependent on users' design? Or shall we instruct them to set sensible eps parameters?
Confused: 
why YEAR and sim_individual_id are not included in parameters.json?😅
Why we restrict the maximum records per individual?　Concerned for too heavy data procession?



As to data.yaml, where we specify:
(1) specified parameters of an experiment run (depend on specific design)
(2) the lowest-boundary-value, highest-boundary-value and step-value of some attributes, (depend on granuarity metric settings, which we leave for users' flexible design)
(3) hard coded grouped attributes. (depend on analysis on possible existing public datasets and we may give you some tips on choosing to group what attributes)
Tips: 
* group those with small domains;
* group those with embedded correlation
* group those essitially the same attributes (for instance, one attribute differs with another only in naming or can be fully determined by the other)
In summary, in data.yaml we ask users to set appropriate bin value parameters, grouping settings, and value-determined attributes which are detected by users themselves.
(TODO: Or should we better implement the attribute selection and combination part of DPSyn paper?)
TODO: As to combination, King seemed to mention one combination package which might help in instructing combining? 
But I can not figure out how it works as we even cannot know the inner features of the to-protect dataset.

### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content, as well as define the bin values of attributes which also depends on pre analysis of the dataset
2. in config/data_type.py, write the value types of the attributes (which should be easy since we must get read_csv_kwargs.json)
3. in config/path.py,  write the paths of input dataset, the possible existing input public dataset, the parameters(attribute name,  value type, valid values, etc), etc
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and write more details in the yaml file which describes what you want to do in this run.
(TODO: what does it mean? why all those xxxx.yaml cares about 'PUMA' and 'YEAR'?😅) - puma is an area code. puma-year is the evaluation metric; maybe it is more interesting to some analytics in census
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


### More configrations to fit our tool to your dataset
I guess more tip documentation are needed..... Since some hard code exist.
Or I need more experience or intelligence in tackling a general case. 😭

## Team Members & Affiliation(s):

Anqi Chen (Peking University)
Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214, @agl-c



