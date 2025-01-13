from os import getenv
from time import sleep
from icecream import ic


def mail_report():
    sleep(5)
    ic(f"sent the report from: {getenv("USERNAME","?")}")
