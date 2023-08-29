from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from New_code.TimeSeriesTransformations import type_transformations,frequency_transformations,normalization_transformations,seasonal_adjustment_transformations

import warnings
warnings.filterwarnings("ignore")

class TransformationFunctions():

    type_transformations = type_transformations()
    frequency_transformations = frequency_transformations()
    normalization_transformations = normalization_transformations()
    seasonal_adjustment_transformations = seasonal_adjustment_transformations()

    application_history = []

    def type_transform(self, ts, instruction = None): ### index, value, rate
        tname = 'type'
        if instruction:
            try:
                instruction_dict = {}
                for k in instruction.keys():
                    instruction_dict[k] = instruction.get(k).get(ts.name)
                ts = self.type_transformations.get_config().get(instruction_dict.get(mif.transf))(ts)
                status = 0
                message = None
            except:
                status = 1
                message = "Method transformation was not performed, instruction was passed"
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation':tname,'series_name':ts.name,'status':status,'message':message})

        return ts

    def freq_transform(self, ts, instruction = None):### frequency
        tname = 'freq'
        if instruction:
            try:
                instruction_dict = {}
                for k in instruction.keys():
                    instruction_dict[k] = instruction.get(k).get(ts.name)
                ts = self.frequency_transformations.get_config().get(f'{instruction_dict.get(mif.freq)}_{instruction_dict.get(mif.calc)}')(ts)
                status = 0
                message = None
            except:
                status = 1
                message = "Method transformation was not performed, instruction was passed"
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation':tname,'series_name':ts.name,'status':status,'message':message})

        return ts

    def norm_transform(self, ts, instruction = None): ### normalization
        tname = 'norm'
        if instruction:
            try:
                instruction_dict = {}
                for k in instruction.keys():
                    instruction_dict[k] = instruction.get(k).get(ts.name)
                ts = self.normalization_transformations.get_config().get(instruction_dict.get(mif.transf))(ts,
                                                                                                           instruction_dict.get(
                                                                                                               mif.norm_d))
                status = 0
                message = None
            except:
                status = 1
                message = "Method transformation was not performed, instruction was passed"
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation':tname,'series_name':ts.name,'status':status,'message':message})

        return ts

    def seasadj_transform(self, ts, instruction = None): ### seasonal adjustment
        tname = 'seasadj'
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1

        return ts

class TrasformationsConfig():
    TF = TransformationFunctions()
    transMethodsDict = {
        'type': {'method':TF.type_transform, 'cols':[mif.transf], 'change_name':None},
        'freq': {'method':TF.freq_transform, 'cols':[mif.freq, mif.calc], 'change_name':None},
        'norm': {'method':TF.norm_transform, 'cols':[mif.norm_d, mif.transf], 'change_name':None},
        'sa': {'method':TF.seasadj_transform, 'cols':[mif.is_sa, mif.is_makesa], 'change_name':None}
    }

