import os
import tempfile
import configparser
from src.riot import Riot

def create_ini_file(content):
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
        temp.write(content)
        return temp.name

class TestRiot:
    def setup_method(self):
        # display template
        self.t1 = "test/DISPLAY.t"

        # a test string
        self.ini_content = """
[EMC]
MACHINE = MyMachine
VERSION = 1.0

[AXIS_X]
MAX_LIMIT = 50.0
MIN_LIMIT = -50.0
"""
        self.ini_file_path = "test/rio-pure.ini"

    def teardown_method(self):
        None

    def test_read(self):
        riot = Riot()
        riot.read(self.ini_file_path)
        
        print(f" filter section: {riot.config_dict["FILTER"]}")

    def test_write(self):
        #riot = Riot()
        None
        
    def test_parse(self):
        riot = Riot()
        riot.read(self.ini_file_path)
        context = {
            "riogen": riot.config_dict['DISPLAY']
        }
        riot.loadTemplate(self.t1,context)
        
        #parsed_config = riot.parse()
        None
        
