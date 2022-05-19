import json
import logging
from phantom_mock import phantom
from tests.conftest import MyDNSConnector, my_dns_connector
from phantom_mock.phantom.action_result import ActionResult

def test_app_error():
    assert phantom.app.APP_ERROR == False

def test_app_success():
    assert phantom.app.APP_SUCCESS == True

def test_debug_print(capsys, my_dns_connector):
    conn = my_dns_connector
    conn.logger.setLevel(logging.DEBUG)
    conn.debug_print("hello")
    out, err = capsys.readouterr()
    assert "BaseConnector.debug_print" in out

def test_connector_has_asset_id(my_dns_connector):
    assert my_dns_connector.get_asset_id() == "1abc234"

def test_connector_has_base_url(my_dns_connector):
    assert my_dns_connector.get_phantom_base_url() == "https://127.0.0.1"

def test_connector_has_base_url(my_dns_connector):
    config = my_dns_connector.get_config()
    assert "dns_server" in config

def test_save_progresss(capsys, my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    conn.logger.setLevel(logging.DEBUG)
    conn.save_progress("my progress")
    assert "progress" in str(conn.progress)

def test_get_action_identifier(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector

    in_json = {
            "parameters": {
                "identifier": "forward_lookup",
                "ip": "52.5.196.118"
            }
    }

    conn._handle_action(json.dumps(in_json), None)
    assert conn.get_action_identifier() == "forward_lookup"

def test_add_action_result(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    parameters = {
        "identifier": "forward_lookup",
        "ip": "52.5.196.118"
    }

    action_result = ActionResult(parameters)
    conn.add_action_result(action_result)

    assert len(conn.action_results) == 1


