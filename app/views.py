from typing import Dict, List
from unicodedata import decimal
from flask import redirect, render_template, request, session, url_for, Response
from flask.views import MethodView
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from . import db
from . import login_manager, bcrypt
from .models import AppUser, Catalogue, CatalogueType, BulkPackType, Producer, MeasurementUnit, Document, DocumentType, Warehouse, TradePartner, DocumentNumberParts, Edition, Language, Platform
from .forms import LoginForm, UpdateUserInformationForm, ChangePasswordForm, CatalogueAddForm, DocumentAddForm, DocumentPositionAddForm, ConfirmCancelDocumentForm, TradePartnerAddForm
from .serializers import CatalogueSchema, DocumentSchema, ItemSchema, DocumentNumberPartsSchema, TradePartnerSchema
from .error_message import MessageLevel, Message

catalogue_schema = CatalogueSchema()
document_schema = DocumentSchema()
document_numbers_parts_schema = DocumentNumberPartsSchema()
items_schema = ItemSchema(many=True)
trade_partner_schema = TradePartnerSchema()


@login_manager.user_loader
def load_user(user_id) -> AppUser:
    return AppUser.query.get(int(user_id))


class LoginView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "login-bulma.html"

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard_view"))
        form = LoginForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = LoginForm(request.form)
        user_email = form.email.data
        user_password = form.password.data
        app_user = AppUser.query.filter_by(email_address=user_email).first()

        if not app_user:
            Message.flash_message(f"Użytkownik z  podanym adresem: {user_email} e-mail nie istnieje.",
                                  MessageLevel.WARNING)
            return redirect(url_for("login_view"))

        if bcrypt.check_password_hash(app_user.password, user_password):
            login_user(app_user)
            next_url = request.args.to_dict().get('next')

            if next_url:
                return redirect(next_url)
            return redirect(url_for("dashboard_view"))

        Message.flash_message("Wprowadzono nieprawidłowe hasło",
                              MessageLevel.WARNING)
        return redirect(url_for("login_view"))


class LogoutView(MethodView):
    """
    Allows the user to log out.
    """

    def get(self) -> Response:
        """
        Redirects logged out user to login site.
        """
        logout_user()
        Message.flash_message("Zostałeś poprawnie wylogowany",
                              MessageLevel.SUCCESS)

        return redirect(url_for("login_view"))


class DashboardView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "dashboard.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next)=' + request.path)

    @login_required
    def get(self):
        return render_template(self.template_name, current_user=current_user)


class CatalogueView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "catalogue.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __set_select_field_choices(self, form: CatalogueAddForm) -> None:
        measurement_units = MeasurementUnit.query.all()
        catalogue_types = CatalogueType.query.all()
        bulk_packs = BulkPackType.query.all()
        producers = Producer.query.all()
        editions = Edition.query.all()
        languages = Language.query.all()
        platforms = Platform.query.all()

        form.measurement_unit_id.choices = [
            (measurement_unit.id, measurement_unit.name) for measurement_unit in measurement_units
        ]
        form.catalogue_type_id.choices = [
            (catalogue_type.id, catalogue_type.name) for catalogue_type in catalogue_types
        ]
        form.bulk_pack_id.choices = [
            (bulk_pack.id, bulk_pack.name) for bulk_pack in bulk_packs
        ]
        form.producer_id.choices = [
            (producer.id, producer.name) for producer in producers
        ]
        form.edition_id.choices = [
            (edition.id, edition.name) for edition in editions
        ]
        form.language_id.choices = [
            (language.id, language.code_two_char) for language in languages
        ]
        form.platform_id.choices = [
            (platform.id, platform.name) for platform in platforms
        ]

    def __get_catalogue_data(self) -> List[tuple]:
        return db.session.query(Catalogue, CatalogueType, BulkPackType, Producer, MeasurementUnit, Edition, Language, Platform) \
            .join(CatalogueType, CatalogueType.id == Catalogue.catalogue_type_id) \
            .join(BulkPackType, BulkPackType.id == Catalogue.bulk_pack_id) \
            .join(Producer, Producer.id == Catalogue.producer_id) \
            .join(MeasurementUnit, MeasurementUnit.id == Catalogue.measurement_unit_id) \
            .join(Edition, Edition.id == Catalogue.edition_id) \
            .join(Language, Language.id == Catalogue.language_id) \
            .join(Platform, Platform.id == Catalogue.platform_id) \
            .all()

    def __remove_unnecessary_entries(self, form_data: CatalogueAddForm, entries: List[str]) -> Catalogue:
        for entry in entries:
            form_data.pop(entry, None)

        return catalogue_schema.make_catalogue(form_data)

    @login_required
    def get(self):
        catalogue_add_form = CatalogueAddForm()
        self.__set_select_field_choices(catalogue_add_form)
        catalogue = self.__get_catalogue_data()

        print(type(catalogue[0][0].name), flush=True)

        return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)

    def post(self):
        catalogue_add_form = CatalogueAddForm(request.form)
        self.__set_select_field_choices(catalogue_add_form)

        if catalogue_add_form.validate_on_submit():
            catalogue_to_add = self.__remove_unnecessary_entries(
                catalogue_add_form.data, ['add_product', 'csrf_token'])

            db.session.add(catalogue_to_add)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                Message.flash_message(f'Istnieje już produkt o symbolu "{catalogue_add_form.stock_code.data}"',
                                      MessageLevel.WARNING)
                catalogue = self.__get_catalogue_data()
                return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)

            Message.flash_message("Produkt został pomyślnie dodany",
                                  MessageLevel.SUCCESS)
        else:
            error_message = Message.get_err_message(
                catalogue_add_form.errors.values())
            Message.flash_message(f'{error_message}', MessageLevel.WARNING)

        catalogue = self.__get_catalogue_data()
        return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)


