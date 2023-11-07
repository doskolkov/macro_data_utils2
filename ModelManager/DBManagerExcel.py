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
        self.miif = info_settings['ModelInputInfoFields']
        self.data_sheet = None
        self.var_guide = None
        self.located_variables = []
        self.not_located_variables = []

    def import_var_guide(self):
        if self.var_guide:
            pass
        else:
            self.var_guide = self.load_excel(self.input_file, self.config['var_list_sheet'], skip_row=None)

    def import_data_sheet(self):
        if self.data_sheet:
            pass
        else:
            self.data_sheet = self.load_excel(self.input_file, self.input_sheet).set_index(self.config['date_column'])


    def get_variable_storage_info(self, variable_info):
        if self.var_guide is None:
            self.import_var_guide()

        guide_locations = self.var_guide.merge(pd.DataFrame(variable_info, index=[0]), how='left',
                                               left_on=[self.miif['fname'], self.miif['is_real'], self.miif['is_sa']],
                                               right_on=[self.config['name'], self.config['real'], self.config[
                                                   'sa']]).dropna().drop_duplicates().reset_index().drop(
            columns='index')
        if len(guide_locations)==0:
            self.logex.error(f'Was unable to locate varibale || {variable_info} ||')
            self.not_located_variables.append(variable_info)
            return None
        if len(guide_locations)>1:
            self.logex.error(f'Variable information is not one-to-one || {variable_info} ||')
            self.not_located_variables.append(variable_info)
            return None
        else:
            with guide_locations.to_dict() as guide:
                return_dict = {}
                for key in [self.config['variable'],self.config['short_name'],self.config['freq'],self.config['type'],self.config['calc']]:
                    try:
                        return_dict[key] = guide.get(key).get(0)
                    except KeyError as e:
                        self.logex.error(f'Var list columns names were not as expected, KeyError was raised with message: {e.args[0]}')
                        return_dict[key] = None
                self.located_variables.append(variable_info)
                return return_dict


    def get_variable_ts_with_attributes(self, variable_info, date_from=None, date_till=None):
        if self.data_sheet is None:
            self.import_data_sheet()

        storage_info = self.get_variable_storage_info(variable_info)
        return_dict = {}
        if storage_info:
            try:
                return_dict['raw_ts'] = self.data_sheet[storage_info.get(self.config['variable'])]
                return_dict['ts_found'] = True
            except KeyError:
                self.logex(f"""Was unable to locate variable {storage_info.get(self.config['variable'])} on input sheet {self.input_sheet}""")
                return_dict['raw_ts'] = None
                return_dict['ts_found'] = False
            return_dict[self.config['short_name']] = storage_info[self.config['short_name']]
            ts_properties = {}
            return_dict['ts_properties_defined'] = True
            for key in [self.config['freq'],self.config['type'],self.config['calc']]:
                if storage_info.get(key):
                    return_dict['ts_properties_defined'] *= True
                else:
                    return_dict['ts_properties_defined'] *= False
                ts_properties[key] = storage_info.get(key)
            return_dict['ts_properties'] = ts_properties
            return_dict['ts_properties_defined'] = bool(return_dict['ts_properties_defined'])
        else:
            return_dict = {
                'raw_ts':None,
                'short_name':None,
                'ts_properties':{
                    self.config['freq']: None,
                    self.config['type']: None,
                    self.config['calc']: None,
                },
                'ts_found':False,
                'ts_properties_defined':False
            }
        return return_dict



    def add_indicators(self):
        True

    def get_inputs(self, return_method_output=True):
        """

        Args:
            return_method_output:

        Returns:

        """
