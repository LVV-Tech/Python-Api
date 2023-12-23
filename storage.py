import sqlite3

conn = sqlite3.connect("vk.db")

sql_file = "init.sql"

cur = conn.cursor()


def init_db():
    try:
        with open(sql_file, "r") as file:
            sql_script = file.read()
        cur.executescript(sql_script)
        conn.commit()
        print("SQL-скрипт успешно выполнен!")
    except sqlite3.Error as e:
        print(f"Ошибка: {e}")


def check_user(login: str, password: str, vk_id: int, tg_id: int) -> bool:
    """
    True => "Вы успешно авторизованы"; False => "Пользователь не найден"
    """
    if login != "":
        res = cur.execute(
            "select login, password from user where login=:login", {"login": login}
        )
        if res[1] == password:
            return True
    if vk_id >= 0:
        res = cur.execute("select vk_id from user where vk_id=:vk_id", {"vk_id": vk_id})
        if len(res.fetchall()) > 0:
            return True
    if tg_id >= 0:
        res = cur.execute("select tg_id from user where tg_id=:tg_id", {"tg_id": tg_id})
        if len(res.fetchall()) > 0:
            return True
    return False


def is_registered(login: str, vk_id: int, tg_id: int) -> bool:
    if login != "" or vk_id != 0 or tg_id != 0:
        res = cur.execute(
            "select login from user where login=:login or vk_id=:vk_id or tg_id=:tg_id",
            {"login": login, "vk_id": vk_id, "tg_id": tg_id},
        )
        if len(res.fetchall()) > 0:
            return True

    return False


def create_user(
    role: int,
    phone: str,
    full_name: str,
    passport: str,
    address: str,
    login: str,
    password: str,
    vk_id: int,
    tg_id: int,
) -> bool:
    if not (is_registered(login, vk_id, tg_id)):
        cur.execute(
            "insert into user(role, phone, full_name, passport, address, login, password, vk_id, tg_id) values (:role, :phone, :full_name, :passport, :address, :login, :password, :vk_id, :tg_id)",
            {
                "role": role,
                "phone": phone,
                "full_name": full_name,
                "passport": passport,
                "address": address,
                "login": login,
                "password": password,
                "vk_id": vk_id,
                "tg_id": tg_id,
            },
        )
        return True
    return False


def get_user(
    login: str,
    vk_id: int,
    tg_id: int,
) -> bool:
    if not (is_registered(login, vk_id, tg_id)):
        cur.execute(
            "select role, phone, full_name, passport, address from user where login=:login or vk_id=:vk_id or tg_id=:tg_id",
            {
                "login": login,
                "vk_id": vk_id,
                "tg_id": tg_id,
            },
        )
        return True
    return False
