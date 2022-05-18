# pytest-splunk-soar-connectors

A plugin to perform unit testing for Splunk SOAR Apps. 

## Features

* Mocks for most Splunk SOAR Python App Authoring APIs, especially `BaseConnector`

## Installation

It is recommended to create a virtual environment for the App under test. Run the below commands to install the package locally into the python environment.

```
git clone https://github.com/dfederschmidt/pytest-splunk-soar-connectors
cd pytest-splunk-soar-connectors
pip install -e .
```

## Documentation


```
python3 -m venv venv
source venv/bin/activate
mkdocs serve -a localhost:9090
```

You should be able to access the local documentation at [https://localhost:9090](http://localhost:9090).