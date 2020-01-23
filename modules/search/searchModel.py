from wtforms import StringField, IntegerField, validators, Form

class SearchModel(Form):
    keyword = StringField('keyword', [validators.DataRequired()])
    credentialId = StringField('credentialId')
    projectId = IntegerField('projectId')