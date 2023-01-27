# Local Development for Splunk SOAR Connectors

**pytest-splunk-soar-connectors** is a plugin for the [pytest](https://docs.pytest.org) framework that provides a set of mock packages and fixtures for unit testing [Splunk SOAR Apps (Connectors)](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/Overview). 


It provides a way to run and test Splunk SOAR connectors locally. Pair it with other pytest packages such as [requests-mock](https://requests-mock.readthedocs.io/en/latest/overview.html) or [vcrpy](https://vcrpy.readthedocs.io/) to test connectors in total isolation, without a development SOAR instance or even access to the remote system the connector integrates with.

Beyond testing, the package can be used to get IDE autocompletions for the `phantom` package that is typically only found within the Splunk SOAR Python environment. This can ease development significantly. The initial scope of this project is to cover the entire [App Authoring API](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/AppDevAPIRef#App_authoring_API).

## Other Projects

Its purpose is similiar to the [phantom-test-harness](https://github.com/iforrest/phantom-test-harness) project and
some of the features fo the [phantom-dev](https://gitlab.com/phantom6/phantom-dev/) framework.


## Support

This is not an official Splunk product.