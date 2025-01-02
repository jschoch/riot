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
        # Create a temporary INI file for testing
        self.ini_content = """
[EMC]
MACHINE = MyMachine
VERSION = 1.0

[AXIS_X]
MAX_LIMIT = 50.0
MIN_LIMIT = -50.0
"""
        self.ini_file_path = create_ini_file(self.ini_content)

    def teardown_method(self):
        # Clean up the temporary INI file after each test
        os.remove(self.ini_file_path)

    def test_read(self):
        riot = Riot(config={})
        riot.read(self.ini_file_path)
        
        expected_config = {
            'EMC': {'MACHINE': 'MyMachine', 'VERSION': '1.0'},
            'AXIS_X': {'MAX_LIMIT': '50.0', 'MIN_LIMIT': '-50.0'}
        }
        assert riot.config == expected_config

    def test_write(self):
        riot = Riot(config={})
        
        output_file_path = tempfile.NamedTemporaryFile(delete=False, mode='w').name
        content = "Test Content"
        riot.write(output_file_path, content)
        
        with open(output_file_path) as f:
            written_content = f.read()
        
        os.remove(output_file_path)
        assert written_content == content

    def test_parse(self):
        riot = Riot(config={})
        riot.read(self.ini_file_path)
        
        parsed_config = riot.parse()
        
        expected_config = {
            'EMC': {'MACHINE': 'MyMachine', 'VERSION': '1.0'},
            'AXIS_X': {'MAX_LIMIT': '50.0', 'MIN_LIMIT': '-50.0'}
        }
        assert parsed_config == expected_config
