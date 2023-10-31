from .Utils import setup_logger, get_config
from .ExcelUtils import DataExcel
from .DBManagerExcel import DBManagerExcel


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
                                 self.config['source_type'],
                                 self.config['input_file'],
                                 self.config['input_sheet'],
                                 ]
        self.InputInfoCols = [self.config['fname'],
                              self.config['is_real'],
                              self.config['is_sa']
                              ]
        self.InputInstructionCols = [self.config['fname'],
                                     self.config['input_sheet'],
                                     self.config['output_sheet'],
                                     self.config['is_real'],
                                     self.config['is_sa'],
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

    def _package_path(self):
        return files("ModelManager")

    def get_model_inputs(self, return_method_output=True):
        """

        Args:
            return_method_output:

        Returns:

        """

        inputs_sheet = self.load_excel(self.model_path, 'input')
        var_list_columns = self.InputInfoCols

        db_sources = inputs_sheet[self.InputSourcesCols].unique()

        for source in db_sources.iterrows():
            if source['source_type'] == 'SQL':
                #data_source = DBManagerSQL()
                pass
            else:
                data_source = DBManagerExcel(source[self.config['source']],
                                             source[self.config['input_file']],
                                             source[self.config['input_sheet']],
                                             )
            data_source.add_indicators()
            self.database_sources.append(data_source)




        inputs_sheet = inputs_sheet.merge(var_list[var_list_columns], how='left', left_on=mif.InputInfoCols,
                                          right_on=mif.InputInfoCols)

        output_keys = list(inputs_sheet[mif.config['output_sheet']].unique())

        self.db_data_sheets = list(inputs_sheet[mif.config['input_sheet']].unique())
        self.InputVarsTranformDict = inputs_sheet[mif.InputInstructionCols].set_index(mif.config['fname']).to_dict()
        for k in output_keys:
            self.model_input_sheets_info[k] = inputs_sheet.loc[
                inputs_sheet[mif.config['output_sheet']] == k].reset_index().drop(
                columns='index')
        print(f'Successfully obtained model inputs || Model input keys are {self.model_input_sheets_info.keys()}')

        if return_method_output:
            return self.model_input_sheets_info
        else:
            return 0
