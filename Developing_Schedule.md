# Developing Schedule
Note that git seetings to check about password login
## we're in week-6 (coding-style should be handled and Configration may be tackled)
1. review the backbone of PrivSyn, as to specific coding logic
2. I'm thinking about how to set command line interface for configration  ( learn and ask) 

Q: what the difference between data.yaml & data_no_encode.yaml?

4. I want to run the code once to test dataset generation (even just on our groundtruth.csv and state-15-data.csv) 
5. As to the research, more related work to read (on histogram publishing, etc.) 


### received (have generally taken a look)
*general open-source repos on github*
*datasets to fit/ experiment/ generalize*
**(little)possible similar dp open-source repos **  
   e.g. https://github.com/opendp/smartnoise-core-python (have taken a look, it actually is a package in python while inner program is in Rust language)
### on-coming:
*schema generation tool will be available by the end of next week*


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
TODO: however, I encountered bugs when compare 2 datasets running the command line using the package's functions


### Done 
1. upload the recommended datasets to s3 for possible use, but till now the local storage should suffice
2. already tried the measurment package use (input 2 csv files but take care for debug I guess)


### Method Core work
1. how to set eps, delta, sensitivity? shall we ask users to specify these parameters? (suppose you want to privatize a dataset and have some detailed needs)
how to design the sensitive function? 
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
## research thinking
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