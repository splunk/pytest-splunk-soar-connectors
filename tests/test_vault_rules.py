import phantom.rules as phantom_rules
from phantom.vault import Vault
 
from pathlib import Path

def test_rules_vault_info():
    vault_id = "sample_id"
    success, message, vault_info = phantom_rules.vault_info(vault_id=vault_id)

    assert success == True


def test_rules_vault_add():
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    container_id = 123
    file_name = "test_name"
    metadata = {}

    vault_add_success, vault_add_msg, vault_id = phantom_rules.vault_add(
        file_location=file_path,
        container=container_id,
        file_name=file_name,
        metadata=metadata,
    )

    assert vault_add_success == True
    assert vault_add_msg == "Success"
    assert vault_id == "a1a7ab3d4e6a4dc80809bfe077bb4373"
     


def test_rules_vault_delete():    
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    container_id = 123
    file_name = "test_name"
    metadata = {}

    vault_add_success, vault_add_msg, vault_id = phantom_rules.vault_add(
        file_location=file_path,
        container=container_id,
        file_name=file_name,
        metadata=metadata,
    )

    success, message, deleted_files = phantom_rules.vault_delete(
        vault_id=vault_id,
        file_name=file_name,
        container_id=container_id,
        remove_all=True,
        trace=True,
    )
    print(message)

    assert message == "deleted from vault"
