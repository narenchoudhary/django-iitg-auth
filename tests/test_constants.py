import re

from django.test import TestCase

from iitgauth.constants import LOGIN_SERVERS


class TestServerList(TestCase):

    def test_server_ips(self):
        """
        Test for login server IPs to match IP pattern.

        :return: None
        """
        server_ips = [item[0] for item in LOGIN_SERVERS]
        ip_pattern = re.compile(r"^202.141.80.[0-9]+$")
        self.assertTrue(all([bool(ip_pattern.match(ip)) for ip in server_ips]))

    def test_server_names(self):
        """
        Test for login server names to match name pattern.

        :return: None
        """
        server_names = [item[1] for item in LOGIN_SERVERS]
        name_pattern = re.compile(r"[a-zA-Z]+$")
        self.assertTrue(all([bool(name_pattern.match(name)) for name in server_names]))
