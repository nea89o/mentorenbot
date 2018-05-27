from typing import List

import yaml


class Config(object):
    token: str
    admin_roles: List[int]

    def __init__(self, **args):
        self.__dict__.update(args)

    @classmethod
    def load(cls, file):
        with open(file) as f:
            return cls(**yaml.load(f))
