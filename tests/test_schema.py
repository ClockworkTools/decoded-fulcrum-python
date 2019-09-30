__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'

from tests import DecodedFulcrumTestCase
from decodedFulcrum import config
from decodedFulcrum.schema import Schema


class SchemaTest(DecodedFulcrumTestCase):
    def test_getFormId(self):
        #TODO replace the following with a hard coded jsonForm
        form = self.fulcrum_api.forms.find(config.FORM_ID)['form']

        schema = Schema(form)

        self.assertEqual(schema.getFormId(), config.FORM_ID)
        self.assertEqual(schema.getFormName(), 'Estimate')

        key_of_customer_name = schema.getFieldKeyByName('customer_name')
        self.assertIsNotNone(key_of_customer_name)

        self.assertEqual(schema.getFieldNameByKey(key_of_customer_name), 'customer_name')

        self.assertEqual(schema.getFieldType('id'), 'System')
        self.assertEqual(schema.getFieldType('created_at'), 'System')

        self.assertEqual(schema.getFieldType('customer_name'), 'TextField')
        self.assertEqual(schema.getFieldType('contact_phone_numbers'), 'Repeatable')
        self.assertEqual(schema.getFieldType('type_of_phone_number'), 'ChoiceField')

        self.assertTrue('customer_name' in list(schema._getAllApplicationFields().keys()))
        self.assertTrue('contact_phone_numbers' in list(schema._getAllApplicationFields().keys()))
        self.assertTrue('type_of_phone_number' in schema._getAllApplicationFields())

        self.assertTrue('customer_name' in schema.getTopLevelApplicationFieldNames())
        self.assertFalse('contact_phone_numbers' in schema.getTopLevelApplicationFieldNames())
        self.assertFalse('type_of_phone_number' in schema.getTopLevelApplicationFieldNames())

        self.assertFalse('customer_name' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))
        self.assertTrue('type_of_phone_number' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))
        self.assertFalse('contact_phone_numbers' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))


