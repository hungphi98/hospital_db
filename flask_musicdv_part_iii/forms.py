# forms.py

from wtforms import Form, StringField, SelectField, validators

class MusicSearchForm(Form):
    choices = [('Patient History', 'Patient History'),
               ('Department', 'Department'),
               ('Staff', 'Staff'), ('Billing', 'Billing')]
    select = SelectField('Search Hospital', choices=choices)
    search = StringField('')
