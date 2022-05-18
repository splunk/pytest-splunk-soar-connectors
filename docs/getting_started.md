# Getting started

## Installation

```
pip install pytest-splunk-soar-connectors
```

## Configuration


Within your tests suites `conftest.py` ([What is conftest.py?](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)) load the plugin:

```
...
pytest_plugins = ("splunk-soar-connectors",) 
...
```

## Usage

It is recommended to create a pytest fixture for the connector under test.
