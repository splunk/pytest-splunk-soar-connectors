from datetime import datetime
import json
import logging
from phantom_mock import phantom
from pytest_splunk_soar_connectors.models import Artifact
from src.pytest_splunk_soar_connectors.models import InputJSON
from tests.conftest import MyDNSConnector
from phantom_mock.phantom.action_result import ActionResult


def test_debug_print(capsys, my_dns_connector):
    my_dns_connector.logger.setLevel(logging.DEBUG)
    my_dns_connector.debug_print("hello")
    out, err = capsys.readouterr()
    assert "BaseConnector.debug_print" in out


def test_connector_has_asset_id(my_dns_connector):
    assert my_dns_connector.get_asset_id() == "default-asset-id"


def test_connector_has_base_url(my_dns_connector):
    assert my_dns_connector.get_phantom_base_url() == "https://127.0.0.1"


def test_connector_get_config(my_dns_connector):
    config = my_dns_connector.get_config()
    assert "dns_server" in config


def test_save_progresss(capsys, my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    conn.logger.setLevel(logging.DEBUG)
    conn.save_progress("my progress")
    assert "progress" in str(conn._BaseConnector__progress)


def test_get_action_identifier(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [
            {
                "ip": "8.8.8.8"
            },
            {
                "ip": "1.1.1.1"
            }
        ],
        "environment_variables": {},
    }

    conn._handle_action(json.dumps(in_json), None)
    assert conn.get_action_identifier() == "forward_lookup"


def test_add_action_result(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    parameters = {"identifier": "forward_lookup", "ip": "52.5.196.118"}

    action_result = ActionResult(parameters)
    conn.add_action_result(action_result)

    assert len(conn.action_results) == 1


def test_get_action_results(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    parameters = {"identifier": "forward_lookup", "ip": "52.5.196.118"}

    action_result = ActionResult(parameters)
    conn.add_action_result(action_result)

    assert len(conn.get_action_results()) == 1


def test_save_artifacts(my_dns_connector: MyDNSConnector):

    test_artifact: Artifact = {
        "id": 123,
        "name": "hello",
        "label": "mylabel",
        "create_time": datetime.now(),
        "start_time": datetime.now(),
        "end_time": None,
        "severity": "low",
        "hash": "123",
        "cef": {"sourceAddress": "8.7.7.7"},
        "container": 1,
        "data": {},
        "source_data_identifier": "1234",
    }

    my_dns_connector.save_artifacts([test_artifact])
    assert len(my_dns_connector._BaseConnector__artifacts) == 1

def test_handle_action_input(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [
            {
                "ip": "8.8.8.8"
            }
        ],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["data"][0]["in_ip"] == "8.8.8.8"

def test_handle_action_input_multiple_params(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [
            {
                "ip": "8.8.8.8"
            },
            {
                "ip": "1.1.1.1"
            }
        ],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["data"][0]["in_ip"] == "8.8.8.8"
    assert action_result[1]["data"][0]["in_ip"] == "1.1.1.1"
