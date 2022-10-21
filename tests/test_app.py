import logging
from this import d
import phantom

def test_app_error():
    assert phantom.app.APP_ERROR is False


def test_app_success():
    assert phantom.app.APP_SUCCESS is True


def test_is_fail():
    assert phantom.is_fail(phantom.app.APP_ERROR) is True


def test_is_fail_false():
    assert phantom.is_fail(phantom.app.APP_SUCCESS) is False

def test_get_req_value():
    dic = {"hello": "world"}
    assert phantom.app.get_req_value(dic, "hello") == "world"
