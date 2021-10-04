import traceback
import os

import requests
from loguru import logger

from config import SENSOR, GATEWAY, ENDPOINT, TOKEN, RETRY_TIME, TIMEOUT


def upload_data(data, sensor=SENSOR, gateway=GATEWAY, endpoint=ENDPOINT, token=TOKEN, retry_time=RETRY_TIME):
    while True:
        logger.info(f"[UPLOAD DATA] Sensor: {sensor}, Gateway: {gateway}")
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        data["sensor"] = sensor
        response = send_post_request(endpoint, headers=headers, json=data)
        if not(response):
            if retry_time > 0:
                logger.warning(f"[UPLOAD DATA]: failed to upload, retry")
                retry_time -= 1
                continue
            else:
                logger.error(f"[UPLOAD DATA] retries exceeded")
                reboot()
        if response.ok:
            logger.success("[UPLOAD DATA] Success")
            break
        else:
            logger.error(f"[UPLOAD DATA] Error.\n Err Msg:{response.text}")


def send_request(request_func):
    """A Decorator for requests module to prevent some exceptions

    Arguments:
        request_func {callable} -- function with requests.get, requests.post
    """

    def wrapper(*args, **kwargs):
        try:
            res = request_func(*args, **kwargs)
            status = res.status_code

            if status != 200:
                logger.warning(f"REQ UNAVAILABLE: {status}")

            return res

        except requests.exceptions.Timeout as error:
            logger.warning(f"UNAVAILABLE: Connection Timeout {error}")
            #reboot()
        except requests.exceptions.ConnectionError as error:
            logger.warning(f"UNAVAILABLE: Connection Error {error}")
            reboot()
        except ConnectionRefusedError as error:
            logger.warning(f"UNAVAILABLE: Connection Refused Error {error}")
            reboot()
        except requests.exceptions.MissingSchema:
            logger.warning(f"UNAVAILABLE: URL Schema Error {traceback.format_exc()}")

    return wrapper


def reboot():
    logger.error("REBOOT")
    os.system("sudo /sbin/reboot")


# pylint: disable=W0621
@send_request
def send_post_request(url, headers=None, data=None, json=None, timeout=TIMEOUT) -> requests.Response:
    if not headers:
        headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, data=data, json=json, timeout=timeout)


# pylint: enable=W0621
