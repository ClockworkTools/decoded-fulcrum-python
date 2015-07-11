__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'

from tests import DecodedFulcrumTestCase
from decodedFulcrum import config
from decodedFulcrum.schema import Schema


class SchemaTest(DecodedFulcrumTestCase):
    def test_getFormId(self):
        form = self.fulcrum_api.forms.find(config.FORM_ID)['form']
        schema = Schema(form)

        self.assertEquals(schema.getFormId(), config.FORM_ID)
        self.assertEquals(schema.getFormName(), 'Estimate')

        key_of_customer_name = schema.getFieldKeyByName('customer_name')
        self.assertIsNotNone(key_of_customer_name)

        self.assertEquals(schema.getFieldNameByKey(key_of_customer_name), 'customer_name')

        self.assertEquals(schema.getFieldType('id'), 'System')
        self.assertEquals(schema.getFieldType('created_at'), 'System')

        self.assertEquals(schema.getFieldType('customer_name'), 'TextField')
        self.assertEquals(schema.getFieldType('contact_phone_numbers'), 'Repeatable')
        self.assertEquals(schema.getFieldType('type_of_phone_number'), 'ChoiceField')

        self.assertTrue('customer_name' in schema._getAllApplicationFields().keys())
        self.assertTrue('contact_phone_numbers' in schema._getAllApplicationFields().keys())
        self.assertTrue('type_of_phone_number' in schema._getAllApplicationFields())

        self.assertTrue('customer_name' in schema.getTopLevelApplicationFieldNames())
        self.assertFalse('contact_phone_numbers' in schema.getTopLevelApplicationFieldNames())
        self.assertFalse('type_of_phone_number' in schema.getTopLevelApplicationFieldNames())

        self.assertFalse('customer_name' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))
        self.assertTrue('type_of_phone_number' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))
        self.assertFalse('contact_phone_numbers' in schema.getApplicationFieldNamesThatAreChildrenOf('contact_phone_numbers'))

