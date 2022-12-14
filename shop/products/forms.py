from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed


class Addproducts(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])

    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg','webp'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg','webp'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg','webp'])])

