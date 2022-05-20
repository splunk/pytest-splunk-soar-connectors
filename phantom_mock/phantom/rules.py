def vault_add(
    container=None, file_location=None, file_name=None, metadata=None, trace=False
):
    success = True
    message = ""
    vault_id = ""

    return success, message, vault_id


def vault_delete(
    vault_id=None, file_name=None, container_id=None, remove_all=False, trace=False
):
    success = True
    message = ""
    file_names = []

    return success, message, file_names


def vault_info(
    vault_id=None, file_name=None, container_id=None, remove_all=False, trace=False
):
    success = True
    message = ""
    vault_info = []

    return success, message, vault_info
