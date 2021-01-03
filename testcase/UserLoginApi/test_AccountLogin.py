import allure
import pytest
from common.base.initializeYamlFile import InitializeYamlFile
from common.base import apiSendCheck


root_path = "E:/FXAPITest/"
case_path = root_path + 'casedata/UserLogin/'
init_file = InitializeYamlFile()
case_dict = init_file.init_Yaml(case_path, 'UserLogin')

@allure.feature(case_dict['test_info']["title"])
class TestLogin:

    @pytest.mark.parametrize("case_data", case_dict['test_case'], ids=[])
    @allure.story('UserLogin')
    def test_UserLogin(self, case_data):
        apiSendCheck.api_send_check(case_data, case_dict)


