from phantom_mock import phantom
from phantom_mock.phantom.base_connector import BaseConnector
import logging
import pytest

class MyDNSConnector(BaseConnector):
    ACTION_ID_FORWARD_LOOKUP = "forward_lookup"
    ACTION_ID_REVERSE_LOOKUP = "reverse_lookup"
    
    def initialize(self):
        pass

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this connector run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if (action_id == self.ACTION_ID_FORWARD_LOOKUP):
            ret_val = self._handle_forward_lookup(param)
        elif (action_id == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            ret_val = self._test_connectivity()

        return ret_val

    def _handle_forward_lookup(self, param):
        return phantom.APP_SUCCESS

@pytest.fixture()
def my_dns_connector():
    conn = MyDNSConnector()

    conn.config = {
        "dns_server": "8.8.8.8",
        "host_name": "splunk.com"
    }

    conn.logger.setLevel(logging.DEBUG)
    conn.initialize()

    return conn