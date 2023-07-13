# チャットモデルのラッパーをインポート
import tiktoken
from langchain.chat_models import ChatOpenAI

# LLMChain をインポート
from langchain import LLMChain

# チャットプロンプト用のテンプレートをインポート
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# チャットモデルのラッパーを初期化
chat = ChatOpenAI(temperature=0.9)

# SystemMessage 用のテンプレートの作成
template = "あなたは優秀なドローンのエンジニアです."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)


def read_file_and_limit_tokens(file_path, max_tokens=3500):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # ファイルを全文読み込む

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

def create_abstruct(data):
    # HumanMessage 用のテンプレートの作成
    human_template = "議事録を作成したいです。会話のトピックを書き出してください。出力は箇条書きでお願いします「{text}」"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Message のテンプレートを組合わせて会話の流れを決めます
    messages_template = [
        system_message_prompt,
        human_message_prompt
    ]

    # チャットプロンプト用のテンプレートを作成します
    chat_prompt_template = ChatPromptTemplate.from_messages(messages_template)

    # LLM チェーンを作成（チャットモデルのラッパーとプロンプトテンプレートから構成）
    chain = LLMChain(llm=chat, prompt=chat_prompt_template)

    # LLM チェーンを実行
    completion = chain.run(text=data)
    return completion


def create_action_item(data):
    # HumanMessage 用のテンプレートの作成
    human_template = "議事録を作成したいです。次回までの宿題事項があれば書き出してください。ない場合は「なし」と回答お願いします。出力は箇条書きでお願いします「{text}」"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Message のテンプレートを組合わせて会話の流れを決めます
    messages_template = [
        system_message_prompt,
        human_message_prompt
    ]

    # チャットプロンプト用のテンプレートを作成します
    chat_prompt_template = ChatPromptTemplate.from_messages(messages_template)

    # LLM チェーンを作成（チャットモデルのラッパーとプロンプトテンプレートから構成）
    chain = LLMChain(llm=chat, prompt=chat_prompt_template)

    # LLM チェーンを実行
    completion = chain.run(text=data)
    return completion
