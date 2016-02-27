from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    
    
class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()], widget=TextArea())    
    
    
class AnswerForm(Form):
    body = StringField('body', validators=[DataRequired()], widget=TextArea())