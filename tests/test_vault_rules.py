from pathlib import Path

import phantom.rules as phantom_rules


def test_rules_vault_info():
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    container_id = 123
    file_name = "test_name"
    metadata = {}

    _, _, vault_id = phantom_rules.vault_add(
        file_location=str(file_path),
        container=container_id,
        file_name=file_name,
        metadata=metadata,
    )

    success, _, _ = phantom_rules.vault_info(vault_id=vault_id)

    assert success


def test_rules_vault_add():
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    container_id = 123
    file_name = "test_name"
    metadata = {}

    vault_add_success, vault_add_msg, vault_id = phantom_rules.vault_add(
        file_location=str(file_path),
        container=container_id,
        file_name=file_name,
        metadata=metadata,
    )

    assert vault_add_success
    assert vault_add_msg == "Success"
    assert vault_id == "a1a7ab3d4e6a4dc80809bfe077bb4373"


def test_rules_vault_delete():
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    container_id = 123
    file_name = "test_name"
    metadata = {}

    _, _, vault_id = phantom_rules.vault_add(
        file_location=str(file_path),
        container=container_id,
        file_name=file_name,
        metadata=metadata,
    )

    result = phantom_rules.vault_delete(
        vault_id=vault_id,
        file_name=file_name,
        container_id=container_id,
        remove_all=True,
        trace=True,
    )
    print(result)

    assert result.get("success")
    assert result.get("message") == "deleted from vault"
