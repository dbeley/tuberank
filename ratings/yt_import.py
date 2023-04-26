from googleapiclient.discovery import build
import configparser
import os


class TooManyResultException(Exception):
    pass


def get_secret(BASE_DIR, config_file):
    try:
        CONFIG = configparser.RawConfigParser()
        CONFIG.read(os.path.join(BASE_DIR, config_file))
        return CONFIG["django"]["YOUTUBE_DEVELOPER_KEY"]
    except Exception as e:
        print(
            f"Error with the config file. Be sure to have a valid config file. Error : {e}.",
        )
        return os.environ.get("YOUTUBE_DEVELOPER_KEY", "")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOUTUBE_DEVELOPER_KEY = get_secret(BASE_DIR, "secret.ini")


def _get_channel_information_from_id(channel_id: str):
    with build("youtube", "v3", developerKey=YOUTUBE_DEVELOPER_KEY) as service:
        response = service.channels().list(part="statistics", id=channel_id).execute()
        if response.get("pageInfo").get("totalResults") == 0:
            raise TooManyResultException()
    return response
