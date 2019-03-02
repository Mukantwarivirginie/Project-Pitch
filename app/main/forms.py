
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required
from wtforms import ValidationError




class CommentForm(FlaskForm):

    title = StringField(' title',validators=[Required()])
    comment= TextAreaField(' review', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')   


class PitchForm(FlaskForm):
    
    pitch = TextAreaField(' pitch', validators=[Required()])
    submit = SubmitField('Submit')
