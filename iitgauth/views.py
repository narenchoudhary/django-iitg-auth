from django.contrib import auth
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.http import is_safe_url

from .forms import WebmailLoginForm


class WebmailLoginView(FormView):
    """
    View class which handles User authentication.

    It works as follows:
    * Renders ``WebmailLoginForm`` on GET
    * Autenticates the User using POST data
    * Redirects to ``success_url`` on successful authentication
    * Re-renders ``WebmailLoginForm`` on unsuccessful authentication
    """
    form_class = WebmailLoginForm

    def form_valid(self, form):
        """
        This method is executed when submitted form is valid.

        It redirects to ``success_url`` if no ``next`` url is provided.
        Otherwise it redirects to ``next`` url.

        :param form: ``forms.Form`` instance
        :return: ``HttpResponse`` instance
        """
        redirect_to = self.request.POST.get('next', '')
        auth.login(self.request, form.user_cache)
        # check if next is a valid url
        if not is_safe_url(redirect_to, self.request.get_host()):
            return super(WebmailLoginView, self).form_valid(form)
        else:
            return redirect(redirect_to)
