__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'
from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from decodedFulcrum.api.endpoints import DecodedRecords, Schemas
from fulcrumJsonUtils import getFieldLookups
from decodedFulcrum.schema import Schema
from decodedFulcrum.fieldnames import SYSTEM_LEVEL_FIELD_NAMES


class DecodedFulcrum(Fulcrum):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
        super(DecodedFulcrum, self).__init__(key=key, uri=uri)

        jsonForms = self.forms.search()['forms']   # this is a list of dictionary objects

        # The dictionary fieldNameLookups is keyed by a tuple (form_id, key)
        # The dictionary fieldKeyLookups is keyed by a tuple (form_id, data_name)
        fieldNameLookups, fieldKeyLookups = getFieldLookups(jsonForms)

        api_config = APIConfig(key=key, uri=uri)

        dictionaryOfSchemas = self._getSchemas()

        # ensure that when the "records" part of the fulcrum_api is called, the DecodedRecords functionality is invoked
        self.records = DecodedRecords(api_config, dictionaryOfSchemas, fieldNameLookups, fieldKeyLookups)
        self.schemas = Schemas(dictionaryOfSchemas)

    def _getSchemas(self):
        # return a dictionry of schemas keyed by formId
        schemas = {}
        jsonForms = self.forms.search()['forms']   # this is a list of dictionary objects
        for jsonForm in jsonForms:
            schema = Schema(jsonForm)
            formId = schema.getFormId()
            schemas[formId] = schema

        return schemas


