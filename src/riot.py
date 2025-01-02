from configparser import ConfigParser
from collections import OrderedDict
from Cheetah.Template import Template
import itertools as itt
import os


# deal with duplicate keys
class MOD(dict):
    def __init__(self, *args, **kwargs):
        self.c = itt.count()
        super().__init__(*args, **kwargs)
         
    def __setitem__(self, k, v):
        if k == 'textsize':
            n = next(self.c)
            k = k + str(n)
        #print('setitem:', id(self), k, v)
        super().__setitem__(k, v)


class Riot:
    def __init__(self):
        self.ini_config = {}
        self.config_dict = {}

        # default template directory
        #  could have a config somewhere for this
        self.tdir = "~/riot/ini_templates"
        self.backupDir = "./riot_backups"
        self.ini_fpath = ""

    def read_ini(self, fpath):
        #config = ConfigParser(strict=False, dict_type=multidict )
        self.ini_fpath = fpath;
        config = ConfigParser(
            strict = False,
            dict_type = MOD,
            allow_no_value=True)
        config.read(fpath)
        for section in config.sections():
            section_data = {}
            #print(f"section {section}")
            self.config_dict[section] = {}
            for key, value in config.items(section):
                if key in self.config_dict[section]:
                    print(f"Duplicate key '{key}' in section '{section}' found. Skipping.")
                else:
                    section_data[key] = value
            self.config_dict[section] = section_data
        self.ini_config = config
        #print(f"Config Dict: {self.config_dict}")

    def write(self, fname, content):
        with open(fname, 'w') as f:
            f.write(content)

    def parse_ini_template(self,section_name):
        output = []
        for key, value in self.config_dict[section_name].items():
            output.append(f"{key.upper()} = {value}")
            
        return "\n".join(output)


    def loadTemplate(self, template_file_path,context):
        # Load the template from a file or other source
        with open(template_file_path, 'r') as f:
            source = f.read()

        # Create a Cheetah template object and populate it
        t = Template(source, searchList=[context])

        generated_string = str(t)
        # Print the populated template
        print(str(t))
        return generated_string

    def regen_ini(self,tdir):
        if tdir == None:
            tdir = self.tdir
        new_config = []
        print(f"Regenerating INI from templates in {tdir}")
        templates = {}
        for root, dirs, files in os.walk(tdir):
            for file in files:
                if file.endswith(".t"):
                    template_file_path = os.path.join(root, file)
                    print(f"found template: {template_file_path}")
                    section_name = os.path.splitext(file)[0]
                    gen_string = self.parse_ini_template(section_name)
                    context = {
                        "riogen": gen_string
                    }
                    generated_section = self.loadTemplate(template_file_path,context)
                    templates[section_name] = generated_section
        for section in self.ini_config.sections():
            
            if section in templates.keys():
                print(f"found generated section template: {section}")
                s = templates[section] 
                new_config.append(s)
                print(s)

            else:
                print(f" {section} template not found, leaving alone")
                output = [f"[{section.upper()}]\n"]
                for key, value in self.config_dict[section].items():
                    output.append(f"{key.upper()} = {value}")
                s = "\n".join(output)
                print( s)
                new_config.append(s)

        new_config_string = "\n".join(new_config)
        new_config_fname = "thenew.ini"
        print("full config generated as file {new_config_fname} \n")
        with open(new_config_fname, 'w') as file:
            file.write(new_config_string)



