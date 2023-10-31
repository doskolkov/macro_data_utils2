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
        self.db_excel_path = input_file
        self.db_excel_sheet = input_sheet
        self.source_name = source
        self.logex = setup_logger('DataBase ' + str(source), 'data.log')

        # Load model settings
        info_settings = get_config(self.config_files)
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))

        self.config = info_settings['DataBaseExcel']




    def get_inputs(self, return_method_output=True):
        """

        Args:
            return_method_output:

        Returns:

        """
