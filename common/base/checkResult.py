

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
                elif isinstance(type(expected_data[check_key]), type(dst_data[check_key])):
                    pass
                else:
                    raise Exception("JSON格式校验，关键字%s与关键字%s类型不符" %(expected_data[check_key],dst_data[check_key]))


    else:
        raise Exception("JSON格式校验非Dict格式")

def check_result():
    if