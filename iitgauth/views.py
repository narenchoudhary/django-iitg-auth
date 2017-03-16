from django.contrib import auth
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.http import is_safe_url

from .forms import WebmailLoginForm


class WebmailLoginView(FormView):
    form_class = WebmailLoginForm

    def form_valid(self, form):
        redirect_to = self.request.POST.get('next', '')
        auth.login(self.request, form.user_cache)
        if not is_safe_url(redirect_to, self.request.get_host()):
            return super(WebmailLoginView, self).form_valid(form)
        else:
            return redirect(redirect_to)
