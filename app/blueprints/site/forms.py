from sanic_wtf import SanicForm
from wtforms import (
    IntegerField, StringField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Length, Email
)


class FormAboutUs(SanicForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=32)],
                         description="local_library")


class FormContactUs(SanicForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=32)], description="local_library")
    phone1 = IntegerField(description="phone")
    phone2 = IntegerField(description="phone")
    email = StringField(validators=[Email()], description="email")