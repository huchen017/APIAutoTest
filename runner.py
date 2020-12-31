import os
import pytest
from datetime import datetime

report_file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
report_dir = os.path.dirname(__file__) + '\\report\\'+ report_file_name
report_xml = report_dir+'\\xml'
report_html = report_dir+'\\html'

if __name__ == '__main__':
    pytest.main(['-sq','testcase/UserLoginApi/test_AccountLogin.py','--alluredir', report_xml])
    os.system("allure generate " + report_xml +" -o " + report_html + " --clean")