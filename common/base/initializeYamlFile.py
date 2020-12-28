import yaml
import os


class InitializeYamlFile:
    # root_path = "E:/Automation/FXAPITest/"
    # case_path = root_path + 'casedata/UserLogin/'

    def init_Yaml(self, case_path, case_File_name):
        case_data_path = case_path + case_File_name + '.yml'
        case_data = open(case_data_path, 'r', encoding='utf-8')
        case_data_json = yaml.load(case_data.read())
        print(case_data_json)
        return case_data_json



if __name__ == '__main__':
    case_File_name = 'UserLogin'
    init_file = InitializeYamlFile()
    init_file.init_Yaml(case_File_name)


