from unittest import mock

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase

from iitgauth.forms import WebmailLoginForm
from iitgauth.views import WebmailLoginView


class TestWebmailLoginView(TestCase):

    initial_data = {'username': 'username', 'password': 'password',
                    'login_server': '202.141.80.10'}
    success_url = "/success_url/"
    template_name = 'form.html'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='username', password='password')

    def setup_view(self, view, request, *args, **kwargs):
        """
        Builtin ``self.client.get()`` performs system tests. We do
        not want to test environment surrounding the view (like url
        routing, template rendering, form handling, etc.). We only
        need to perform unit tests. That too, for ``form_valid()``
        method.

        Tests for rest of the methods of View are already in Django's
        repository and we don't need to test them again.

        This view mimics as_view() returned callable, but returns
        view instance.
        http://tech.novapost.fr/django-unit-test-your-views-en.html

        :param view: View instance
        :param request: a HttpRequest type instance
        :param args: non-keyworded, variable-length argument list
        :param kwargs: a keyworded, variable-length argument list
        :return: View instance
        """
        view.request = request
        view.success_url = self.success_url
        view.template_name = self.template_name
        view.args = args
        view.kwargs = kwargs
        return view

    @mock.patch('django.contrib.auth.login')
    def test_form_valid_without_next(self, mock_login):
        """
        Test ``form_valid`` when ``next`` is ``None``.
        :param mock_login: mock patch for login
        :return: None
        """
        mock_login.return_value = None
        form = WebmailLoginForm(self.initial_data)
        form.user_cache = self.user

        request = RequestFactory().get("")
        request.POST = dict(next="")
        view = WebmailLoginView()
        view = self.setup_view(view, request)
        response = view.form_valid(form)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTemplateUsed(view.template_name)
        self.assertEqual(response.status_code, 302)

    @mock.patch('django.contrib.auth.login')
    def test_form_valid_without_next(self, mock_login):

        mock_login.return_value = None
        form = WebmailLoginForm(self.initial_data)
        form.user_cache = self.user

        request = RequestFactory().get("")
        request.POST = dict(next="")
        view = WebmailLoginView()
        view = self.setup_view(view, request)
        response = view.form_valid(form)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTemplateUsed(view.template_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), view.success_url)

    @mock.patch('django.contrib.auth.login')
    def test_form_valid_with_next(self, mock_login):
        """
        Test ``form_valid`` when ``next`` is not ``None``.
        :param mock_login: mock patch for login
        :return: None
        """
        mock_login.return_value = None
        form = WebmailLoginForm(self.initial_data)
        form.user_cache = self.user

        request = RequestFactory().get("")
        # "./next" is used becuase urls starting with "./" and "../"
        # are not resolved by url. Resolution of urls will raise error
        # because ROOT_URLCONF is not configured.
        request.POST = dict(next="./next/")
        view = WebmailLoginView()
        view = self.setup_view(view, request)
        response = view.form_valid(form)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTemplateUsed(view.template_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), "./next/")
