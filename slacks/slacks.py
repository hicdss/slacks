#!/usr/bin/env python

import argparse
import requests
import json
import sys
import pprint
import os

from example import EXAMPLE
from custom_exceptions import InvalidMessageObjectException
from custom_exceptions import NotImplementedException

EMPTY = "_[WARNING]: no message provided_"
DEFAULT = ["*Hello, world*!\n", "This is _slacks_, a command-line utility for your Slack integrations!"]


class Config:
    def __init__(self):
        self.config_file = self._find_config_file()
        self.config = self._parse_config_file()

    def __getitem__(self, key):
        return self.config[key]

    def _find_config_file(self):
        try_files = [
            '.slacksrc',
            '%s/.slacksrc' % (os.environ['HOME'])
        ]
        for file in try_files:
            if os.path.isfile(file):
                return file
        return self._create_config_file_from_user_input()

    def _create_config_file_from_user_input(self):
        raise NotImplementedException('User input is not yet implemented')

    def _parse_config_file(self):
        with open(self.config_file, 'r') as f:
            return { key: value for key, value in [ (line.split('=')[0].strip(), line.split('=')[1].strip())  for line in f.readlines() ] }


class ApiClient:
    def __init__(self, config):
        self.webhook_url = config['WEBHOOK_URL']
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
            raise InvalidMessageObjectException("message_object variable is not of type MessageObject!")


class MessageObject(dict):

    def __init__(self, message, args):
        self.dict = self._create_message_dict(message)
        self.json = json.dumps(self.dict)

    def __repr__(self):
        return json.dumps(self.dict, indent=4)

    def _format_text(self, message):
        if args.block:
            return self._format_block(message)
        return message

    def _format_block(self, txt):
        return "```\n%s\n```" % (txt)

    def _create_message_dict(self, message):
        if isinstance(message, dict):
            return message
        return {
            "blocks": 
                [
                    {
                        "type" : "section",
                        "text" : {
                            "type": "mrkdwn",
                            "text": self._format_text(message)
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Sent with <https://github.com/hicdss/slacks|slacks> by <https://hicron.com|Hicron>"
                            }
                        ]
                    }
                ]
            }


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        help="use contents of a FILE as text message",
        nargs="?",
        action="store"
    )
    parser.add_argument(
        "-b", "--block",
        help="Message will be a markdown block",
        action="store_true"
    )
    parser.add_argument(
        "-t", "--test",
        help="Use exapmle from example.py",
        action="store_true"
    )

    args = parser.parse_args()

    if args.test:
        text = DEFAULT
    else:
        if args.file:
            print(args.file)
            with open(args.file, 'r') as f:
                text = f.readlines()
        else:
            text = EMPTY if sys.stdin.isatty() else sys.stdin.readlines()
    mo = MessageObject(
        "".join(
            text
        ),
        args
    )

    print(mo)
    config = Config()
    print(config.config)
    api = ApiClient(config)
    resp = api.send_message(mo)
    print(resp.status_code, resp.text)
