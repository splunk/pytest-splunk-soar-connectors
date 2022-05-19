# pytest-splunk-soar-connectors

A pytest plugin to perform unit testing for Splunk SOAR Apps. Please [review the documentation](https://splunk.github.io/pytest-splunk-soar-connectors/) on how to use this plugin.

## Local Development

It is recommended to create a virtual environment for this plugin. Run the below commands to install the package locally into a Python environment.

```
git clone https://github.com/dfederschmidt/pytest-splunk-soar-connectors
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

```
pytest
```

## Building the Documentation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdocs serve -a localhost:9090
```

You should be able to access the local documentation at [https://localhost:9090](http://localhost:9090).

## NOTICE File

Generate from requirements.txt
```
pip-licenses --format=markdown  > NOTICE.md
```