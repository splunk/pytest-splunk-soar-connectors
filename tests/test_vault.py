from pathlib import Path
from phantom import vault
import os

def test_add_file_to_vault():
    path = Path(__file__)

    vault.vault_add(1, str(path))

    assert len(vault.__VAULT.files) == 1