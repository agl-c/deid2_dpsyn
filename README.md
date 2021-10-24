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

```
PS C:\Users\陈安琪\Desktop\nist_comp\deid2_s2 - clean_refresh\deid2_dpsyn> docker run -it --name testio1 -v /c/test:/DPSyn/tmp dpsyn:v3 --priv_data_name testio --priv_data /DPSyn/tmp/test.csv --target_path /DPSyn/tmp/testout.csv
------------------------> config yaml file loaded in DataLoader, config file:  ./config/data.yaml
------------------------> parameter file loaded in DataLoader, parameter file:  ./data/parameters.json
************* start loading private data *************
------------------------> process and store with pkl file name:  preprocessed_priv_testio.pkl
           ID  Date  Age     Sex   Race Residence State Death County  ... Xylazine Opiate NOS Any Opioid CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  WHITE             NaN    FAIRFIELD  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
1     12-0258  2012   51    MALE  WHITE             NaN    MIDDLESEX  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
2     13-0146  2013   28    MALE  WHITE             NaN     HARTFORD  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
3     14-0150  2014   46    MALE  WHITE             NaN   LITCHFIELD  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
4     14-0183  2014   52    MALE  WHITE             NaN   NEW LONDON  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
...       ...   ...  ...     ...    ...             ...          ...  ...      ...        ...        ...             ...                  ...              ...               ...
7629  14-0128  2014   25    MALE  WHITE             NaN          NaN  ...      NaN        NaN        NaN             NaN                  NaN              NaN               NaN
7630  20-1217  2020   62  FEMALE  WHITE              CT    FAIRFIELD  ...      NaN        NaN          Y             NaN                  NaN              NaN               NaN
7631  20-1138  2020   50  FEMALE  WHITE              CT     HARTFORD  ...        Y        NaN          Y             NaN                  NaN              NaN               NaN
7632  16-0640  2016   36    MALE  WHITE              CT          NaN  ...      NaN        NaN          Y             NaN                  NaN              NaN               NaN
7633  19-0963  2019   33    MALE  WHITE              CT    NEW HAVEN  ...      NaN        NaN          Y               Y                  NaN              NaN               NaN

[7634 rows x 32 columns]
********** afer fillna ***********
           ID  Date  Age     Sex   Race Residence State Death County  ... Xylazine Opiate NOS Any Opioid CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition
0     12-0187  2012   34  FEMALE  WHITE                    FAIRFIELD  ...                                                                                                   
1     12-0258  2012   51    MALE  WHITE                    MIDDLESEX  ...                                                                                                   
2     13-0146  2013   28    MALE  WHITE                     HARTFORD  ...                                                                                                   
3     14-0150  2014   46    MALE  WHITE                   LITCHFIELD  ...                                                                                                   
4     14-0183  2014   52    MALE  WHITE                   NEW LONDON  ...                                                                                                   
...       ...   ...  ...     ...    ...             ...          ...  ...      ...        ...        ...             ...                  ...              ...               ...
7629  14-0128  2014   25    MALE  WHITE                               ...                                                                                                   
7630  20-1217  2020   62  FEMALE  WHITE              CT    FAIRFIELD  ...                              Y                                                                    
7631  20-1138  2020   50  FEMALE  WHITE              CT     HARTFORD  ...        Y                     Y                                                                    
7632  16-0640  2016   36    MALE  WHITE              CT               ...                              Y                                                                    
7633  19-0963  2019   33    MALE  WHITE              CT    NEW HAVEN  ...                              Y               Y                                                    

[7634 rows x 32 columns]
------------------------> private dataset:  /DPSyn/tmp/test.csv
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
2021-10-24 02:55:37.157 | INFO     | __main__:run_method:106 - working on eps=10.0, delta=3.4498908254380166e-11, and sensitivity=1
------------------------> all two way marginals generated
**************** help debug ************** num of records averaged from all two-way marginals: 7633.419354838709
**************** help debug ************** num of records from marginal count before adding noise: 7633.419354838709
------------------------> now we decide the noise type:
considering eps: 10.0 , delta: 3.4498908254380166e-11 , sensitivity: 1 , len of marginals: 465
------------------------> noise type: gauss
------------------------> noise parameter: 16.386725928253217
2021-10-24 02:55:45.646 | INFO     | method.synthesizer:anonymize:79 - marginal priv_all_two_way use eps=10.0, noise type:gauss, noise parameter=16.386725928253217, sensitivity:1
------------------------> now we get the estimate of records' num by averaging from nosiy marginals: 7630
2021-10-24 02:55:53.952 | DEBUG    | lib_dpsyn.consistent:consist_views:105 - dependency computed
2021-10-24 02:55:54.551 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:54.570 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:55.144 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:55.161 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:55.739 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:55.757 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:56.320 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:56.335 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:56.931 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:56.946 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:57.544 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:57.561 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:58.102 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:58.117 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:58.713 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:58.728 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:59.341 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:55:59.358 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:55:59.990 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:00.004 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:00.603 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:00.617 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:01.218 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:01.232 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:01.808 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:01.822 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:02.438 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:02.454 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:03.044 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:03.058 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:03.664 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:03.677 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:04.252 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:04.268 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:04.843 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:04.861 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:05.407 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:05.421 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:05.996 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:06.011 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:06.587 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:06.603 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:07.173 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:07.188 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:07.764 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:07.777 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:08.413 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:08.427 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:08.989 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:09.004 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:09.593 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:09.608 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:10.217 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:10.233 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:10.819 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:10.835 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:11.422 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:11.439 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
2021-10-24 02:56:12.017 | DEBUG    | lib_dpsyn.consistent:consist_views:131 - consist finish
2021-10-24 02:56:12.032 | DEBUG    | lib_dpsyn.consistent:consist_views:148 - non-negativity finish
------------------------> attributes:
['Date', 'Age', 'Sex', 'Race', 'Residence State', 'Death County', 'Location', 'Location if Other', 'Injury County', 'Injury State', 'Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl Analogue', 'Oxycodone', 'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine (Not Heroin)', 'Hydromorphone', 'Xylazine', 'Opiate NOS', 'Any Opioid', 'CardioCondition', 'RespiratoryCondition', 'ObesityCondition', 'DiabetesCondition']
------------------------> domains:
[ 9  9  2  7 11  9  7 10 15  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2
  2  2  2  2  2  2  2]
------------------------> cluseters:
{('ObesityCondition', 'Methadone', 'Benzodiazepine', 'Opiate NOS', 'Fentanyl Analogue', 'Fentanyl', 'Any Opioid', 'Hydromorphone', 'Tramad', 'DiabetesCondition', 'Cocaine', 'Oxycodone', 'Date', 'Sex', 'Location', 'Amphet', 'Morphine (Not Heroin)', 'Heroin', 'Hydrocodone', 'Ethanol', 'Location if Other', 'Death County', 'Injury County', 'Race', 'Oxymorphone', 'Injury State', 'Residence State', 'Xylazine', 'CardioCondition', 'Age', 'RespiratoryCondition'): [frozenset({'Date', 'Age'}), frozenset({'Date', 'Sex'}), frozenset({'Date', 'Race'}), frozenset({'Date', 'Residence State'}), frozenset({'Date', 'Death County'}), frozenset({'Date', 'Location'}), frozenset({'Date', 'Location if Other'}), frozenset({'Date', 'Injury County'}), frozenset({'Date', 'Injury State'}), frozenset({'Heroin', 'Date'}), frozenset({'Date', 'Cocaine'}), frozenset({'Date', 'Fentanyl'}), frozenset({'Date', 'Fentanyl Analogue'}), frozenset({'Date', 'Oxycodone'}), frozenset({'Date', 'Oxymorphone'}), frozenset({'Date', 'Ethanol'}), frozenset({'Date', 'Hydrocodone'}), frozenset({'Date', 'Benzodiazepine'}), frozenset({'Date', 'Methadone'}), frozenset({'Date', 'Amphet'}), frozenset({'Date', 'Tramad'}), frozenset({'Date', 'Morphine (Not Heroin)'}), frozenset({'Date', 'Hydromorphone'}), frozenset({'Date', 'Xylazine'}), frozenset({'Date', 'Opiate NOS'}), frozenset({'Date', 'Any Opioid'}), frozenset({'Date', 'CardioCondition'}), frozenset({'Date', 'RespiratoryCondition'}), frozenset({'Date', 'ObesityCondition'}), frozenset({'Date', 'DiabetesCondition'}), frozenset({'Sex', 'Age'}), frozenset({'Age', 'Race'}), frozenset({'Residence State', 'Age'}), frozenset({'Death County', 'Age'}), frozenset({'Location', 'Age'}), frozenset({'Location if Other', 'Age'}), frozenset({'Injury County', 'Age'}), frozenset({'Age', 'Injury State'}), frozenset({'Heroin', 'Age'}), frozenset({'Age', 'Cocaine'}), frozenset({'Age', 'Fentanyl'}), frozenset({'Fentanyl Analogue', 'Age'}), frozenset({'Age', 'Oxycodone'}), frozenset({'Age', 'Oxymorphone'}), frozenset({'Age', 'Ethanol'}), frozenset({'Hydrocodone', 'Age'}), frozenset({'Benzodiazepine', 'Age'}), frozenset({'Age', 'Methadone'}), frozenset({'Amphet', 'Age'}), frozenset({'Tramad', 'Age'}), frozenset({'Morphine (Not Heroin)', 'Age'}), frozenset({'Hydromorphone', 'Age'}), frozenset({'Xylazine', 'Age'}), frozenset({'Opiate NOS', 'Age'}), frozenset({'Age', 'Any Opioid'}), frozenset({'CardioCondition', 'Age'}), frozenset({'Age', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Age'}), frozenset({'DiabetesCondition', 'Age'}), frozenset({'Sex', 'Race'}), frozenset({'Residence State', 'Sex'}), frozenset({'Sex', 'Death County'}), frozenset({'Location', 'Sex'}), frozenset({'Sex', 'Location if Other'}), frozenset({'Sex', 'Injury County'}), frozenset({'Sex', 'Injury State'}), frozenset({'Heroin', 'Sex'}), frozenset({'Sex', 'Cocaine'}), frozenset({'Sex', 'Fentanyl'}), frozenset({'Sex', 'Fentanyl Analogue'}), frozenset({'Sex', 'Oxycodone'}), frozenset({'Sex', 'Oxymorphone'}), frozenset({'Sex', 'Ethanol'}), frozenset({'Sex', 'Hydrocodone'}), frozenset({'Sex', 'Benzodiazepine'}), frozenset({'Sex', 'Methadone'}), frozenset({'Sex', 'Amphet'}), frozenset({'Sex', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Sex'}), frozenset({'Sex', 'Hydromorphone'}), frozenset({'Sex', 'Xylazine'}), frozenset({'Sex', 'Opiate NOS'}), frozenset({'Sex', 'Any Opioid'}), frozenset({'Sex', 'CardioCondition'}), frozenset({'Sex', 'RespiratoryCondition'}), frozenset({'Sex', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Sex'}), frozenset({'Residence State', 'Race'}), frozenset({'Death County', 'Race'}), frozenset({'Location', 'Race'}), frozenset({'Location if Other', 'Race'}), frozenset({'Injury County', 'Race'}), frozenset({'Injury State', 'Race'}), frozenset({'Heroin', 'Race'}), frozenset({'Race', 'Cocaine'}), frozenset({'Fentanyl', 'Race'}), frozenset({'Fentanyl Analogue', 'Race'}), frozenset({'Race', 'Oxycodone'}), frozenset({'Race', 'Oxymorphone'}), frozenset({'Ethanol', 'Race'}), frozenset({'Hydrocodone', 'Race'}), frozenset({'Benzodiazepine', 'Race'}), frozenset({'Race', 'Methadone'}), frozenset({'Amphet', 'Race'}), frozenset({'Tramad', 'Race'}), frozenset({'Morphine (Not Heroin)', 'Race'}), frozenset({'Hydromorphone', 'Race'}), frozenset({'Xylazine', 'Race'}), frozenset({'Opiate NOS', 'Race'}), frozenset({'Race', 'Any Opioid'}), frozenset({'CardioCondition', 'Race'}), frozenset({'RespiratoryCondition', 'Race'}), frozenset({'ObesityCondition', 'Race'}), frozenset({'DiabetesCondition', 'Race'}), frozenset({'Residence State', 'Death County'}), frozenset({'Residence State', 'Location'}), frozenset({'Residence State', 'Location if Other'}), frozenset({'Residence State', 'Injury County'}), frozenset({'Residence State', 'Injury State'}), frozenset({'Heroin', 'Residence State'}), frozenset({'Residence State', 'Cocaine'}), frozenset({'Residence State', 'Fentanyl'}), frozenset({'Residence State', 'Fentanyl Analogue'}), frozenset({'Residence State', 'Oxycodone'}), frozenset({'Residence State', 'Oxymorphone'}), frozenset({'Residence State', 'Ethanol'}), frozenset({'Residence State', 'Hydrocodone'}), frozenset({'Residence State', 'Benzodiazepine'}), frozenset({'Residence State', 'Methadone'}), frozenset({'Residence State', 'Amphet'}), frozenset({'Residence State', 'Tramad'}), frozenset({'Residence State', 'Morphine (Not Heroin)'}), frozenset({'Residence State', 'Hydromorphone'}), frozenset({'Residence State', 'Xylazine'}), frozenset({'Residence State', 'Opiate NOS'}), frozenset({'Residence State', 'Any Opioid'}), frozenset({'Residence State', 'CardioCondition'}), frozenset({'Residence State', 'RespiratoryCondition'}), frozenset({'Residence State', 'ObesityCondition'}), frozenset({'Residence State', 'DiabetesCondition'}), frozenset({'Location', 'Death County'}), frozenset({'Location if Other', 'Death County'}), frozenset({'Injury County', 'Death County'}), frozenset({'Death County', 'Injury State'}), frozenset({'Heroin', 'Death County'}), frozenset({'Death County', 'Cocaine'}), frozenset({'Death County', 'Fentanyl'}), frozenset({'Fentanyl Analogue', 'Death County'}), frozenset({'Death County', 'Oxycodone'}), frozenset({'Death County', 'Oxymorphone'}), frozenset({'Death County', 'Ethanol'}), frozenset({'Death County', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Death County'}), frozenset({'Death County', 'Methadone'}), frozenset({'Amphet', 'Death County'}), frozenset({'Death County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Death County'}), frozenset({'Death County', 'Hydromorphone'}), frozenset({'Death County', 'Xylazine'}), frozenset({'Opiate NOS', 'Death County'}), frozenset({'Death County', 'Any Opioid'}), frozenset({'CardioCondition', 'Death County'}), frozenset({'Death County', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Death County'}), frozenset({'DiabetesCondition', 'Death County'}), frozenset({'Location', 'Location if Other'}), frozenset({'Location', 'Injury County'}), frozenset({'Location', 'Injury State'}), frozenset({'Heroin', 'Location'}), frozenset({'Location', 'Cocaine'}), frozenset({'Location', 'Fentanyl'}), frozenset({'Location', 'Fentanyl Analogue'}), frozenset({'Location', 'Oxycodone'}), frozenset({'Location', 'Oxymorphone'}), frozenset({'Location', 'Ethanol'}), frozenset({'Location', 'Hydrocodone'}), frozenset({'Location', 'Benzodiazepine'}), frozenset({'Location', 'Methadone'}), frozenset({'Location', 'Amphet'}), frozenset({'Location', 'Tramad'}), frozenset({'Location', 'Morphine (Not Heroin)'}), frozenset({'Location', 'Hydromorphone'}), frozenset({'Location', 'Xylazine'}), frozenset({'Location', 'Opiate NOS'}), frozenset({'Location', 'Any Opioid'}), frozenset({'Location', 'CardioCondition'}), frozenset({'Location', 'RespiratoryCondition'}), frozenset({'Location', 'ObesityCondition'}), frozenset({'Location', 'DiabetesCondition'}), frozenset({'Location if Other', 'Injury County'}), frozenset({'Location if Other', 'Injury State'}), frozenset({'Heroin', 'Location if Other'}), frozenset({'Location if Other', 'Cocaine'}), frozenset({'Location if Other', 'Fentanyl'}), frozenset({'Location if Other', 'Fentanyl Analogue'}), frozenset({'Location if Other', 'Oxycodone'}), frozenset({'Location if Other', 'Oxymorphone'}), frozenset({'Location if Other', 'Ethanol'}), frozenset({'Location if Other', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Location if Other'}), frozenset({'Location if Other', 'Methadone'}), frozenset({'Amphet', 'Location if Other'}), frozenset({'Location if Other', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Location if Other'}), frozenset({'Location if Other', 'Hydromorphone'}), frozenset({'Location if Other', 'Xylazine'}), frozenset({'Opiate NOS', 'Location if Other'}), frozenset({'Location if Other', 'Any Opioid'}), frozenset({'Location if Other', 'CardioCondition'}), frozenset({'Location if Other', 'RespiratoryCondition'}), frozenset({'Location if Other', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Location if Other'}), frozenset({'Injury County', 'Injury State'}), frozenset({'Heroin', 'Injury County'}), frozenset({'Injury County', 'Cocaine'}), frozenset({'Injury County', 'Fentanyl'}), frozenset({'Fentanyl Analogue', 'Injury County'}), frozenset({'Injury County', 'Oxycodone'}), frozenset({'Injury County', 'Oxymorphone'}), frozenset({'Injury County', 'Ethanol'}), frozenset({'Injury County', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Injury County'}), frozenset({'Injury County', 'Methadone'}), frozenset({'Amphet', 'Injury County'}), frozenset({'Injury County', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Injury County'}), frozenset({'Injury County', 'Hydromorphone'}), frozenset({'Injury County', 'Xylazine'}), frozenset({'Opiate NOS', 'Injury County'}), frozenset({'Injury County', 'Any Opioid'}), frozenset({'CardioCondition', 'Injury County'}), frozenset({'Injury County', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Injury County'}), frozenset({'DiabetesCondition', 'Injury County'}), frozenset({'Heroin', 'Injury State'}), frozenset({'Injury State', 'Cocaine'}), frozenset({'Fentanyl', 'Injury State'}), frozenset({'Fentanyl Analogue', 'Injury State'}), frozenset({'Injury State', 'Oxycodone'}), frozenset({'Injury State', 'Oxymorphone'}), frozenset({'Ethanol', 'Injury State'}), frozenset({'Hydrocodone', 'Injury State'}), frozenset({'Benzodiazepine', 'Injury State'}), frozenset({'Injury State', 'Methadone'}), frozenset({'Amphet', 'Injury State'}), frozenset({'Tramad', 'Injury State'}), frozenset({'Morphine (Not Heroin)', 'Injury State'}), frozenset({'Hydromorphone', 'Injury State'}), frozenset({'Xylazine', 'Injury State'}), frozenset({'Opiate NOS', 'Injury State'}), frozenset({'Injury State', 'Any Opioid'}), frozenset({'CardioCondition', 'Injury State'}), frozenset({'RespiratoryCondition', 'Injury State'}), frozenset({'ObesityCondition', 'Injury State'}), frozenset({'DiabetesCondition', 'Injury State'}), frozenset({'Heroin', 'Cocaine'}), frozenset({'Heroin', 'Fentanyl'}), frozenset({'Heroin', 'Fentanyl Analogue'}), frozenset({'Heroin', 'Oxycodone'}), frozenset({'Heroin', 'Oxymorphone'}), frozenset({'Heroin', 'Ethanol'}), frozenset({'Heroin', 'Hydrocodone'}), frozenset({'Heroin', 'Benzodiazepine'}), frozenset({'Heroin', 'Methadone'}), frozenset({'Heroin', 'Amphet'}), frozenset({'Heroin', 'Tramad'}), frozenset({'Heroin', 'Morphine (Not Heroin)'}), frozenset({'Heroin', 'Hydromorphone'}), frozenset({'Heroin', 'Xylazine'}), frozenset({'Heroin', 'Opiate NOS'}), frozenset({'Heroin', 'Any Opioid'}), frozenset({'Heroin', 'CardioCondition'}), frozenset({'Heroin', 'RespiratoryCondition'}), frozenset({'Heroin', 'ObesityCondition'}), frozenset({'Heroin', 'DiabetesCondition'}), frozenset({'Fentanyl', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Cocaine'}), frozenset({'Oxycodone', 'Cocaine'}), frozenset({'Oxymorphone', 'Cocaine'}), frozenset({'Ethanol', 'Cocaine'}), frozenset({'Hydrocodone', 'Cocaine'}), frozenset({'Benzodiazepine', 'Cocaine'}), frozenset({'Methadone', 'Cocaine'}), frozenset({'Amphet', 'Cocaine'}), frozenset({'Tramad', 'Cocaine'}), frozenset({'Morphine (Not Heroin)', 'Cocaine'}), frozenset({'Hydromorphone', 'Cocaine'}), frozenset({'Xylazine', 'Cocaine'}), frozenset({'Opiate NOS', 'Cocaine'}), frozenset({'Any Opioid', 'Cocaine'}), frozenset({'CardioCondition', 'Cocaine'}), frozenset({'RespiratoryCondition', 'Cocaine'}), frozenset({'ObesityCondition', 'Cocaine'}), frozenset({'DiabetesCondition', 'Cocaine'}), frozenset({'Fentanyl Analogue', 'Fentanyl'}), frozenset({'Fentanyl', 'Oxycodone'}), frozenset({'Fentanyl', 'Oxymorphone'}), frozenset({'Ethanol', 'Fentanyl'}), frozenset({'Hydrocodone', 'Fentanyl'}), frozenset({'Benzodiazepine', 'Fentanyl'}), frozenset({'Fentanyl', 'Methadone'}), frozenset({'Amphet', 'Fentanyl'}), frozenset({'Tramad', 'Fentanyl'}), frozenset({'Morphine (Not Heroin)', 'Fentanyl'}), frozenset({'Hydromorphone', 'Fentanyl'}), frozenset({'Xylazine', 'Fentanyl'}), frozenset({'Opiate NOS', 'Fentanyl'}), frozenset({'Fentanyl', 'Any Opioid'}), frozenset({'CardioCondition', 'Fentanyl'}), frozenset({'RespiratoryCondition', 'Fentanyl'}), frozenset({'ObesityCondition', 'Fentanyl'}), frozenset({'DiabetesCondition', 'Fentanyl'}), frozenset({'Fentanyl Analogue', 'Oxycodone'}), frozenset({'Fentanyl Analogue', 'Oxymorphone'}), frozenset({'Fentanyl Analogue', 'Ethanol'}), frozenset({'Fentanyl Analogue', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Methadone'}), frozenset({'Amphet', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Hydromorphone'}), frozenset({'Fentanyl Analogue', 'Xylazine'}), frozenset({'Opiate NOS', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'Any Opioid'}), frozenset({'CardioCondition', 'Fentanyl Analogue'}), frozenset({'Fentanyl Analogue', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Fentanyl Analogue'}), frozenset({'DiabetesCondition', 'Fentanyl Analogue'}), frozenset({'Oxymorphone', 'Oxycodone'}), frozenset({'Ethanol', 'Oxycodone'}), frozenset({'Hydrocodone', 'Oxycodone'}), frozenset({'Benzodiazepine', 'Oxycodone'}), frozenset({'Methadone', 'Oxycodone'}), frozenset({'Amphet', 'Oxycodone'}), frozenset({'Tramad', 'Oxycodone'}), frozenset({'Morphine (Not Heroin)', 'Oxycodone'}), frozenset({'Hydromorphone', 'Oxycodone'}), frozenset({'Xylazine', 'Oxycodone'}), frozenset({'Opiate NOS', 'Oxycodone'}), frozenset({'Any Opioid', 'Oxycodone'}), frozenset({'CardioCondition', 'Oxycodone'}), frozenset({'RespiratoryCondition', 'Oxycodone'}), frozenset({'ObesityCondition', 'Oxycodone'}), frozenset({'DiabetesCondition', 'Oxycodone'}), frozenset({'Ethanol', 'Oxymorphone'}), frozenset({'Hydrocodone', 'Oxymorphone'}), frozenset({'Benzodiazepine', 'Oxymorphone'}), frozenset({'Methadone', 'Oxymorphone'}), frozenset({'Amphet', 'Oxymorphone'}), frozenset({'Tramad', 'Oxymorphone'}), frozenset({'Morphine (Not Heroin)', 'Oxymorphone'}), frozenset({'Hydromorphone', 'Oxymorphone'}), frozenset({'Xylazine', 'Oxymorphone'}), frozenset({'Opiate NOS', 'Oxymorphone'}), frozenset({'Any Opioid', 'Oxymorphone'}), frozenset({'CardioCondition', 'Oxymorphone'}), frozenset({'RespiratoryCondition', 'Oxymorphone'}), frozenset({'ObesityCondition', 'Oxymorphone'}), frozenset({'DiabetesCondition', 'Oxymorphone'}), frozenset({'Hydrocodone', 'Ethanol'}), frozenset({'Benzodiazepine', 'Ethanol'}), frozenset({'Ethanol', 'Methadone'}), frozenset({'Amphet', 'Ethanol'}), frozenset({'Tramad', 'Ethanol'}), frozenset({'Morphine (Not Heroin)', 'Ethanol'}), frozenset({'Hydromorphone', 'Ethanol'}), frozenset({'Xylazine', 'Ethanol'}), frozenset({'Opiate NOS', 'Ethanol'}), frozenset({'Ethanol', 'Any Opioid'}), frozenset({'CardioCondition', 'Ethanol'}), frozenset({'RespiratoryCondition', 'Ethanol'}), frozenset({'ObesityCondition', 'Ethanol'}), frozenset({'DiabetesCondition', 'Ethanol'}), frozenset({'Benzodiazepine', 'Hydrocodone'}), frozenset({'Hydrocodone', 'Methadone'}), frozenset({'Amphet', 'Hydrocodone'}), frozenset({'Tramad', 'Hydrocodone'}), frozenset({'Morphine (Not Heroin)', 'Hydrocodone'}), frozenset({'Hydromorphone', 'Hydrocodone'}), frozenset({'Xylazine', 'Hydrocodone'}), frozenset({'Opiate NOS', 'Hydrocodone'}), frozenset({'Hydrocodone', 'Any Opioid'}), frozenset({'CardioCondition', 'Hydrocodone'}), frozenset({'Hydrocodone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Hydrocodone'}), frozenset({'DiabetesCondition', 'Hydrocodone'}), frozenset({'Benzodiazepine', 'Methadone'}), frozenset({'Benzodiazepine', 'Amphet'}), frozenset({'Benzodiazepine', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Benzodiazepine'}), frozenset({'Benzodiazepine', 'Hydromorphone'}), frozenset({'Benzodiazepine', 'Xylazine'}), frozenset({'Benzodiazepine', 'Opiate NOS'}), frozenset({'Benzodiazepine', 'Any Opioid'}), frozenset({'Benzodiazepine', 'CardioCondition'}), frozenset({'Benzodiazepine', 'RespiratoryCondition'}), frozenset({'Benzodiazepine', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Benzodiazepine'}), frozenset({'Amphet', 'Methadone'}), frozenset({'Tramad', 'Methadone'}), frozenset({'Morphine (Not Heroin)', 'Methadone'}), frozenset({'Hydromorphone', 'Methadone'}), frozenset({'Xylazine', 'Methadone'}), frozenset({'Opiate NOS', 'Methadone'}), frozenset({'Any Opioid', 'Methadone'}), frozenset({'CardioCondition', 'Methadone'}), frozenset({'RespiratoryCondition', 'Methadone'}), frozenset({'ObesityCondition', 'Methadone'}), frozenset({'DiabetesCondition', 'Methadone'}), frozenset({'Amphet', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Amphet'}), frozenset({'Amphet', 'Hydromorphone'}), frozenset({'Amphet', 'Xylazine'}), frozenset({'Amphet', 'Opiate NOS'}), frozenset({'Amphet', 'Any Opioid'}), frozenset({'Amphet', 'CardioCondition'}), frozenset({'Amphet', 'RespiratoryCondition'}), frozenset({'Amphet', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Amphet'}), frozenset({'Morphine (Not Heroin)', 'Tramad'}), frozenset({'Hydromorphone', 'Tramad'}), frozenset({'Xylazine', 'Tramad'}), frozenset({'Opiate NOS', 'Tramad'}), frozenset({'Tramad', 'Any Opioid'}), frozenset({'CardioCondition', 'Tramad'}), frozenset({'Tramad', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Tramad'}), frozenset({'DiabetesCondition', 'Tramad'}), frozenset({'Morphine (Not Heroin)', 'Hydromorphone'}), frozenset({'Morphine (Not Heroin)', 'Xylazine'}), frozenset({'Morphine (Not Heroin)', 'Opiate NOS'}), frozenset({'Morphine (Not Heroin)', 'Any Opioid'}), frozenset({'Morphine (Not Heroin)', 'CardioCondition'}), frozenset({'Morphine (Not Heroin)', 'RespiratoryCondition'}), frozenset({'Morphine (Not Heroin)', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Morphine (Not Heroin)'}), frozenset({'Hydromorphone', 'Xylazine'}), frozenset({'Opiate NOS', 'Hydromorphone'}), frozenset({'Hydromorphone', 'Any Opioid'}), frozenset({'CardioCondition', 'Hydromorphone'}), frozenset({'Hydromorphone', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Hydromorphone'}), frozenset({'DiabetesCondition', 'Hydromorphone'}), frozenset({'Opiate NOS', 'Xylazine'}), frozenset({'Xylazine', 'Any Opioid'}), frozenset({'CardioCondition', 'Xylazine'}), frozenset({'Xylazine', 'RespiratoryCondition'}), frozenset({'ObesityCondition', 'Xylazine'}), frozenset({'DiabetesCondition', 'Xylazine'}), frozenset({'Opiate NOS', 'Any Opioid'}), frozenset({'Opiate NOS', 'CardioCondition'}), frozenset({'Opiate NOS', 'RespiratoryCondition'}), frozenset({'Opiate NOS', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'Opiate NOS'}), frozenset({'CardioCondition', 'Any Opioid'}), frozenset({'RespiratoryCondition', 'Any Opioid'}), frozenset({'ObesityCondition', 'Any Opioid'}), frozenset({'DiabetesCondition', 'Any Opioid'}), frozenset({'CardioCondition', 'RespiratoryCondition'}), frozenset({'CardioCondition', 'ObesityCondition'}), frozenset({'DiabetesCondition', 'CardioCondition'}), frozenset({'ObesityCondition', 'RespiratoryCondition'}), frozenset({'DiabetesCondition', 'RespiratoryCondition'}), frozenset({'DiabetesCondition', 'ObesityCondition'})]}
********************* START SYNTHESIZING RECORDS ********************
------------------------> num of synthesized records:
7630
2021-10-24 02:56:12.048 | INFO     | method.dpsyn:synthesize_records:155 - synthesizing for ('ObesityCondition', 'Methadone', 'Benzodiazepine', 'Opiate NOS', 'Fentanyl Analogue', 'Fentanyl', 'Any Opioid', 'Hydromorphone', 'Tramad', 'DiabetesCondition', 'Cocaine', 'Oxycodone', 'Date', 'Sex', 'Location', 'Amphet', 'Morphine (Not Heroin)', 'Heroin', 'Hydrocodone', 'Ethanol', 'Location if Other', 'Death County', 'Injury County', 'Race', 'Oxymorphone', 'Injury State', 'Residence State', 'Xylazine', 'CardioCondition', 'Age', 'RespiratoryCondition')
2021-10-24 02:56:12.056 | INFO     | method.dpsyn:synthesize_records:171 - update round: 0
2021-10-24 02:56:12.891 | INFO     | method.dpsyn:synthesize_records:171 - update round: 1
2021-10-24 02:56:13.824 | INFO     | method.dpsyn:synthesize_records:171 - update round: 2
2021-10-24 02:56:14.768 | INFO     | method.dpsyn:synthesize_records:171 - update round: 3
2021-10-24 02:56:15.740 | INFO     | method.dpsyn:synthesize_records:171 - update round: 4
2021-10-24 02:56:16.677 | INFO     | method.dpsyn:synthesize_records:171 - update round: 5
2021-10-24 02:56:17.574 | INFO     | method.dpsyn:synthesize_records:171 - update round: 6
2021-10-24 02:56:18.557 | INFO     | method.dpsyn:synthesize_records:171 - update round: 7
2021-10-24 02:56:19.475 | INFO     | method.dpsyn:synthesize_records:171 - update round: 8
2021-10-24 02:56:20.410 | INFO     | method.dpsyn:synthesize_records:171 - update round: 9
2021-10-24 02:56:21.304 | INFO     | method.dpsyn:synthesize_records:171 - update round: 10
2021-10-24 02:56:22.208 | INFO     | method.dpsyn:synthesize_records:171 - update round: 11
2021-10-24 02:56:23.191 | INFO     | method.dpsyn:synthesize_records:171 - update round: 12
2021-10-24 02:56:24.100 | INFO     | method.dpsyn:synthesize_records:171 - update round: 13
2021-10-24 02:56:25.083 | INFO     | method.dpsyn:synthesize_records:171 - update round: 14
2021-10-24 02:56:26.088 | INFO     | method.dpsyn:synthesize_records:171 - update round: 15
2021-10-24 02:56:26.988 | INFO     | method.dpsyn:synthesize_records:171 - update round: 16
2021-10-24 02:56:27.896 | INFO     | method.dpsyn:synthesize_records:171 - update round: 17
2021-10-24 02:56:28.774 | INFO     | method.dpsyn:synthesize_records:171 - update round: 18
2021-10-24 02:56:29.664 | INFO     | method.dpsyn:synthesize_records:171 - update round: 19
2021-10-24 02:56:30.559 | INFO     | method.dpsyn:synthesize_records:171 - update round: 20
2021-10-24 02:56:31.492 | INFO     | method.dpsyn:synthesize_records:171 - update round: 21
2021-10-24 02:56:32.401 | INFO     | method.dpsyn:synthesize_records:171 - update round: 22
2021-10-24 02:56:33.313 | INFO     | method.dpsyn:synthesize_records:171 - update round: 23
2021-10-24 02:56:34.290 | INFO     | method.dpsyn:synthesize_records:171 - update round: 24
2021-10-24 02:56:35.267 | INFO     | method.dpsyn:synthesize_records:171 - update round: 25
2021-10-24 02:56:36.238 | INFO     | method.dpsyn:synthesize_records:171 - update round: 26
2021-10-24 02:56:37.207 | INFO     | method.dpsyn:synthesize_records:171 - update round: 27
2021-10-24 02:56:38.205 | INFO     | method.dpsyn:synthesize_records:171 - update round: 28
2021-10-24 02:56:39.222 | INFO     | method.dpsyn:synthesize_records:171 - update round: 29
------------------------> synthetic dataframe before postprocessing:
      Date  Age  Sex  Race  Residence State  Death County  ...  Opiate NOS  Any Opioid  CardioCondition  RespiratoryCondition  ObesityCondition  DiabetesCondition
0        3    4    1     6                8             7  ...           0           0                1                     1                 1                  1
1        6    0    1     0               10             6  ...           1           1                0                     0                 0                  0
2        5    5    0     4                3             4  ...           1           0                0                     1                 1                  1
3        8    8    0     3                4             5  ...           1           1                1                     0                 1                  1
4        4    3    1     2                5             7  ...           1           1                1                     0                 1                  1
...    ...  ...  ...   ...              ...           ...  ...         ...         ...              ...                   ...               ...                ...
7625     6    4    1     1                5             0  ...           0           0                0                     1                 0                  0
7626     0    4    0     2                2             5  ...           1           0                0                     1                 0                  1
7627     3    2    1     3                8             3  ...           0           1                1                     1                 0                  1
7628     7    2    0     2                5             1  ...           1           1                0                     0                 1                  1
7629     0    1    1     6               10             8  ...           1           1                1                     0                 1                  1

[7630 rows x 31 columns]
********************* START POSTPROCESSING ***********************
unbinning attributes ------------------------>
decode other attributes ------------------------>
2021-10-24 02:56:40.341 | INFO     | __main__:run_method:162 - ------------------------>synthetic data post-processed:
      Date  Age     Sex             Race Residence State Death County  ... Any Opioid CardioCondition RespiratoryCondition ObesityCondition DiabetesCondition epsilon
0     2015   49    MALE            WHITE              PA      TOLLAND  ...                          Y                    Y                Y                 Y    10.0
1     2018   13    MALE                               TX   NEW LONDON  ...          Y                                                                            10.0
2     2017   59  FEMALE  HISPANIC, WHITE              FL    MIDDLESEX  ...                                               Y                Y                 Y    10.0
3     2020   85  FEMALE  HISPANIC, BLACK              MA    NEW HAVEN  ...          Y               Y                                     Y                 Y    10.0
4     2016   39    MALE            BLACK              NC      TOLLAND  ...          Y               Y                                     Y                 Y    10.0
...    ...  ...     ...              ...             ...          ...  ...        ...             ...                  ...              ...               ...     ...
7625  2018   49    MALE            ASIAN              NC               ...                                               Y                                       10.0
7626  2012   49  FEMALE            BLACK              CT    NEW HAVEN  ...                                               Y                                  Y    10.0
7627  2015   29    MALE  HISPANIC, BLACK              PA   LITCHFIELD  ...          Y               Y                    Y                                  Y    10.0
7628  2019   29  FEMALE            BLACK              NC    FAIRFIELD  ...          Y                                                     Y                 Y    10.0
7629  2012   19    MALE            WHITE              TX      WINDHAM  ...          Y               Y                                     Y                 Y    10.0

[7630 rows x 32 columns]
```



