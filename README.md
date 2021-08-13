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
FYI, you should firstly do a preprocessing of the datasets to find the schema of the datasets before utilizing the package's implemented tools. 
### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content, as well as define the bin values of attributes which also depends on pre analysis of the dataset
2. in config/data_type.py, write the value types of the attributes
3. in config/path.py,  write the paths of input dataset, the possible existing input public dataset, the parameters(attribute name,  value type, valid values, etc), etc
4. add in config 'eps=xxx.yaml' where xxx means the epsilon value(privacy budget) you want to set and write more details in the yaml file which describes what you want to do in this run.
<font color=red>
For instance, 
attributes:
    - 'PUMA'
    - 'YEAR'
means we want to generate a privatized 2-way marginal on those 2 attributes,
and to solve your confusion about how we generate a complete row with all the attributes, 
please refer to the paper

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




