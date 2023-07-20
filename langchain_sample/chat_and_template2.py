# チャットモデルのラッパーをインポート
from langchain.chat_models import ChatOpenAI

# LLMChain をインポート
from langchain import LLMChain, OpenAI

# チャットプロンプト用のテンプレートをインポート
from langchain.memory import ConversationSummaryMemory
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# チャットモデルのラッパーを初期化
from langchain.schema import LLMResult

chat = ChatOpenAI(temperature=0.7)

# memory = ConversationBufferMemory(memory_key="chat_history")
memory = ConversationSummaryMemory(llm=OpenAI())

# SystemMessage 用のテンプレートの作成
template="あなたはリーンキャンバスを作成する優秀な事業責任者です"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

# HumanMessage 用のテンプレートの作成
human_template="こんなアイデアを思いつきました。解決する課題と既存の競合製品を考えてください。出力は箇条書きでお願いします「{text}」"
human_message_prompt1 = HumanMessagePromptTemplate.from_template(human_template)

# HumanMessage 用のテンプレートの作成
human_template="このアイデアの独自の価値提案と分かりやすいコンセプトを考えてください。出力は箇条書きでお願いします「{text}」"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

batch_messages = [
    [
        system_message_prompt,
        human_message_prompt1
    ],
    [
        system_message_prompt,
        human_message_prompt
    ],
]
# チャットモデルにメッセージを渡して、予測を受け取る
result: LLMResult = chat.generate(batch_messages)

# 予測結果を表示する
for generations in result.generations:
    for generation in generations:
        print(generation.text,"\n")