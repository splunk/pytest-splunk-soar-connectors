# Using VCR.py

Using the [VCR.py](https://vcrpy.readthedocs.io/en/latest/usage.html) library may be appropriate if you have access to the remote system in your lab environment from your local laptop, but don't want to configure it within your CI pipeline.

By running pytest in different *record modes*, VCR.py can save network responses to *cassettes* that can be committed to version control.

## Example Test

Running the below test for the first time with a configured connector pointing to a live instance of Redmine, will create a new `cassettes/` directory in the `tests` folder. Within this folder, a local copy of the `list_tickets` API response will be saved. On following executions, pytest will not do network requests but use the local copy instead.

!!! warning

    Please ensure that your local copies don't contain sensitive informations such as cookie values, API tokens, passwords. Review the VCR.py documentation on how to scrub sensitive information from your local copy. 


```python
@pytest.mark.vcr()
def test_list_tickets_vcrpy(configured_connector: RedmineConnector):

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
    assert "issues" in action_result[0]["data"][0]
```