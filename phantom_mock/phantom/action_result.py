import pprint

class ActionResult:
    def __init__(self, param={}):
        self.param = param
        self.message = ""
        self.status = False
        self.data = []
        self._debug_data = []
        self._extra_data = []
        self.summary = {}
        self.logger = None
        self.pp = pprint.PrettyPrinter(indent=4)
        return

    def set_logger(self, logger):
        self.logger = logger

    def get_message(self):
        return self.message

    def set_status(self, status, message=None, error=None):
        self.status = status
        self.message = message
        self.logger.info(
            "ActionResult.set_status() - Status: {}; Message: {}; Exception: {}".format(
                status, message, str(error)
            )
        )
        return status

    def add_data(self, data):
        self.data.append(data)
        self.logger.info(
            "ActionResult.add_data() - Data (next line):\n{}".format(
                self.pp.pformat(self.data)
            )
        )
        return

    def update_data(self, data):
        self.data.extend(data)
        return

    def get_data(self):
        return self.data

    def get_data_size(self):
        return len(self.data)

    def add_debug_data(self, item):
        self._debug_data.append(str(item))

    def get_debug_data(self):
        return self._debug_data

    def get_debug_data_size(self):
        return len(self._debug_data)

    def add_extra_data(self, item):
        return self._extra_data.append(item)

    def get_extra_data(self):
        return self._extra_data

    def get_extra_data_size(self):
        return len(self._extra_data)

    def update_extra_data(self, item):
        self._extra_data.extend(item)

    def add_exception_details(exception):
        # TODO
        pass

    def update_summary(self, summary):
        self.summary = summary
        self.logger.info(
            "ActionResult.update_summary() - Summary (next line):\n{}".format(
                self.pp.pformat(summary)
            )
        )
        return self.summary

    def set_summary(self, summary):
        self.update_summary(summary)
        return

    def get_status(self):
        return self.status

    def append_to_message(self, message_str):
        self.message += message_str

    def get_summary(self):
        return self.summary

    def get_param(self):
        return self.param

    def update_param(self, param):
        self.param.update(param)

    def set_param(self, param):
        self.param = param

    def get_dict(self) -> dict:
        return {
            "context": {},
            "data": self.data,
            "extra_data": [],
            "message": self.message,
            "parameter": self.param,
            "summary": self.summary,
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ActionResult):
            return hash(str(self.data)) == hash(str(other.data))
        return False



