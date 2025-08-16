from django import forms
from events.models import Category, Events, Participant
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ["name", "description", "date", "time", "location", "category"]
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "events": forms.CheckboxSelectMultiple
        }