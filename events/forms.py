from django import forms
from events.models import Category, Events, Participant
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
            "description": forms.Textarea(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors", "rows": 4}),
        }
class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ["name", "description", "date", "time", "location", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
            "description": forms.Textarea(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors", "rows": 4}),
            "date": forms.DateInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors", "type": "time"}),
            "location": forms.TextInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
            "category": forms.Select(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
        }
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
            "email": forms.EmailInput(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"}),
            "events": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        }