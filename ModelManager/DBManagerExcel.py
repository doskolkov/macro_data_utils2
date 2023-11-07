import pandas as pd

from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel


class DBManagerExcel(DataExcel):
    """

    Class to manage model updates - top level:
    - read file with settings
    - read Model excel file with instructions
    - determine data sources
    - initiate ExcelDBManager ans SqlDBManager

    """
    db_excel_path = ""
    config_files = ["config.yaml"]

    def __init__(self, source, input_file, input_sheet):
        """
        Load model settings

        Args:
            model_path:
        """
        self.source_name = source
        self.input_file = input_file
        self.input_sheet = input_sheet
        self.logex = setup_logger('DataBase ' + str(source), 'data.log')

        # Load model settings
        info_settings = get_config(self.config_files)
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))

        self.config = info_settings['DataBaseExcel']
        self.data_sheet = None
        self.var_guide = None

    def import_var_guide(self):
        if self.var_guide:
            pass
        else:
            self.var_guide = self.load_excel(self.input_file, self.config['var_list_sheet'], skip_row=None)

    def import_data_sheet(self):
        if self.data_sheet:
            pass
        else:
            self.data_sheet = self.load_excel(self.input_file, self.input_sheet)


    def get_variable_name(self):
        True

    def get_variable_ts(self):
        True

    def add_indicators(self):
        True

    def get_inputs(self, return_method_output=True):
        """

        Args:
            return_method_output:

        Returns:

        """
