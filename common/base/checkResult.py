import allure

def check_json(expected_data, dst_data):
    '''
    校验json数据
    :param expected_data: 校验的内容
    :param dst_data: 接口返回的数据
    :return:
    '''
    if isinstance(expected_data, dict):
        for key in expected_data.keys():
            if key not in dst_data:
                raise Exception("JSON格式校验，关键字%s不在返回结果%s中" %(key, dst_data))
            else:
                check_key = key
                if isinstance(expected_data[check_key], dict) and isinstance(dst_data[check_key], dict):
                    check_json(expected_data[check_key], dst_data[check_key])
                elif isinstance(expected_data[check_key], type(dst_data[check_key])):
                    if expected_data[check_key]==dst_data[check_key]:
                        pass
                    else:
                        raise Exception("实际结果%s与期望结果%s不相同"%(expected_data[check_key], dst_data[check_key]))
                else:
                    raise Exception("JSON格式校验，关键字%s与关键字%s类型不符" %(expected_data[check_key], dst_data[check_key]))
    else:
        raise Exception("JSON格式校验非Dict格式")


def check_result(case, code, subCode, data):
    check = case['check']
    # 不校验结果
    if check['check_type'] == 'no_check':
        with allure.step("不校验结果"):
            pass

    # json格式校验
    elif check['check_type'] == 'json':
        expected_result = ''
        try:
            expected_result = check['expected_result']
        except KeyError:
            pass
        with allure.step('JSON格式校验'):
            allure.attach("期望code", str(check['expected_code']))
            allure.attach("期望SubCode", str(check['expected_SubCode']))
            if expected_result != '':
                allure.attach("期望data", str(expected_result))
            allure.attach("实际data", str(code))
            allure.attach("实际SubCode", str(subCode))
            allure.attach("实际data", str(data))
        if int(code) == check['expected_code']:
            if str(subCode) == check['expected_SubCode']:
                try:
                    expected_result = check['expected_result']
                    if expected_result is not None:
                        check_json(expected_result, data)
                except KeyError:
                    pass
            else:
                raise Exception("subCode错误 \n {0} != {1}".format(subCode, check['expected_SubCode']))
        else:
            raise Exception("code错误 \n {0} != {1}".format(code, check['expected_code']))





