from apps.base_app import BaseApp


class ShowerApp(BaseApp):
    def __init__(self):
        super(ShowerApp, self).__init__()
        self.name = 'ShowerApp'