# class DeleteProductFromCatalogueView(MethodView):
#     methods = ["POST"]

#     def post(self, id_product: int):
#         # print(id_product, flush=True)
#         catalogue_product_to_del = Catalogue.query.filter_by(id=id_product)
#         catalogue_product_to_del.delete()
#         db.session.commit()

#         return redirect("/katalog")


class ProfileView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "profile.html"

    @ login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __update_user(self, user, data_form):
        user.name = data_form.name.data
        user.surname = data_form.surname.data
        user.phone_number = data_form.phone_number.data

        db.session.commit()
        Message.flash_message(
            "Dane zaktualizowane-data", MessageLevel.SUCCESS)

    def __update_password(self, password_form):
        if bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            user = AppUser.query \
                .filter_by(email_address=current_user.email_address) \
                .first()
            user.password = bcrypt.generate_password_hash(
                password_form.new_password.data)
            db.session.commit()
            Message.flash_message(
                "Hasło zostało zmienione-password", MessageLevel.SUCCESS)
        else:
            Message.flash_message(
                "Podaj poprawne aktualne hasło-password", MessageLevel.WARNING)

    @ login_required
    def get(self):
        data_form = UpdateUserInformationForm()
        password_form = ChangePasswordForm()
        return render_template(self.template_name, current_user=current_user, data_form=data_form, password_form=password_form)

    def post(self):
        data_form = UpdateUserInformationForm(request.form)
        password_form = ChangePasswordForm(request.form)

        if data_form.validate_on_submit():
            user_to_update = AppUser.query \
                .filter_by(email_address=current_user.email_address) \
                .first()
            self.__update_user(user_to_update, data_form)
        elif data_form.save.data:
            error_message = Message.get_err_message(data_form.errors.values())
            Message.flash_message(f'{error_message}-data',
                                  MessageLevel.WARNING)

        if password_form.validate_on_submit():
            self.__update_password(password_form)
        elif password_form.change_password.data:
            error_message = Message \
                .get_err_message(password_form.errors.values())
            Message.flash_message(f'{error_message}-password',
                                  MessageLevel.WARNING)

        return render_template(self.template_name, current_user=current_user, data_form=data_form, password_form=password_form)


