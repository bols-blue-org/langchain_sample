import json
import os

import tiktoken
from notion_client import Client

# ディレクトリ内のすべてのファイルに対して処理をするためのクラスを作成するユーティリティ関数
from langchain_sample.langchain_minutes import create_abstruct, create_action_item


def file_loader(path):
    files = os.listdir(path)
    classes = []
    for name in files:
        classes.append(FilePath(os.path.join(path, name)))
    return classes


class FilePath:
    def __init__(self, path):
        self.absolute_path = os.path.abspath(path)
        self.directory, self.filename = os.path.split(path)  # パスをディレクトリとファイル名に分割
        self.name, self.extension = os.path.splitext(self.filename)  # ファイル名を名称と拡張子に分割

    def save_to_json(self, file_path):
        data = self.__dict__  # クラスのインスタンスの属性を辞書として取得
        with open(file_path, 'w') as file:
            json.dump(data, file)

    @classmethod
    def load_from_json(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        u = cls.__new__(cls)
        u.__dict__.update(data)
        return u


class Minutes(FilePath):
    abstruct = []
    action_item = []

    def create_abstruct(self):
        if len(self.abstruct) == 0:
            for data in self.split_from_token:
                self.abstruct.append(create_abstruct(data))

    def create_action_item(self):
        if len(self.action_item) == 0:
            for data in self.split_from_token:
                self.action_item.append(create_action_item(data))

    def contents_split_limit_tokens(self, content, max_tokens=3500):
        sentences = content.split("。")  # "。"で文章を分割する
        result = []
        current_sentence = ""

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

        for sentence in sentences:
            tokens = encoding.encode(sentence)  # 文章をトークン化してトークン数を取得
            if len(current_sentence) + len(tokens) <= max_tokens:
                current_sentence += sentence + "。"  # 文章を現在の文字列に追加
            else:
                result.append(current_sentence.strip())  # 古い文字列を配列に追加
                current_sentence = sentence + "。"  # 新しい文字列を開始
        if current_sentence:
            result.append(current_sentence.strip())  # 最後の文字列を配列に追加
        return result

    def __init__(self, path):
        super(Minutes, self).__init__(path)
        with open(self.absolute_path, 'r', encoding='utf-8') as file:
            self.content = file.read()
            self.split_from_token = self.contents_split_limit_tokens(self.content)
            split_from_token = self.contents_split_limit_tokens(self.content)


class NotionController:

    def __init__(self):
        self.notion = Client(auth=os.environ["NOTION_TOKEN"])
        pass

    def load_contents(self):
        response = self.notion.databases.list()
        for database in response.results:
            print(database.title)
