import json

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urljoin


class Message:
    def __init__(self, token):
        self.url = urlparse("https://open.larksuite.com/open-apis/im/v1/messages")
        auth_contents = "Bearer " + token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": auth_contents
        }
        pass

    # チャットIDを指定してメッセージを送信
    def send_to_chat(self, chat_id="oc_984315087cae65cd3a9415b0974b30c2", message="test content"):
        query = parse_qs(self.url.query, True)
        query["receive_id_type"] = "chat_id"

        msg_dict = {"text": message}

        json_str = json.dumps(msg_dict)
        print(json_str)
        data = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json_str
        }
        result = self.url._replace(query=urlencode(query, doseq=True))

        url = result.geturl()
        response = requests.post(url, headers=self.headers, json=data)
        print(response.text)

    # メッセージを削除
    def delete_from_msgid(self, id):
        url = urljoin(self.url.geturl(), id)

        response = requests.delete(url, headers=self.headers)
        print(response.text)


class Client:
    cat_list_url = "https://open.larksuite.com/open-apis/im/v1/chats"
    def __init__(self):
        url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "app_id": "cli_a5a74ae43678d02e",
            "app_secret": "0zyZsbzh33DbdgGjXXEqiepEc88Y4TFi"
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            ret_json = response.json()
            self.access_token = ret_json.get("tenant_access_token")
            self.expire = ret_json.get("expire")
            print(f"Tenant Access Token: {self.access_token}")
            self.message = Message(self.access_token)
        else:
            print(f"Request failed with status code: {response.status_code}")

        pass

    def get_chat_list(self):

        auth_contents = "Bearer " + self.access_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": auth_contents
        }
        response = requests.get(self.cat_list_url, headers=self.headers)
        if response.status_code == 200:
            chat_list = response.json()
            print(chat_list)
        else:
            print(f"Request failed with status code: {response.status_code}")


if __name__ == '__main__':
    msg = "タイトル: ドローンの安全なマルチエージェントの動作計画に関する論文の重要なポイント" \
          "- 強化学習と制約制御ベースの軌道計画を組み合わせたトラクタブルな動作計画手法を提案" \
          "- シングルエージェントの強化学習を使用して、目標に到達するが衝突しない動作計画を学習" \
          "- 確率制約、セットベースの制御手法を使用して、不確実性や障害物との衝突を回避しながら安全性を確保 " \
          "URL:http://arxiv.org/pdf/2311.00063v1"

    ret = Client()
    #ret.message.send_to_chat()
    ret.message.send_to_chat(chat_id="oc_223fb7451d5265ebdc49fd3029da6392", message=msg)
    ret.get_chat_list()
    # ret.message.delete_from_msgid("om_9c5f0b2b44eb1d2d60839c11d8937091")
