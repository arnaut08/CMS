from wtforms import StringField, IntegerField, DateTimeField, validators, Form

class CredentialModel(Form):
    id = IntegerField('id')
    name = StringField('name', [validators.DataRequired(), validators.Length(max=45)])
    projectId = IntegerField('projectId', [validators.DataRequired()])
    createdBy = IntegerField('createdBy', [validators.DataRequired()])
    version = IntegerField('version')
    createdAt = DateTimeField('createdAt')
    description = StringField('description')