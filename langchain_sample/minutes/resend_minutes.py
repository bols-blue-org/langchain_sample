import os

from langchain_sample.minutes.loader import Minutes, NotionController

database_id = "3b6673eca2414b81832904f837497fc5"

if __name__ == '__main__':
    path = './'
    files = os.listdir(path)
    print(files)
    for name in files:
        data = Minutes.load_from_json(name)
        data.action_item

        notion = NotionController(database_id)
        notion.create_auto_minutes(data, set_raw_text=False)