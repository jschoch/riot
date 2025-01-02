import configparser
from Cheetah.Template import Template

class Riot:
    def __init__(self, config):
        self.config = config

    def read(self, fpath):
        config = configparser.ConfigParser()
        config.read(fpath)
        config_dict = {}
        for section in config.sections():
            section_data = {}
            for key, value in config.items(section):
                section_data[key] = value
            config_dict[section] = section_data

        print(f"Config Dict: {config_dict}")

    def write(self, fname, content):
        with open(fname, 'w') as f:
            f.write(content)

    def parse(self):
        return
