__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'
from tests import DecodedFulcrumTestCase
from decodedFulcrum import config


class FormsTest(DecodedFulcrumTestCase):
    def testGetForm(self):
        form = self.fulcrum_api.forms.find(config.FORM_ID)['form']
        self.assertTrue(form['id'],config.FORM_ID)

