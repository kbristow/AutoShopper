import json

__author__ = 'BristK'

settings_file = "settings.json"


def password():
    with open(settings_file) as file_handle:
        settings = json.load(file_handle)

    return settings["user"]["password"]


def username():
    with open(settings_file) as file_handle:
        settings = json.load(file_handle)

    return settings["user"]["username"]