# YagiAntennaOpt-using-Parl
Optimization of Yagi Antenna Based on Reinforcement Learning Framework Parl

# 基于百度强化学习框架Parl的八木天线参数优化与仿真

如果该环境对您的研究有帮助，请考虑引用:

```txt
@misc{Quadrotor,
    author = {Kan Ni},
    title = {{Optimization of Yagi Antenna Based on Reinforcement Learning Framework Parl}},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/PaddlePaddle/RLSchool/tree/master/rlschool/quadrotor}},
}
```

## 介绍
本项目利用百度强化学习框架对UHF段八木天线进行了参数优化，并利用HFSS有限元仿真软件对天线模型进行了仿真对比。仿真结果表明：经强化学习优化后，5个天线参数从初始乱序状态变为接近理论计算的状态，天线方向性从0.98上升到14.29。项目工作探索了强化学习在天线设计中的应用，对后续相关工作起到很好的参考作用。

八木天线本身可解析计算，本项目工作主要是探索了强化学习用于天线计算中的新方法，可迁移到其他更复杂的天线设计中。

## 项目工作

###1 天线介绍及设计目标确定

八木天线是业余无线电中一种常用的指向性天线，主要由主振子、反射器、引向器组成。每个元件称为一个单元，各单元的尺寸及单元间距对八木天线性能起决定作用。

八木天线图片

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/timg.jpg)

本项目拟设计一款7单元八木天线，包含1个主振子，1个反射器，5个引向器，中心频率435MHz

优化目标为：最大化八木天线前向增益，使八木天线指向性最好。

### 2 辅助软件计算

八木天线有成熟的计算软件，计算如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/4.png)

### 3 HFSS建模

HFSS是一款有限元电磁仿真软件

利用2中的计算结果对八木天线进行参数化建模并仿真，结果如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/1.png)

仿真收敛，方向性指标为14.87

部分设计参数：

名称：'drv_l', 'ref_l', 'dir1_l','drv_l', 'ref_l', 'dir1_l'

值：325.6,328.5,303,182.5,120.2

### 4 HFSS二次开发

可在python中对HFSS进行修改参数、启动仿真、获取结果等操作

具体代码在PythonPrj/HFSS.py中

### 5 构建Gym环境

本次比赛要求RL环境可以自己找，但必须兼容Gym，所以搭建了简单的Gym环境

具体代码在PythonPrj/HFSS_Gym.py中

### 6 调整天线参数

八木天线辅助软件计算出的设计参数过于理想，不利于体现强化学习效果，故对反射器、主振子、第一引向器的长度、间距进行了调整。仿真结果如下图所示：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/2.png)

调整后，方向性指标为0.98，可见八木天线对设计参数较为敏感。

参数：

名称：'drv_l', 'ref_l', 'dir1_l','drv_l', 'ref_l', 'dir1_l'

值：300,350,350,150,150

### 7 构建强化学习器

利用Parl库搭建强化学习算法，基于DDPG算法。

算法对反射器、主振子、第一引向器的长度及其间距共5个参数进行调整，即为Action。

算法的State/Observation为每次调整后，上述各参数对应的电气尺寸。

算法的Reward为HFSS仿真中的方向性指标。

算法对上述5个参数进行50步调整后进行一次HFSS仿真，经实践发现：参数调整步数可适当缩减。

具体代码在PythonPrj/HFSS_Agent.py、PythonPrj/HFSS_Model.py、PythonPrj/train.py中。

### 8 优化结果

强化学习过程中，方向性指标变化曲线为：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/5.png)

取较好的一组，参数修正值为：

名称：'drv_l', 'ref_l', 'dir1_l','drv_l', 'ref_l', 'dir1_l'

值：352.2,354.5,306.6,157.8,131.1

仿真结果：

![image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/3.png)

优化后，方向性指标为14.29，接近理论计算结果。

## 关于作者
姓名：倪侃

现居：上海

业余无线电呼号：BH4FAP
