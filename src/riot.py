from configparser import ConfigParser
from collections import OrderedDict
from Cheetah.Template import Template
import itertools as itt
import os
from multidict import MultiDict


# deal with duplicate keys
class MOD(dict):
    def __init__(self, *args, **kwargs):
        self.c = itt.count()
        super().__init__(*args, **kwargs)
         
    def __setitem__(self, k, v):
        print(f"k:{k} v: {v}")
        t = self.get(k)
        if t is not None and len(t) >0:  # if key exists, create new key with unique number appended to it. 
            n = next(self.c)
            new_key = f"{k}_____{n}"
            if(t[0] == v):
                #print(f"HOLY SHIT WHY?  k: {k} v: {v}")
                super().__setitem__(k, v)
            else: 
                super().__setitem__(new_key, v)
            #print("i hate you python")
        else:
            super().__setitem__(k, v)


class Riot:
    def __init__(self):
        self.ini_config = {}
        self.ini_config_dict = {}

        # default template directory
        #  could have a config somewhere for this
        self.tdir = "~/riot/ini_templates"
        self.backupDir = "./riot_backups"
        self.ini_fpath = ""

    def read_ini(self, fpath):
        print(f"opening file: {fpath}  ")

        self.ini_fpath = fpath;
        config = ConfigParser(
            strict = False,
            dict_type = MOD,
            empty_lines_in_values = False
            #allow_no_value=True
            )

        conf_string = ""
        if(not os.path.exists(fpath)):
            print("file does not exist")
            return None
        else:
            with open(fpath) as f:
                conf_string = f.read()
    

        config.read_string(conf_string)


        tmp_config = {}
        for section in config.sections():
            section_data = {}
            #section_data = MOD()
            print(f"section {section}")
            for key, value in config.items(section):
                section_data[key] = value
            tmp_config[section] = section_data
        print("read_ini: file parsed")
        self.ini_config = config
        self.ini_config_dict = tmp_config

    def ini_conf_to_string(self,section_name,header=True):
        output = []
        if header:
            output = [ f"[{section_name}]"]

        for key, value in self.ini_config_dict[section_name].items():
            if "_____" in key:
                [a,b ]= key.split("_____")
                output.append(f"{a.upper()} = {value}")
            else:
                output.append(f"{key.upper()} = {value}")
        return "\n".join(output)



    def write(self, fname, content):
        with open(fname, 'w') as f:
            f.write(content)



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
                    gen_string = self.ini_conf_to_string(section_name,header=False)
                    context = {
                        "riogen": gen_string
                    }
                    generated_section = self.loadTemplate(template_file_path,context)
                    templates[section_name] = generated_section


        print("processing sections")
        for section in self.ini_config.sections():
            print(f"section {section}") 
            if section in templates.keys():
                print(f"found generated section template: {section}")
                s = templates[section] 
                new_config.append(s)
                print(s)

            else:
                print(f" {section} template not found, leaving alone")
                s = self.ini_conf_to_string(section)
                print( s)
                new_config.append(s)

        new_config_string = "\n".join(new_config)
        new_config_fname = "thenew.ini"
        print(f"full config generated as file {new_config_fname} \n")
        with open(new_config_fname, 'w') as file:
            file.write(new_config_string)



