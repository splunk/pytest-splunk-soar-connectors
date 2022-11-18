from pathlib import Path

from phantom.vault import get_vault_tmp_dir, Vault


def test_get_vault_tmp_dir():
    directory = get_vault_tmp_dir()
    print(directory)
    assert "tmpdir" in directory


def test_create_attachment():
    container_id = 1
    file_path = Path(__file__).parent / Path("assets/sample.txt")
    file_name = file_path.name

    file_contents = file_path.read_text("utf-8")
    metadata = {}
    Vault.create_attachment(
        file_contents=file_contents, container_id=container_id, file_name=file_name, metadata=metadata
    )
    
    assert len(Vault._vault.files) == 1
