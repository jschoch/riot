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
        self.t1 = "./test/DISPLAY.t"
        self.ini_file_path = "./test/rio-pure.ini"

    def teardown_method(self):
        None

    def test_read_ini(self):
        riot = Riot()
        riot.read_ini(self.ini_file_path)
        #print(f"keys: {riot.config_dict.keys()}") 
        for key in riot.ini_config_dict.keys():
            print(f"key: {key}")
        #print(f"display section: {riot.config_dict["DISPLAY"]}") 
        print(f" filter section: {riot.ini_config_dict["FILTER"]}")
        #riot.ini_config.get("DISPLAY")

    def test_parse_template_dir(self):
        riot = Riot()
        riot.read_ini(self.ini_file_path)
        riot.regen_ini(tdir="./ini_templates")

        
    def test_parse_test_tmplate(self):
        riot = Riot()
        riot.read_ini(self.ini_file_path)
        section_name = "DISPLAY"
        gen_string = riot.ini_conf_to_string(section_name,header=False) 

        context = {
            "riogen": gen_string
        }
        riot.loadTemplate(self.t1,context)
        
        #parsed_config = riot.parse()
        None
        

    def test_regen(self):
        riot = Riot()
        riot.read_ini(self.ini_file_path)
        riot.regen_ini(tdir="./ini_templates")

