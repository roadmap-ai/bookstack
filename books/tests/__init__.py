def make_user(**kwargs):
    default_user = {
        "username": "mahi",
        "first_name": "mahima",
        "last_name": "choudhary",
        "email": "mahi87mnit@x.in",
        "password": "1234",
    }

    return default_user | dict(kwargs)
