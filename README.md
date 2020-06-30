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

## 项目工作
###1 天线介绍及设计目标确定
八木天线是一种
[!image](https://github.com/nikankind/YagiAntennaOpt-using-Parl/blob/master/images/timg.jpg)
