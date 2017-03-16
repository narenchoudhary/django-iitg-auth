from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View

from iitgauth.views import WebmailLoginView


class LoginView(WebmailLoginView):
    """
    View class which handles logging in users. It is subclass of
    ``WebmailLoginView`` class provided by ``iitgauth`` package.
    """
    template_name = 'app/login.html'
    success_url = reverse_lazy('home')


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View class for rendering home page with user added to context.
    """
    login_url = reverse_lazy('login')
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LogoutView(LoginRequiredMixin, View):
    """
    View class which handles logging out users.
    """
    login_url = reverse_lazy('login')
    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        auth.logout(request)
        return redirect('login')