class DocumentsView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "document.html"

    @ login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __set_select_field_choices(self, form: DocumentAddForm) -> None:
        document_types = DocumentType.query.all()
        warehouses = Warehouse.query.all()
        trade_partners = TradePartner.query.all()

        form.document_type_id.choices = [
            (document_type.id, document_type.name) for document_type in document_types
        ]
        form.warehouse_from_id.choices = [
            (warehouse.id, warehouse.name) for warehouse in warehouses
        ]
        # form.warehouse_to_id.choices = [
        #     (warehouse.id, warehouse.name) for warehouse in warehouses
        # ]
        form.trade_partner_id.choices = [
            (trade_partner.id, trade_partner.name) for trade_partner in trade_partners
        ]

    def __prepare_document_info(self, form: DocumentAddForm) -> dict:
        document_dict = {}

        for field_name, field_details in form._fields.items():
            if field_name not in ['add_document', 'csrf_token']:
                selected_choice = dict(form.data).get(field_name)
                selected_choice_label = dict(
                    field_details.choices).get(selected_choice)
                document_dict[field_name] = {
                    'id': selected_choice,
                    'label': selected_choice_label
                }

        return document_dict

    @ login_required
    def get(self):
        document_add_form = DocumentAddForm()
        self.__set_select_field_choices(document_add_form)
        documents = Document.query.all()

        return render_template(self.template_name, documents=documents, document_add_form=document_add_form)

    def post(self):
        document_add_form = DocumentAddForm(request.form)
        self.__set_select_field_choices(document_add_form)

        if document_add_form.validate_on_submit():
            document = self.__prepare_document_info(document_add_form)
            session['document'] = document

            return redirect(url_for('add_document_position_view'))
        else:
            print('document add  error', flush=True)
            documents = Document.query.all()

            return render_template(self.template_name, current_user=current_user, documents=documents,
                                   document_add_form=document_add_form)


class AddDocumentPositionView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "add_position.html"

    def __set_select_field_choices(self, form: DocumentPositionAddForm) -> None:
        catalogues = Catalogue.query.all()

        form.catalogue_id.choices = [
            (catalogue.id, catalogue.stock_code) for catalogue in catalogues
        ]

    @ login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __prepare_position_info(self, form: DocumentPositionAddForm, positions: List) -> None:
        position_dict = {}

        for field_name, field_details in form._fields.items():
            if field_name not in ['add_document_position', 'csrf_token']:
                selected = dict(form.data).get(field_name)
                if field_details.type == 'SelectField':
                    selected_label = dict(field_details.choices).get(selected)
                    position_dict[field_name] = {
                        'id': selected,
                        'label': selected_label
                    }
                else:
                    selected_label = field_details.name
                    position_dict[field_name] = {
                        'value': selected,
                        'label': selected_label
                    }

        positions.append(position_dict)

    def __clear_session(self, *variables) -> None:
        for variable in variables:
            session.pop(variable, None)

    def __update_document_number(self, data: DocumentNumberParts, field) -> None:
        data.field += 1
        db.session.flush()

    def __create_document_number(self) -> str:
        last_document_num_parts = DocumentNumberParts.query.filter(
            DocumentNumberParts.warehouse_id == session["document"]["warehouse_from_id"]["id"],
            extract("month", DocumentNumberParts.document_date) == datetime.now().month).first()

        warehouse = Warehouse.query.filter_by(
            id=session["document"]["warehouse_from_id"]["id"]).first()

        next_document_number = f"{1:02d}"
        print(warehouse, flush=True)
        warehouse_code = warehouse.code
        month = f"{datetime.now().month:02d}"
        year = datetime.now().year

        if last_document_num_parts is not None:
            next_document_number = f"{last_document_num_parts.last_document_number+1:02d}"
            last_document_num_parts.last_document_number += 1
            db.session.flush()
        else:
            data = {
                "warehouse_id": session["document"]["warehouse_from_id"]["id"],
                "last_document_number": 1
            }

            document_numbers_parts = document_numbers_parts_schema.make_document_numers_parts(
                data)
            db.session.add(document_numbers_parts)
            db.session.flush()

        new_document_number = f"{next_document_number}/{warehouse_code}/{month}/{year}"
        return new_document_number

    def __prepare_document_data(self) -> Dict:
        document_data = {
            "app_user_id": current_user.id,
            "number": self.__create_document_number(),
            "date_added": None,
            "modification_date": None,
            "total": None
        }

        for key, value in session["document"].items():
            document_data[key] = value["id"]

        return document_data

    def __add_document_to_db(self, document_data: Dict) -> int:
        document_model = document_schema.make_document(document_data)
        db.session.add(document_model)
        db.session.flush()

        return document_model.id

    def __prepare_positions_data(self, document_id: int) -> List:
        positions = []

        for pos in session["positions"]:
            position = {
                "document_id": document_id
            }
            for key, value in pos.items():
                if value.get("id"):
                    position[key] = value["id"]
                else:
                    position[key] = float(value["value"])
            position["amount"] = \
                float(position["quantity"]) * float(position["price"])
            print(position, flush=True)
            positions.append(position)

        return positions

    def __add_positions_to_db(self, test: List) -> None:
        # positions_model = items_schema.make_item(positions)
        # positions = {
        #     "positions": test
        # }
        positions_model = items_schema.load(test, many=True)
        print(positions_model, flush=True)
        for pos in positions_model:
            db.session.add(pos)
        db.session.flush()

    @ login_required
    def get(self):
        if 'document' not in session:
            return redirect(url_for("documents_view"))

        document_position_add_form = DocumentPositionAddForm()
        confirm_cancel_document_form = ConfirmCancelDocumentForm()
        self.__set_select_field_choices(document_position_add_form)

        # print(session.get('document'), flush=True)
        # print(session.get('positions'), flush=True)

        return render_template(self.template_name, document_position_add_form=document_position_add_form,
                               confirm_cancel_document_form=confirm_cancel_document_form, session=session)

    def post(self):
        document_position_add_form = DocumentPositionAddForm(request.form)
        confirm_cancel_document_form = ConfirmCancelDocumentForm(request.form)
        self.__set_select_field_choices(document_position_add_form)
        positions = []

        if document_position_add_form.validate_on_submit():
            if 'positions' not in session:
                self.__prepare_position_info(
                    document_position_add_form, positions)
                session['positions'] = positions
            else:
                positions = session['positions']
                self.__prepare_position_info(
                    document_position_add_form, positions)
                session['positions'] = positions
        elif document_position_add_form.add_document_position.data:  # refaktor ifow
            # error_message = Message.get_err_message(
            #     document_position_add_form.errors.values())
            # Message.flash_message(f'{error_message}', MessageLevel.WARNING)
            print('INVALID POSITION FORM', flush=True)

        if confirm_cancel_document_form.confirm_document.data:
            if 'positions' not in session:
                Message.flash_message(f"Brak pozycji, nie można dodać dokumentu.",
                                      MessageLevel.WARNING)
                return redirect(url_for("add_document_position_view"))
            db.session.rollback()

            document_data = self.__prepare_document_data()
            new_document_id = self.__add_document_to_db(document_data)

            positions_data = self.__prepare_positions_data(new_document_id)
            print(positions_data, flush=True)
            self.__add_positions_to_db(test=positions_data)
            db.session.commit()
            self.__clear_session('document', 'positions')
            return redirect(url_for('documents_view'))
        elif confirm_cancel_document_form.cancel_document.data:
            self.__clear_session('document', 'positions')
            return redirect(url_for('documents_view'))

        return render_template(self.template_name, document_position_add_form=document_position_add_form,
                               confirm_cancel_document_form=confirm_cancel_document_form, session=session)


