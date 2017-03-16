from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

import poplib

from .constants import LOGIN_SERVERS


class WebmailLoginForm(forms.Form):
    username = forms.CharField(max_length=254, label=_('Webmail'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    login_server = forms.ChoiceField(choices=LOGIN_SERVERS)

    port = poplib.POP3_SSL_PORT

    error_messages = {
        'invalid_login': _('No user found for given credentials.'),
        'inactive': _('This account is inactive')
    }

    def __init__(self, request=None, port=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self.port = port if port is not None else poplib.POP3_SSL_PORT

        super(WebmailLoginForm, self).__init__(*args, **kwargs)

        user_model = get_user_model()
        self.username_field = user_model._meta.get_field(
            user_model.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        login_server = self.cleaned_data.get('login_server')
        port = self.port if self.port is not None else poplib.POP3_SSL_PORT
        if username and password and login_server:
            self.user_cache = authenticate(
                username=username, password=password,
                login_server=login_server, port=port)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params=dict(username=self.username_field.verbose_name)
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'], code='inactive'
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
