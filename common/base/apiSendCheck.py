import ast
import json
from common.base import apiSend
from common.base import checkResult

def api_send_check(case_data, case_dict):
    result = apiSend.send_request(case_data, case_dict)
    code = result[0]
    subCode = result[1].get('subCode')
    bodyMessage = result[1].get('bodyMessage')
    if bodyMessage !='':
        bodyMessage = json.loads(bodyMessage)
    checkResult.check_result(case_data, code, subCode, bodyMessage)


