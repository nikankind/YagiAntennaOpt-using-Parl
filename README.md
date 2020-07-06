# YagiAntennaOpt-using-Parl
Optimization of Yagi Antenna Based on Reinforcement Learning Framework Parl

# 基于百度强化学习框架Parl的八木天线参数优化与仿真

Please consider to cite this environment if it can help your research.

如果该环境对您的研究有帮助，请考虑引用:

```txt
@misc{Quadrotor,
    author = {Kan Ni},
    title = {{Optimization of Yagi Antenna Based on Reinforcement Learning Framework Parl}},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/nikankind/YagiAntennaOpt-using-Parl/}},
}
```
## Introduction

In this project, design factor of an UHF band Yagi antenna was optimized using Baidu's reinforcement learning framework Parl. FEA simulation was performed with HFSS to compare the optimized antenna model with theoretical antenna model. And the result shows that all 5 design factors were approaching theoretical design after optimization,and the directivity factor of antenna model had raised to 14.29 from 0.98 in initial state. This project had explored utilization of reinforcement learning in antenna design, and is helpful to similar works in the future.

Please note that the Yagi antenna is analytically solutable, and in this project, a new method in antenna design was presented and tested deliberately with Yagi antenna model to judge the performance of the new method by comparing it with theoretical design. The method mentioned is also capable in design of more complicated antennas.

## 介绍
本项目利用百度强化学习框架对UHF段八木天线进行了参数优化，并利用HFSS有限元仿真软件对天线模型进行了仿真对比。仿真结果表明：经强化学习优化后，5个天线参数从初始乱序状态变为接近理论计算的状态，天线方向性从0.98上升到14.29。项目工作探索了强化学习在天线设计中的应用，对后续相关工作起到很好的参考作用。

八木天线本身可解析计算，本项目工作主要是探索了强化学习用于天线计算中的新方法，可迁移到其他更复杂的天线设计中。

## Project Work

## 项目工作

### 1 Introduction & Design Goal of Yagi Antenna

### 1 天线介绍及设计目标确定

Yagi antenna is popular in HAM radio as one kind of directive antenna. It is composed of driver, reflector and several directors, each of which is called an element. And the size of the elements and the distance between them are critical to performance of Yagi antenna.

八木天线是业余无线电中一种常用的指向性天线，主要由主振子、反射器、引向器组成。每个元件称为一个单元，各单元的尺寸及单元间距对八木天线性能起决定作用。

Image of Yagi Antenna

八木天线图片

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/timg.jpg)

A Yagi antenna with 7 elements, containing a driver, a reflector and 5 directors, were considered in this project, and the center frequency is 435MHz.

本项目拟设计一款7单元八木天线，包含1个主振子，1个反射器，5个引向器，中心频率435MHz

The optimization target is to maximize forward gain of Yagi antenna to achieve best directivity.

优化目标为：最大化八木天线前向增益，使八木天线指向性最好。

### 2 Design Factor Calculation

### 2 辅助软件计算

Theroetical calculation of Yagi antenna was performed as the illustration below. 

八木天线有成熟的计算软件，计算如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/4.png)

### 3 HFSS Modelling

### 3 HFSS建模

HFSS is a finite element analysis (FEA) software for electromagnetic simulation.

HFSS是一款有限元电磁仿真软件

Model path is as below.

模型路径：https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/Model/Yagi.aedt

HFSS version is 2018.2.

HFSS版本：2018.2

Modelling and simulation of Yagi antenna was performed using data in step 2, and the simulation result is shown below.

利用2中的计算结果对八木天线进行参数化建模并仿真，结果如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/1.png)

The simulation has achieved convergence and the directivity result is 14.87.

仿真收敛，方向性指标为14.87

Part of design factors.

部分设计参数：

Name 'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（half-length of driver，length of reflector，length of director 1，reflector-driver distance，driver-director1 distance）

名称：'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（振子半长度，反射器长度，第一引向器长度，反射器-振子距离，振子-第一引向器距离）

Value 325.6,328.5,303,182.5,120.2

值：325.6,328.5,303,182.5,120.2

### 4 HFSS Interface Development

### 4 HFSS二次开发

Operations like design factor manipulation, simulation commition and result fetching were made avaliable in python during this part of work.

可在python中对HFSS进行修改参数、启动仿真、获取结果等操作

Code as regards are in PythonPrj/HFSS.py. 

具体代码在PythonPrj/HFSS.py中

### 5 Gym Environment Construction

### 5 构建Gym环境

A simple environment in compatible with Gym was developed in this part of work.

本次比赛要求RL环境可以自己找，但必须兼容Gym，所以搭建了简单的Gym环境

