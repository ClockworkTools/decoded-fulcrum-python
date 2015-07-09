__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'
from tests import DecodedFulcrumTestCase
from decodedFulcrum import config


class SchemasTest(DecodedFulcrumTestCase):
    def testFind(self):
        schema = self.fulcrum_api.schemas.find(config.FORM_ID)['form']
        self.assertTrue(schema.getName() == 'Estimate')



