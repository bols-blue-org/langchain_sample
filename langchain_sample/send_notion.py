
import requests
import json
import datetime

import os
import mimetypes
import whisper

model = whisper.load_model("large")

def convert_txt(file_path,dirname, mock=False, lang = "ja"):
  basename = os.path.basename(file_path)
  print(file_path)
  output_file = f"{dirname}/{basename}.txt"
  if mock == True:
    return
  is_file = os.path.isfile(output_file)
  if is_file:
    print(f"{output_file} は存在します。処理をスキップします。")
    return
  # Load audio
  audio = whisper.load_audio(f"{dirname}/{basename}")

  result = model.transcribe(audio, verbose=True, language=lang)
  # Write into a text file
  with open(f"{dirname}/{basename}.txt", "w") as f:
    f.write(result["text"])


def create_meeting_log(data):

  today = datetime.date.today()
  title = "MTG_"
  title_today = title+ str(today)
  created_iso_format = today.isoformat()
  api_key = "secret_qkIapVO8mFlvuOLrM6v025e15T9mIlYk2wt9QoY4sbb"
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

  payload = {
      "parent": {
          "database_id": data_base_id
      },
      "icon":{
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
      "children":[
          {
          "object": 'block',
          "type": 'heading_1',
          "heading_1":{
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
              "heading_2":{
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
              "heading_2":{
                  "rich_text": [
              {
                  "text": {
                  "content": data
                  }
              }
              ],
              }
          },
          {
              "object": 'block',
              "type": 'to_do',
              "to_do":{
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

  response = requests.post(url, json=payload, headers=headers)
  result_dict = response.json()
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