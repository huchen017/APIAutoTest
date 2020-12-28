def send_request(data, project_dict, _path, relevance=None):
    """
    封装请求
    :param data: 测试用例
    :param project_dict: 用例文件内容字典
    :param relevance: 关联对象
    :param _path: case路径
    :return:
    """
    logging.info("="*100)
    try:
        # 获取用例基本信息
        get_header =project_dict["test_info"].get("headers")
        get_host = project_dict["test_info"].get("host")
        get_address = project_dict["test_info"].get("address")
        get_http_type = project_dict["test_info"].get("http_type")
        get_request_type = project_dict["test_info"].get("request_type")
        get_parameter_type = project_dict["test_info"].get("parameter_type")
        get_cookies = project_dict["test_info"].get("cookies")
        get_file = project_dict["test_info"].get("file")
        get_timeout = project_dict["test_info"].get("timeout")
    except Exception as e:
        logging.exception('获取用例基本信息失败，{}'.format(e))

    try:
        # 如果用例中写了headers关键字，则用用例中的headers值（若该关键字没有值，则会将其值置为none），否则用全局headers
        get_header = data["headers"]
    except KeyError:
        pass
    try:
        # 替换成用例中相应关键字的值，如果用例中写了host和address，则使用用例中的host和address，若没有则使用全局传入的默认值
        get_host = data["host"]
    except KeyError:
        pass
    try:
        get_address = data["address"]
    except KeyError:
        pass
    try:
        get_http_type = data["http_type"]
    except KeyError:
        pass
    try:
        get_request_type = data["request_type"]
    except KeyError:
        pass
    try:
        get_parameter_type = data["parameter_type"]
    except KeyError:
        pass
    try:
        get_cookies = data["cookies"]
    except KeyError:
        pass
    try:
        get_file = data["file"]
    except KeyError:
        pass
    try:
        get_timeout = data["timeout"]
    except KeyError:
        pass

    Cookie = None

    header = get_header
    if get_header:
        if isinstance(get_header, str):
            header = confManage.conf_manage(get_header, "header")  # 处理请求头中的变量
            if header == get_header:
                pass

            else:
                var_list = re.findall('\$.*?\$', header)
                header = literal_eval(header)  # 将字典类型的字符串，转成字典
                # 处理请求头中的变量和函数
                if var_list:
                    # 将关联对象里的键值对遍历出来，并替换掉字典值中的函数
                    rel = dict()
                    for key, value in header.items():
                        rel[key] = replace_random(value)
                    header = rel
                    logging.debug("替换请求头中的函数处理结果为：{}".format(header))

                    str_header = str(header)
                    var_list = re.findall('\${.*?}\$', str_header)
                    if var_list:
                        # 用自身关联对象里的变量值，替换掉自身关联对象里的变量
                        header = replaceRelevance.replace(header, header)

                        str_header = str(header)
                        var_list = re.findall('\$.*?\$', str_header)
                        if var_list:
                            # 再次将关联对象里的键值对遍历出来，并替换掉字典值中的函数
                            rel = dict()
                            for key, value in header.items():
                                rel[key] = replace_random(value)
                            header = rel
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass
    else:
        pass
    logging.debug("请求头处理结果为：{}".format(header))

    if get_cookies is True:
        cookie_path = root_path + "/common/configModel/relevance"
        Cookie = ini_relevance(cookie_path, 'cookie')   # 为字典类型的字符串
        logging.debug("cookie处理结果为：{}".format(Cookie))
    else:
        pass

    parameter = readParameter.read_param(data["test_name"], data["parameter"], _path, relevance)    #处理请求参数（含参数为文件的情况）
    logging.debug("请求参数处理结果：{}".format(parameter))

    get_address = str(replaceRelevance.replace(get_address, relevance))  # 处理请求地址中的变量
    logging.debug("请求地址处理结果：{}".format(get_address))

    get_host = str(confManage.conf_manage(get_host, "host"))   # host处理，读取配置文件中的host
    logging.debug("host处理结果：{}".format(get_host))
    if not get_host:
        raise Exception("接口请求地址为空 {}".format(get_host))
    logging.info("请求接口：{}".format(data["test_name"]))
    logging.info("请求地址：{}".format((get_http_type + "://" + get_host + get_address)))
    logging.info("请求头: {}".format(header))
    logging.info("请求参数: {}".format(parameter))

    # 通过get_request_type来判断，如果get_request_type为post_cookie；如果get_request_type为get_cookie
    if get_request_type.lower() == 'post_cookie':
        with allure.step("保存cookie信息"):
            allure.attach("请求接口：", data["test_name"])
            allure.attach("用例描述：", data["info"])
            allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))

        result = apiMethod.save_cookie(header=header, address=get_http_type + "://" + get_host + get_address,
                                  request_parameter_type=get_parameter_type,
                                  data=parameter,
                                  cookie=Cookie,
                                  timeout=get_timeout)

    elif get_request_type.lower() == 'post':
        logging.info("请求方法: POST")
        if get_file:
            with allure.step("POST上传文件"):
                allure.attach("请求接口：",data["test_name"])
                allure.attach("用例描述：", data["info"])
                allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
                allure.attach("请求头", str(header))
                allure.attach("请求参数", str(parameter))

            result = apiMethod.post(header=header,
                                    address=get_http_type + "://" + get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    files=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
        else:
            with allure.step("POST请求接口"):
                allure.attach("请求接口：", data["test_name"])
                allure.attach("用例描述：", data["info"])
                allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
                allure.attach("请求头", str(header))
                allure.attach("请求参数", str(parameter))
            result = apiMethod.post(header=header,
                                    address=get_http_type + "://" + get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    data=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
    elif get_request_type.lower() == 'get':
        with allure.step("GET请求接口"):
            allure.attach("请求接口：", data["test_name"])
            allure.attach("用例描述：", data["info"])
            allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))
            logging.info("请求方法: GET")
        result = apiMethod.get(header=header,
                               address=get_http_type + "://" + get_host + get_address,
                               data=parameter,
                               cookie=Cookie,
                               timeout=get_timeout)
    elif get_request_type.lower() == 'put':
        logging.info("请求方法: PUT")
        if get_file:
            with allure.step("PUT上传文件"):
                allure.attach("请求接口：", data["test_name"])
                allure.attach("用例描述：", data["info"])
                allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
                allure.attach("请求头", str(header))
                allure.attach("请求参数", str(parameter))
            result = apiMethod.put(header=header,
                                    address=get_http_type + "://" + get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    files=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
        else:
            with allure.step("PUT请求接口"):
                allure.attach("请求接口：", data["test_name"])
                allure.attach("用例描述：", data["info"])
                allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
                allure.attach("请求头", str(header))
                allure.attach("请求参数", str(parameter))
            result = apiMethod.put(header=header,
                                    address=get_http_type + "://" + get_host + get_address,
                                    request_parameter_type=get_parameter_type,
                                    data=parameter,
                                    cookie=Cookie,
                                    timeout=get_timeout)
    elif get_request_type.lower() == 'delete':
        with allure.step("DELETE请求接口"):
            allure.attach("请求接口：", data["test_name"])
            allure.attach("用例描述：", data["info"])
            allure.attach("请求地址", get_http_type + "://" + get_host + get_address)
            allure.attach("请求头", str(header))
            allure.attach("请求参数", str(parameter))
        logging.info("请求方法: DELETE")
        result = apiMethod.delete(header=header,
                               address=get_http_type + "://" + get_host + get_address,
                               data=parameter,
                               cookie=Cookie,
                               timeout=get_timeout)
    …………………………
    else:
        result = {"code": False, "data": False}
        logging.info("没有找到对应的请求方法！")
    logging.info("请求接口结果：\n {}".format(result))
    return result