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
        'type': {'method':TF.type_transform, 'cols':['type']},
        'freq': {'method':TF.freq_transform, 'cols':['freq','calc']},
        'norm': {'method':TF.norm_transform, 'cols':['transf', 'satype']},
        'sa': {'method':TF.seasadj_transform, 'cols':[None]},
        None: None
    }
