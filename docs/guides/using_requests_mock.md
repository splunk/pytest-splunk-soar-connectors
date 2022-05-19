# Using requests-mocks

The [requests-mock](https://requests-mock.readthedocs.io/en/latest/overview.html) package allows to intercept network requests and provide prepared responses to avoid network dependencies in tests. Please refer to its documentation for full background on what it can be used for.

## Example Test

The Connector from the [Redmine App](https://github.com/splunk-soar-connectors/redmine) is instantiated in `conftest.py` (not shown) with a `base_url` pointing to `https://localhost:3000`. Now in the test, we can use the `requests_mock` fixture to provide a prepared response to avoid running a local Redmine instance.


```python
def test_list_tickets(configured_connector: RedmineConnector, requests_mock):

    # Mock HTTP response
    sample_issues = {
        "issues": [{
            "id": 1
        },{
            "id": 2
        }]
    }

    requests_mock.get("http://localhost:3000/issues.json", json=sample_issues, headers={"Content-Type": "application/json"})

    # Configure action parameters
    in_json = {
            "parameters": {
                "identifier": "list_tickets"
            }
    }

    # Execute Action
    action_result_str = configured_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["summary"]["num_tickets"] == 2

```

