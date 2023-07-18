import os
import unittest

from langchain_sample.langchain_minutes import create_abstruct, create_action_item
import tiktoken

from langchain_sample.minutes.loader import Minutes, NotionController
from langchain_sample.send_notion import create_meeting_log, parse_file_path, get_meeting_log


class MyTestCase(unittest.TestCase):
    def test_something(self):
        path ="resoces/"
        files = os.listdir(path)
        for name in files:
            ret = Minutes(path + "/" + name)
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
