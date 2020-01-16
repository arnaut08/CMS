from wtforms import StringField, IntegerField, validators, Form

class AccessModel(Form):
    id = IntegerField('id')
    userId = IntegerField('userId', [validators.DataRequired()])
    canRead = IntegerField('canRead', [validators.any_of([0,1])])
    canWrite = IntegerField('canWrite', [validators.any_of([0,1])])
    description = StringField('description', [validators.Length(min=0, max=100)])
    credentialId = StringField('credentialId')
    projectId = IntegerField('projectId')