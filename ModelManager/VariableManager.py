import pandas as pd

from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel
from .DBManagerExcel import DBManagerExcel
from .Transformations import TrasformationsConfig

class Variable():
    config_files = ["config.yaml"]
    def __init__(self, variable_info, datasource_info, dataloader_instance, destinations):
        info_settings = get_config(self.config_files)
        self.logex = setup_logger('Model', 'data.log')
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))

        self.transformation_types = info_settings['TransformationTypes']
        self.rdp = info_settings['StorageInfoFields']['RawDataProperties']
        self.tif = info_settings['ModelInfoFields']['TransformationInstructionFields']

        self.variable_info = variable_info
        self.datasource_info = datasource_info
        self.destinations = destinations
        self.dataloader_instance = dataloader_instance

        self.transformers = []

        self.raw_data_obtained = False
        self.raw_data_properties_defined = False

        self.raw_ts:pd.Series = None
        self.raw_ts_properties = None

        self.destination_ts:dict = {}

    def define(self, date_from = None, date_till = None):

        raw_data = self.dataloader_instance.get_variable_ts_with_attributes(variable_info = self.variable_info,
                                                               date_from = date_from,
                                                               date_till = date_till)
        # if raw_data.get('ts_found'):
        self.raw_ts = raw_data.get('raw_ts')
        self.raw_data_obtained = raw_data.get('ts_found')
        # if raw_data.get('ts_properties_defined'):
        self.raw_ts_properties = raw_data.get('ts_properties')
        self.raw_data_properties_defined = raw_data.get('rs_properties_defined')

        for destination in self.destinations:
            transformer = TrasformationsConfig(properties=self.raw_ts_properties, destination=destination)
            transformer_config = transformer.TransformMethodsDict
            self.transformers.append({'instance':transformer,'config':transformer_config,'key':self.tif['output_sheet']})

    def transform(self):
        if not self.raw_data_properties_defined or not self.raw_data_obtained:
            pass
        else:
            for transformer in self.transformers:
                ts = self.raw_ts
                transformer_config = transformer.get('config')
                for transformation in self.transformation_types.keys():
                    transformation_config = transformer_config.get(transformation)
                    method = transformation_config.get('method')
                    prop = transformation_config.get('property')
                    instruciton = transformation_config.get('instruction')
                    ts = method(ts, prop, instruciton)
                self.destination_ts[transformer['key']] = ts


    def put_value(self):
        True






