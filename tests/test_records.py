__author__ = 'Keith Hannon'
__datecreated__ = '10/07/2015'
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
from decodedFulcrum.api.endpoints import DecodedRecords
from tests import DecodedFulcrumTestCase
from decodedFulcrum import config
import time

class RecordsTest(DecodedFulcrumTestCase):

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

    def testTime(self):
        start = time.time()
        done = time.time()
        elapsed = done - start
        print(elapsed)


