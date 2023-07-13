import os
import unittest

from langchain_sample.langchain_minutes import create_abstruct, create_action_item
import tiktoken

from langchain_sample.minutes.loader import Minutes
from langchain_sample.send_notion import create_meeting_log, parse_file_path, get_meeting_log


class MyTestCase(unittest.TestCase):
    def test_something(self):
        path ="resoces/"
        files = os.listdir(path)
        for name in files:
            print(name)
            print(parse_file_path(name))
            ret = Minutes(path + "/" + name)
            ret.create_abstruct()
            ret.create_action_item()
            print(ret.abstruct)
            print(ret.action_item)
            create_meeting_log(name, ret.content)
        self.assertEqual(True, True)  # add assertion here


    def test_send_notion(self):
        get_meeting_log()
        create_meeting_log("テスト送信", "テスト", mocking=True)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
