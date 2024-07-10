import configparser

class Config:
    class Visualization:
        def __init__(self, data):
            self.color = '#BDB76B'
            self.prediction_color = '#F08080'
            self.width = int(data['width'])
    def __init__(self, config: str):
        config_ = configparser.ConfigParser()
        config_.read(config)
        self.visualization = self.Visualization(config_['visualization'])

config = Config("config.ini")