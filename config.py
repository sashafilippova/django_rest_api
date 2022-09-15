from configparser import ConfigParser

def config(filename = 'db.ini', section='postgresql'):
    config_params = dict()
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        for key, value in parser.items(section):
            config_params[key] = value
    else:
        raise Exception(f'section {section} in {filename} not found')

    return config_params