class DocumentView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "document_view.html"

    @ login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    @ login_required
    def get(self, document_id: int):

        document = Document.query.get(document_id)

        return render_template(self.template_name, document=document)


class TradePartnerView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "trade-partner.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __get_trade_partner_data(self) -> List[tuple]:
        return TradePartner.query.all()

    def __remove_unnecessary_entries(self, form_data: TradePartnerAddForm, entries: List[str]) -> TradePartner:
        for entry in entries:
            form_data.pop(entry, None)

        return trade_partner_schema.make_trade_partner(form_data)

    @login_required
    def get(self):
        trade_partner_add_form = TradePartnerAddForm()
        trade_partners = self.__get_trade_partner_data()

        return render_template(self.template_name, current_user=current_user, trade_partners=trade_partners, trade_partner_add_form=trade_partner_add_form)

    def post(self):
        trade_partner_add_form = TradePartnerAddForm(request.form)

        if trade_partner_add_form.validate_on_submit():
            trade_partner_to_add = self.__remove_unnecessary_entries(
                trade_partner_add_form.data, ['add_trade_partner', 'csrf_token'])

            db.session.add(trade_partner_to_add)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                Message.flash_message(f'Istnieje już kontrahent o nazwie "{trade_partner_add_form.name.data}" lub adresie e-mail "{trade_partner_add_form.email_address.data}"',
                                      MessageLevel.WARNING)
                trade_partners = self.__get_trade_partner_data()
                return render_template(self.template_name, current_user=current_user, trade_partners=trade_partners, trade_partner_add_form=trade_partner_add_form)

            Message.flash_message("Kontrahent został pomyślnie dodany",
                                  MessageLevel.SUCCESS)
        else:
            error_message = Message.get_err_message(
                trade_partner_add_form.errors.values())
            Message.flash_message(f'{error_message}', MessageLevel.WARNING)

        trade_partners = self.__get_trade_partner_data()
        return render_template(self.template_name, current_user=current_user, trade_partners=trade_partners, trade_partner_add_form=trade_partner_add_form)