Code as regards are in PythonPrj/HFSS_Gym.py. 

具体代码在PythonPrj/HFSS_Gym.py中

### 6 Design Factor Modification

### 6 调整天线参数

Theoretical design factor for Yagi antenna are too good to conclude optimization effect, so some modification were conducted to the size of reflector, driver and director #1, as well as the distance between them. And the simulation result after that is shown below.

八木天线辅助软件计算出的设计参数过于理想，不利于体现强化学习效果，故对反射器、主振子、第一引向器的长度、间距进行了调整。仿真结果如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/2.png)

After modification, the directivity result is 0.98, indicating a high sensitivity to design factors in Yagi antenna design.

调整后，方向性指标为0.98，可见八木天线对设计参数较为敏感。

Parameters:

参数：

Name 'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（half-length of driver，length of reflector，length of director 1，reflector-driver distance，driver-director1 distance）

名称：'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（振子半长度，反射器长度，第一引向器长度，反射器-振子距离，振子-第一引向器距离）

Value 300,350,350,150,150

值：300,350,350,150,150

### 7 Reinforcement Learning Process

### 7 构建强化学习器

The reinforcement learning algorithm was realized based on DDPG using Parl framework. 

利用Parl库搭建强化学习算法，基于DDPG算法。

The algorithm's action parameters are the length of reflector, driver, director #1 and the distance between them.

算法对反射器、主振子、第一引向器的长度及其间距共5个参数进行调整，即为Action。

The algorithm's state/observation parameters are the electric size of the parameters above after manipulation. 

算法的State/Observation为每次调整后，上述各参数对应的电气尺寸。

The algorithm's reward is directivity result in HFSS simulation

算法的Reward为HFSS仿真中的方向性指标。

One simulation was triggered each 50 steps of design factor manipulation. In future practice, a reduction in number of manipulation steps is advised.

算法对上述5个参数进行50步调整后进行一次HFSS仿真，经实践发现：参数调整步数可适当缩减。

Code as regards are in PythonPrj/HFSS_Agent.py, PythonPrj/HFSS_Model.py, PythonPrj/train.py. 

具体代码在PythonPrj/HFSS_Agent.py、PythonPrj/HFSS_Model.py、PythonPrj/train.py中。

### 8 Result

### 8 优化结果

Variation of directivity result during RL process is shown below.

强化学习过程中，方向性指标变化曲线为：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/5.png)

The parameters below are the best parameter group during RL training process.

取较好的一组，参数修正值为：

Name 'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（half-length of driver，length of reflector，length of director 1，reflector-driver distance，driver-director1 distance）

名称：'drv_l', 'ref_l', 'dir1_l','ref_drv_d', 'drv_dir1_d'（振子半长度，反射器长度，第一引向器长度，反射器-振子距离，振子-第一引向器距离）

Value 352.2,354.5,306.6,157.8,131.1

值：352.2,354.5,306.6,157.8,131.1

Simulation Result

仿真结果：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/3.png)

By RL optimization, the directivity result has raised up to 14.29, which is close to result achieved by theoretical design.

优化后，方向性指标为14.29，接近理论计算结果。

## Notification

## 使用说明

This project is developed in Windows 10 64bit, CPU place. 

实验环境：win10 64位，CPU环境

Antenna model should be loaded in HFSS software first. By running train.py, the training process will be started, and results will be stored in log file, whose path in the code may have to be forked with actural condition.

首先在HFSS中打开模型，然后运行train.py进行训练，训练结果会保存为log文件，源代码中可能有一些绝对路径需要根据实际情况修改

The shape of optimizaion results are [action list],[state list],reward. The action list infers the relative varience of the 5 design factors mentioned above. 

强化学习结束后，log文件及IDE的log框中按行记录了运行情况，行中数据格式为：[action list], [state list], reward。其中，action_list为上述设计参数缩放量。

Modefied_Design_Factor Value[i] = Initial_Design_Factor_Value[i] * (1+action_list[i])

设计参数修正值=参数初始值*(1+参数缩放量)

The final simulation in HFSS may introduce an error less than 4% compared to reward data in the log file. Adaptive meshing may be the cause of this. And the error will not inference the conclusion of this project.

可在HFSS中设置这些参数修正值，对结果进行验证。验证结果与log中的reward的方向性指标会有4%以内的差异，可能是因为自适应网格划分等过程造成的，基本不影响对设计参数优化过程的评判。

## About the Author

## 关于作者

Name KanNi

姓名：倪侃

Location Shanghai

现居：上海

Callsign BH4FAP

业余无线电呼号：BH4FAP
