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
        self.ini_file_path = "test/rio-pure.ini"

    def teardown_method(self):
        None

    def test_read(self):
        riot = Riot()
        riot.read(self.ini_file_path)
        
        print(f" filter section: {riot.config_dict["FILTER"]}")
        riot.config.get("DISPLAY")

    def test_write(self):
        #riot = Riot()
        None
        
    def test_parse(self):
        riot = Riot()
        riot.read(self.ini_file_path)
        output = []
        section_name = "DISPLAY"
        for key, value in riot.config_dict[section_name].items():
            output.append(f"{key.upper()} = {value}")
        context = {
            "riogen": "\n".join(output),
        }
        riot.loadTemplate(self.t1,context)
        
        #parsed_config = riot.parse()
        None
        
