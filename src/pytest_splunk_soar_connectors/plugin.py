import pytest
import logging


def configure_connector(connector, configuration):
    def make_configured_connector():
        conn = connector()
        conn.config = configuration
        conn.logger.setLevel(logging.INFO)
        return conn
    return make_configured_connector
