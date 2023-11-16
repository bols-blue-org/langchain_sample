
import requests
import json
import datetime

import mimetypes

from langchain_sample.minutes.loader import Minutes, NotionController, Slack
import tiktoken

from langchain_sample.send_notion import create_meeting_log, parse_file_path, get_meeting_log

import os

import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

if __name__ == '__main__':
    slack = Slack()
    api_response = slack.client.api_test()
    print(api_response)

    path = '/mnt/GoogleAeronext/Meet Recordings'

    files = os.listdir(path)

    for name in files:
        file_type = mimetypes.guess_type(name)
        print(file_type)
        if file_type[0] == "text/plain":
            ret = Minutes(path + "/" + name)
            print("split count:" + str(len(ret.contents_split_limit_tokens(ret.content, max_tokens=13000))))
            ret.create_abstruct()
            ret.create_action_item()
            print("file path:" + ret.absolute_path + "\t" + str(ret.abstruct))
            print(ret.action_item)
            database_id = "3b6673eca2414b81832904f837497fc5"
            notion = NotionController(database_id)
            notion.create_auto_minutes(ret)
            ret.save_to_json("./")

    path = '/mnt/GoogleAeronext/Meet Recordings naitou'
    files = os.listdir(path)
    print(files)
    for name in files:
        file_type = mimetypes.guess_type(name)
        print(file_type)
        if file_type[0] == "text/plain":
            ret = Minutes(path + "/" + name)
            print("split count:" + str(len(ret.contents_split_limit_tokens(ret.content, max_tokens=13000))))
            ret.save_to_json("./")
            ret.create_abstruct()
            ret.create_action_item()
            print("file path:" + ret.absolute_path + "\t" + str(ret.abstruct))
            print(ret.action_item)
            database_id = "3b6673eca2414b81832904f837497fc5"
            notion = NotionController(database_id)
            notion.create_auto_minutes(ret)
            if notion.page_id != "":
                slack.send_slack_message(
                    "<https://www.notion.so/" + notion.page_id + "|created notion 議事録:" + ret.name + ">")
            ret.save_to_json("./")

