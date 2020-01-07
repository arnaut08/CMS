from wtforms import StringField, IntegerField, validators, Form

class AccessModel(Form):
    id = IntegerField('id')
    userId = IntegerField('userId', [validators.DataRequired()])
    canRead = IntegerField('canRead', [validators.InputRequired()])
    canWrite = IntegerField('canWrite', [validators.InputRequired()])
    description = StringField('description')
    credentialId = StringField('credentialId')
    projectId = IntegerField('projectId')