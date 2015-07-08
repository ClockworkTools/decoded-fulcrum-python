__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'
__author__ = 'Keith Hannon'
__datecreated__ = '8/07/2015'


from decodedFulcrum.fieldnames import SYSTEM_LEVEL_FIELD_NAMES

class Schema():
    def __init__(self, jsonForm):
        self._jsonForm = jsonForm

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

    def _getJsonElement(self, fieldName):
        applicationFields = self._getAllApplicationFields()
        if fieldName in applicationFields:
            return applicationFields[fieldName]

    def getFieldKeyByName(self, fieldName):
        jsonApplicationField = self._getJsonElement(fieldName)
        if jsonApplicationField:
            return jsonApplicationField['key']

    def getFieldNameByKey(self, fieldKey):
        formFields = self._getAllApplicationFields()

        for fieldName, jsonApplicationField in formFields.items():
            if jsonApplicationField["key"] == fieldKey:
                return fieldName

    def getFieldType(self, fieldName):
        if fieldName in SYSTEM_LEVEL_FIELD_NAMES:
            return 'System'
        else:
            jsonApplicationField = self._getJsonElement(fieldName)

            if jsonApplicationField:
                return jsonApplicationField['type']

    def getTopLevelValueFieldNames(self):
        return SYSTEM_LEVEL_FIELD_NAMES \
               + self._new_getApplicationFields(recurseRepeatables=False
                                                ,includeValueFields=True
                                                ,includeRepeatables=False
                                                ,includeSectionFields=False).keys()

    def _getAllApplicationFields(self):
        # This returns all the KeyedFields in the form
        # A Repeatable is a KeyedField, as well as all the fields defined within it
        # Both a Section and the fields defined within the Section are classed as KeyedFields
        return self._new_getApplicationFields(True, True, True, True)

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



    def getTopLevelRepeatableFieldNames(self):
        return self._new_getApplicationFields(
                recurseRepeatables=False
                ,includeValueFields=False
                ,includeRepeatables=True
                ,includeSectionFields=False)

    def _getApplicationField(self, fieldName):
        if fieldName in self._getAllApplicationFields().keys():
            return self._getAllApplicationFields[fieldName]

    def getValueFieldNamesThatAreChildrenOf(self, repeatableFieldName):
        if self.getFieldType(repeatableFieldName) != 'Repeatable':
            raise Exception('Error in Schema: a non repeatable field name: "{}" was passed to getValueFieldNamesThatAreChildrenOf'.format(repeatableFieldName))

        jsonElement = self._getJsonElement(repeatableFieldName)
        if jsonElement:
            return self._new_getApplicationFields(
                                                recurseRepeatables=False
                                                ,includeValueFields=True
                                               ,includeRepeatables=False
                                               ,includeSectionFields=False
                                               ,json_structure=jsonElement['elements'])

    def getRepeatableFieldNamesThatAreChildrenOfs(self, repeatableFieldName):
        if self.getFieldType(repeatableFieldName) != 'Repeatable':
            raise Exception('Error in Schema: a non repeatable field name: "{}" was passed to getRepeatableFieldNamesThatAreChildrenOf'.format(repeatableFieldName))

        jsonElement = self._getJsonElement(repeatableFieldName)
        if jsonElement:
            return self._new_getApplicationFields(
                                                recurseRepeatables=False
                                               ,includeValueFields=False
                                               ,includeRepeatables=True
                                               ,includeSectionFields=False
                                               ,json_structure=jsonElement['elements'])
