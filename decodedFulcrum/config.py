__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'

import os

# look for the config.config file in the same directory as this source code file
_source_code_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)))
configFile = open(os.path.join(_source_code_folder, 'config.config'))

settings = {}

for line in configFile:
    if '=' in line:
        # split on option char:
        setting, value = line.split('=', 1)
        # strip spaces:
        setting = setting.strip()
        value = value.strip()
        # store in dictionary:
        settings[setting] = value

API_KEY = settings['API_KEY']
FORM_ID = settings['FORM_ID']
