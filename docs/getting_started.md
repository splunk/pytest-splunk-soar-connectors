## Getting Started

As this plugin is not yet published to the Python Package Index (PyPi) we'll outline the steps needed to install the plugin from its Github repository. 

It is strongly recommended to install this package in your projects [virtual environment](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.) as part of your local development. The commands below assume you are located in the the SOAR connectors root directory. If you already have an existing virtual environment, you can skip these steps.

### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/splunk/pytest-splunk-soar-connectors
```

### Connector Fixture

Create a `tests` directory in the root of your connector project if you have not already and create a `conftest.py` within.
```
mkdir tests && cd tests
touch conftest.py
```

Open the created `conftest.py` in your favorite editor and create a new [pytest fixture](https://docs.pytest.org/en/6.2.x/fixture.html) for your connector. The example below uses the Connector from the [DNS App](https://github.com/splunk-soar-connectors/dns).


```python
import os
import sys
import logging

# Add root directory to path
sys.path.insert(0, os.getcwd()) 

import pytest
# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")

# Replace this with the import for your connector
from dns_connector import DNSConnector

@pytest.fixture(scope='function')
def configured_connector():
    conn = DNSConnector()

    # Define the asset configuration to be used 
    conn.config = {
        "dns_server": "8.8.8.8",
        "host_name": "splunk.com"
    }

    conn.logger.setLevel(logging.INFO)
    return conn
```

Now, create a test file in your `tests/` directory, eg. `test_dns_connector.py` and define your tests eg.

```python
import json
import os, sys
from pytest_splunk_soar_connectors.models import InputJSON

sys.path.insert(0, os.getcwd()) 
import pytest

from dns_connector import DNSConnector

def test_lookup_domain(configured_connector: DNSConnector):

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

def test_lookup_ip(configured_connector: DNSConnector):

    in_json: InputJSON = {
        "action": "lookup ip",
        "identifier": "reverse_lookup",
        "config": {},
        "parameters": [
            {
                "ip": "52.5.196.118"
            },
            {
                "ip": "8.8.8.8"
            }
        ],
        "environment_variables": {},
    }

    # Execute Action
    action_result_str = configured_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["summary"]["cannonical_name"] == "118.196.5.52.in-addr.arpa."
```

## Mocking Network Calls

In this case, the configured DNS server is publicly accessible, so running the action is not an issue. But what if that is not the case? Consider using [requests-mock](https://requests-mock.readthedocs.io/en/latest/overview.html) or [vcrpy](https://vcrpy.readthedocs.io/en/latest/) in your tests to avoid doing actual network calls as part of your CI exution.