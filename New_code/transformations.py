from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

class TransformationFunctions():

    def type_transform(self, ts, params = None):
        return ts

    def freq_transform(self, ts, params = None):
        return ts

    def norm_transform(self, ts, params = None):
        return ts

    def seasadj_transform(self, ts, params = None):
        return ts

class TrasformationsConfig():
    TF = TransformationFunctions()
    transMethodsDict = {
        'type': {'method':TF.type_transform, 'cols':['real','norm'], 'info_cols':['real']},
        'freq': {'method':TF.freq_transform, 'cols':['freq','calc'], 'is transform':[], 'transf instr':['freq','calc']},
        'norm': {'method':TF.norm_transform, 'cols':['transf', 'norm']},
        'sa': {'method':TF.seasadj_transform, 'cols':['sa']},
        None: None
    }
