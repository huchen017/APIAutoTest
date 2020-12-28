import json
from common.base.initializeYamlFile import InitializeYamlFile

class ReadParameter:
    case_File_name = 'UserLogin'
    init_file = InitializeYamlFile()
    case_data = init_file.init_Yaml(case_File_name)

    def read_parameter(self, case_name):
        case_list = self.case_data.get("test_case")
        for i in range(len(case_list)):
            if case_list[i].get('test_name') == case_name:
                case_parameter = case_list[i].get('parameter')
                print(case_parameter)
                return case_parameter


        # if case_name in case_list:
        #     print("pass")
        print(case_list['test_name'])

if __name__ == '__main__':
    case_name = '账号密码登录成功'
    read_para = ReadParameter()
    read_para.read_parameter(case_name)