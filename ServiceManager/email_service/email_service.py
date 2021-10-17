import json
import os
from collections.abc import Iterable

import emails
from ServiceManager.util.config import check_key_in_dict
from jinja2 import Template as T


def check_mail_config(mail_config):
    return all([check_key_in_dict('html', mail_config, str),
                check_key_in_dict('text', mail_config, str),
                check_key_in_dict('subject', mail_config, str),
                check_key_in_dict('mail_from', mail_config, (str, Iterable)),
                check_key_in_dict('mail_to', mail_config, str),
                check_key_in_dict('smtp', mail_config, dict)])


def send_email(mail_config, render):
    if check_mail_config(mail_config):
        m = emails.Message(html=T(mail_config["html"]),
                           text=T(mail_config["text"]),
                           subject=T(mail_config["subject"]),
                           mail_from=mail_config["mail_from"])

        response = m.send(render=render,
                          to=mail_config["mail_to"],
                          smtp=mail_config["smtp"])

        if response.status_code not in [250]:
            raise Exception(f"Mail could not be send! Error-code: {response.status_code} - {response}")


def send_job_fail_mail(job_name):
    script_path = os.path.dirname(__file__)
    mail_cfg_path = os.path.join(script_path, 'mail.json')

    with open(mail_cfg_path, "r") as mail_cfg_file:
        mail_cfg = json.load(mail_cfg_file)
        send_email(mail_cfg, {'job_name': job_name})


if __name__ == "__main__":
    send_job_fail_mail("epicJobV2")
    print("done!")
