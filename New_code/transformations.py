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
        'type': {'method':TF.type_transform, 'cols':[mif.is_real, mif.norm_d], 'change_name':mif.is_real},
        'freq': {'method':TF.freq_transform, 'cols':[mif.freq, mif.calc], 'change_name':None},
        'norm': {'method':TF.norm_transform, 'cols':[mif.transf, mif.norm_d], 'change_name':None},
        'sa': {'method':TF.seasadj_transform, 'cols':[mif.is_sa, mif.is_makesa], 'change_name':mif.is_makesa}
    }
