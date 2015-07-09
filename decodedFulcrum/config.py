__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'

"""
   Copyright 2015 Keith Hannon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
