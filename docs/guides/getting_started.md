This page will guide you through creating a unit test setup for your SOAR connector. It assumes you successfully installed the package in your projects virtual environment. It also assumes you have [pytest](https://docs.pytest.org/en/7.2.x/) installed.


## Preparations

Create a `tests` directory in the root of your connector project if you have not already and create a `conftest.py` within that directory.
```sh
mkdir tests && cd tests
touch conftest.py
```

## Loading the plugin in conftest

In your `conftest.py` add the plugin to your `pytest_plugins` definition
```py
import pytest

# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")

```

## Create your Connector Fixture

Create a new [pytest fixture](https://docs.pytest.org/en/6.2.x/fixture.html) for your connector. The example below uses the connector from the [DNS App](https://github.com/splunk-soar-connectors/dns). We'll use the `configure_connector` utility function which takes the connector class and the desired asset settings as input.

```py
from dns_connector import DNSConnector
from pytest_splunk_soar_connectors import configure_connector

@pytest.fixture(scope="function")
def configured_dns_connector():
    return configure_connector(DNSConnector, {
        "dns_server": "8.8.8.8",
        "host_name": "splunk.com"
    })
```


## Write a simple test

Now, create a test file in your `tests/` directory, eg. `test_dns_connector.py`. Pass the fixture (here: `configured_dns_connector`) as a parameter to your test.
In order to call the action, the `_handle_action` method of the connector needs to be called with an `InputJSON`. The `InputJSON` is simply 
a dictionary structure that is initializing the connector run.

`_handle_action` returns the action results that were created during the run as a string, so they need to be parsed back into a python list before any
`asserts` can be done.

```python
import pytest
import json
import os
import sys
from pytest_splunk_soar_connectors.models import InputJSON

sys.path.insert(0, os.getcwd()) 

from dns_connector import DNSConnector

def test_lookup_domain(configured_dns_connector: DNSConnector):

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "forward_lookup",
        "config": {},
        "parameters": [
            {
                "domain": "splunk.com"
            }
        ],
        "environment_variables": {},
    }

    # Execute Action
    action_result_str = configured_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["summary"]["record_info"] == "52.5.196.118"

```

## What's next?

In the above example, the DNS server was accessible over the internet and could be called as part of a test without any authentication required. But 
how do you write tests where you don't have a live instance to test against? Using [requests-mock](https://requests-mock.readthedocs.io/en/latest/) you can 
write unittests that are fully offline. Read on in [Using requests-mock](using_requests_mock.md)