### Run the python file 

You can directly download the repository from github and use our tool without docker support.

Firstly, create an environment with python 3.9.0 and install relied packages by:

```
pip install -r requirements.txt
```

Then you can directly run the python file.

We use the tool argparse for users to customize the input parameters and the usage message is shown below.

To get a better understanding of the args' meanings, you can refer to the default values of them in experiment.py and the run example we provided in later part.

We require you to input **--priv_data_name** to help us naming processed pkl files and avoid possible faults like mistaking A dataset for B.

Since we already include the accidential_drug_deaths dataset as an example, in this case, the simplest command looks like below：

Note that the existing "preprocessed_priv_testpkl.pkl" in /data/pkl is generated by the command and the pkl step serves for storing a processed dataset and reuse it later, for more details you can search "how pickle file works" in Google ; )

```
>python experiment.py --priv_data_name testpkl
```

As to the meanings of all parameters, we display it as below:

```
>python experiment.py -h
usage: experiment.py [-h] [--priv_data PRIV_DATA] [--priv_data_name PRIV_DATA_NAME] [--config CONFIG] [--n N]
                     [--params PARAMS] [--datatype DATATYPE] [--marginal_config MARGINAL_CONFIG]
                     [--update_iterations UPDATE_ITERATIONS] [--target_path TARGET_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --priv_data PRIV_DATA
                        specify the path of original data file in csv format
  --priv_data_name PRIV_DATA_NAME
                        users must specify it to help mid-way naming and avoid possible mistakings
  --config CONFIG       specify the path of config file in yaml format
  --n N                 specify the number of records to generate
  --params PARAMS       specify the path of parameters file in json format
  --datatype DATATYPE   specify the path of datatype file in json format
  --marginal_config MARGINAL_CONFIG
                        specify the path of marginal config file in yaml format
  --update_iterations UPDATE_ITERATIONS
                        specify the num of update iterations
  --target_path TARGET_PATH
                        specify the target path of the synthetic dataset
```



