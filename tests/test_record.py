__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'

from decodedFulcrum.api.endpoints import DecodedRecords
from tests import DecodedFulcrumTestCase
from decodedFulcrum import config


class RecordTest(DecodedFulcrumTestCase):
    def testSettings(self):
        print config.API_KEY

    def test_records(self):
        records = self.fulcrum_api.records.search(url_params={'form_id': config.FORM_ID})
        print records

    def testUpdateRecord(self):
        records = self.fulcrum_api.records.search(url_params={'form_id': config.FORM_ID})
        fulcrumRecord = records['records'][0]
        id = fulcrumRecord['id']
        fulcrumRecord['form_values']['customer_name'] = 'xyz'
        api_resp = self.fulcrum_api.records.update(id,fulcrumRecord)
        record = api_resp['record']

        new_customer_name = record['form_values']['customer_name']
        self.assertEquals(new_customer_name, 'xyz')

    def test_forms(self):
        forms = self.fulcrum_api.forms.search()['forms']   # this is a list of dictionary objects

    def textX(self):
        pass
