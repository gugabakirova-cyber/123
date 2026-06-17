class Config:
    SECRET_KEY = "cafe_diploma_secret_key"

    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "2006",   # если пароль есть — впиши сюда
        "database": "cafe_system",
        "charset": "utf8mb4",
        "use_unicode": True
    }


DB_CONFIG = Config.DB_CONFIG
SECRET_KEY = Config.SECRET_KEY