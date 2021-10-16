import json
from collections.abc import Iterable

import emails
from ServiceManager.util.Config import checkKeyInDict
from jinja2 import Template as T


def checkMailConfig(mailConfig):
    return all([checkKeyInDict('html', mailConfig, str),
                checkKeyInDict('text', mailConfig, str),
                checkKeyInDict('subject', mailConfig, str),
                checkKeyInDict('mail_from', mailConfig, (str, Iterable)),
                checkKeyInDict('mail_to', mailConfig, str),
                checkKeyInDict('smtp', mailConfig, dict)])


def sendEmail(mailConfig, render):
    if checkMailConfig(mailConfig):
        m = emails.Message(html=T(mailConfig["html"]),
                           text=T(mailConfig["text"]),
                           subject=T(mailConfig["subject"]),
                           mail_from=mailConfig["mail_from"])

        response = m.send(render=render,
                          to=mailConfig["mail_to"],
                          smtp=mailConfig["smtp"])

        if response.status_code not in [250]:
            raise Exception(f"Mail could not be send! Error-code: {response.status_code} - {response}")


def sendJobFailMail(jobName):
    with open('EmailService\\mail.json', "r") as mailCfgFile:
        mailCfg = json.load(mailCfgFile)
        sendEmail(mailCfg, {'jobName': jobName})


if __name__ == "__main__":
    sendJobFailMail("epicJobV2")
    print("done!")
