from wtforms import StringField, PasswordField, validators, SubmitField, DecimalField, IntegerField, SelectField, EmailField
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
                                      message="Nazwisko musi zawierać od %(min)d do %(max)d znaków."),
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
    edition_id = SelectField()
    language_id = SelectField()
    platform_id = SelectField()
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
    add_product = SubmitField(label="Dodaj")


class DocumentAddForm(FlaskForm):
    document_type_id = SelectField(coerce=int)
    warehouse_from_id = SelectField(coerce=int)
    # warehouse_to_id = SelectField(coerce=int)
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


class TradePartnerAddForm(FlaskForm):
    name = StringField(validators=[validators.Length(min=3, max=50,
                                                     message="Nazwa musi zawierać od %(min)d do %(max)d znaków.")])
    email_address = EmailField(validators=[validators.Regexp(regex="([a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", message="Podaj poprawny adres email.")],
                               filters=[lambda alias: alias or None])
    phone_number = StringField(
        validators=[validators.Optional(),
                    validators.Length(min=9, max=9,
                                      message="Telefon musi składać się z %(max)d cyfr"),
                    validators.Regexp(regex="([0-9]{9})", message='Podaj 9 cyfrowy numer telefonu bez dodatkowych znaków')])
    street = StringField(validators=[validators.Length(min=3, max=50,
                                                       message="Ulica musi zawierać od %(min)d do %(max)d znaków.")],
                         filters=[lambda alias: alias or None])
    street_number = StringField(validators=[validators.Length(min=1, max=50,
                                                              message="Numer ulicy / domu musi zawierać od %(min)d do %(max)d znaków.")],
                                filters=[lambda alias: alias or None])
    city = StringField(validators=[validators.Optional()],
                       filters=[lambda name: name or None])
    post_code = StringField(validators=[validators.Optional(),
                                        validators.Regexp(regex="([0-9]{2}-[0-9]{3})", message='Podaj kod pocztowy w postaci XX-XXX.')],
                            filters=[lambda name: name or None])
    nip = StringField(
        validators=[validators.Optional(),
                    validators.Length(min=10, max=10,
                                      message="NIP musi składać się z %(max)d cyfr"),
                    validators.Regexp(regex="([0-9]{9})", message='Podaj 10 cyfrowy numer NIP bez dodatkowych znaków')])
    regon = StringField(
        validators=[validators.Optional(),
                    validators.Length(min=9, max=14,
                                      message="REGON musi składać się z %(min)d lub %(max)d cyfr"),
                    validators.Regexp(regex="(^([0-9]{10}|[0-9]{14})$)", message='Podaj 9 lub 14 cyfrowy numer REGON bez dodatkowych znaków')])
    add_trade_partner = SubmitField(label="Dodaj")
