
from win32com import client
import os
import pandas as pd

class HFSS:
    def __init__(self,_prj_nme='Yagi',_dsn_nme='Yagi'):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        #self.oProject = self.oDesktop.NewProject()
        self.oProject=self.oDesktop.SetActiveProject(_prj_nme)
        self.oDesign = self.oProject.SetActiveDesign(_dsn_nme)
        #self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('ReportSetup')

    def chg_variable(self, _var_names, _var_values):
        assert len(_var_names)==len(_var_values),print('unequal parameter number')

        _prop_arr=["NAME:ChangedProps"]
        for _name,_value in zip(_var_names,_var_values):
            _prop_arr.append(['NAME:'+_name,'Value:=',str(_value)+'mm'])
        self.oDesign.ChangeProperty(["NAME:AllTabs",
                                     ["NAME:LocalVariableTab",
                                      ["NAME:PropServers", "LocalVariables"],
                                      _prop_arr
                                      ]])

    #输出[reward[DirTotal],states[MxaU,FBR,MaxrE,AcptPwr,RadPwr]]
    def output(self):
        pth="D:/AI/百度飞桨深度学习集训/作业/强化学习/6强化学习创意赛/RL_HFSS/Model"
        self.oModule.ExportToFile('AntennaReward',os.path.join(pth,'Reward.csv'))
        self.oModule.ExportToFile('AntennaStates', os.path.join(pth, 'States.csv'))

        #fls=['DirTotal.csv','MaxU.csv','FBR.csv','MaxrE.csv','AcptPwr.csv','RadPwr.csv']
        rst=[]

        with open(os.path.join(pth,'Reward.csv'),'r') as f:
            csv_data=pd.read_csv(f)
            rst.append(csv_data.values[0][-1])
        f.close()
        with open(os.path.join(pth,'States.csv'),'r') as f:
            csv_data=pd.read_csv(f)
            rst.extend(csv_data.values[0][1:6])
        f.close()
        rst[3]=rst[3]/1000.0
        return rst

    def save_prj(self):
        _base_path = os.getcwd()
        _prj_num = 1
        while True:
            _path = os.path.join(_base_path, 'Prj{}.aedt'.format(_prj_num))
            if os.path.exists(_path):
                _prj_num += 1
            else:
                break
        self.oProject.SaveAs(_path, True)

    def run(self,_setup_nme='Setup1'):
        self.oDesign.Analyze(_setup_nme)
        self.oModule.UpdateReports(['AntennaReward','AntennaStates'])

    def test(self):
        #oModule=self.oDesign.GetModule('RadField')
        #return oModule.GetSolutionContexts('Far Fields','Gain Plot 1','Setup1 : LastAdaptive')
        #oModule=self.oDesign.GetModule('OutputVariable')
        #return oModule.GetOutputVariableValue('directivity',"Freq='0.435GHz' Theta='90deg' Phi='90deg'","Setup1 : LastAdaptive","Standard",[])
        #return oModule.GetOutputVariableValue('directivity1',"","Setup1 : LastAdaptive","Modal Solution Data",[])
        #return self.oProject.GetVariableValue('directivity1')
        self.oModule.UpdateReports(['Directivity Table 1'])
    def state(self):
        return self.oDesktop.RefreshJobMonitor()