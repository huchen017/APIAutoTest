import logging
import allure
import ast
from common.base.initializeYamlFile import InitializeYamlFile
from common.confManage.confRead import ConfRead
from common.base import apiMethod


def send_request(case_data, project_dict):
    '''
    封装请求
    :param data: 测试用例数据
    :param prohect_dict: 测试用例文件的数据
    :return:
    '''
    logging.info("*"*100)
    try:
        # 获取用例基本信息
        get_header = project_dict['test_info'].get('headers')
        get_host = project_dict['test_info'].get('host')
        get_address = project_dict['test_info'].get('address')
        get_http_type = project_dict['test_info'].get('http_type')
        get_request_type = project_dict['test_info'].get('request_type')
        get_parameter_type = project_dict['test_info'].get('parameter_type')
        get_cookies = project_dict['test_info'].get('cookies')
        get_file = project_dict['test_info'].get('file')
        get_timeout = project_dict['test_info'].get('timeout')
    except Exception as e:
        logging.exception('获取用例基础信息失败, {}'.format(e))

    try:
        # 如果用例中写了headers关键字，则用用例中的headers值（若该关键字没有值，则会将其值置为none），否则用全局headers
        get_header = case_data["headers"]
    except KeyError:
        pass
    try:
        # 替换成用例中相应关键字的值，如果用例中写了host和address，则使用用例中的host和address，若没有则使用全局传入的默认值
        get_host = case_data["host"]
    except KeyError:
        pass
    try:
        get_address = case_data["address"]
    except KeyError:
        pass
    try:
        get_http_type = case_data["http_type"]
    except KeyError:
        pass
    try:
        get_request_type = case_data["request_type"]
    except KeyError:
        pass
    try:
        get_parameter_type = case_data["parameter_type"]
    except KeyError:
        pass
    try:
        get_cookies = case_data["cookies"]
    except KeyError:
        pass
    try:
        get_file = case_data["file"]
    except KeyError:
        pass
    try:
        get_timeout = case_data["timeout"]
    except KeyError:
        pass

    Cookie=None
    header = get_header
    if get_header is None:
        header = ConfRead().get_header('header')
        header = ast.literal_eval(header)

    if get_host is None:
        get_host = ConfRead().get_host('test_host')
        logging.debug("请求地址处理结果：{}".format(get_host))
        if get_host is None:
            raise Exception("请求地址为空：{}".format(get_host))

    parameter = case_data.get('parameter')
    logging.info("请求接口：{}".format(case_data.get('test_name')))
    logging.info("请求地址：{}".format((get_http_type+"://"+ get_host + get_address)))
    logging.info("请求header：{}".format(header))
    logging.info("请求参数：{}".format(parameter))

    if get_request_type.lower() == 'post':
        logging.info("请求方法:POST")
        if get_file:
            with allure.step("POST请求接口"):
                allure.attach("请求接口：", case_data.get('test_name'))
                allure.attach("用例描述：", case_data.get('test_info'))
                allure.attach("请求地址：", get_http_type+"://"+get_host+get_address)
                allure.attach("请求参数：", str(parameter))
            result = apiMethod.post(header=header, address=get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    files=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
        else:
            with allure.step("POST请求接口"):
                allure.attach("请求接口：", case_data.get('test_name'))
                allure.attach("用例描述：", case_data.get('test_info'))
                allure.attach("请求地址：", get_http_type+"://"+get_host+get_address)
                allure.attach("请求参数：", str(parameter))
            result = apiMethod.post(header=header, address=get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    data=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
    return result








        










if __name__ == '__main__':
    send_request()