__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'
from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from decodedFulcrum.api.endpoints import DecodedRecords
from fulcrumJsonUtils import getFieldLookups


class DecodedFulcrum(Fulcrum):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
        super(DecodedFulcrum, self).__init__(key=key, uri=uri)

        jsonForms = self.forms.search()['forms']   # this is a list of dictionary objects

        # The dictionary fieldNameLookups is keyed by a tuple (form_id, key)
        # The dictionary fieldKeyLookups is keyed by a tuple (form_id, data_name)
        fieldNameLookups, fieldKeyLookups = getFieldLookups(jsonForms)

        api_config = APIConfig(key=key, uri=uri)

        # ensure that when the "records" part of the fulcrum_api is called, the DecodedRecords functionality is invoked
        self.records = DecodedRecords(api_config, fieldNameLookups, fieldKeyLookups)


