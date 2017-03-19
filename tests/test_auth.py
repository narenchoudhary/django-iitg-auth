import poplib
try:
    from unittest import mock
except ImportError:
    import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from iitgauth.auth import WebMailAuthenticationBackend


class TestWebmailAuthBackend(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='username', password='password'
        )

    @mock.patch('django.contrib.auth.get_user_model')
    def test_get_user(self, mock_get_user_model):
        """
        Test ``get_user`` for a valid user.

        :param mock_get_user_model: mock path for `get_user``
        :return: None
        """
        mock_get_user_model.return_value = User
        auth_backend = WebMailAuthenticationBackend()
        self.assertEqual(auth_backend.get_user(self.user.id), self.user)

    @mock.patch('django.contrib.auth.get_user_model')
    def test_get_user_fail(self, mock_get_user_model):
        """
        Test ``get_user`` for a valid user.

        :param mock_get_user_model: mock path for `get_user``
        :return: None
        """
        mock_get_user_model.return_value = User
        auth_backend = WebMailAuthenticationBackend()
        self.assertNotEqual(auth_backend.get_user(-1), self.user)

    @mock.patch('poplib.POP3_SSL')
    def test_authenticate_success(self, mock_pop3_ssl):
        """
        Test ``authenticate`` for a valid user.

        :param mock_pop3_ssl: mock path for `poplib.POP3_SSL``
        :return: None
        """
        response = mock_pop3_ssl.return_value
        response.username.return_value = self.user.username
        response.pass_.return_value = b'+OK'

        credentials = {
            'username': 'username',
            'password': 'password',
            'login_server': '202.141.80.10',
            'port': '995'
        }
        auth_backend = WebMailAuthenticationBackend()
        self.assertEqual(auth_backend.authenticate(**credentials), self.user)

    def test_authenticate_invalid_user(self):
        """
        Test ``authenticate`` for an invalid user.

        :return: None
        """
        credentials = {
            'username': 'username2',
            'password': 'password',
            'login_server': '202.141.80.10',
            'port': '995'
        }
        auth_backend = WebMailAuthenticationBackend()
        self.assertIsNone(auth_backend.authenticate(**credentials))

    @mock.patch('poplib.POP3_SSL')
    def test_authenticate_poplib_exception(self, mock_pop3_ssl):
        """
        Test ``authenticate`` for ``poplib.error_proto`` exception.

        :param mock_pop3_ssl: mock path for `poplib.POP3_SSL``
        :return: None
        """
        mock_pop3_ssl.side_effect = poplib.error_proto
        # response.side_effect = poplib.error_proto
        # response.username.return_value = self.user.username
        # response.pass_.return_value = b'+OK'
        credentials = {
            'username': 'username',
            'password': 'password',
            'login_server': '202.141.80.10',
            'port': '995'
        }
        auth_backend = WebMailAuthenticationBackend()
        self.assertIsNone(auth_backend.authenticate(**credentials))

    @mock.patch('poplib.POP3_SSL')
    def test_authenticate_value_type_exception(self, mock_pop3_ssl):
        """
        Test ``authenticate`` for ``ValueError`` or ``TypeError``
        exception.

        :param mock_pop3_ssl: mock path for `poplib.POP3_SSL``
        :return: None
        """
        response = mock_pop3_ssl.return_value
        response.username.return_value = 123456
        response.pass_.return_value = 12345

        credentials = {
            'username': 'username',
            'password': 'password',
            'login_server': '202.141.80.10',
            'port': '995'
        }
        auth_backend = WebMailAuthenticationBackend()
        self.assertRaises(TypeError, auth_backend.authenticate, **credentials)
