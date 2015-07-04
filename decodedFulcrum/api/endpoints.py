__author__ = 'Keith Hannon'
from decodedFulcrum.mixins import Findable, Deleteable, Createable, Searchable, Updateable
from fulcrum.api import BaseAPI

class DecodedRecords(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'records'
    def __init__(self, api_config, fieldNameLookups, fieldKeyLookups):
        super(DecodedRecords, self).__init__(api_config)

        self.fieldNameLookups = fieldNameLookups
        self.fieldKeyLookups = fieldKeyLookups

    def history(self, id):
        api_resp = api_resp = self.call('get', '{0}/{1}/history'.format(self.path, id))
        return api_resp



