__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'
__copyright__ = 'Copyright (c)  2015 Keith Hannon, Clockwork. Email keith@clockwork.co.nz'
__license__ = "AGPL-3.0-only"
"""
   Licensed under the GNU AGPL-3.0 License (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   https://www.gnu.org/licenses/agpl-3.0.en.html

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from decodedFulcrum.api.endpoints import DecodedRecords, Schemas
from fulcrumJsonUtils import getFieldLookups
from decodedFulcrum.schema import Schema
from decodedFulcrum.fieldnames import SYSTEM_LEVEL_FIELD_NAMES


class DecodedFulcrum(Fulcrum):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
        super(DecodedFulcrum, self).__init__(key=key, uri=uri)

        self.api_config = APIConfig(key=key, uri=uri)

        self.schemas = Schemas(self.forms.search()['forms'])

        # ensure that when the "records" part of the fulcrum_api is called, the DecodedRecords functionality is invoked
        # self.records = DecodedRecords(api_config, dictionaryOfSchemas, fieldNameLookups, fieldKeyLookups)
        self.records = DecodedRecords(self.api_config, self.schemas.search())



