import requests
import json
import logging
import os
import random
from requests_toolbelt import MultipartEncoder

def post(header, address, request_parameter_type, timeout=8, data=None, files=None, cookie=None):
    '''
    post请求
    :param header:请求头
    :param address:请求地址
    :param request_parameter_type:请求参数格式
    :param timeout:超时时间
    :param data:请求参数
    :param files:文件路径
    :param cookie:
    :return:
    '''
    if 'data' in request_parameter_type:
        response = requests.post(url=address, data=data, headers=header, timeout=timeout, cookies=cookie, files=files)

    elif 'json' in request_parameter_type:
        response = requests.post(url=address, json=data, headers=header, timeout=timeout, cookies=cookie, files=files)

    elif 'form_data' in request_parameter_type:
        for i in files:
            value = files[i]
            if '/' in value:
                file_param = i
                files[file_param] = (os.path.basename(),open(value, 'rb'))
        enc = MultipartEncoder(fields=files, boundary='--------------' + str(random.randint(1e28, 1e29 - 1)))
        header['Contrnt-Type'] = enc.content_type
        response = requests.post(url=address, data=enc, headers=header, timeout=timeout, cookies=cookie)

    try:
        if response.status_code != 200:
            return response.status_code, response.text
        else:
            return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise

def get(header, address ,data, timeout=8, cookie=None):
    '''
    get请求
    :param header:请求头
    :param address:请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :param cookie: 
    :return: 
    '''
    response = requests.get(url=address, params=data, headers=header, timeout=timeout, cookies=cookie)
    if response.status_code == 301:
        response = requests.get(url=response.headers['location'])
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        logging.exception("ERROR")
        logging.error(e)
        raise

def put(header, address, request_parameter_type, data, timeout=8,  files=None, cookie=None):
    if request_parameter_type == 'raw':
        data = json.jumps(data)
    response = requests.put(url=address, data=data, headers=header, timeout=timeout,  files=files, cookies=cookie)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        logging.exception("ERROR")
        logging.error(e)
        raise

def delete(header, address, data, timeout=8, cookie=None):
    response = requests.delete(url=address, params=data, headers=header, timeout=timeout, cookies=cookie)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        logging.exception("ERROR")
        logging.error(e)
        raise

