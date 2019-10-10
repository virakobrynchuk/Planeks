from .models import AppUser
from django import forms


class UserCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100)

    class Meta:
        model = AppUser
        fields = ('email', 'first_name', 'last_name', 'age', 'password', 'confirm_password')

    def clean(self):
        password = self.cleaned_data['password']
        if password != self.cleaned_data['confirm_password']:
            self.add_error('password',
                           'Password dont match')
        return self.cleaned_data


class UserLoginForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AppUser
        fields = ("email", "password")

    user_cache = None

    def get_user(self, username=None, password=None, **kwargs):
        try:
            user = AppUser.objects.get(email=username)
        except AppUser.DoesNotExist:
            return None

        if user is not None:
            if user.check_password(password):
                return user
        return

