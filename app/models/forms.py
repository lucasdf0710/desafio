from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ColabForm(FlaskForm):
    colab_id = StringField("colab_id", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    idade = StringField("idade", validators=[DataRequired()])
    cargo = StringField("cargo", validators=[DataRequired()])

class Colab_Form(FlaskForm):
    colab_id = StringField("colab_id", validators=[DataRequired()])
