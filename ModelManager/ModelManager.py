from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel
from .DBManagerExcel import DBManagerExcel
from .DBManagerSQL import DBManagerSQL
from .VariableManager import Variable


class ModelManager(DataExcel):
    """

    Class to manage model updates - top level:
    - read file with settings
    - read Model excel file with instructions
    - determine data sources
    - initiate ExcelDBManager ans SqlDBManager

    """
    model_path = ""
    config_files = ["config.yaml"]

    database_sources = []
    db_data_sheets = []
    model_input_sheets_info = {}
    InputVarsTranformDict = {}
    raw_model_data_stage1 = {}
    raw_model_data_to_transform = {}
    transformation_stages = []
    model_data = {}

    def __init__(self, model_path):
        """
        Load model settings

        Args:
            model_path:
        """
        self.model_path = model_path
        self.logex = setup_logger('Model', 'data.log')

        # Load model settings
        info_settings = get_config(self.config_files)
        if info_settings is None:
            self.logex.error("Error loading setting file: ", str(self.config_files))

        self.config = info_settings['ModelInputInfoFields']

        self.InputSourcesCols = [self.config['source'],
                                 self.config['sourcetype'],
                                 self.config['input_file'],
                                 self.config['input_sheet'],
                                 ]
        self.InputInfoCols = [self.config['fname'],
                              self.config['is_real'],
                              self.config['is_sa']
                              ]
        self.InputInstructionCols = [
                                     self.config['output_sheet'],
                                     self.config['transf'],
                                     self.config['calc'],
                                     self.config['is_makesa'],
                                     self.config['freq'],
                                     self.config['ds'],
                                     self.config['de'],
                                     self.config['norm_d']
                                     ]

        self.config_output = info_settings['ModelOutputUnits']
        self.UnitsValueSet = set([self.config_output['m'],
                                  self.config_output['msa'],
                                  self.config_output['q'],
                                  self.config_output['qsa'],
                                  self.config_output['d'],
                                  self.config_output['a'],
                                  self.config_output['w']])
        self.SourceTypeManagerMap = {
            'RE_INT_DB':DBManagerExcel,
            'SQL':DBManagerSQL
        }

        self.database_sources = {}
        self.variables = []

    # def _package_path(self):
    #     return files("ModelManager")
    def initialize_raw_data_loaders(self):
        inputs_sheet = self.load_excel(self.model_path, 'input')
        var_list_columns = self.InputInfoCols
        for source_type in inputs_sheet[self.config['sourcetype']].unique():
            self.database_sources[source_type] = {}
            source_type_part = inputs_sheet.loc[inputs_sheet[self.config['sourcetype']] == source_type]
            for source in source_type_part[self.config['source']].unique():
                self.database_sources[source_type][source] = {}
                source_part = source_type_part.loc[source_type_part[self.config['source']] == source]
                for input_file in source_part[self.config['input_file']].unique():
                    self.database_sources[source_type][source][input_file] = {}
                    input_file_part = source_part.loc[source_part[self.config['input_file']] == input_file]
                    for input_sheet in input_file_part[self.config['input_sheet']].unique():
                        self.database_sources[source_type][source][input_file][
                            input_sheet] = self.SourceTypeManagerMap.get(source_type)(source, input_file, input_sheet)
                        input_sheet_part = input_file_part.loc[input_file_part[self.config['input_sheet']]==input_sheet]
                        for variable_fname in input_sheet_part[self.config['fname']].unique():
                            # variable_info = {self.config['fname']:variable_fname}
                            fname_part = input_sheet_part.loc[input_sheet_part[self.config['fname']]==variable_fname]
                            for is_real in fname_part[self.config['is_real']].unique():
                                is_real_part = fname_part.loc[fname_part[self.config['is_real']]==is_real]
                                for is_sa in is_real_part[self.config['is_sa']].unique():
                                    is_sa_part = is_real_part.loc[is_real_part[self.config['is_sa']]==is_sa]
                                    variable_info = {
                                        self.config['fname']:variable_fname,
                                        self.config['is_real']:is_real,
                                        self.config['is_sa']:is_sa
                                    }
                                    datasource_info = {
                                        self.config['source_type']: source_type,
                                        self.config['source']: source,
                                        self.config['input_file']: input_file,
                                        self.config['input_sheet']: input_sheet
                                    }
                                    destinations = []
                                    for destination_row in is_sa_part.iterrows():
                                        destination = {}
                                        for col in self.InputInstructionCols:
                                            destination[col] = destination_row[col]
                                        destinations.append(destination)
                                    self.variables.append(Variable(
                                        variable_info=variable_info,
                                        datasource_info=datasource_info,
                                        dataloader_instance=self.database_sources[source_type][source][input_file][input_sheet],
                                        destinations=destinations
                                    ))

    def initialize_variables(self):



    # def get_model_inputs(self, return_method_output=True):
    #     """
    #
    #     Args:
    #         return_method_output:
    #
    #     Returns:
    #
    #     """
    #
    #     inputs_sheet = self.load_excel(self.model_path, 'input')
    #     var_list_columns = self.InputInfoCols
    #
    #     db_sources = inputs_sheet[self.InputSourcesCols].unique()
    #
    #     for source in db_sources.iterrows():
    #
    #
    #         if source['source_type'] == 'SQL':
    #             #data_source = DBManagerSQL()
    #             pass
    #         else:
    #             data_source = DBManagerExcel(source[self.config['source']],
    #                                          source[self.config['input_file']],
    #                                          source[self.config['input_sheet']],
    #                                          )
    #         data_source.add_indicators()
    #         self.database_sources.append(data_source)
    #
    #
    #
    #
    #     inputs_sheet = inputs_sheet.merge(var_list[var_list_columns], how='left', left_on=mif.InputInfoCols,
    #                                       right_on=mif.InputInfoCols)
    #
    #     output_keys = list(inputs_sheet[mif.config['output_sheet']].unique())
    #
    #     self.db_data_sheets = list(inputs_sheet[mif.config['input_sheet']].unique())
    #     self.InputVarsTranformDict = inputs_sheet[mif.InputInstructionCols].set_index(mif.config['fname']).to_dict()
    #     for k in output_keys:
    #         self.model_input_sheets_info[k] = inputs_sheet.loc[
    #             inputs_sheet[mif.config['output_sheet']] == k].reset_index().drop(
    #             columns='index')
    #     print(f'Successfully obtained model inputs || Model input keys are {self.model_input_sheets_info.keys()}')
    #
    #     if return_method_output:
    #         return self.model_input_sheets_info
    #     else:
    #         return 0

    def assert_model_integrity(self):
        True

    def load_model_inputs(self):
        True

    def transform_model_inputs(self):
        True

    def put_model_inputs(self):
        True

