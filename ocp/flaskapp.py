from flask import Config, Flask


class App(Flask):
    config: Config

    def get_config_value_or_exception(self, key):
        val = self.config.get(key)
        if val:
            return val
        raise ValueError
