# DataManage project

Description:
Load data from different datasources (excel, sql, etc), transform it according to rules and save to model files

## DataManage structure:

### 1. Class `ModelManager` 
Main class to work with `models`: excel files with settings and list of variables to load and to transform. 

Has following methods:

1.  **constructor**
inputs: file path to the model
outputs:
function: 
	- initialize logger
	- load YAML file with model settings
TODO:

2. **get_model_inputs**
inputs: `return_method_output` flag, if `True` returns `model_input_sheets_info`
outputs: `model_input_sheets_info`
function:
	- load variables list to use in the model from `input` sheet  
	- create list of unique datasources based on `InputSourcesCols`
	- create datasource objects depending on Source Type: `DBManagerSQL` for SQL, `DBManagerExcel` for Excel 
TODO: -add proper `logging`

3. **check_model_integrity - TODO**
TODO: check the integrity of the model, column names in `input` sheet corresponds to `ModelInputInfoFields` 

4. **load_model_inputs - TODO**
use `load_inputs` method of `DBManagerExcel/DBManagerSQL` objects to load data from DataSources 
return list of `Variables` objects

6. **transform_model_inputs - TODO**
use rules for transformation from  `input` sheet to transform `Variables` objects
return list (or dictionary) of transformed `Variables`

8. **save_model_inputs - TODO**
use output location from `input` sheet to save transformed `Variables`

### 2. Class `DBManagerExcel`
Main class to work with Excel DataBases: excel files with list of variables on `var_list` sheet and data sheets: `daily`, `monthly`, `quarterly`, `annual` and etc

Has following methods:

1.  **constructor**
inputs: file path to the model
outputs:
function: 
	- initialize logger
	- load YAML file with model settings
TODO:

2. **get_inputs**
inputs: `return_method_output` flag, if `True` returns `model_input_sheets_info`
outputs: `model_input_sheets_info`
function:
	- load variables list to use in the model from `input` sheet  
	- create list of unique datasources based on `InputSourcesCols`
	- create datasource objects depending on Source Type: `DBManagerSQL` for SQL, `DBManagerExcel` for Excel 
TODO: -add proper `logging`

3. **check_model_integrity**
TODO: check the integrity of the model, column names in `input` sheet corresponds to `ModelInputInfoFields` 

### 2. Class `DBManagerExcel`