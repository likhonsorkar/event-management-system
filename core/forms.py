from django import forms
from core.models import CustomUser as User
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Events
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

class StyleMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "w-full px-4 py-3 bg-gray-50 dark:bg-zinc-900 border border-gray-200 dark:border-zinc-700 rounded-xl text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, (forms.PasswordInput, forms.DateInput, forms.TimeInput, forms.NumberInput)):
                field.widget.attrs.update({
                    'class': self.default_classes,
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 4
                })
            elif isinstance(field.widget, (forms.Select, forms.SelectDateWidget)):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
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
class ProfileUpdateForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "phone", "profile_picture"]

class UpdatePasswordForm(StyleMixin, PasswordChangeForm):
    pass
class CustomPasswordResetForm(StyleMixin, PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyleMixin, SetPasswordForm):
    pass