----

### How to configure?

First, you preprocess the input dataset (the input dataset should be in format of filename.csv with its first row a header row). A [tool]( https://github.com/hd23408/nist-schemagen ) is provided to help generate schema files: **(1) [parameters.json](data/parameters.json)** ( users should add "runs" parameters later in this file ) **(2) [column_datatypes.json](data/column_datatypes.json)** from the original dataset.

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
The next step is to specify marginal settings in marginal config file like **[eps=xxx.yaml](config/eps=10.0.yaml)** ( each eps=xxx.yaml corresponds to each epsilon=xxx in parameters.json ).

##### 2. Marginal selection config

Suppose epsilon parameter in "runs" of parameters.json is 10 now.  We will go to eps=10.0.yaml ( in [/config](config) ) to find the marginal configuration. In this example, we use all the two way marginals, i.e., "priv_all_two_way":

```yaml
priv_all_two_way:
  total_eps: 10
```

##### 3. Data config

Finally, you need to config [data.yaml](config/data.yaml) ( in [/config](config) ): 

You can specify the **identifier** attribute's name in data.yaml (we assume your dataset has the identifer attribute by default; obviously, in synthetic dataset the column should be removed to protect privacy). 

You can also specify **bin** settings in the format of [min, max, step] in numerical_binning in data.yaml based on your granuarity preference. ( Further, you can change more details in bin generation in binning_attributes() in DataLoader.py. )

Notice: by default we assume your input dataset include **identifier column** and at least one column with **numerical binning** specified.

Below is one example:

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

You can refer to **Synthpop** (a R package) as a tool to compare the synthesized dataset against the original one. And we provide a quick start document on using it in our repository: [Dataset comparison using Synthpop.docx](Dataset comparison using Synthpop.docx)

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



