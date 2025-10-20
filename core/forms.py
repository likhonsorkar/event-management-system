from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Events

class StyleMixin:
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{self.default_class} {existing_classes}".strip()
class RegistrationFrom(StyleMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class LoginForm(StyleMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
class CategoryForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
}

class EventsForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Events
        fields = ["name", "description", "date", "time", "location", "category"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
}