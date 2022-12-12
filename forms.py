from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class TransactionForm(FlaskForm):
    """
    Form to handle transaction filtering by the user.

    Note: These two custom methods are a little hokey. I 
    didn't have the time to research the library to see 
    if there was a native way to handle non-required field
    validation.
    """
    account_first_name = StringField()
    account_last_name = StringField()
    fi_name = StringField()
    qldb_id = StringField()
    transaction_type = StringField()

    def get_validly_bound_field_names(self):
        " Return a list of field names that have valid data associated to them. "
        validly_bound_field_names = []
        for field, value in self.data.items():
            # Ignore non-meaningful form fields
            if field in ['csrf']:
                continue

            # Ignore fields that don't have meaningful data bound to them
            if not value:
                continue 

            validly_bound_field_names.append(field)
        return validly_bound_field_names

    def has_valid_data(self):
        " Returns true if the form has any validly bound data. "
        if self.get_validly_bound_field_names():
            return True 
        return False
