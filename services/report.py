from os import getenv
from icecream import ic


def mail_report():
    ic(f"sent the report from: {getenv("USERNAME","?")}")
