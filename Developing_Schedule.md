# Developing Schedule
(tip: Note that git seetings to check about password login)

fix github use:

https://wallesspku.space/clash/caq@pku.edu.cn/njbet8z8v6
## we're in week-7 (Configration should be tackled)
1. review the backbone of PrivSyn, as to specific coding logic
2. run the code once to test dataset generation (even just on our groundtruth.csv and state-15-data.csv) 
3. As to the research, more related work to read (on histogram publishing, etc.) 


#### code essential problems
1.RecordPostprocessor()
2.Consistenter(self.onehot_view_dict, self.domain_list)
3.maybe need manully set: 
def update_alpha(self, iteration):
   self.alpha = 1.0 * 0.84 ** (iteration // 20)
4.tmp = synthesizer.synthesize(fixed_n=n) n=0 means what?
 "max_records": 1350000 (looks like this one?)

5.it seems that the coding logic already uses only general functions without relation with PUMA, YEAR things?
    #　we call it in experiment.py by 
    #  tmp = synthesizer.synthesize(fixed_n=n)
    # in below function, we call synthesize_records()
    # it further utilize the lib function in record_synthesizer.py
    # def synthesize(self, fixed_n=0) -> pd.DataFrame:
6.As to the project here, we skip the step of choosing marginals and simply do that manually...
(I haven't found where we choose marginals)

------------------------------------------------
#### not very import problems 
1.what the difference between data.yaml & data_no_encode.yaml?
2.what's the scoring functions in original experiment.py file?
```
    # if n == 0:
    #     # here we encounter the use of bias_penalty_cutoff, but what does it mean?
    #     score_online(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data, parameters_json=Path(config['parameter_spec']), bias_penalty_cutoff=bias_penalty_cutoff)
    # else:
    #     if args.method == 'sample' or 'direct_sample':
    #         puma_year_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)
    #     else:
    #         iteration_detailed_score(ground_truth_csv=DATA_DIRECTORY / f"{config['priv_dataset_path']}.csv", submission_df=syn_data)
```
3.in experiment.py:
```
      # we import logger in synthesizer.py
      # we import DPSyn which inderitats synthesizer 
      # and I'm not sure whether it will import synthesizer.py too
```
4.there is a parameter called pub_only in load_data and I guess whether it is when we only input the public dataset?
5.earlier confusions:  
  noise_type = priv_split_method[set_key]
  def lap_adv_comp(epsilon, delta, sensitivity, k):
  zcdp and zcdp2 and rdp perform the same
  with open(args.config, 'r') as f:
  if pub_only:
  def reload_priv(self, new_data_path):


### received (have generally taken a look)
*general open-source repos on github*
*datasets to fit/ experiment/ generalize*
**(little)possible similar dp open-source repos **  
   e.g. https://github.com/opendp/smartnoise-core-python (have taken a look, it actually is a package in python while inner program is in Rust language)


### Done Background Knowledge:
0.python style guide by Google/official
1.python *logger*
2.*pylint* ( give it a shot ) to check code standard things 
Q：logger.()直接调用的话日志会去哪里，是不是跑该.py会输出呢，还是说存到了某个log文件
A：查资料发现默认是在运行时输出到终端，可以对basic setting做各种修改，只需要加上一两句话即可；
例如为输出到文件或者某些destination
Q:  为什么我在注释里面加option都能识别有用呢
A：可能和pylint运行时候的编译有关，总之这样可以对该module作出测试的option管理输出信息
3.yaml language specifications read
4.quick note about Package module to install by pip
5.learn the python package pandas in dealing with data
6.leran .csv file format
7.install R, Rstudio and learn the quick start of Synthpop R package



### Done 
1. upload the recommended datasets to s3 for possible use, but till now the local storage should suffice
2. already tried the measurment package synthpop (input 2 csv files but take care for debug I guess)


### Method Core work
1.
2. 







## for future possible use: 
0. sample/direct_sample/plain_pub(which use deepcopy, any polishing?)
1. <font color=red>generalization take care of fixed values:</font>>
   e.g.
    bias_penalty_cutoff = 250
   e.g.
    sensitivity = 'max_records_per_individual' which relies on the dataset settings
   e.g.
    post_processing (......)
    cases like puma_year_detailed......
2.### General configrations in ./config directory
1. in config/data.yaml, write the paths as claimed in the file's content
2. in config/data_type.py, write the value types of the attributes (easy with read_csv_kwargs.json obtained)
3. in config/path.py,  write the paths of input original dataset file, the public dataset file(if there exists one to refer to), the parameters file (attribute name,  value type, valid values, etc), etc
A: it seems that we set in data.yaml the path of parameters.json which is the schema, as well as the pub and priv data's paths that should suffice




## research thinking
 Besides, inspired by the access to a public dataset in the 20deID2 competition, in some cases (which is decided by specific method_decision algorithm), we turn to the public dataset instead of the privatized one to generate the query answer. 

refer to overleaf link


https://aws.amazon.com/s3/?did=ft_card&trk=ft_card
https://aws.amazon.com/sdk-for-python/
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

08/11 meet notes
1. maybe on Nov.8th(date to sync via email spread sheet) they'll hold a virtual workshop where we 3 teams are required to present how our package works and the output of the challenges
2. they've provided more public safety datasets to test on certain point (despite the fact that some of them might have to be cleaned to test on)
3. as to dataset storage, they suggest use free-tier aws3, for which tool related tutorials are offered, too
4. next week they want us to discuss more on how we think about configration and perhaps show user experience on how it works
5. a metric related package is also offered to help measure the synthesized dataset, which link is also provided (seeming that some fellows we can ask for help if in need)
6. they mention that after we supply the final work, they might ask NIST for help to allocate a permanent space to store our repositories for contributing to open-source work