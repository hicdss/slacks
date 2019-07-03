#!/usr/bin/env python

import requests
import json
import sys
import pprint

from custom_exceptions import InvalidMessageObject

WEBHOOK_URL = "https://hooks.slack.com/services/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"

class ApiClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.headers = {
            'Content-Type' : 'application/json',
        }

    def send_message(self, message_object):
        resp = requests.post(
            self.webhook_url,
            data=self._validate_message(message_object)
        )
        return resp

    def _validate_message(self, message_object):
        if isinstance(message_object, MessageObject):
            return message_object.json
        else:
            raise InvalidMessageObject("message_object is not of type MessageObject!")


class MessageObject(dict):

    def __init__(self, text):
        self.dict = self._create_message_dict(text)
        self.json = json.dumps(self.dict)

    def _create_message_dict(self, text):
        return {
            "text" : text,
        }

    def __repr__(self):
        return json.dumps(self.dict, indent=4)


if __name__ == "__main__":
    stdin = sys.stdin.readable()
    mo = MessageObject(
        "\n".join(
            # sys.stdin.readlines()
            ["test"]
        )
    )

    print(mo)
    api = ApiClient(WEBHOOK_URL)
    resp = api.send_message(mo)
