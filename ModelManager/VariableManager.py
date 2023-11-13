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

        self.transforming_instance = TrasformationsConfig()
        self.transforming_instance_config = self.transforming_instance.transMethodsDict

        self.variable_info = variable_info
        self.datasource_info = datasource_info
        self.destinations = destinations
        self.dataloader_instance = dataloader_instance

        self.raw_data_obtained = False
        self.raw_data_properties_defined = False

        self.raw_ts:pd.Series = None
        self.raw_ts_properties = None

        self.destination_ts:dict = {}

    def define(self, date_from = None, date_till = None):

        raw_data = self.dataloader_instance.get_variable_ts_with_attributes(variable_info = self.variable_info,
                                                               date_from = date_from,
                                                               date_till = date_till)
        if raw_data.get('ts_found'):
            self.raw_ts = raw_data.get('raw_ts')
            self.raw_data_obtained = True
        if raw_data.get('ts_properties_defined'):
            self.raw_ts_properties = raw_data.get('ts_properties')
            self.raw_data_properties_defined = True

    def transform(self):
        True

    def put_value(self):
        True






