# Developing Schedule

*<font color=green>2021.8.4</font>*

### received (have generally taken a look)

*general open-source repos on github*

### on-coming:

1. **(little)possible similar dp open-source repos **  

   e.g. https://github.com/opendp/smartnoise-core-python

2. **datasets to fit/ experiment/ generalize** 

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


## we're in week-4 (coding-style should be handled and Configration may be tackled ahead)

0. run pylint in method directory to test (naming, abbreviation)
1. read and understand,  add docstring / comments 
2. I'm thinking about how to set interface for configration (maybe read code and ask people for help) 
3. and I worry about generalization to some extent, maybe for I should consider the general performance later and do things step by step...
   
   
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




