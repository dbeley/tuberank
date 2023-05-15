import configparser
import logging
import os
from django.utils.translation import gettext as _

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


def get_human_readable_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    if hours > 0:
        return _("%(hours)sH %(minutes)sm %(seconds)ss") % {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }
    return _("%(minutes)sm %(seconds)ss") % {"minutes": minutes, "seconds": seconds}
