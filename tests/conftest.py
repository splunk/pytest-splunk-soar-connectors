import logging

import pytest

from tests.my_dns_app.my_dns_app_connector import MyDNSConnector


@pytest.fixture()
def my_dns_connector():
    conn = MyDNSConnector()

    conn.config = {"dns_server": "8.8.8.8", "host_name": "splunk.com"}
    conn.logger.setLevel(logging.DEBUG)

    return conn
