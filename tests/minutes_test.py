import os
import unittest

from slack_sdk import WebClient

from langchain_sample.langchain_minutes import create_abstruct, create_action_item
import tiktoken

from langchain_sample.minutes.loader import Minutes, NotionController, Slack
from langchain_sample.send_notion import create_meeting_log, parse_file_path, get_meeting_log


class MyTestCase2(unittest.TestCase):
    def setUp(self) -> None:
        self.slack = Slack()
        api_response = self.slack.client.api_test()
        print(api_response)
    # すべての処理内容をリソース内の文字起こしファイルに対して実行する
    def test_all_path(self):
        path ="resoces/"
        files = os.listdir(path)
        for name in files:
            ret = Minutes(path + "/" + name)
            ret.contents_split_limit_tokens(ret.content, max_tokens=10000)
            ret.create_abstruct()
            ret.create_action_item()
            print("file path:" + ret.absolute_path+"\t" + str(ret.abstruct))
            print(ret.action_item)
            database_id = "3b6673eca2414b81832904f837497fc5"
            notion = NotionController(database_id)
            notion.create_auto_minutes(ret)
            self.slack.send_slack_message("<https://www.notion.so/"+notion.page_id+"|created notion 議事録:" + ret.name + ">")
            ret.save_to_json("./")
        self.assertEqual(True, True)

    def test_load_dumpdata(self):
        data = Minutes.load_from_json("./resoces/末広さんNotionについて (2023-07-07 15:00 GMT+9).json")
        data.action_item

class MyTestCase(unittest.TestCase):
    # すべての処理内容をリソース内の文字起こしファイルに対して実行する
    def test_all_path(self):
        path ="resoces/"
        files = os.listdir(path)
        for name in files:
            ret = Minutes(path + "/" + name)
            ret.contents_split_limit_tokens(ret.content, max_tokens=2000)
            ret.create_abstruct()
            ret.create_action_item()
            print("file path:" + ret.absolute_path+"\t" + str(ret.abstruct))
            print(ret.action_item)
            database_id = "3b6673eca2414b81832904f837497fc5"
            notion = NotionController(database_id)
            notion.create_auto_minutes(ret)
            ret.save_to_json("./")
        self.assertEqual(True, True)  # add assertion here

    # データベースの読み込みテスト
    def test_database(self):
        database_id ="3b6673eca2414b81832904f837497fc5"
        notion = NotionController(database_id)
        notion.load_page_contents()
        notion.create_database_page()

    def test_send_notion(self):
        get_meeting_log()
        create_meeting_log("テスト送信", "テスト", mocking=True)


if __name__ == '__main__':
    unittest.main()
