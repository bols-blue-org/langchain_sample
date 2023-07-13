import json
import os
import unittest

from langchain_sample.minutes.loader import FilePath


class FilePathTestCase(unittest.TestCase):
    def test_absolute_path(self):
        file_path = "/path/to/filename.txt"
        path_info = FilePath(file_path)

        self.assertEqual(path_info.directory, "/path/to")
        self.assertEqual(path_info.filename, "filename.txt")
        self.assertEqual(path_info.name, "filename")
        self.assertEqual(path_info.extension, ".txt")

    def test_relative_path(self):
        file_path = "relative/path/to/filename.txt"
        path_info = FilePath(file_path)

        self.assertEqual(path_info.directory, "relative/path/to")
        self.assertEqual(path_info.filename, "filename.txt")
        self.assertEqual(path_info.name, "filename")
        self.assertEqual(path_info.extension, ".txt")

    def test_double_ext(self):
        file_path = "relative/path/to/filename.mp4.txt"
        path_info = FilePath(file_path)

        self.assertEqual(path_info.directory, "relative/path/to")
        self.assertEqual(path_info.filename, "filename.mp4.txt")
        self.assertEqual(path_info.name, "filename.mp4")
        self.assertEqual(path_info.extension, ".txt")

    def setUp(self):
        self.file_path = "resoces/filename.txt"
        self.path_info = FilePath(self.file_path)
        self.json_file = "data.json"

    def tearDown(self):
        # テストで生成されたJSONファイルを削除
        try:
            os.remove(self.json_file)
        except FileNotFoundError:
            pass

    def test_save_and_load_json(self):
        # JSONに保存
        self.path_info.save_to_json(self.json_file)

        # JSONから読み込み
        loaded_path_info = FilePath.load_from_json(self.json_file)

        # 結果を検証
        self.assertEqual(loaded_path_info.directory, self.path_info.directory)
        self.assertEqual(loaded_path_info.filename, self.path_info.filename)
        self.assertEqual(loaded_path_info.name, self.path_info.name)
        self.assertEqual(loaded_path_info.extension, self.path_info.extension)

    def test_json_data(self):
        # JSONに保存
        self.path_info.save_to_json(self.json_file)

        # JSONファイルを読み込んでデータを検証
        with open(self.json_file, 'r') as file:
            json_data = json.load(file)

        expected_data = {
            'absolute_path': self.path_info.absolute_path,
            'directory': self.path_info.directory,
            'filename': self.path_info.filename,
            'name': self.path_info.name,
            'extension': self.path_info.extension
        }
        self.assertEqual(json_data, expected_data)


if __name__ == '__main__':
    unittest.main()
