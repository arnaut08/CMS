from wtforms import StringField, IntegerField, DateTimeField, validators, Form
from config import constants


def validateFieldType(form, field):
    if constants.fieldTypes.index(field.data) == -1:
        raise ValidationError("fieldType must be a value from the following set : {}".format(constants.fieldTypes))


class CredentialModel(Form):
    id = StringField('id')
    name = StringField('name', [validators.DataRequired(), validators.Length(max=45)])
    projectId = IntegerField('projectId', [validators.DataRequired()])
    createdBy = IntegerField('createdBy', [validators.DataRequired()])
    version = IntegerField('version')
    createdAt = DateTimeField('createdAt')
    description = StringField('description')


class FieldModel(Form):
    id = StringField('id')
    credentialId = StringField('credentialId')
    fieldType = StringField('fieldType', [validators.DataRequired(), validateFieldType])
    label = StringField('label')
    value = StringField('value', [validators.DataRequired()])
    version = IntegerField('version')
    
