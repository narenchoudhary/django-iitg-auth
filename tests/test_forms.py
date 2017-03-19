import poplib
try:
    from unittest import mock
except ImportError:
    import mock

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from iitgauth.auth import WebMailAuthenticationBackend
from iitgauth.forms import WebmailLoginForm


class WebmailLoginFormTestActiveUser(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='username',password='password')

    @mock.patch('django.contrib.auth.get_user_model')
    def test_form_init(self, mock_get_user_model):
        mock_get_user_model.return_value = User
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        self.assertIsInstance(form.fields['username'], forms.CharField)
        self.assertIsInstance(form.fields['password'], forms.CharField)
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)
        self.assertEqual(form.data.get('username'),
                         initial_data.get('username'))
        self.assertEqual(form.data.get('password'),
                         initial_data.get('password'))
        self.assertEqual(form.data.get('login_server'),
                         initial_data.get('login_server'))
        self.assertEqual(form.port, poplib.POP3_SSL_PORT)
        self.assertEqual(form.username_field.verbose_name, User.USERNAME_FIELD)

    @mock.patch('django.contrib.auth.get_user_model')
    @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
    @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
    @mock.patch.object(WebmailLoginForm, 'confirm_login_allowed')
    def test_form_valid(self, mock_confirm_login_allowed, mock_authenticate,
                        mock_get_user, mock_get_user_model):
        mock_get_user_model.return_value = User
        mock_confirm_login_allowed.return_value = None
        mock_authenticate.return_value = self.user
        mock_get_user.return_value = self.user
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.user_cache, mock_get_user_model.return_value)
        self.assertEqual(form.user_cache.username, self.user.username)
        self.assertEqual(form.user_cache.id, self.user.id)

    @mock.patch('django.contrib.auth.get_user_model')
    @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
    @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
    @mock.patch.object(WebmailLoginForm, 'confirm_login_allowed')
    def test_form_invalid(self, mock_confirm_login_allowed, mock_authenticate,
                          mock_get_user, mock_get_user_model):
        mock_get_user_model.return_value = User
        mock_confirm_login_allowed.return_value = None
        mock_authenticate.return_value = self.user
        mock_get_user.return_value = self.user
        initial_data = {'username': 'username', 'password': 'password'}
        form = WebmailLoginForm(data=initial_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors['login_server'])

    @mock.patch('django.contrib.auth.get_user_model')
    @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
    @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
    @mock.patch.object(WebmailLoginForm, 'confirm_login_allowed')
    def test_get_user_after_full_clean(
            self, mock_confirm_login_allowed, mock_authenticate,
            mock_get_user, mock_get_user_model):
        mock_get_user_model.return_value = User
        mock_confirm_login_allowed.return_value = None
        mock_authenticate.return_value = self.user
        mock_get_user.return_value = self.user
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        form.full_clean()
        self.assertEqual(form.get_user(), self.user)

    @mock.patch('django.contrib.auth.get_user_model')
    @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
    @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
    @mock.patch.object(WebmailLoginForm, 'confirm_login_allowed')
    def test_get_user_id_after_full_clean(
            self, mock_confirm_login_allowed, mock_authenticate,
            mock_get_user, mock_get_user_model):
        mock_get_user_model.return_value = User
        mock_confirm_login_allowed.return_value = None
        mock_authenticate.return_value = self.user
        mock_get_user.return_value = self.user
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        form.full_clean()
        self.assertEqual(form.get_user_id(), self.user.pk)

    @mock.patch('django.contrib.auth.get_user_model')
    @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
    @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
    @mock.patch.object(WebmailLoginForm, 'confirm_login_allowed')
    def test_get_user_id_none_before_full_clean(
            self, mock_confirm_login_allowed, mock_authenticate,
            mock_get_user, mock_get_user_model):
        mock_get_user_model.return_value = User
        mock_confirm_login_allowed.return_value = None
        mock_authenticate.return_value = self.user
        mock_get_user.return_value = self.user
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        self.assertIsNone(form.get_user_id())


class WebmailLoginFormTestInactiveUser(TestCase):

    def setUp(self):
        # cannot include is_active in create_user() becuase in Django==1.8
        # is_active=False is already included in _create_user() in auth
        # package. Including is_active in create_user() leads to following
        # TypeError.
        # TypeError: ModelBase object got multiple values for keyword 
        # argument 'is_active'.
        self.user = get_user_model().objects.create_user(
            username='username', password='password')
        self.user.is_active = False
        self.user.save()

    @mock.patch('django.contrib.auth.get_user_model')
    def test_confirm_login_allowed_for_inactive_user(self, mock_get_user_model):
        mock_get_user_model.return_value = User
        initial_data = {'username': 'username', 'password': 'password',
                        'login_server': '202.141.80.10'}
        form = WebmailLoginForm(data=initial_data)
        self.assertRaises(forms.ValidationError, form.confirm_login_allowed, self.user)
        # error_message = form.error_messages.get('invalid')
        error_message = 'This account is inactive'
        with self.assertRaisesMessage(forms.ValidationError, error_message):
            form.confirm_login_allowed(self.user)


# class WebmailLoginFormTestInvalidUser(TestCase):
#
#     @mock.patch('django.contrib.auth.get_user_model')
#     @mock.patch.object(WebMailAuthenticationBackend, 'get_user')
#     @mock.patch.object(WebMailAuthenticationBackend, 'authenticate')
#     def test_clean_for_invalid_user(self, mock_authenticate, mock_get_user, mock_get_user_model):
#         mock_get_user_model.return_value = User
#         mock_authenticate.return_value = None
#         mock_get_user.return_value = None
#         initial_data = {'username': 'username2', 'password': 'password2',
#                         'login_server': '202.141.80.10'}
#         form = WebmailLoginForm(data=initial_data)
#         form.cleaned_data = dict()
#         form._clean_fields()
#         # form.clean_username()
#         # form.clean_password()
#         # form.clean_login_server()
#         # form.clean()
#         self.assertRaises(forms.ValidationError, form.clean)
#         # error_message = 'No user found for given credentials.'
#         # with self.assertRaisesMessage(forms.ValidationError, error_message):
#         #     form.clean()
