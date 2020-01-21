from wtforms import StringField, IntegerField, DateTimeField, validators, Form, ValidationError
from config import constants


def validateFieldType(form, field):
    if field.data not in constants.fieldTypes:
        raise ValidationError("fieldType must be a value from the following set : {}".format(constants.fieldTypes))


def validateDescription(form, field):
    if not len(field.raw_data):
        raise ValidationError("This field is required.")
    

class CredentialModel(Form):
    id = StringField('id')
    name = StringField('name', [validators.DataRequired(), validators.Length(max=45)])
    projectId = IntegerField('projectId', [validators.DataRequired()])
    createdBy = IntegerField('createdBy')
    version = IntegerField('version')
    createdAt = DateTimeField('createdAt')
    description = StringField('description', [validateDescription])


class FieldModel(Form):
    id = StringField('f_id')
    fieldType = StringField('fieldType', [validators.DataRequired(), validateFieldType])
    label = StringField('label')
    value = StringField('value', [validators.DataRequired()])
    version = IntegerField('version')
    
