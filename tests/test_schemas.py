__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'
from tests import DecodedFulcrumTestCase
from decodedFulcrum import config


class SchemasTest(DecodedFulcrumTestCase):
    def testFind(self):
        schema = self.fulcrum_api.schemas.find(config.FORM_ID)
        self.assertTrue(schema.getFormName() == 'Estimate')

    def testSearch(self):
        schemas = self.fulcrum_api.schemas.search()
        self.assertTrue(schemas[config.FORM_ID]) == 'Estiamte'





