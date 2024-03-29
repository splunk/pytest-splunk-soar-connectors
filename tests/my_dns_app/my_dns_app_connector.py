import phantom
import phantom.action_result
import phantom.base_connector


class MyDNSConnector(phantom.base_connector.BaseConnector):
    ACTION_ID_FORWARD_LOOKUP = "forward_lookup"
    ACTION_ID_REVERSE_LOOKUP = "reverse_lookup"

    def initialize(self):
        pass

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this connector run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == self.ACTION_ID_FORWARD_LOOKUP:
            ret_val = self._handle_forward_lookup(param)
        elif action_id == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
            ret_val = self._test_connectivity(param)

        return ret_val

    def _test_connectivity(self, param):
        action_result = phantom.action_result.ActionResult(dict(param))

        return action_result.set_status(phantom.APP_ERROR, "Not implemented yet")

    def _handle_forward_lookup(self, param):
        action_result = phantom.action_result.ActionResult(dict(param))
        self.add_action_result(action_result)

        response = {"in_ip": param["ip"]}
        action_result.add_data(response)

        return phantom.APP_SUCCESS
