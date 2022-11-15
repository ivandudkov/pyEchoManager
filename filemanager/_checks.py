import os

class Checks:
    @staticmethod
    def check_path(path):
        if os.path.exists(path):
            pass
        else:
            raise RuntimeError('Path either not exists or not correct ' + path)
