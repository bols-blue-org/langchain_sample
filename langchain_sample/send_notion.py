import re
import requests
import json
import datetime

import os
import mimetypes
import whisper


def sprit_limit_len(data, max_len=1500):
    sentences = data.split("\n")
    if len(sentences) < 5:
        sentences = data.split("。")  # "。"で文章を分割する
    result = []
    current_sentence = ""

    for sentence in sentences:
        tokens = sentence  # 文章をトークン化してトークン数を取得
        if len(current_sentence) + len(tokens) <= max_len:
            current_sentence += sentence + "。"  # 文章を現在の文字列に追加
        else:
            result.append(current_sentence.strip())  # 古い文字列を配列に追加
            current_sentence = sentence + "。"  # 新しい文字列を開始
    if current_sentence:
        result.append(current_sentence.strip())  # 最後の文字列を配列に追加
    return result


def parse_file_path(file_path):
    file_name = os.path.basename(file_path)  # ファイルパスからファイル名を取得

    # ファイル名から名称とdate情報を分離
    match = re.search(r'(.+?)\s*\((.*?)\)', file_name)
    if match:
        name = match.group(1)  # 名称部分
        date_str = match.group(2)  # date情報部分
        # date情報をパース
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H_%M GMT+9")  # 必要に応じてフォーマットを変更
        except ValueError:
            date = None  # パースに失敗した場合はNone

        return name, date
    else:
        return None, None  # 名称とdate情報が見つからない場合はNoneを返す


def convert_txt(file_path, dirname, whisper_model, mock=False, lang="ja"):
    basename = os.path.basename(file_path)
    print(file_path)
    output_file = f"{dirname}/{basename}.txt"
    if mock:
        return
    is_file = os.path.isfile(output_file)
    if is_file:
        print(f"{output_file} は存在します。処理をスキップします。")
        return
    # Load audio
    audio = whisper.load_audio(f"{dirname}/{basename}")

    result = whisper_model.transcribe(audio, verbose=True, language=lang)
    # Write into a text file
    with open(f"{dirname}/{basename}.txt", "w") as f:
        f.write(result["text"])


def get_meeting_log(mocking=False):
    api_key = "secret_qkIapVO8mFlvuOLrM6v025e15T9mIlYk2wt9QoY4sbb"
    data_base_id = '63c0af58ef1743b78ce6b69d03f74490'
    query_url = "https://api.notion.com/v1/databases/" + data_base_id + "/query"

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    if mocking:
        return
    response = requests.post(query_url, headers=headers)
    result_dict = response.json()
    if response.status_code != 200:
        print("status is not 200\n response=" + response)
    print(result_dict)
    return result_dict


def create_meeting_log(filename, data, mocking=False, test_mode=True):
    title_today = filename
    api_key = "secret_qkIapVO8mFlvuOLrM6v025e15T9mIlYk2wt9QoY4sbb"
    if test_mode:
        data_base_id = '3b6673eca2414b81832904f837497fc5'
    else:
        data_base_id = '63c0af58ef1743b78ce6b69d03f74490'
    emoji = "🤠"
    tag_name = "Weekly Sync"
    detail_text = "チームの定例MTG"

    url = 'https://api.notion.com/v1/pages'

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    data_len = len(data)
    print(f"data len={data_len}")
    splited_data = sprit_limit_len(data)
    payload = {
        "parent": {
            "database_id": data_base_id
        },
        "icon": {
            "emoji": emoji

        },
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title_today
                        }
                    }
                ],
            }
        },
        "children": [
            {
                "object": 'block',
                "type": 'heading_1',
                "heading_1": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Topics!!!"
                            }
                        }
                    ],
                }
            },
            {
                "object": 'block',
                "type": 'heading_2',
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "agenda"
                            }
                        }
                    ],
                }
            },
            {
                "object": 'block',
                "type": 'heading_2',
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": splited_data[0]
                            }
                        }
                    ],
                }
            },
            {
                "object": 'block',
                "type": 'to_do',
                "to_do": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "ToDo 1"
                            }
                        }
                    ],
                    "checked": False,
                    "color": "default",
                }
            }
        ],
    }
    if mocking:
        return
    response = requests.post(url, json=payload, headers=headers)
    result_dict = response.json()
    if response.status_code != 200:
        print("status is not 200\n response=" + response)
        raise Exception("notion create error", response)
    print(result_dict)
    result = result_dict["object"]
    page_url = result_dict["url"]


if __name__ == '__main__':
    path = '/content/drive/MyDrive/Meet Recordings'

    files = os.listdir(path)

    for name in files:
        file_type = mimetypes.guess_type(name)
        print(file_type)
        if file_type[0] == "text/plain":
            create_meeting_log(name)
