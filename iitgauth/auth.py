import poplib

from django.conf import settings
from django.contrib.auth import get_user_model


class WebMailAuthenticationBackend(object):
    """
    Authenticate against IIT Guwahati IMAP webmail servers.

    Use the webmail-username, password, IP of login server
    and valid port.

    Default port is set to ``poplib.POP3_SSL_PORT``.
    """
    user_model = settings.AUTH_USER_MODEL

    def get_user(self, user_id):
        """
        Return user object.
        :param user_id: primary key of user object
        :return: user object
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None

    def authenticate(self, **credentials):
        """
        Returns user for credentials provided if credentials are valid.
        Returns ``None`` otherwise.

        :param credentials: keyword arguments
        :return: user object
        """
        username = credentials.get('username')
        password = credentials.get('password')
        login_server = credentials.get('login_server')
        port = credentials.get('port')

        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return None
        try:
            response = poplib.POP3_SSL(host=login_server, port=port)
            response.user(user=username)
            password_string = response.pass_(pswd=password)
            if b'OK' in password_string:
                response.quit()
                return user
        except poplib.error_proto:
            return None
        except (ValueError, TypeError) as e:
            raise e
