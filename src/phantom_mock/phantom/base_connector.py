import json
import logging
from typing import List
import uuid
from rich.logging import RichHandler
import glob
import inspect
import os
import pprint
from tempfile import NamedTemporaryFile, TemporaryDirectory
from abc import ABC, abstractmethod

from pytest_splunk_soar_connectors.models import Artifact
from . import app as phantom


class BaseConnector(ABC):
    def __init__(self):
        # asset configuration settings
        self.config = {}
        self.action_results = []

        # other asset settings
        self.asset_id = "default-asset-id"

        # app settings
        self.app_id = "default-app-id"
        self.app_json_file_loc = None

        # log settings
        self.log_path = "debug_log.log"
        self.log_to_console = True
        self._setup_logger()

        # current container settings
        self.container_id = 123

        # the following is an example
        self.container_info = {
            "1": {"container_info_would_go_here": True},
            "2": {"container_info_would_go_here": True},
        }
        # used when saving containers
        self.starting_container_id = 2

        # artifact settings
        self.starting_artifact_id = 1

        # product information settings
        self.product_install_id = "1234"
        self.product_version = "4.5.15370"

        # state settings
        self.state_file_location = NamedTemporaryFile().name

        # polling settings
        self.poll_now = False

        # baseurl
        self.base_url = "https://127.0.0.1"

        # internal trackers
        self.message = ""
        self.progress_message = ""
        self.state = None
        self.status = None
        self.action_results = []
        self.pp = pprint.PrettyPrinter(indent=4)
        self.action_identifier = ""
        self.__action_run_id = str(uuid.uuid4())

        # Mock test helpers - those are not part of the BaseConnector API but have been added here
        self.__progress = []
        self.__artifacts = []

        return

    def _setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            filename=(self.log_path or "debug_log.log"),
            filemode="a",
        )
        self.logger = logging.getLogger(__name__)

        # Add console output if configured
        if self.log_to_console:
            self.logger.addHandler(RichHandler())

    def _config_parser_to_dict(self, config_parser):
        return {s: dict(config_parser.items(s)) for s in config_parser.sections()}

    def get_config(self) -> dict:
        return self.config

    def get_phantom_base_url(self):
        return self.base_url

    def get_container_id(self):
        return self.container_id

    def get_container_info(self, container_id=None):
        if not container_id:
            container_id = self.container_id
        return True, self.container_info[container_id], "200"

    def get_product_installation_id(self):
        return self.product_install_id

    def get_product_version(self):
        return self.product_version

    def load_state(self):
        try:
            with open(self.state_file_location, "r+") as state_file:
                self.state = json.loads(state_file.read() or "{}")
            self.logger.info(
                "load_state() - State: {}".format(self.pp.pformat(self.state))
            )
            return self.state
        except Exception as e:
            print(e)
            return None

    def get_state(self):
        return self.state

    def save_state(self, state=None):
        self.state = state or self.state
        with open(self.state_file_location, "w+") as state_file:
            state_file.write(json.dumps(self.state))
        self.logger.info("save_state() - State: {}".format(self.pp.pformat(self.state)))
        return

    def save_artifact(self, artifact):
        artifact_id = self.starting_artifact_id
        self.starting_artifact_id += 1
        self.__artifacts.append(artifact)
        return (phantom.APP_SUCCESS, "Artifact saved", artifact_id)

    def save_artifacts(self, artifacts: List[Artifact]):
        return_val = []
        for artifact in artifacts:
            self.__artifacts.append(artifact)
            return_val.append(
                [phantom.APP_SUCCESS, "Artifact saved", self.starting_artifact_id]
            )
            self.starting_artifact_id += 1

        return return_val

    def save_container(self, container):
        container_id = self.container_artifact_id
        self.starting_container_id += 1
        return (phantom.APP_SUCCESS, "Container saved", container_id)

    def save_containers(self, containers):
        return_val = []
        for container in containers:
            return_val.append(
                [phantom.APP_SUCCESS, "Container saved", self.starting_container_id]
            )
            self.starting_container_id += 1

        return return_val

    def debug_print(self, message, dump_obj=None):
        self.logger.debug(
            "BaseConnector.debug_print - Message: {}; Object (next line):\n{}".format(
                message, (self.pp.pformat(dump_obj) if dump_obj else "")
            )
        )
        return

    def error_print(self, message, dump_obj=None):
        self.logger.error(
            "BaseConnector.error_print - Message: {}; Object (next line):\n{}".format(
                message, (self.pp.pformat(dump_obj) if dump_obj else "")
            )
        )
        return

    def set_status(self, status, message=None, error=None):
        self.status = status
        self.message = message
        self.logger.info(
            "BaseConnector.set_status - State: {}; Message: {};".format(status, message)
        )
        return status

    def append_to_message(self, message):
        self.message += message
        self.logger.info(
            "BaseConnector.append_to_message - Message: {}".format(message)
        )
        return

    def set_status_save_progress(self, status, message):
        self.status = status
        self.progress_message = message
        self.logger.info(
            "BaseConnector.set_status_save_progress - Status: {}, Message: {}".format(
                status, message
            )
        )
        return self.status

    def send_progress(self, message):
        self.progress_message = message
        self.logger.info("BaseConnector.send_progress - Progress: {}".format(message))
        return

    def save_progress(self, message, more=None):
        self.progress_message = message
        self.__progress.append(message)
        self.logger.info(
            "BaseConnector.save_progress - Progress: {}; More: {}".format(message, more)
        )
        return

    def add_action_result(self, action_result):
        action_result.set_logger(self.logger)
        self.action_results.append(action_result)
        return action_result

    def remove_action_result(self, action_result_to_remove):
        for i, action_result in enumerate(self.action_results):
            if action_result == action_result_to_remove:
                del self.action_results[i]

    def get_action_results(self):
        return self.action_results

    def get_status(self):
        return self.status

    def get_status_message(self):
        return self.message

    def get_action_identifier(self):
        return self.action_identifier

    def is_poll_now(self):
        return self.poll_now

    def get_app_id(self):
        return self.app_id

    def get_connector_id(self):
        return self.app_id

    def get_app_config(self):
        return self.__app_json["app_config"]

    def get_ca_bundle(self):
        return NotImplemented

    def get_app_json(self):
        return self.__app_json

    def get_asset_id(self):
        return self.asset_id

    def update_summary(self, summary):
        self.summary = summary

    def set_validator(self, type=None, validation_function=None):
        # TODO: Make this do something. For now, it does nothing
        return None

    def _is_app_json(self, json_file_path, connector_py):

        self.debug_print("Connector class File: {0}".format(connector_py))
        # Load the file
        with open(json_file_path) as app_json_file:
            try:
                app_json = json.load(app_json_file)
                connector_file = app_json.get("main_module")  # pylint: disable=E1103
                if connector_file:
                    connector_file = connector_file[: connector_file.find(".")]
                    if connector_file == connector_py:
                        self.__app_json = app_json
                        return True
            except Exception as e:
                self.debug_print(
                    "Failed to load JSON: {0}, reason: {1}".format(
                        json_file_path, getattr(e, "message", str(e))
                    )
                )
                return False

        return False

    def _load_app_json(self):
        dirpath = os.path.dirname(inspect.getfile(self.__class__))
        # get the directory of the derived class
        dirpath = os.path.dirname(inspect.getfile(self.__class__))
        self.debug_print("Derived class dir: '{}'".format(dirpath))
        if not dirpath:
            dirpath = os.curdir

        # Create the glob to the json file
        json_file_glob = "{0}/*.json".format(dirpath)

        # Check if it exists
        files_matched = glob.glob(json_file_glob)

        # Get the connector file
        connector_py_file = inspect.getfile(self.__class__)
        self.debug_print("connector_py_file: {0}".format(connector_py_file))

        # Split into head and tail
        connector_py = os.path.split(connector_py_file)

        # get the tail, which will be the file name
        connector_py = connector_py[1]

        self.debug_print("connector_py: {0}".format(connector_py))

        # The extension of the file could be pyc or py
        connector_py = connector_py[: connector_py.find(".")]

        json_file = None
        for file_path in files_matched:
            if self._is_app_json(file_path, connector_py):
                json_file = file_path
                break

        if json_file is None:
            return self.set_status(phantom.APP_ERROR, "Could not load Connector")

        self.debug_print("App Json:", self.__app_json)
        self.app_id = self.__action_json["appid"]

        return phantom.APP_SUCCESS

    def get_state_file_path(self):
        self.state_dir + "statefile"

    def get_state_dir(self):
        return self.state_dir

    def get_current_param(self):
        return self.__action_json["parameters"]

    def handle_cancel(self):
        pass

    @abstractmethod
    def finalize(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def handle_action(self, parameters):
        pass

    def validate_parameters(self, parameters):
        raise NotImplementedError

    def _handle_action(self, in_json, handle) -> str:

        self.__action_json = json.loads(in_json)
        success = self._load_app_json()
        with TemporaryDirectory() as tmp_dir:
            self.state_dir = tmp_dir

            for param in self.__action_json["parameters"]:
                self.__current_param = param
                try:
                    self.action_identifier = self.__action_json["parameters"][
                        "identifier"
                    ]
                    self.initialize()
                    self.handle_action(self.__action_json["parameters"])
                except KeyboardInterrupt:
                    self.__was_cancelled = True
                    self.handle_cancel()
                except Exception as error:
                    logging.exception(error)
                    self.handle_exception(error)

        self.logger.info(json.dumps(list(r.get_dict() for r in self.action_results)))
        self.finalize()
        return json.dumps(list(r.get_dict() for r in self.action_results))

    def handle_exception(self, exception: Exception):
        raise exception

    def is_action_cancelled(self):
        return self.__was_cancelled

    def is_fail(self):
        return phantom.is_fail(self.status)

    def is_success(self):
        return not phantom.is_success(self.status)