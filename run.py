from New_code.DataManager import InputHandler
from Utils.information import INFO as info
from Utils.information import ModelInputInfoFields as mif
from Utils.information import ModelOutputUnits as mou


IH = InputHandler('kzt')
IH.get_model_inputs()
IH.get_model_data()