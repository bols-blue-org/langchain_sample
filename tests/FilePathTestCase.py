import unittest

from langchain_sample.minutes.loader import FilePath


class MyTestCase(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()
