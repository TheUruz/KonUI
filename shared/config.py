CONFIG = {"app_name": "KonUI"}


class Config:
    __app_name = CONFIG["app_name"]

    @staticmethod
    def get_app_name():
        return Config.__app_name
