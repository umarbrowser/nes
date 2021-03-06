# coding=utf-8
from django.forms import ModelForm, Form, TextInput, CharField, BooleanField, MultipleChoiceField, \
    CheckboxSelectMultiple, ValidationError, ChoiceField, SelectMultiple, IntegerField, NumberInput, \
    RadioSelect, CheckboxInput

from django.utils.translation import ugettext_lazy as _


from patient.models import Patient

# FAVORITE_COLORS_CHOICES = (
#     ('blue', 'Blue'),
#     ('green', 'Green'),
#     ('black', 'Black'),
# )

# SEARCH_PARTICIPANTS_CHOICES = (
#     ('all', _('All participants')),
#     ('selected', _('Selected participants'))
# )

HEADINGS_CHOICES = (
    ('code', _("Question code")),
    ('full', _("Full question text")),
    ('abbreviated', _("Abbreviated question text")),
)

RESPONSES_CHOICES = (
    ('short', _("Answer codes")),
    ('long', _("Full answers")),
)


class ExportForm(Form):
    title = CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'disabled': ''}))
    per_participant = BooleanField(initial=True, required=False)
    per_questionnaire = BooleanField(initial=True, required=False)

    questionnaire_entrance_selected = []

    # patient_fields_selected = MultipleChoiceField(required=True,
    #                                               widget=CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)

    headings = ChoiceField(widget=RadioSelect(), choices=HEADINGS_CHOICES)
    responses = MultipleChoiceField(widget=CheckboxSelectMultiple(attrs={'data-error': _('Response must be selected')}),
                                    choices=RESPONSES_CHOICES, )
    #
    # questionnaire_entrance_fields_selected = []
    #
    # patient_fields_selected = []
    #
    # diagnosis_fields_selected = []
    #
    # per_questionnaire_field = True

    def clean(self):
        cleaned_data = super(ExportForm, self).clean()
        participant_field = cleaned_data.get("per_participant")
        questionnaire_field = cleaned_data.get("per_questionnaire")

        if not (participant_field or questionnaire_field):
            self.add_error('per_participant',
                           _("Either one or both Per participant/Per questionnaire must be set."))

    # def __init__(self, *args, **kwargs):
    #     super(ExportForm, self).__init__(*args, **kwargs)
    #     self.base_fields['headings'].initial = 'abbreviated'
    #     self.base_fields['responses'].initial = 'short'


class ParticipantsSelectionForm(ModelForm):

    class Meta:
        model = Patient

        fields = [
            'gender', 'marital_status'
        ]

        widgets = {
            'gender': SelectMultiple(attrs={'class': 'form-control', 'required': "", 'disabled': ''}),
            'marital_status': SelectMultiple(attrs={'class': 'form-control', 'required': "", 'disabled': ''}),
        }

    def __init__(self, *args, **kwargs):
        super(ParticipantsSelectionForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = None
        self.fields['marital_status'].empty_label = None


class AgeIntervalForm(Form):

    min_age = IntegerField(min_value=0, widget=NumberInput(attrs={'class': 'form-control', 'required': "",
                                                                  'data-error': _('Min age must be filled.'),
                                                                  'disabled': ''}))
    max_age = IntegerField(min_value=0, widget=NumberInput(attrs={'class': 'form-control', 'required': "",
                                                                  'data-error': _('Max age must be filled.'),
                                                                  'disabled': ''}))
