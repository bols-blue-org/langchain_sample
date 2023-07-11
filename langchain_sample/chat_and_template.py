# チャットモデルのラッパーをインポート
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
chat = ChatOpenAI(temperature=0.7)

# SystemMessage 用のテンプレートの作成
template="あなたはリーンキャンバスを作成する優秀な事業責任者です"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

# HumanMessage 用のテンプレートの作成
human_template="こんなアイデアを思いつきました。解決する課題と既存の競合製品を考えてください。出力は箇条書きでお願いします「{text}」"
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
completion = chain.run(text="AIによるリーンキャンバス作成サービス")
print(completion)

human_template="このアイデアの「独自の価値提案」と「分かりやすいコンセプト」を考えてください。出力は箇条書きでお願いします「{text}」"
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
completion = chain.run(text="AIによるリーンキャンバス作成サービス")
print(completion)

human_template="このアイデアの「圧倒的な優位性」と「顧客セグメント」「アーリーアダプタになりそうな人物像」を考えてください。出力は箇条書きでお願いします「{text}」"
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
completion = chain.run(text="AIによるリーンキャンバス作成サービス")
print(completion)