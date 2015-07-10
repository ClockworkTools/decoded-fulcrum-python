__author__ = 'Keith Hannon'
__datecreated__ = '4/07/2015'
import unittest
from decodedFulcrum import config

from decodedFulcrum import DecodedFulcrum


class DecodedFulcrumTestCase(unittest.TestCase):
    api_root = 'https://api.fulcrumapp.com/api/v2'

    def setUp(self):
        self.fulcrum_api = DecodedFulcrum(key=config.API_KEY)
