import glob
import inspect
import json
import logging
import os
import pprint
import uuid
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import List, Optional, Tuple, Union
import pathlib

from rich.logging import RichHandler

from pytest_splunk_soar_connectors.models import Artifact
from phantom.action_result import ActionResult

from . import app as phantom


class BaseConnector(ABC):
    __message: str = ""

    def __init__(self):
        # asset configuration settings
        self.config = {}
        self.__action_results = []

        # other asset settings
        self.asset_id = "default-asset-id"

        # app settings
        self.app_id = "default-app-id"
        self.app_json_file_loc = None
        self.__app_json = None

        # log settings
        self.log_path = "debug_log.log"
        self.log_to_console = True
        self._setup_logger()

        # current container settings
        self.container_id = 123
        self.container_artifact_id = 1234

        # state
        self.state_file_location = NamedTemporaryFile().name
        self.state_dir = TemporaryDirectory()

        # the following is an example
        self.container_info = {
            "1": {"container_info_would_go_here": True},
            "2": {"container_info_would_go_here": True},
            "123": {"container_info_would_go_here": True},
        }
        # used when saving containers
        self.starting_container_id = 2

        # artifact settings
        self.starting_artifact_id = 1

        # product information settings
        self.product_install_id = "1234"
        self.product_version = "4.5.15370"

        # polling settings
        self.poll_now = False

        # baseurl
        self.base_url = "https://127.0.0.1"

        # internal trackers
        self.__message = ""
        self.__progress_message = ""
        self._state = None
        self.__status = False
        self.__action_results = []
        self.__pretty_printer = pprint.PrettyPrinter(indent=4)
        self.action_identifier = ""

        # pylint: disable=unused-private-member
        self.__action_run_id = str(uuid.uuid4())
        self.__action_json = None

        self.summary = {}
        self.__was_cancelled = False

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
        """Returns the current connector run configuration dictionary.

        Returns:
            dict: connector run configuration
        """
        return self.config

    def get_phantom_base_url(self):
        return self.base_url

    def get_container_id(self) -> int:
        """Returns the current container ID passed in the connector run action JSON.

        Returns:
            int: container id
        """
        return self.container_id

    def get_container_info(self, container_id: Optional[int] = None) -> Tuple[bool, dict, str]:
        """Returns info about the container. If container_id is not passed, returns info about the current container.

        Args:
            container_id (Optional[int], optional): Container ID. Defaults to current container id when None is passed.

        Returns:
            Tuple[bool, dict, str]: Returns error value, container info dict and a response code
        """

        if not container_id:
            container_id = self.container_id
        return True, self.container_info[str(container_id)], "200"

    def get_product_installation_id(self) -> str:
        """Returns the unique ID of the Splunk SOAR (Cloud) product installation.

        Returns:
            string: product installation id
        """
        return self.product_install_id

    def get_product_version(self) -> str:
        """Returns the version of Splunk SOAR (Cloud).

        Returns:
            string: product version
        """
        return self.product_version

    def load_state(self) -> Union[None, dict]:
        """Loads the current state file into the state dictionary. If a state file does not exist, it creates one with the app_version field. This returns the state dictionary. If an error occurs, this returns None.

        Returns:
            Union[None, dict]: state dict or none
        """
        try:
            with open(self.state_file_location, "r+", encoding="utf-8") as state_file:
                self._state = json.loads(state_file.read() or "{}")
            self.logger.info("load_state() - State: %s", self.__pretty_printer.pformat(self._state))
            return self._state
        # pylint:disable=broad-except
        # TODO: This may be problematic if the state exists, but loading it actually fails
        except Exception as exc:
            if self._state is None:
                self._state = {}
            print(exc)
            return {}

    def get_state(self) -> Union[dict, None]:
        """Gets the current state dictionary of the asset. Will return None if load_state() has not been previously called.

        Returns:
            Union[dict, None]: returns state dict or none
        """
        return self._state

    def save_state(self, state: dict):
        """Writes a given dictionary to a state file that can be loaded during future app runs. This is especially crucial with ingestion apps. The saved state is unique per asset. An app_version field will be added to the dictionary before saving.

        Args:
            state (dict): The dictionary to write to the state file.
        """

        if self._state:
            self._state = {**self._state, **state}
        else:
            self._state = state
        with open(self.state_file_location, "w+", encoding="utf-8") as state_file:
            state_file.write(json.dumps(self._state))
        self.logger.info("save_state() - State: %s", self.__pretty_printer.pformat(self._state))
        return

    def save_artifact(self, artifact: Artifact) -> Tuple[bool, str, int]:
        """Saves an artifact to Splunk SOAR (Cloud).

        Args:
            artifact (dict): Dictionary containing information about an artifact.

        Returns:
            Tuple[bool, str, int]: status, status message, saved artifact ID if successful
        """
        artifact_id = self.starting_artifact_id
        self.starting_artifact_id += 1
        self.__artifacts.append(artifact)
        return (phantom.APP_SUCCESS, "Artifact saved", artifact_id)

    def save_artifacts(self, artifacts: List[Artifact]) -> Tuple[bool, str, List[int]]:
        """Saves a list of artifacts to Splunk SOAR (Cloud).

        Args:
            artifacts (List[Artifact]): A list of dictionaries that each contain artifact data. Don't set the run_automation key for the any artifacts as the API will automatically set this value to 'False' for all but the last artifact in the list to start any active playbooks after the last artifact is ingested.

        Returns:
            Tuple[bool, str, List[int]]: status, status message, list of saved artifact IDs if successful, none otherwise
        """
        return_val = []
        for artifact in artifacts:
            self.__artifacts.append(artifact)
            return_val.append(self.starting_artifact_id)
            self.starting_artifact_id += 1

        return phantom.APP_SUCCESS, "Artifact saved", return_val

    def save_container(self, container: dict) -> Tuple[bool, str, int]:
        """Saves a container and artifacts to Splunk SOAR (Cloud).

        Args:
            container (dict): Dictionary containing info about a container

        Returns:
            Tuple[bool, str, int]: status, status message, container id
        """
        container_id = self.container_artifact_id
        self.starting_container_id += 1
        # Not actually adding a container currently

        return (phantom.APP_SUCCESS, "Container saved", container_id)

    def save_containers(self, containers: List[dict]) -> Tuple[bool, str, List[Tuple[bool, str, int]]]:
        """Saves a list of containers to the phantom platform.

        Args:
            containers (List[dict]): A list of dictionaries that each contain information about a container. Each dictionary follows the same rules as the input to save_container.

        Returns:
            Tuple[bool, str, List[Tuple[bool, str, int]]]: _description_
        """
        return_val = []
        for _ in containers:
            return_val.append([phantom.APP_SUCCESS, "Container saved", self.starting_container_id])
            self.starting_container_id += 1

        return phantom.APP_SUCCESS, "Containers saved", return_val

    def debug_print(self, tag: str, dump_obj: object = False):
        """Dumps a pretty printed version of the 'dump_object' in the <syslog>/phantom/spawn.log file, where <syslog> typically is /var/log/.

        Args:
            tag (str): The string that is prefixed before the dump_object is dumped.
            dump_obj (object, optional): The dump_object to dump. If the object is a list, dictionary and so on it is automatically pretty printed. Defaults to False.
        """
        out = ""

        if dump_obj:
            out = self.__pretty_printer.pformat(dump_obj)

        self.logger.debug("BaseConnector.debug_print - Message: %s; Object (next line):\n%s", tag, out)
        return

    def error_print(self, tag: str, dump_obj: object = False):
        """Dumps an ERROR as a pretty printed version of the 'dump_object' in the <syslog>/phantom/spawn.log file, where <syslog> typically is /var/log/. Refrain from using this API to dump an error that is handled by the App. By default the log level of the platform is set to ERROR.

        Args:
            tag (str): The string that is prefixed before the dump_object is dumped.
            dump_obj (object, optional): The dump_object to dump. If the object is a list, dictionary and so on it is automatically pretty printed. Defaults to False.
        """
        out = ""

        if dump_obj:
            out = self.__pretty_printer.pformat(dump_obj)

        self.logger.error("BaseConnector.error_print - Message: %s; Object (next line):%s", tag, out)
        return

    def set_status(self, status: bool, message: Optional[str] = None, error: Optional[str] = None) -> bool:
        """Sets the status of the connector run result, phantom.APP_SUCCESS or phantom.APP_ERROR. Optionally, you can set the message. If an exception object is specified, it is recorded in the connector run result. It will replace any status and message previously saved in the object. Returns the status_code set.

        Args:
            status (bool): phantom.APP_SUCCESS or phantom.APP_ERROR
            message (Optional[str], optional): status message. Defaults to None.
            error (Optional[str], optional): status error. Defaults to None.

        Returns:
            bool: status
        """
        self.__status = status
        if message:
            self.__message = message
        self.logger.info("BaseConnector.set_status - State: %s; Message: %s; Error: %s", status, message, error)
        return status

    def append_to_message(self, message: str):
        """Appends a string to the current result message.

        Args:
            message (str): The string that is to be appended to the existing message
        """
        self.__message += message
        self.logger.info("BaseConnector.append_to_message - Message: %s", message)
        return

    def set_status_save_progress(self, status: bool, message: str) -> bool:
        """Helper function that sets the status of the connector run. This needs to be phantom.APP_SUCCESS or phantom.APP_ERROR

        Args:
            status (bool): status to set
            message (str): status message

        Returns:
            bool: status that was set
        """

        self.__status = status
        self.__progress_message = message
        self.logger.info("BaseConnector.set_status_save_progress - Status: %s, Message: %s", status, message)
        return self.__status

    def send_progress(self, message: str):
        """Sends a progress message to the Splunk SOAR core. It is written to persistent storage, but is overwritten by the message that comes in through the next send_progress call

        Args:
            message (str): message to send
        """
        self.__progress_message = message
        self.logger.info("BaseConnector.send_progress - Progress: %s", message)
        return

    def save_progress(self, message: str, more=None):
        """Sends a progress message to the Splunk SOAR core, which is saved in persistent storage.

        Args:
            message (str): The progress message to send to the Splunk Phantom core. Typically, this is a short description of the current task.
            more (str, optional): The various parameters that need to be formatted into the progress_str_config string. Defaults to none.
        """
        self.__progress_message = message
        self.__progress.append(message)
        self.logger.info("BaseConnector.save_progress - Progress: %s; More: %s", message, more)
        return

    def add_action_result(self, action_result: ActionResult) -> ActionResult:
        """Add an ActionResult object into the connector run result. Returns the object added.

        Args:
            action_result (ActionResult): The ActionResult object to add to the connector run.

        Returns:
            ActionResult: The ActionResult added to the connector run
        """
        action_result.set_logger(self.logger)
        self.__action_results.append(action_result)
        return action_result

    def remove_action_result(self, action_result: ActionResult) -> ActionResult:
        """Removes an ActionResult object from the connector run result. Returns the removed object.

        Args:
            action_result (ActionResult): The ActionResult object that is to be removed from the connector run.
        Raises:
            Exception: In case the action result is not found
        Returns:
            ActionResult: The ActionResult that was removed
        """

        for i, action_result in enumerate(self.__action_results):
            if action_result == action_result:
                return self.__action_results.pop(i)
        raise Exception("Could not find action Result")

    def get_action_results(self) -> List[ActionResult]:
        """Returns the list of ActionResult objects added to the connector run.

        Returns:
            List[ActionResult]: List of action results
        """
        return self.__action_results

    def get_status(self) -> bool:
        """Gets the current status of the connector run. Returns either phantom.APP_SUCCESS or phantom.APP_ERROR.

        Returns:
            bool: current status of the connector run
        """
        return self.__status

    def get_status_message(self) -> str:
        """Gets the current status message of the connector run.

        Returns:
            str: current status message
        """
        return self.__message

    def get_action_identifier(self) -> str:
        """Returns the action identifier that the AppConnector is supposed to run.

        Returns:
            str: Action Identifier
        """
        return self.action_identifier

    def is_poll_now(self) -> bool:
        """The on_poll action is called during Poll Now and scheduled polling. Returns 'True' if the current on_poll is run through the Poll Now button. Otherwise, it returns 'False'.

        Returns:
            bool: whether or not it is a poll-now execution
        """
        return self.poll_now

    def get_app_id(self) -> str:
        """Returns the appid of the app that was specified in the app JSON.

        Returns:
            str: The appid of the app
        """
        return self.app_id

    def get_connector_id(self) -> str:
        """Returns the appid of the app that was specified in the app JSON.

        Returns:
            str: appid of the app
        """
        return self.app_id

    def get_app_config(self) -> dict:
        """Returns the app configuration dictionary.

        Raises:
            Exception: If the app configuration cannot be retrieved

        Returns:
            dict: App configuration
        """
        if self.__app_json:
            return self.__app_json
        raise Exception("Could not retrieve app config")

    def get_ca_bundle(self) -> str:
        """Returns the current CA bundle file.

        Raises:
            NotImplementedError: Currently not implemented

        Returns:
            str: CA Bundle File Path
        """
        raise NotImplementedError

    def get_app_json(self) -> dict:
        """Returns the complete app JSON as a dictionary.

        Returns:
            dict: app JSON in diction_
        """
        return self.get_app_config()

    def get_asset_id(self) -> str:
        """Returns the current asset ID passed in the connector run action JSON.

        Returns:
            str: The asset ID in string format.
        """
        return self.asset_id

    def update_summary(self, summary: dict):
        """Updates the connector run summary dictionary with the passed dictionary.

        Args:
            summary (dict): summary dictionary to update
        """
        if self.summary:
            self.summary = {**self.summary, **summary}
        else:
            self.summary = summary

    # pylint:disable=unused-argument,redefined-builtin
    def set_validator(self, type=None, validation_function=None):
        # TODO: Validators are a rarely used feature and not implemented yet.
        raise NotImplementedError

    def _is_app_json(self, json_file_path, connector_py):

        self.debug_print(f"Connector class File: {connector_py}")
        # Load the file
        with open(json_file_path, encoding="utf-8") as app_json_file:
            try:
                app_json = json.load(app_json_file)
                connector_file = app_json.get("main_module")  # pylint: disable=E1103
                if connector_file:
                    connector_file = connector_file[: connector_file.find(".")]
                    if connector_file == connector_py:
                        self.__app_json = app_json
                        return True
            # pylint:disable=broad-except
            except Exception as exc:
                reason = getattr(exc, "message", str(exc))
                self.debug_print(f"Failed to load JSON: {json_file_path}, reason: {reason}")
                return False

        return False

    def _load_app_json(self):
        dirpath = os.path.dirname(inspect.getfile(self.__class__))
        # get the directory of the derived class
        dirpath = os.path.dirname(inspect.getfile(self.__class__))
        self.debug_print(f"Derived class dir: '{dirpath}'")
        if not dirpath:
            dirpath = os.curdir

        # Create the glob to the json file
        json_file_glob = f"{dirpath}/*.json"

        # Check if it exists
        files_matched = glob.glob(json_file_glob)

        # Get the connector file
        connector_py_file = inspect.getfile(self.__class__)
        self.debug_print(f"connector_py_file: {connector_py_file}")
        # Split into head and tail
        connector_py = os.path.split(connector_py_file)

        # get the tail, which will be the file name
        connector_py = connector_py[1]

        self.debug_print(f"connector_py: {connector_py}")

        # The extension of the file could be pyc or py
        connector_py = connector_py[: connector_py.find(".")]

        json_file = None
        for file_path in files_matched:
            if self._is_app_json(file_path, connector_py):
                json_file = file_path
                break

        if json_file is None:
            return self.set_status(phantom.APP_ERROR, "Could not load Connector")

        if not self.__app_json:
            return self.set_status(phantom.APP_ERROR, "Could not find App ID in JSON")

        self.app_id = self.__app_json["appid"]

        return phantom.APP_SUCCESS

    def get_state_file_path(self) -> str:
        """Get the full current state file path.

        Returns:
            str: state file path
        """
        state_file_path = pathlib.Path(self.state_dir.name) / pathlib.Path("statefile")
        return str(state_file_path)

    def get_state_dir(self) -> str:
        """Used for apps that must create files to access during action executions. It can use the state directory returned by this API to store such files.

        Returns:
            str: state file directory
        """
        return self.state_dir.name

    def get_current_param(self) -> dict:
        """Returns the current parameter dictionary that the app is working on.

        Returns:
            dict: param dictionary
        """
        if self.__action_json:
            return self.__action_json["parameters"]
        return {}

    def handle_cancel(self):
        """Optional function that can be implemented by the AppConnector. Called if the BaseConnector::_handle_action function code throws an exception that is not handled."""

    def finalize(self):
        """Optional function that can be implemented by the AppConnector. Called by the BaseConnector once all the elements in the parameter list are processed."""

    @abstractmethod
    def initialize(self):
        """Optional function that can be implemented by the AppConnector. It is called once before starting the parameter list iteration, for example, before the first call to AppConnector::handle_action()"""

    @abstractmethod
    def handle_action(self, param: dict) -> bool:
        """Every AppConnector is required to implement this function. It is called for every parameter dictionary in the parameter list.

        Args:
            param (dict): current param dictionary

        Returns:
            bool: return value (phantom.APP_ERROR or phantom.APP_SUCCESS)
        """

    def validate_parameters(self, parameters):
        raise NotImplementedError

    def _handle_action(self, in_json, handle) -> str:

        self.__action_json = json.loads(in_json)

        _ = self._load_app_json()

        # pylint:disable=broad-except
        for param in self.__action_json["parameters"]:
            current_param = param
            try:
                self.action_identifier = self.__action_json["identifier"]
                self.initialize()
                ret_val = self.handle_action(current_param)
                self.__status = ret_val
            except KeyboardInterrupt:
                self.__was_cancelled = True
                self.handle_cancel()
            except Exception as error:
                logging.exception(error)
                self.handle_exception(error)

        self.logger.info(json.dumps(list(r.get_dict() for r in self.__action_results)))
        self.finalize()
        self.state_dir.cleanup()
        return json.dumps(list(r.get_dict() for r in self.__action_results))

    def handle_exception(self, exception: Exception):
        raise exception

    def is_action_cancelled(self) -> bool:
        """Returns 'True' if the connector run was cancelled. Otherwise, it returns as 'False'.

        Returns:
            bool: whether or not the action was cancelled
        """
        return self.__was_cancelled

    def is_fail(self) -> bool:
        """Returns 'True' if the status of the connector run result is failure. Otherwise, it returns as 'False'.

        Returns:
            bool: whether or not the connector run result is failure
        """
        return phantom.is_fail(self.__status)

    def is_success(self) -> bool:
        """Returns 'True' if the status of the connector run result is success. Otherwise, it returns as 'False'.

        Returns:
            bool: whether or not the connector run result is success
        """
        return not phantom.is_success(self.__status)
