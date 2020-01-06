from wtforms import StringField, Form, validators

class AuthModel(Form):
    username = StringField('username', [validators.DataRequired()])
    password = StringField('password', [validators.DataRequired()])
