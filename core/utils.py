import configparser
import os
import logging


logger = logging.getLogger(__name__)


def get_secret(base_dir: str, config_file: str, key_name: str) -> str:
    try:
        config = configparser.RawConfigParser()
        config.read(os.path.join(base_dir, config_file))
        return config["django"][key_name]
    except Exception as err:
        logger.warning("Error with the config file: %s", err)
        return os.environ.get(key_name, "")


def get_base_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
