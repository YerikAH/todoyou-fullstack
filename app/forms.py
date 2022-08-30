
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Email
#Form 
class LoginForm(FlaskForm):
  fullname = StringField("Full name",validators=[DataRequired()])
  password = PasswordField("Password",validators=[DataRequired()])
  submit = SubmitField('Submit')

class TodoForm(FlaskForm):
  description = StringField("Description",validators=[DataRequired()])
  submit = SubmitField('Create')

class DeleteTodoForm(FlaskForm):
  submiDelete = SubmitField('Remove task')

class UpdateTodoForm(FlaskForm):
  submiUpdate = SubmitField('Update task')