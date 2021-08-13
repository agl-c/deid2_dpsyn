# Developing Schedule
weekly sync Link:
https://teams.microsoft.com/l/meetup-join/19%3ameeting_NzFjNmI1YWItYzMxOC00ZTYxLWExOGUtNzZkOGM4ZjI4NmJh%40thread.v2/0?context=%7b%22Tid%22%3a%222ab5d82f-d8fa-4797-a93e-054655c61dec%22%2c%22Oid%22%3a%221e8e3294-bdc8-4b0b-a61d-697689c9ea2a%22%7d
### received (have generally taken a look)
*general open-source repos on github*

### on-coming:
1. **(little)possible similar dp open-source repos **  
   e.g. https://github.com/opendp/smartnoise-core-python (have taken a look, it actually is a paclage in python while inner program is in Rust language)

2. **datasets to fit/ experiment/ generalize** (wait)

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
0. have run pylint in ./data, ./method  test
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