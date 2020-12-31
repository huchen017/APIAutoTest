import os
import configparser

# 获取config文件的根目录
root_dir = os.path.dirname(os.path.split(os.path.dirname(__file__))[0])
# config.ini的目录
conf_path = root_dir+'/config/apiConfig.ini'

class ConfRead:
    def read_apiConfig(self, conf_path):
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        return conf

    def get_host(self, option):
        conf = ConfRead().read_apiConfig(conf_path)
        return conf.get('host', option)

    def get_header(self, option):
        conf = ConfRead().read_apiConfig(conf_path)
        return conf.get('header', option)




if __name__ == '__main__':
    option = 'test_host'