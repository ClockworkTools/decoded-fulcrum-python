__author__ = 'Keith Hannon'
__copyright__ = 'Copyright (c)  2015 Keith Hannon, Clockwork'
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

from fulcrum.api.endpoints import Records
from decodedFulcrum.fulcrumJsonUtils import decode, recode
from decodedFulcrum.schema import Schema

class DecodedRecords(Records):
    path = 'records'

    def __init__(self, api_config, dictionaryOfSchemas):
        super(DecodedRecords, self).__init__(api_config)
        self.dictionaryOfSchemas = dictionaryOfSchemas

    def find(self, id):
        api_resp = super(DecodedRecords, self).find(id)

        # decode the api response
        # decode(api_resp, self.fieldNameLookups)
        decode(api_resp, self.dictionaryOfSchemas)

        return api_resp

    def search(self, url_params=None):
        api_resp = super(DecodedRecords, self).search(url_params)

        # decode the api response
        decode(api_resp, self.dictionaryOfSchemas)

        return api_resp

    def create(self, obj):
        # reapply the keys to the json object that has been passed back before it written to Fulcrum
        recode(obj, self.dictionaryOfSchemas)

        api_resp = super(DecodedRecords, self).create(obj)

        # now decode the api response
        decode(api_resp, self.dictionaryOfSchemas)

        return api_resp

    def update(self, id, obj):
        # reapply the keys to the json object that has been passed back before it is written back to Fulcrum
        recode(obj, self.dictionaryOfSchemas)

        api_resp = super(DecodedRecords, self).update(id, obj)

        # now decode the api response
        decode(api_resp, self.dictionaryOfSchemas)

        return api_resp

    def history(self, id):
        api_resp = super(DecodedRecords, self).history(id)

         # now decode the api response
        # probably need to extract the record aspects before this works
        api_resp= decode(api_resp, self.dictionaryOfSchemas)

        return api_resp


class Schemas(object):
    path = 'schemas'

    def __init__(self, jsonForms):
        #jsonForms is a list of forms
        self.dictionaryOfSchemas = {}

        for jsonForm in jsonForms:
            schema = Schema(jsonForm)
            formId = schema.getFormId()
            self.dictionaryOfSchemas[formId] = schema

    def find(self, formIdOrName):
        if formIdOrName in self.dictionaryOfSchemas:
            return self.dictionaryOfSchemas[formIdOrName]
        else:
            for formId, schema in self.dictionaryOfSchemas.items():
                if schema.getFormName() == formIdOrName:
                    return schema

        raise Exception ('no such form')

    def search(self):
        return self.dictionaryOfSchemas

