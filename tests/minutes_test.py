import unittest

from langchain_sample.langchain_minutes import create_abstruct, create_action_item
import tiktoken

from langchain_sample.send_notion import create_meeting_log


class MyTestCase(unittest.TestCase):
    def test_something(self):
        f = open("resoces/末広さん、鈴木さん (2022-10-11 14_44 GMT+9).mp4.txt", 'r')
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        count = 0
        for data in f:
            count += len(encoding.encode(data))
            print("now token %i" % count)
        print("total token size is %i" % count)
        f.close()
        create_abstruct(data)
        create_action_item(data)
        self.assertEqual(True, False)  # add assertion here


    def test_send_notion(self):
        f = open("resoces/末広さん、鈴木さん (2022-10-11 14_44 GMT+9).mp4.txt", 'r')
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        count = 0
        for data in f:
            count += len(encoding.encode(data))
            print("now token %i" % count)
        print("total token size is %i" % count)
        f.close()
        create_meeting_log("テスト")
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
