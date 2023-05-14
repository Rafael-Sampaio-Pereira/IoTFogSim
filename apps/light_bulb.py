from apps.base_app import BaseApp


class LightBulbApp(BaseApp):
    def __init__(self):
        super(LightBulbApp, self).__init__()
        self.name = 'LightBulbApp'