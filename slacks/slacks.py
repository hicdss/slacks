#!/usr/bin/env python

import argparse
import requests
import json
import sys
import pprint
import os
import select

from custom_exceptions import InvalidMessageObjectException
from custom_exceptions import NotImplementedException
from custom_exceptions import NoWebhookUrlException
from custom_exceptions import NoMessageException

EMPTY = "_[WARNING]: no message provided_"
DEFAULT = ["*Hello, world*!\n", "This is _slacks_, a command-line utility for your Slack integrations!"]


def _get_text_from_stdin():
    text = []
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line:
            text.append(line)
        else:
            break
    return text

def _get_text_from_file(file):
    with open(file, 'r') as f:
        text = f.readlines()
    return text

class Config:
    def __init__(self):
        self.config = self._parse_configuration()

    def __getitem__(self, key):
        return self.config[key]

    def _parse_configuration(self):
        try:
            return {
                'WEBHOOK_URL': os.environ['WEBHOOK_URL'],
            }
        except KeyError:
            raise NoWebhookUrlException('WEBHOOK_URL was not provided!')


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
        self.dict = self._create_message_dict(message, args)
        self.json = json.dumps(self.dict)

    def __repr__(self):
        return json.dumps(self.dict, indent=4)

    def _format_text(self, message):
        if args.block:
            return self._format_block(message)
        return message

    def _format_block(self, txt):
        return "```\n%s\n```" % (txt)

    def _create_message_dict(self, message, args):
        if isinstance(message, dict):
            return message
        return {
            "blocks": 
                [
                    {
                        "type" : "section",
                        "text" : {
                            "type": "plain_text" if args.plaintext else "mrkdwn",
                            "text": self._format_text(message)
                        }
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
        "-m", "--message",
        help="pass message as string",
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
    parser.add_argument(
        "-p", "--plaintext",
        help="Format with plaintext instead of markdown",
        action="store_true"
    )

    args = parser.parse_args()

    if args.test:
        text = DEFAULT
    elif args.message:
        text = args.message
    else:
        if args.file:
            text = _get_text_from_file(args.file)
        else:
            text = _get_text_from_stdin()
    
    if text:
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
    else: 
        raise NoMessageException("No message was provided")

