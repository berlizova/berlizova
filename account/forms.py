from django import forms
from django.contrib.auth.models import User


# RegisterForm class inherits from forms.ModelForm and is used for user registration.
class RegisterForm(forms.ModelForm):
    # Field for the password, using PasswordInput widget for security.
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="This field is required",
    )

    # Field for confirming the password, also using PasswordInput widget.
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="This field is required",
    )

    class Meta:
        model = User  # Specifies that this form is associated with the User model.
        fields = ["username", "email"]  # Fields to be included in the form.
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # Custom widget for username.
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),  # Custom widget for email.
        }
        labels = {
            "username": "Username",  # Custom label for the username field.
            "email": "Email",  # Custom label for the email field.
        }
        help_texts = {
            "username": "This field is required",  # Help text for the username field.
            "email": "This field is required",  # Help text for the email field.
        }
        error_messages = {
            "username": {
                "required": "This field is required",  # Error message for missing username.
            },
            "email": {
                "required": "This field is required",  # Error message for missing email.
            },
        }

    def clean_password2(self):
        """
        Custom validation method to ensure that the two password fields match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Passwords do not match"
            )  # Raises an error if passwords don't match.
        return password2

    def save(self, commit=True):
        """
        Overrides the save method to hash the password before saving the user object.
        """
        user = super().save(commit=False)
        user.set_password(
            self.cleaned_data["password1"]
        )  # Sets the password after hashing.
        if commit:
            user.save()  # Saves the user object if commit is True.
        return user
