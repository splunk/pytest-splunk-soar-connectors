from pathlib import Path
from phantom_mock.phantom import vault
import os

def test_add_file_to_vault():
    path = Path(__file__)

    vault.vault_add(1, str(path))

    assert len(vault.__VAULT.files) == 1

def test_vault_info():
    path = Path(__file__)

    success, message, vault_id = vault.vault_add(1, str(path))

    print(vault_id)

    success, message, vault_info = vault.vault_info(vault_id)

    assert vault_info["file_name"] == "test_vault.py"

    vault.__VAULT.root.cleanup()
