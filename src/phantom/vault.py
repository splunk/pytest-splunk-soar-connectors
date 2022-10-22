from pathlib import Path
import pathlib
import tempfile
from typing import Dict
import shutil
import hashlib


class Vault:
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

        return True, "added file to vault", vault_id

    def get_vault_tmp_dir(self) -> pathlib.Path:
        return self.root.name / Path("tmpdir")


__VAULT: Vault = Vault()


def vault_add(container, file_location, file_name=None, metadata=None, trace=False):

    return __VAULT.add(container, file_location, file_name, metadata, trace)


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
