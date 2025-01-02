from configparser import ConfigParser
from collections import OrderedDict
from Cheetah.Template import Template
import itertools as itt


class MOD(dict):
    def __init__(self, *args, **kwargs):
        self.c = itt.count()
        super().__init__(*args, **kwargs)
         
    def __setitem__(self, k, v):
        if k == 'textsize':
            n = next(self.c)
            k = k + str(n)
        print('setitem:', id(self), k, v)
        super().__setitem__(k, v)


class Riot:
    def __init__(self):
        self.config = {}
        self.config_dict = {}

    def read(self, fpath):
        #config = ConfigParser(strict=False, dict_type=multidict )
        config = ConfigParser(
            strict = False,
            dict_type = MOD,
            allow_no_value=True)
        config.read(fpath)
        for section in config.sections():
            section_data = {}
            print(f"section {section}")
            self.config_dict[section] = {}
            for key, value in config.items(section):
                if key in self.config_dict[section]:
                    print(f"Duplicate key '{key}' in section '{section}' found. Skipping.")
                else:
                    section_data[key] = value
            self.config_dict[section] = section_data

        print(f"Config Dict: {self.config_dict}")

    def write(self, fname, content):
        with open(fname, 'w') as f:
            f.write(content)

    def parse(self):
        return

    def loadTemplate(self, template_file_path,context):
        # Load the template from a file or other source
        with open(template_file_path, 'r') as f:
            source = f.read()

        # Create a Cheetah template object and populate it
        t = Template(source, searchList=[context])

        # Print the populated template
        print(str(t))

