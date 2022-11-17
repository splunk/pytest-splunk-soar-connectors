from pathlib import Path
import pathlib
import tempfile
from typing import Dict
import shutil
import hashlib


class VirtualVault:
    """VirtualVault is the internal representation backing the Vault and the Rules API"""

    def __init__(self) -> None:
        self.root = tempfile.TemporaryDirectory()
        self.files: Dict[str, Dict] = {}

    def isempty(self):
        return len(self.files) == 0

    def add(self, container, file_location, file_name, metadata, trace):
        container_dir = self.root.name / Path(str(container))
        container_dir.mkdir(parents=True, exist_ok=True)

        file_name = Path(file_location).name
        target_location = container_dir / Path(file_name)

        shutil.copyfile(file_location, target_location)

        with target_location.open("rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
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
        file = self.files[vault_id]
        del self.files[vault_id]
        return True, file

    def get_vault_tmp_dir(self) -> pathlib.Path:
        return self.root.name / Path("tmpdir")


class VaultAPI:
    """VaultAPI is the class encapsulating the App Vault API"""

    def __init__(self) -> None:
        self._vault = VirtualVault()

    def create_attachment(
        self, file_contents: str, container_id: int, file_name: str, metadata: dict
    ):
        pass

    def add_attachment(
        self, local_path: str, container_id: int, file_name: str, metadata=dict
    ):
        succeeded, added_to_vault, id = self.__vault.add(
            container_id, local_path, file_name, metadata, trace=False
        )

        return {
            "succeeded": succeeded,
        }

    def get_vault_tmp_dir(self):
        pass

    def get_file_path(self, vault_id: int):
        pass

    def get_file_info(self, vault_id: int, file_name: str, container_id: int):
        pass


# Vault API
Vault: VaultAPI = VaultAPI()

# Rules API


def vault_add(container, file_location, file_name=None, metadata=None, trace=False):
    return Vault._vault.add(container, file_location, file_name, metadata, trace=trace)


def vault_delete(
    vault_id: str, file_name: str, container_id: int, remove_all: bool, trace: bool
):
    success, file = Vault._vault.delete(vault_id)

    return {
        "success": success,
        "message": "deleted from vault",
        "deleted_files": [file],
    }


def vault_info(
    vault_id, file_name=None, container_id=None, remove_all=False, trace=False
):

    if __VAULT.isempty():
        raise Exception("Cannot get file info from uninitialized Vault")

    file = __VAULT.files.get(vault_id)

    if not file:
        return False, "file not found in vault", []

    success = True
    message = "successfully retrieved file from vault"
    vault_info = file

    return success, message, vault_info


def add_attachment(local_path: str, container_id: int, file_name: str, metadata: dict):
    return __VAULT.add(container_id, local_path, file_name, metadata, trace=None)
