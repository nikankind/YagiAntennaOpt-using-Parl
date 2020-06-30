import logging
import random
import gym
import numpy as np
import Logger
import HFSS

fmt = '%(asctime)s - %(levelname)s: %(message)s'
log = Logger.Logger('recordings.log',level='info',fmt=fmt)

class HFSS_env(gym.Env):
    metadata={
        'render.modes':['human','rgb_array'],
        'video.frames_per_second':2
    }
    #action为调节各尺寸，新尺寸=旧尺寸*(ofst_rto+1)
    def __init__(self,ofst_rtos=[0,0,0,0,0]):
        self.mdl=HFSS.HFSS() #HFSS八木天线模型，首先要打开HFSS
        '''
        self.var_param_nmes=[
            'drv_l','ref_l','dir1_l','dir2_l','dir3_l','dir4_l','dir5_l',
            'gap_w','ref_drv_d','drv_dir1_d','dir1_dir2_d','dir2_dir3_d','dir3_dir4_d','dir4_dir5_d'
        ]        
        self.var_init_params=np.array([
            325.57,328.45,302.96,301.0,290.21,288.74,281.39,
            0.5,182.47,120.18,130.57,167.14,155.27,172.09
        ])
        '''
        self.var_param_nmes = [
            'drv_l', 'ref_l', 'dir1_l',
            'ref_drv_d', 'drv_dir1_d'
        ]
        self.var_init_params = np.array([
            300,350,350,
            150,150
        ])
        self.ofst_rtos=np.array(ofst_rtos)
        self.wave_lenth=689.66

    def reset(self):
        self.var_params=self.var_init_params*(self.ofst_rtos+1)
        self.mdl.chg_variable(self.var_param_nmes,list(self.var_params))
        # 初始状态
        self.state=[1.008412,3.709934,25.768845,0.851206,0.901285]
        self.reward=13.373002
        return self.state

    # action为ofst_rto
    # 先给50步调整尺寸，每一步的观察值为调整后天线各部分的电尺寸
    # en_sim为有限元仿真开关
    # state/observation为电尺寸：drv_l,ref_l,dir1_l,ref_drv_d,drv_dir1_d
    def step(self,action=[0,0,0,0,0],en_sim=False):
        self.ofst_rtos=np.clip(action,-0.3,0.3) #变化量限幅
        self.var_params=self.var_init_params*(self.ofst_rtos+1)
        self.reward=0 # 如果不仿真只是变换尺寸，则不计reward
        self.state=list(self.var_params/self.wave_lenth)
        self.done=False
        if en_sim:
            self.mdl.chg_variable(self.var_param_nmes,list(self.var_params))
            self.mdl.run()
            self.rsts=self.mdl.output()
            #self.state=self.rsts[1:]
            self.reward=self.rsts[0]
            self.done=True
        return (self.state,self.reward,self.done)

    def render(self):
        log.logger.info(str(self.ofst_rtos)+'\t'+str(self.state)+'\t'+str(self.reward))

    def observation_space(self):
        return self.state

    def action_space(self):
        return self.ofst_rtos