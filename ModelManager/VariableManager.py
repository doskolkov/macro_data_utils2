import pandas as pd

from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel
from .DBManagerExcel import DBManagerExcel



class VariableManager():

    def __init__(self):
        """
        Load model settings

        Args:
            model_path:
        """
        return True

class Variable():

    def __init__(self, variable_info, datasource_info, dataloader_instance, destinations):

        self.variable_info = variable_info
        self.datasource_info = datasource_info
        self.destinations = destinations
        self.dataloader_instance = dataloader_instance

        self.raw_ts = pd.Series()
        self.destination_ts = {}




