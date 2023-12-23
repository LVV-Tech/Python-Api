import storage


if __name__ == "__main__":
    storage.init_db()
    if storage.create_user(
        0,
        "89509141911",
        "Mihail",
        "7012 12309712",
        "huevayeet",
        "govno",
        "zalupa",
        0,
        0,
    ):
        print("User created")

    if storage.check_user:
        print("Вы авторизованы")
