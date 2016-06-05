from ConfigParser import ConfigParser

def parse(filename):
    config_dir = ""
    parser = ConfigParser()

    parser.read(config_dir + filename + ".conf")

    return parser._sections[filename]
