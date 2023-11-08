
# from Utils.information import ModelInputInfoFields as mif
from .TimeSeriesTransformations import type_transformations,frequency_transformations,normalization_transformations,seasonal_adjustment_transformations
from .TimeSeriesTransformations import FrequencyException
from .Utils import setup_logger, get_config

import warnings
warnings.filterwarnings("ignore")

class TransformationFunctions():

    type_transformations = type_transformations()
    frequency_transformations = frequency_transformations()
    normalization_transformations = normalization_transformations()
    seasonal_adjustment_transformations = seasonal_adjustment_transformations()

    config_files = ["config.yaml"]

    application_history = []
    def __init__(self):
        info_settings = get_config(self.config_files)
        self.logex = setup_logger('Model', 'data.log')
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))
        self.config = info_settings['ModelInputInfoFields']

    def type_transform(self, ts, instruction = None): ### index, value, rate
        tname = 'type'
        instruction_dict = {}
        if instruction:
            for k in instruction.keys():
                instruction_dict[k] = instruction.get(k).get(ts.name)
            try:
                ts = self.type_transformations.get_config().get(instruction_dict.get(mif.transf))(ts)
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = e.args[0]
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation family':'type','transformation':instruction_dict.get(mif.transf),'series_name':ts.name,'status':status,'message':message})

        return ts

    def freq_transform(self, ts, instruction = None):### frequency
        tname = 'freq'
        instruction_dict = {}
        if instruction:
            for k in instruction.keys():
                instruction_dict[k] = instruction.get(k).get(ts.name)
            try:
                ts = self.frequency_transformations.get_config().get(f'{instruction_dict.get(mif.freq)}_{instruction_dict.get(mif.calc)}')(ts)
                status = 0
                message = None
            except FrequencyException as fe:
                status = 1
                message = fe.args[0]
            except Exception as e:
                status = 1
                message = e.args[0]
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation family':'freq','transformation':f'{instruction_dict.get(mif.freq)}_{instruction_dict.get(mif.calc)}','series_name':ts.name,'status':status,'message':message})

        return ts

    def norm_transform(self, ts, instruction = None): ### normalization
        tname = 'norm'
        instruction_dict = {}
        if instruction:
            for k in instruction.keys():
                instruction_dict[k] = instruction.get(k).get(ts.name)
            try:
                ts = self.normalization_transformations.get_config().get(instruction_dict.get(mif.transf))(ts,
                                                                                                           instruction_dict.get(
                                                                                                               mif.norm_d))
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = e.args[0]
        else:
            status = 1
            message = "Method transformation was not performed, instruction was not passed"
        self.application_history.append({'transformation family':'norm','transformation':instruction_dict.get(mif.transf),'series_name':ts.name,'status':status,'message':message})

        return ts

    def seasadj_transform(self, ts, instruction = None): ### seasonal adjustment
        tname = 'seasadj'
        instruction_dict = {}
        for k in instruction.keys():
            instruction_dict[k] = instruction.get(k).get(ts.name)
        ts *= 1

        return ts

class TrasformationsConfig():
    config_files = ["config.yaml"]
    TF = TransformationFunctions()

    def __init__(self):
        info_settings = get_config(self.config_files)
        self.logex = setup_logger('Model', 'data.log')
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))
        self.tic = info_settings['ModelInfoFields']['TransformationInstructionFields'] #transformation instruction cols
        self.pic = info_settings['DataBaseExcel']['RawDataProperties'] #properties information cols

        transMethodsDict = {
            'type': {
                'method': self.TF.type_transform,
                'property': [self.pic['type']],
                'instruction': [self.tic['transf']],
                'change_name': None
            },
            'freq': {
                'method': self.TF.freq_transform,
                'property': [self.pic['freq']],
                'instruction': [self.tic['freq'],self.tic['calc']],
                'change_name': None
            },
            'norm': {
                'method': self.TF.norm_transform,
                'property':None,
                'instruction':[self.tic['norm_d'], self.tic['transf']],
                'change_name': None
            },
            'sa': {
                'method': self.TF.seasadj_transform,
                'property':[self.pic['sa']],
                'instruction':[self.tic['is_makesa']],
                'change_name': None}
        }



