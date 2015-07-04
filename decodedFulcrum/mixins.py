__author__ = 'Keith Hannon'
__datecreated__ = '04/07/2015'

from fulcrumJsonUtils import decode, recode

class Findable(object):
    def find(self, id):
        api_resp = self.call('get', '{0}/{1}'.format(self.path, id))

        # decode the api response
        decode(api_resp, self.fieldNameLookups)

        return api_resp

class Deleteable(object):
    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))

class Createable(object):
    def create(self, obj):
        # reapply the keys to the json object that has been passed back before it written to Fulcrum
        recode(obj, self.fieldKeyLookups)

        api_resp = self.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})

        return api_resp

class Searchable(object):
    def search(self, url_params=None):
        api_resp = self.call('get', self.path, url_params=url_params)

        # decode the api response
        decode(api_resp, self.fieldNameLookups)

        return api_resp

class Updateable(object):
    def update(self, id, obj):
        # reapply the keys to the json object that has been passed back before it written back to Fulcrum
        recode(obj, self.fieldKeyLookups)

        api_resp = self.call('put', '{0}/{1}'.format(self.path, id), data=obj, extra_headers={'Content-Type': 'application/json'})

        # now decode the api response
        decode(api_resp, self.fieldNameLookups)

        return api_resp



