import os
import unittest

from langchain_sample.langchain_minutes import create_abstruct, create_action_item, read_file_and_limit_tokens
import tiktoken

from langchain_sample.send_notion import create_meeting_log, parse_file_path, get_meeting_log


class MyTestCase(unittest.TestCase):
    def test_something(self):
        path ="resoces/"
        files = os.listdir(path)
        for name in files:
            print(name)
            print(parse_file_path(name))
            ret = read_file_and_limit_tokens(path + "/" + name)
            print(ret)
            abstruct = []
            action_item = []
            for data in ret:
                abstruct = create_abstruct(data)
                action_item = create_action_item(data)
            print(abstruct)
            print(action_item)
            create_meeting_log(name, data)
        self.assertEqual(True, True)  # add assertion here


    def test_send_notion(self):
        get_meeting_log()
        create_meeting_log("テスト送信","テスト", mocking=True)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
