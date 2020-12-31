import os
from common.base.initializeYamlFile import InitializeYamlFile
from common.base import apiSend
from common.base import checkResult

def api_send_check(case_data, case_dict):
    result = apiSend.send_request(case_data, case_dict)
    code = result[0]
    subCode = result[1].get('subCode')
    data = result[1].get('bodyMessage')
    checkResult.check_result(case_data, code, subCode, data)


