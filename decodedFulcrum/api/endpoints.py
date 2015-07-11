__author__ = 'Keith Hannon'

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
        print 'x'

        return api_resp

    def create(self, obj):
        # reapply the keys to the json object that has been passed back before it written to Fulcrum
        recode(obj, self.dictionaryOfSchemas)

        api_resp = super(DecodedRecords, self).create(obj)
        api_resp = self.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})

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
                if schema.getName() == formIdOrName:
                    return schema

        raise Exception ('no such form')

    def search(self):
        return self.dictionaryOfSchemas

