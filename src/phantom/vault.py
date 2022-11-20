# pylint: disable=protected-access

from pathlib import Path
import pathlib
import tempfile
from typing import Dict, Union
import shutil
import hashlib


class VirtualVault:
    """VirtualVault is the internal representation backing the Vault and the Rules API"""

    def __init__(self) -> None:
        self.root = tempfile.TemporaryDirectory()
        self.files: Dict[str, Dict] = {}

    def isempty(self):
        return len(self.files) == 0

    def add(
        self,
        container: Union[dict, int],
        file_location: str,
        file_name: str,
        metadata: dict,
        trace: bool = False,
    ):
        print(f"trace: {trace}")

        container_dir = self.root.name / Path(str(container))
        container_dir.mkdir(parents=True, exist_ok=True)

        file_name = Path(file_location).name
        target_location = container_dir / Path(file_name)

        shutil.copyfile(file_location, target_location)

        with target_location.open("rb") as f_to_read:
            file_hash = hashlib.md5()
            while chunk := f_to_read.read(8192):
                file_hash.update(chunk)

        vault_id = file_hash.hexdigest()

        self.files[vault_id] = {
            "file_name": file_name,
            "metadata": metadata,
            "path": target_location,
            "hash": vault_id,
            "vault_id": vault_id,
            "container": container,
        }

        return True, "Success", vault_id

    def delete(self, vault_id):
        file_to_delete = self.files[vault_id]
        del self.files[vault_id]
        return True, file_to_delete

    def get_vault_tmp_dir(self) -> pathlib.Path:
        path = self.root.name / Path("tmpdir")
        path.mkdir(exist_ok=True)
        return path


def get_vault_tmp_dir():
    return str(Vault._vault.get_vault_tmp_dir())


class VaultAPI:
    """VaultAPI is the class encapsulating the App Vault API"""

    def __init__(self) -> None:
        self._vault = VirtualVault()

    def create_attachment(self, file_contents: str, container_id: int, file_name: str, metadata: dict):

        tmp_file = self._vault.get_vault_tmp_dir() / "tmpfile"
        tmp_file.touch(exist_ok=True)
        tmp_file.write_text(file_contents)

        self._vault.add(container=container_id, file_location=str(tmp_file), file_name=file_name, metadata=metadata)


# Vault API
Vault: VaultAPI = VaultAPI()

# Rules API https://docs.splunk.com/Documentation/SOAR/current/PlaybookAPI/VaultAPI


def vault_add(
    container: Union[dict, int],
    file_location: str,
    file_name: Union[str, None] = None,
    metadata: Union[dict, None] = None,
    trace: bool = False,
):
    """
    The container parameter deviates from the real Vault Automation API where it is optional.

    Due to the structure of the Mock, it's non-trivial and probably not worth the
    effort to mirror that functionality. Most calling code on github.com/splunk-soar-connectors
    provides that parameter.

    Ideally, you can simply use self.get_container_id() in the calling code to get the ID.
    """
    if isinstance(container, dict):
        container = container["id"]

    if not file_name:
        file_name = Path(file_location).name

    if not metadata:
        metadata = {}

    return Vault._vault.add(container, file_location, file_name, metadata, trace=trace)


def vault_delete(vault_id: str, file_name: str, container_id: int, remove_all: bool, trace: bool):
    print(f"file_name={file_name} container_id={container_id} remove_all={remove_all} trace={trace}")

    success, deleted_file = Vault._vault.delete(vault_id)

    return {
        "success": success,
        "message": "deleted from vault",
        "deleted_files": [deleted_file],
    }


def vault_info(vault_id, file_name=None, container_id=None, trace=False):
    print(f"file_name={file_name} container_id={container_id} trace={trace}")

    if Vault._vault.isempty():
        raise Exception("Cannot get file info from uninitialized Vault")

    file = Vault._vault.files.get(vault_id)

    if not file:
        return False, "file not found in vault", []

    success = True
    message = "successfully retrieved file from vault"

    return success, message, file
