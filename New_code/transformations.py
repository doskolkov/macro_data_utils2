from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif

class TransformationFunctions():

    def type_transform(self, ts, instruction = None):
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts*=1
        return ts

    def freq_transform(self, ts, instruction = None):
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1
        return ts

    def norm_transform(self, ts, instruction = None):
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1
        return ts

    def seasadj_transform(self, ts, instruction = None):
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1
        return ts

class TrasformationsConfig():
    TF = TransformationFunctions()
    transMethodsDict = {
        'type': {'method':TF.type_transform, 'cols':['real','norm']},
        'freq': {'method':TF.freq_transform, 'cols':['freq','calc']},
        'norm': {'method':TF.norm_transform, 'cols':['transf', 'norm']},
        'sa': {'method':TF.seasadj_transform, 'cols':['sa']}
    }
