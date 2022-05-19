# pytest-splunk-soar-connectors

A pytest plugin to perform unit testing for Splunk SOAR Apps. Please [review the documentation](https://splunk.github.io/pytest-splunk-soar-connectors/) on how to use this plugin.

## Installation

It is recommended to create a virtual environment for the App under test. Run the below commands to install the package locally into the python environment.

```
git clone https://github.com/dfederschmidt/pytest-splunk-soar-connectors
cd pytest-splunk-soar-connectors
pip install -e .
```

## Building the Documentation

```
python3 -m venv venv
source venv/bin/activate
mkdocs serve -a localhost:9090
```

You should be able to access the local documentation at [https://localhost:9090](http://localhost:9090).
