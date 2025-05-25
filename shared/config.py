CONFIG = {"app_name": "KonsaveUI"}


class Config:
    __app_name = CONFIG["app_name"]

    @staticmethod
    def get_app_name():
        return Config.__app_name
