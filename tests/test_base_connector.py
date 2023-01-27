# pylint: disable=protected-access

import json
import logging
from datetime import datetime

import phantom
from phantom.action_result import ActionResult
from pytest_splunk_soar_connectors.models import Artifact
from src.pytest_splunk_soar_connectors.models import InputJSON
from tests.conftest import MyDNSConnector
import pytest


def test_debug_print(capsys, my_dns_connector):
    my_dns_connector.logger.setLevel(logging.DEBUG)
    my_dns_connector.debug_print("hello")

    out, _ = capsys.readouterr()
    assert "BaseConnector.debug_print" in out


def test_error_print(capsys, my_dns_connector: MyDNSConnector):
    my_dns_connector.logger.setLevel(logging.DEBUG)
    my_dns_connector.error_print("hello")

    out, _ = capsys.readouterr()
    assert "BaseConnector.error_print" in out


def test_connector_has_asset_id(my_dns_connector: MyDNSConnector):
    assert my_dns_connector.get_asset_id() == "default-asset-id"


def test_connector_has_base_url(my_dns_connector):
    assert my_dns_connector.get_phantom_base_url() == "https://127.0.0.1"


def test_connector_get_config(my_dns_connector):
    config = my_dns_connector.get_config()
    assert "dns_server" in config


def test_save_progresss(my_dns_connector):
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
        "parameters": [{"ip": "8.8.8.8"}, {"ip": "1.1.1.1"}],
        "environment_variables": {},
    }

    conn._handle_action(json.dumps(in_json), None)
    assert conn.get_action_identifier() == "forward_lookup"


def test_add_action_result(my_dns_connector):
    conn: MyDNSConnector = my_dns_connector
    parameters = {"identifier": "forward_lookup", "ip": "52.5.196.118"}

    action_result = ActionResult(parameters)
    conn.add_action_result(action_result)

    assert len(conn._BaseConnector__action_results) == 1


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
        "parameters": [{"ip": "8.8.8.8"}],
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
        "parameters": [{"ip": "8.8.8.8"}, {"ip": "1.1.1.1"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["data"][0]["in_ip"] == "8.8.8.8"
    assert action_result[1]["data"][0]["in_ip"] == "1.1.1.1"


def test_append_to_message(my_dns_connector: MyDNSConnector) -> None:

    my_dns_connector.append_to_message("first ")
    my_dns_connector.append_to_message("second")

    assert my_dns_connector._BaseConnector__message == "first second"


from unittest.mock import MagicMock


def test_finalize_called(my_dns_connector: MyDNSConnector) -> None:
    """Tests whether finalize is called once after the execution"""

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    my_dns_connector.finalize = MagicMock(return_value=3)

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    my_dns_connector.finalize.assert_called_once()


def test_get_app_config(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert "actions" in my_dns_connector.get_app_config()


def test_get_app_id(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert "876ab991-313e-48e7-bccd-e8c9650c239d" == my_dns_connector.get_app_id()


def test_get_app_json(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    app_json = my_dns_connector.get_app_json()

    assert app_json is not None
    assert "actions" in app_json


def test_get_asset_id(my_dns_connector: MyDNSConnector) -> None:
    assert my_dns_connector.asset_id == "default-asset-id"


def test_get_ca_bundle(my_dns_connector: MyDNSConnector) -> None:
    with pytest.raises(NotImplementedError):
        my_dns_connector.get_ca_bundle()


def test_get_connector_id(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert "876ab991-313e-48e7-bccd-e8c9650c239d" == my_dns_connector.get_connector_id()


def test_get_container_id(my_dns_connector: MyDNSConnector) -> None:
    assert my_dns_connector.get_container_id() == 123


def test_get_container_info(my_dns_connector: MyDNSConnector) -> None:
    _, info, _ = my_dns_connector.get_container_info(container_id=123)
    assert info.get("container_info_would_go_here")


def test_get_current_param(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert len(my_dns_connector.get_current_param()) == 1


def test_get_product_installation_id(my_dns_connector: MyDNSConnector) -> None:
    product_id = my_dns_connector.get_product_installation_id()
    assert product_id == "1234"


def test_get_product_version(my_dns_connector: MyDNSConnector) -> None:
    product_id = my_dns_connector.get_product_version()
    assert product_id == "4.5.15370"


def test_load_state_none(my_dns_connector: MyDNSConnector) -> None:
    ret_val = my_dns_connector.get_state()
    assert ret_val is None


def test_load_state_is_dict(my_dns_connector: MyDNSConnector) -> None:
    my_dns_connector.load_state()
    ret_val = my_dns_connector.get_state()
    assert ret_val == {}


def test_get_state_file_path(my_dns_connector: MyDNSConnector) -> None:
    location = my_dns_connector.state_file_location
    assert location


def test_get_state_dir(my_dns_connector: MyDNSConnector) -> None:
    location = my_dns_connector.get_state_dir()
    assert location


def test_get_status_success(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [{"ip": "8.8.8.8"}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert my_dns_connector.get_status()


def test_get_status_fail(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "test connectivity",
        "identifier": "test_connectivity",
        "config": {},
        "parameters": [{}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    assert my_dns_connector.get_status() is False


def test_get_status_message(my_dns_connector: MyDNSConnector) -> None:

    in_json: InputJSON = {
        "action": "test connectivity",
        "identifier": "test_connectivity",
        "config": {},
        "parameters": [{}],
        "environment_variables": {},
    }

    action_result_str = my_dns_connector._handle_action(json.dumps(in_json), None)
    _ = json.loads(action_result_str)

    my_dns_connector.set_status(phantom.APP_ERROR, "fail")
    assert my_dns_connector.get_status_message() == "fail"
