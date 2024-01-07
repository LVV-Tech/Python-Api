import sqlite3

conn = sqlite3.connect("vk.db", check_same_thread=False)

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


def check_user(
    login: str = None, password: str = None, vk_id: int = None, tg_id: int = None
) -> bool:
    """
    True => "Вы успешно авторизованы"; False => "Пользователь не найден"
    """
    if vk_id and vk_id >= 0:
        res = cur.execute(
            "select vk_id from user where vk_id=:vk_id", {"vk_id": vk_id}
        ).fetchall()
        if len(res) > 0:
            return True
    if tg_id and tg_id >= 0:
        res = cur.execute("select tg_id from user where tg_id=:tg_id", {"tg_id": tg_id}).fetchall()
        if len(res) > 0:
            return True
    return False


def is_registered(login: str = None, vk_id: int = None, tg_id: int = None) -> bool:
    if login != "" or vk_id != 0 or tg_id != 0:
        res = cur.execute(
            "select login from user where login=:login or vk_id=:vk_id or tg_id=:tg_id",
            {"login": login, "vk_id": vk_id, "tg_id": tg_id},
        ).fetchall()
        if len(res) > 0:
            return True

    return False


def create_user(
    role: int,
    phone: str,
    full_name: str,
    passport: str = None,
    address: str = None,
    login: str = None,
    password: str = None,
    vk_id: int = None,
    tg_id: int = None,
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
        conn.commit()
        return True
    return False


def get_user(
    login: str,
    vk_id: int,
    tg_id: int,
) -> list[any]:
    if not (is_registered(login, vk_id, tg_id)):
        res = cur.execute(
            "select role, phone, full_name, passport, address from user where login=:login or vk_id=:vk_id or tg_id=:tg_id",
            {
                "login": login,
                "vk_id": vk_id,
                "tg_id": tg_id,
            },
        ).fetchall()
        return res
    return None

def get_user_vk_id(
    vk_id: int,
) -> list[any]:
    if not (is_registered(vk_id)):
        res = cur.execute(
            "select role, phone, full_name, passport, address from user where vk_id=:vk_id",
            {
                "vk_id": vk_id,
            },
        ).fetchall()
        return res
    return None

def get_user_tg_id(
    tg_id: int,
) -> list[any]:
    if not (is_registered(tg_id)):
        res = cur.execute(
            "select role, phone, full_name, passport, address from user where tg_id=:tg_id",
            {
                "tg_id": tg_id,
            },
        ).fetchall()
        return res
    return None
