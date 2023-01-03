from wtforms import StringField, PasswordField, validators, SubmitField, DecimalField, IntegerField, SelectField
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField(
        validators=[validators.DataRequired(), validators.InputRequired()])
    password = PasswordField()
    submit = SubmitField(label="Zaloguj")


class UpdateUserInformationForm(FlaskForm):
    name = StringField(
        validators=[validators.InputRequired(),
                    validators.Length(min=3, max=50,
                                      message="Imie musi zawierać od %(min)d do %(max)d znaków."),
                    validators.Regexp(regex="^[a-zA-Z0-9żźćńółęąśŻŹĆĄŚĘŁÓŃ]+$", message="Imię może zaiwerać tylko znaki alfabetu oraz")]
    )
    surname = StringField(
        validators=[validators.Optional(),
                    validators.Length(min=3, max=50,
                                      message="Imie musi zawierać od %(min)d do %(max)d znaków."),
                    validators.Regexp(regex="^[-a-zA-Z0-9żźćńółęąśŻŹĆĄŚĘŁÓŃ]+$", message='Nazwisko może składać się tylko ze znaków alfabetu')]
    )
    phone_number = StringField(
        validators=[validators.Optional(),
                    validators.Length(min=9, max=9,
                                      message="Telefon musi składać się z %(max)d cyfr"),
                    validators.Regexp(regex="([0-9]{9})", message='Podaj 9 cyfrowy numer telefonu bez dodatkowych znaków')]
    )
    save = SubmitField(label="Zapisz")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        validators=[validators.InputRequired()]
    )
    new_password = PasswordField(
        validators=[validators.InputRequired(),
                    validators.Length(min=4, max=20,
                                      message="Hasło musi zawierać od 4 do 20 znaków."),
                    validators.Regexp(regex="^[a-zA-Z0-9!@#$_-]+$",
                                      message='Hasło może składać się tylko ze znaków alfabetu, cyfr oraz znaków !, @, #, $, -, _'),
                    validators.EqualTo(fieldname="repeated_new_password", message="Hasła muszą być identyczne")]
    )
    repeated_new_password = PasswordField(
        validators=[validators.InputRequired()]
    )
    change_password = SubmitField(label="Zmień hasło")


class CatalogueAddForm(FlaskForm):
    measurement_unit_id = SelectField()
    catalogue_type_id = SelectField()
    bulk_pack_id = SelectField()
    producer_id = SelectField()
    stock_code = StringField(validators=[validators.InputRequired()])
    name = StringField(validators=[validators.Optional()],
                       filters=[lambda name: name or None])
    alias = StringField(validators=[validators.Optional()],
                        filters=[lambda alias: alias or None])
    last_purchase_price = DecimalField(
        validators=[validators.Optional()], places=2)
    bulk_pack_capacity = DecimalField(
        validators=[validators.Optional()], places=2)
    no_bulk_pack_on_palette = IntegerField(validators=[validators.Optional()])
    burning_time = DecimalField(validators=[validators.Optional()], places=2)
    height = DecimalField(validators=[validators.Optional()], places=2)
    width = DecimalField(validators=[validators.Optional()], places=2)
    diameter = DecimalField(validators=[validators.Optional()], places=2)
    add_product = SubmitField(label="Dodaj")


class DocumentAddForm(FlaskForm):
    document_type_id = SelectField(coerce=int)
    warehouse_from_id = SelectField(coerce=int)
    warehouse_to_id = SelectField(coerce=int)
    trade_partner_id = SelectField(coerce=int)
    add_document = SubmitField(label="Dodaj")


class DocumentPositionAddForm(FlaskForm):
    catalogue_id = SelectField(coerce=int)
    quantity = DecimalField(places=2)
    price = DecimalField(validators=[validators.Optional()], places=2)
    add_document_position = SubmitField(label="Dodaj pozycję")


class ConfirmCancelDocumentForm(FlaskForm):
    confirm_document = SubmitField(label="Zatwierdź")
    cancel_document = SubmitField(label="Anuluj")
