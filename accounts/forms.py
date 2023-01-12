from django import forms
from .models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password"}))

    class Meta:
        model = User
        fields = ("username", "password",)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This user doesn't exist")
        else:
            user = User.objects.get(username=username)

            if not user.is_active:
                raise forms.ValidationError('User is not activated')
            if not user.check_password(password):
                raise forms.ValidationError("Password is wrong")
        return self.cleaned_data
