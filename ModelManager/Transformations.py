
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
        self.tt = info_settings['TransformationTypes']
        self.type_transformations = type_transformations().get_config()
        self.frequency_transformations = frequency_transformations().get_config()
        self.normalization_transformations = normalization_transformations().get_config()
        self.seasonal_adjustment_transformations = seasonal_adjustment_transformations().get_config()

        self.transformation_status = {}

    def type_transform(self, ts, property, instruction):
        key = f"{property[0]}_{instruction[0]}"
        try:
            method = self.type_transformations.get(key)
            try:
                ts = method(ts)
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = e.args[0]
        except KeyError:
            message = f"Failed to map property_instruction pair {key} to type_transformation config"
            status = 1
        self.transformation_status[self.tt['type']] = {'status':status,'message':message,'config_key':key}
        return ts

    def freq_transform(self, ts, property, instruction):
        key = "_".join([f"{component}" for component in instruction])
        try:
            method = self.frequency_transformations.get(key)
            try:
                ts = method(ts)
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = f"{e.args[0]}; stated timeseries frequency is {property}"
            except FrequencyException as fe:
                status = 1
                message = f"{fe.args[0]}; stated timeseries frequency is {property}"
        except KeyError:
            message = f"Failed to map coded instruction pair {key} to frequency_transformation config"
            status = 1
        self.transformation_status[self.tt['frequency']] = {'status':status,'message':message,'config_key':key}
        return ts

    def norm_transform(self, ts, property, instruction):
        if 'type' in self.transformation_status.keys():
            key = property[1]
        else:
            key = property[0]
        try:
            method = self.normalization_transformations.get(key)
            try:
                ts = method(ts, norm_date=instruction[0])
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = e.args[0]
        except KeyError:
            message = f"Failed to map data type {key} to normalization_transformation config"
            status = 1
        self.transformation_status[self.tt['normalization']] = {'status':status,'message':message,'config_key':key}
        return ts

    def seasadj_transform(self, ts, property, instruction): ### seasonal adjustment
        key = f"{property[0]}_{instruction[0]}"
        try:
            method = self.seasonal_adjustment_transformations.get(key)
            try:
                ts = method(ts)
                status = 0
                message = None
            except Exception as e:
                status = 1
                message = e.args[0]
        except KeyError:
            message = f"Failed to map property-instruction key {key} to sa_transformation config"
            status = 1
        self.transformation_status[self.tt['seasonal_adjustment']] = {'status':status,'message':message,'config_key':key}
        return ts

class TrasformationsConfig():
    config_files = ["config.yaml"]
    TF = TransformationFunctions()

    def __init__(self,properties, destination):
        info_settings = get_config(self.config_files)
        self.logex = setup_logger('Model', 'data.log')
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))
        self.tif = destination #info_settings['ModelInfoFields']['TransformationInstructionFields'] #transformation instruction cols
        self.rdp = properties#info_settings['DataBaseExcel']['RawDataProperties'] #properties information cols
        self.tt = info_settings['TransformationTypes']

        self.TransformMethodsDict = {
            self.tt['type']: {
                'method': self.TF.type_transform,
                'property': [self.rdp['type']],
                'instruction': [self.tif['transf']],
                'change_name': None
            },
            self.tt['frequency']: {
                'method': self.TF.freq_transform,
                'property': [self.rdp['freq']],
                'instruction': [self.tif['freq'],self.tif['calc']],
                'change_name': None
            },
            self.tt['normalization']: {
                'method': self.TF.norm_transform,
                'property':[self.rdp['type'], self.tif['transf']],
                'instruction':[self.tif['norm_d']],
                'change_name': None
            },
            self.tt['seasonal_adjustment']: {
                'method': self.TF.seasadj_transform,
                'property':[self.rdp['sa']],
                'instruction':[self.tif['is_makesa']],
                'change_name': None}
        }



