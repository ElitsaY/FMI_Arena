import random
import string
from users.service import create_user, login_user


def test_registered_user_can_login(test_app):
    random_name = "".join(random.choices(string.ascii_lowercase, k=10))
    random_password = "".join(random.choices(string.ascii_lowercase, k=10))
    user = create_user(
        random_name,
        "chains",
        f"{random_name}@example.com",
        random_password,
    )
    assert user.first_name == random_name
    assert user.last_name == "chains"
    assert user.email == f"{random_name}@example.com"
    assert user.password  # exists
    logged_in_user = login_user(
        f"{random_name}@example.com",
        random_password,
    )
    assert logged_in_user.email == user.email
