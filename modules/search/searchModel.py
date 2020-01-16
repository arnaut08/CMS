from wtforms import StringField, IntegerField, validators, Form

class SearchEmployeeModel(Form):
    keyword = StringField('keyword', [validators.DataRequired()])
    credentialId = StringField('credentialId')
    projectId = IntegerField('projectId')