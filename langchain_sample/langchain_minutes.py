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
chat = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-16k-0613")

# SystemMessage 用のテンプレートの作成
template = "あなたは優秀な人事担当者です."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)


def create_abstruct(data):
    # HumanMessage 用のテンプレートの作成
    human_template = "次の行以降の会話から会話のトピックを書き出してください。出力は箇条書きでお願いします\n{text}"
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
    human_template = "次の行以降の会話から次回までの宿題事項があれば書き出してください。ない場合は「なし」と回答お願いします。出力は箇条書きでお願いします\n{text}"
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
