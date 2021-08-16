# DPSyn: a quick start tutorial 
## What is DPsyn?
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


As to data.yaml, where we specify:
(1) specified parameters of an experiment run
(2) the lowest-boundary-value, highest-boundary-value and step-value of some attributes, 
(3) some hard coded grouped attributes. 😅
TODO: how we generate it(data.yaml)?
Should we ask users to set appropriate bin value parameters and grouping settings themselves? 
Or should we better implement the attribute selection and combination part of DPSyn paper?



### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content, as well as define the bin values of attributes which also depends on pre analysis of the dataset
2. in config/data_type.py, write the value types of the attributes (which should be easy since we must get read_csv_kwargs.json)
3. in config/path.py,  write the paths of input dataset, the possible existing input public dataset, the parameters(attribute name,  value type, valid values, etc), etc
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and write more details in the yaml file which describes what you want to do in this run.
(TODO: what does it mean? why all those xxxx.yaml cares about 'PUMA' and 'YEAR'?😅)
<font color=red>
For instance, 
attributes:
    - 'PUMA'
    - 'YEAR'
means we want to generate a privatized 2-way marginal on those 2 attributes,
and to solve your confusion about how we generate a complete row with all the attributes, 
please refer to the paper *PrivSyn: Differentially Private Data Synthesis*, https://www.usenix.org/conference/usenixsecurity21/presentation/zhang-zhikun


#### Interesting，as to the paper, I found myself memory-lost...
(1) what does it mean by constructing a graph with all the 2-way marginals? (even though I konw it's not our method in DPSyn)
(2) as to selecting marginals, check whether it means choose from all the possible pairs to a selected set until the calculated error can not be decreased? (noting it is greedy algorithm)
as to the project here:
(3)  besides, tianhao mentioned that in this project, we skip the part of choosing marginals by programes, but instead, do this job manually by ourselves? (sorry, )
(4) 

1.what is the formal definition of the graphical model? refer to paper: *Graphical-model based estimation and inference for differential privacy*

### More configrations to fit our tool to your dataset





































## Team Members & Affiliation(s):

Ninghui Li (Purdue University)
Zitao Li (Purdue University)
Tianhao Wang (Purdue University)

## GitHub User(s) Serving as POC:

@vvv214

## How to Cite:

- Author: Ninghui Li, Zitao Li, Tianhao Wang
- Date: May 30, 2021
- Title: DPSyn
- Type: source code




