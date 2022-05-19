# Welcome to pytest-splunk-soar-connectors

pytest-splunk-soar-connectors is a plugin for the [pytest](https://docs.pytest.org) framework that provides a set of mock packages and fixtures for unit testing [Splunk SOAR Apps (Connectors)](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/Overview).

## Quick Start

As this plugin is not yet published to the Python Package Index (PyPi) we'll outline the steps needed to install the plugin from its Github repository. 

It is strongly recommended to install this package in your projects [virtual environment](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.) as part of your local development.

```
```



## What does the plugin do?

The main feature of the plugin is that it provides a set of python packages that mock the Splunk SOAR Python environment. It's purpose is similiar to the [phantom-test-harness](https://github.com/iforrest/phantom-test-harness) project and
some of the features fo the [phantom-dev](https://gitlab.com/phantom6/phantom-dev/) framework.

## Design Goals

- Be easy to integrate into pytest suites
- Work well with existing connector implementations
- Create test suites that can run as part of CI 

## Why would I use this?

It provides an easy way to test Splunk SOAR connectors. Combining it with other pytest packages such as [requests-mock](https://requests-mock.readthedocs.io/en/latest/overview.html) or [vcrpy](https://vcrpy.readthedocs.io/), SOAR connectors
can be tested in total isolation, without a development SOAR instance or even access to the external system.


## Any examples?

Please take a look in the `tests` folder of the  [Redmine](https://github.com/splunk-soar-connectors/redmine) connector for an example of a test suite using this package.