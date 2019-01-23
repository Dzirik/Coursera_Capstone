import os
import configparser

class ConfigHandler(object):
    
    def __init__(self, config):
        """
        :param config: None or configparser. If None, default configparser 
                       "config.ini" is read from parenct directory.
        """
        
        if config is None:
            self.config = configparser.ConfigParser()
            par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            self.config.read(os.path.join(par_dir, "config.ini"))
        else:
            self.config = config   