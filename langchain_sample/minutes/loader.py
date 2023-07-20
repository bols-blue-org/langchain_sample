import json
import logging
import os

import tiktoken
from notion_client import Client, APIResponseError, APIErrorCode

# ディレクトリ内のすべてのファイルに対して処理をするためのクラスを作成するユーティリティ関数
from langchain_sample.langchain_minutes import create_abstruct, create_action_item
from langchain_sample.send_notion import sprit_limit_len


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

    def save_to_json(self, dir_path):
        data = self.__dict__  # クラスのインスタンスの属性を辞書として取得
        with open(os.path.join(dir_path, self.name+".json"), 'w') as file:
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    def load_from_json(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        u = cls.__new__(cls)
        u.__dict__.update(data)
        return u


class Minutes(FilePath):

    def create_abstruct(self):
        if len(self.abstruct) == 0:
            for data in self.split_from_token:
                self.abstruct.append(create_abstruct(data))

    def create_action_item(self):
        if len(self.action_item) == 0:
            for data in self.split_from_token:
                self.action_item.append(create_action_item(data))

    def contents_split_limit_tokens(self, content, max_tokens=2800):
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

    def __init__(self, path, max_tokens=2800):
        super(Minutes, self).__init__(path)
        with open(self.absolute_path, 'r', encoding='utf-8') as file:
            self.content = file.read()
            self.split_from_token = self.contents_split_limit_tokens(self.content, max_tokens=max_tokens)
            self.abstruct = []
            self.action_item = []


class NotionController:
    pages = ""
    paragraph = {"paragraph": {"rich_text": [{"text": {"content": "I'm a paragraph."}}]}}


    def __init__(self, database_id):
        self.database_id = database_id
        self.notion = Client(auth=os.environ["NOTION_TOKEN"])
        pass

    def load_contents(self):
        response = self.notion.databases.list()
        for database in response.results:
            print(database.title)

    def load_page_contents(self, database_id=None):
        if database_id is None:
            database_id = self.database_id
        try:
            self.pages = self.notion.databases.query(
                **{
                    "database_id": database_id
                }
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                ...  # For example: handle by asking the user to select a different database
            else:
                # Other error handling code
                logging.error(error)

    def create_database_page(self, database_id=None):
        if database_id is None:
            database_id = self.database_id
        try:
            response = self.notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "title": [{"text": {"content": "Test Page"}}],
                },
                icon={"type": "emoji", "emoji": "🤠"},
                children=[self.paragraph],
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                ...  # For example: handle by asking the user to select a different database
            else:
                # Other error handling code
                logging.error(error)

    def create_auto_minutes(self, minutes:Minutes,  database_id=None):
        minutes.name
        children = []
        children.extend(self.split_topic_text(minutes))
        children.extend(self.split_raw_text(minutes.content))
        if database_id is None:
            database_id = self.database_id
        try:
            response = self.notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "title": [{"text": {"content": minutes.name}}],
                },
                icon={"type": "emoji", "emoji": "🤠"},
                children=children,
            )
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                ...  # For example: handle by asking the user to select a different database
            else:
                # Other error handling code
                logging.error(error)

    def create_paragraph(self, text):
        return {
                "object": 'block',
                "type": 'paragraph',
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": text
                            }
                        }
                    ],
                }
            }

    def create_topic(self, text):
        return {
                "object": 'block',
                "type": 'heading_1',
                "heading_1": {
                    "rich_text": [
                        {
                            "text": {
                                "content": text
                            }
                        }
                    ],
                }
            }

    def split_raw_text(self, content):
        splited_text = sprit_limit_len(content)
        ret = []
        for tmp in splited_text:
            ret.append(self.create_paragraph(tmp))
        return ret

    def split_topic_text(self, minutes:Minutes):
        ret = [self.create_topic("Topics!!!")]
        for tmp in minutes.abstruct:
            ret.append(self.create_topic(tmp))
        return ret

    def split_action_item_text(self, minutes:Minutes):
        ret = [self.create_topic("Todo")]
        for tmp in minutes.action_item:
            ret.append(self.create_paragraph(tmp))
        return ret
