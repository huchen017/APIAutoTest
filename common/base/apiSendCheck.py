import os
from common.base.initializeYamlFile import InitializeYamlFile
from common.base import apiSend


case_File_name = 'UserLogin'
init_file = InitializeYamlFile()
case_data = init_file.init_Yaml(case_File_name)
def api_send_check(case_data, case_dict, case_path):
    result = apiSend.send_request(case_data, case_dict)


