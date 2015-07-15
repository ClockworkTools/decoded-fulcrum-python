__author__ = 'Keith Hannon'
__datecreated__ = '5/07/2015'

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


def getFieldLookups(jsonForms):
    fieldNameLookups = {}
    fieldKeyLookups = {}

    for jsonForm in jsonForms:
        form_id = jsonForm['id']
        applicationFieldNames = getApplicationFieldNames(jsonForm['elements'])

        for key, data_name in  applicationFieldNames.items():
            lookupKey = (form_id, key)
            fieldNameLookups[lookupKey] = data_name

            lookupKey = (form_id, data_name)
            fieldKeyLookups[lookupKey] = key

    return fieldNameLookups, fieldKeyLookups

def getApplicationFieldNames(jsonElements):
    applicationFieldNames = {}
    for jsonElement in jsonElements:
        data_name = jsonElement['data_name']
        key = jsonElement['key']
        fieldType = jsonElement['type']

        applicationFieldNames[key] = data_name
        if fieldType in ('Section', 'Repeatable'):
            nested_application_field_names = getApplicationFieldNames(jsonElement['elements'])
            applicationFieldNames.update(nested_application_field_names)

    return applicationFieldNames


def decode(json, dictionaryOfSchemas):
    if 'records' in json:
        for record in json['records']:
            form_id = record['form_id']
            schema = dictionaryOfSchemas[form_id]
            _decode(record['form_values'], schema)
    elif 'record' in json:
        form_id = json['record']['form_id']
        schema = dictionaryOfSchemas[form_id]
        _decode(json['record']['form_values'], schema)
    elif 'form_values' in json:
        form_id = json['form_id']
        schema = dictionaryOfSchemas[form_id]
        _decode(json['form_values'], schema)
    else:
        raise Exception('its not working')

def _decode(jsonFormValuesField, schema):
    # jsonFormValuesField, is a dictionary item of a fulcrum record or child record with the key 'form_values'

    # Note that a jsonFormValuesField is not the same as a jsonFieldValue, but is either:
    #       a dictionary item in a jsonFieldValue with the key 'form_values'; or
    #       a dictionary item in a Fulcrum Json Record with the key 'form_values'

    #TODO abstract a json record and json child record, into a common class to deal with situations such as this

    # Build up the form fields with the field codes replaced by the field names

    # documentation indicates that using dict.items() instead of d.iterItems() means it should
    # be safe to delete or modify items in the dictionary while iterating over it
    for fieldCode, fieldValue in jsonFormValuesField.items():
        # add a copy of the field with the fieldName instead of the fieldCode
        fieldName = schema.getFieldNameByKey(fieldCode)
        jsonFormValuesField[fieldName]=fieldValue

        # delete the original field
        del jsonFormValuesField[fieldCode]

        # process any children of the added field
        fieldType = schema.getFieldType(fieldName)

        if fieldType == 'Repeatable':
            # fieldValue is a list of child records
            for childRecord in fieldValue:
                _decode(childRecord['form_values'], schema)

def recode(fulcrumJsonRecord, dictionaryOfSchemas):
    if 'form_values' not in fulcrumJsonRecord:
        raise Exception('its gone wrong on recode')

    form_id = fulcrumJsonRecord['form_id']
    schema = dictionaryOfSchemas[form_id]
    _recode(fulcrumJsonRecord['form_values'], schema)

def _recode(jsonFormValuesField, schema):
    # jsonFormValuesField, is a dictionary item of a fulcrum record or child record with the key 'form_values'

    # Note that a jsonFormValuesField is not the same as a jsonFieldValue, bu tis either:
    #       a dictionary item in a jsonFieldValue with the key 'form_values'; or
    #       a dictionary item in a Fulcrum Json Record with the key 'form_values'

    # Build up the form fields with the field names replaced by the field codes
    for fieldName, fieldValue in jsonFormValuesField.items():
        # add a copy of the field with the fieldName instead of the fieldCode
        key = schema.getFieldKeyByName(fieldName)
        jsonFormValuesField[key]=fieldValue

        # delete the original field
        del jsonFormValuesField[fieldName]

        # process any children of the added field
        if isinstance(fieldValue, list):

            # fieldValue is a list of child records
            for childRecord in fieldValue:
                _recode(childRecord['form_values'], schema)

    return jsonFormValuesField
