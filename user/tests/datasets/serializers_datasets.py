from user.tests.datasets.user_datasets import get_user_object


def get_register_by_system_serializer_data():
    data = get_user_object()
    del data["is_active"]
    data["lng"] = data["coordinates"].x
    data["lat"] = data["coordinates"].y
    del data["coordinates"]
    data["confirm_password"] = data["password"]
    return data
