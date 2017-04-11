__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'
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


from decodedFulcrum.fieldnames import SYSTEM_LEVEL_FIELD_NAMES, CHILD_LEVEL_FIELD_NAMES

class Schema(object):
    def __init__(self, jsonForm):
        self._jsonForm = jsonForm
        #the following dictionaries are populated on demand
        self._applicationFieldsKeyedByFieldName = None
        self._applicationFieldsKeyedByKey = None

    def getFormId(self):
        return self._jsonForm['id']

    def getFormName(self):
        return self._jsonForm['name']

    def getFormDescription(self):
        description = self._jsonForm['description']
        if description == None:
            return ''
        else:
            return description

    def _getJsonElementByFieldName(self, fieldName):
        applicationFields = self._getAllApplicationFields()
        if fieldName in applicationFields:
            return applicationFields[fieldName]

    def _getJsonElementByFieldKey(self, searchKey):
        if self._applicationFieldsKeyedByKey == None:
            self._applicationFieldsKeyedByKey = {}
            applicationFieldsKeyedByName = self._getAllApplicationFields()
            for fieldName, jsonElement in applicationFieldsKeyedByName.items():
                key = jsonElement['key']
                if key is None:
                    pass
                self._applicationFieldsKeyedByKey[key] = jsonElement

        # A json file may contain a key which is not present in the form. If this is the case return None
        # This can happen because either:
        #   1) a field has been deleted from the form, and a device which whad not been synchronized with the latest change
        #      submits a record including the value
        #   2) the field has been added since the schema was cached

        if searchKey in self._applicationFieldsKeyedByKey:
            return self._applicationFieldsKeyedByKey[searchKey]

    def getFieldKeyByName(self, fieldName):
        jsonApplicationField = self._getJsonElementByFieldName(fieldName)
        if jsonApplicationField:
            return jsonApplicationField['key']

    def getFieldNameByKey(self, fieldKey):
        jsonElement = self._getJsonElementByFieldKey(fieldKey)

        # if the schema does not contain this key, return None
        if jsonElement:
            return jsonElement['data_name']

    def getFieldType(self, fieldName):
        if fieldName in SYSTEM_LEVEL_FIELD_NAMES or fieldName in CHILD_LEVEL_FIELD_NAMES:
            return 'System'
        else:
            jsonApplicationField = self._getJsonElementByFieldName(fieldName)

            if jsonApplicationField:
                return jsonApplicationField['type']

    def getChoiceListIdForField(self, fieldName):
        fieldType = self.getFieldType(fieldName)
        if fieldType is None:
            return None

        if fieldType != 'ChoiceField':
            return None

        jsonApplicationField = self._getJsonElementByFieldName(fieldName)

        if 'choice_list_id' in jsonApplicationField:
            return jsonApplicationField['choice_list_id']

    def getChoiceFieldSpecifiedLookupValues (self, fieldName):
        """

        :param fieldName: string
        :return: a dictionary of key - value pairs
        """

        fieldType = self.getFieldType(fieldName)
        if fieldType != 'ChoiceField':
            return None

        jsonApplicationField = self._getJsonElementByFieldName(fieldName)
        if 'choices' not in  jsonApplicationField:
            return None

        dictionaryOfSpecifiedLookupValues = {}
        for item in jsonApplicationField['choices']:
            itemKey = item['value']
            itemName = item['label']
            dictionaryOfSpecifiedLookupValues[itemKey] = itemName

        return dictionaryOfSpecifiedLookupValues


    def _getAllApplicationFields(self):
        # This returns all the KeyedFields in the form
        # A Repeatable is a KeyedField, as well as all the fields defined within it
        # Both a Section and the fields defined within the Section are classed as KeyedFields
        if self._applicationFieldsKeyedByFieldName == None:
            self._applicationFieldsKeyedByFieldName = self._new_getApplicationFields(True, True, True, True)

        return self._applicationFieldsKeyedByFieldName

    def _new_getApplicationFields(self
                                  , recurseRepeatables
                                  , includeValueFields
                                  , includeRepeatables
                                  , includeSectionFields
                                  , json_structure=None
                                  ):
        # If no json structure is passed, the top level of the form is assumed
        # If passed, this should be a JSON structure mapping to an 'elements' section of a record in Fulcrum

        # A section is classed as an Application Field, as well as all the fields within it, which
        # are at the same level as the sections container
        if json_structure == None:
            json_structure = self._jsonForm['elements']

        applicationFields = {}
        for jsonElement in json_structure:
            fieldName = jsonElement['data_name']
            type = jsonElement['type']

            if (not includeRepeatables and type == 'Repeatable')\
                or (not includeSectionFields and type == 'Section'):
                # do not return this field
                pass
            else:
                if (not includeValueFields) \
                        and type != 'Repeatable'\
                        and type != 'Section':
                    pass
                else:
                    applicationFields[fieldName] = jsonElement

            if jsonElement['type'] == 'Section'\
                    or (recurseRepeatables and jsonElement['type'] == 'Repeatable'):
                # always recurse section fields - the fields belonging to a section are recorded in the fulcrum record
                # at the same level as the fields in the section's container
                nestedFields = self._new_getApplicationFields(recurseRepeatables = recurseRepeatables
                                                              , includeValueFields = includeValueFields
                                                              , includeRepeatables = includeRepeatables
                                                              , includeSectionFields = includeSectionFields
                                                              , json_structure = jsonElement['elements']
                                                              )
                applicationFields.update(nestedFields)

        return applicationFields

    def getTopLevelApplicationFieldNames(self):
        return self._new_getApplicationFields(recurseRepeatables=False
                                                ,includeValueFields=True
                                                ,includeRepeatables=False
                                                ,includeSectionFields=True).keys()
    def getTopLevelRepeatableFieldNames(self):
        return self._new_getApplicationFields(
                recurseRepeatables=False
                ,includeValueFields=False
                ,includeRepeatables=True
                ,includeSectionFields=False).keys()


    def _getApplicationField(self, fieldName):
        if fieldName in self._getAllApplicationFields().keys():
            return self._getAllApplicationFields()[fieldName]

    def getApplicationFieldNamesThatAreChildrenOf(self, repeatableOrSectionFieldName):
        if self.getFieldType(repeatableOrSectionFieldName) not in ('Repeatable', 'Section'):
            raise Exception('Error in Schema: a field name that is not a repeatable or section: "{}" was passed to getApplicationFieldNamesThatAreChildrenOf'.format(repeatableOrSectionFieldName))

        jsonElement = self._getJsonElementByFieldName(repeatableOrSectionFieldName)

        if jsonElement:
            return self._new_getApplicationFields(
                      recurseRepeatables=False
                      ,includeValueFields=True
                      ,includeRepeatables=False
                      ,includeSectionFields=False
                      ,json_structure=jsonElement['elements']).keys()

    def flushForm(self, jsonForm):
        # This is used when it is possible the schema has changed, and is invoked from the Fulcrum Account
        self._schema = jsonForm

    def getFormIdOfRecordLinkField(self, fieldName):
       if self.getFieldType(fieldName) != 'RecordLinkField':
            raise Exception('getFormIdOfRecordLinkField was passed a field that is not a record link field')

       recordLinkField = self._getApplicationField(fieldName)
       formId = recordLinkField['form_id']
       return formId

    def getAllowMultipleRecordSettingOfRecordLinkField(self, fieldName):
       if self.getFieldType(fieldName) != 'RecordLinkField':
            raise Exception('getAllowMultipleRecordSettingOfRecordLinkField was passed a field that is not a record link field')

       recordLinkField = self._getApplicationField(fieldName)
       allowMultipleRecords =  recordLinkField['allow_multiple_records']
       return allowMultipleRecords

    def getDisabledSettingOfRecordLinkField(self, fieldName):
       if self.getFieldType(fieldName) != 'RecordLinkField':
            raise Exception('getReadOnlySettingOfRecordLinkField was passed a field that is not a record link field')

       recordLinkField = self._getApplicationField(fieldName)
       disabledSetting =  recordLinkField['disabled']
       return disabledSetting


    def getAutopopulatedFieldSourcesForRecordLinkField(self, recordLinkFieldName, otherSchema):
        #other schema is required in order to retrieve the source field name

        #returns a dictionary of field sources keyed by field name
        # i.e. the key is the field name in this schema
        # the  value is the field name in the other schema
        autopopulatedFieldSources = {}
        if self.getFieldType(recordLinkFieldName) != 'RecordLinkField':
            raise Exception('getAutopopulatedFieldSoucesForRecordLinkField was passed a field that is not a record link field')

        recordLinkField = self._getApplicationField(recordLinkFieldName)
        for listItem in recordLinkField['record_defaults']:
            destFieldKey = listItem['destination_field_key']
            sourceFieldKey = listItem['source_field_key']

            destFieldName = self.getFieldNameByKey(destFieldKey)
            sourceFieldName = otherSchema.getFieldNameByKey(sourceFieldKey)

            autopopulatedFieldSources[destFieldName] = sourceFieldName

        return autopopulatedFieldSources
