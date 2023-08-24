from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from New_code.TimeSeriesTransformations import type_transformations,frequency_transformations,normalization_transformations,seasonal_adjustment_transformations

class TransformationFunctions():

    type_transformations = type_transformations()
    frequency_transformations = frequency_transformations()
    normalization_transformations = normalization_transformations()
    seasonal_adjustment_transformations = seasonal_adjustment_transformations()

    def type_transform(self, ts, instruction = None): ### index, value, rate
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts = self.type_transformations.get_config().get(mif.transf)

        return ts

    def freq_transform(self, ts, instruction = None): ### frequency
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1

        return ts

    def norm_transform(self, ts, instruction = None): ### normalization
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1

        return ts

    def seasadj_transform(self, ts, instruction = None): ### seasonal adjustment
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1

        return ts

class TrasformationsConfig():
    TF = TransformationFunctions()
    transMethodsDict = {
        'type': {'method':TF.type_transform, 'cols':[mif.transf], 'change_name':mif.is_real},
        'freq': {'method':TF.freq_transform, 'cols':[mif.freq, mif.calc], 'change_name':None},
        'norm': {'method':TF.norm_transform, 'cols':[mif.norm_d], 'change_name':None},
        'sa': {'method':TF.seasadj_transform, 'cols':[mif.is_sa, mif.is_makesa], 'change_name':mif.is_makesa}
    }

