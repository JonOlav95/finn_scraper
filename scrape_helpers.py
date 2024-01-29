import os
import yaml



def load_flags():
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(location, "parameters.yml"), "r")
    flags = yaml.safe_load(f)
    f.close()

    return flags
