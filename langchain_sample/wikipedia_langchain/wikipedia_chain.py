# 環境変数の準備
import os
os.environ["OPENAI_API_KEY"] = "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"

# langchain
from langchain.llms import OpenAI, OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import wikipedia

# エージェント
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, load_tools, initialize_agent

# wikipediaの言語を日本語にセット
wikipedia.set_lang('ja')

# 例示付きプロンプトの設定
# 指定のJSON形式を短くしてみる。特に複数出してほしいreralted_eventsとbattleをひとつにしたらどうなるか。プロンプトは短い方が良い。
# 同じ形式で複数出力してほしい場合は"$複数ある場合は同じ形式で繰り返す"を入れると良い

# prefixで基本指示およびツール利用が可能であることを指示する
prefix = """あなたは入力された文章をもとに、関連する情報を調査するAIです。調査した結果は日本語でまとめてください。
次のツールにアクセスすることができます。入力された文章からはわからない情報は検索してください。
"""

# suffixに出力形式の指定
suffix = """# 指定のJSON形式
---
(
    "event":(
        "name":"$本文のタイトル（入力された文章をもっともよく表すワードを選択）"
    )
)
---

Human: {input}
AI:{agent_scratchpad}"""

if __name__ == '__main__':
    llm = OpenAIChat(model_name="gpt-3.5-turbo",
                     temperature=0.2)

    # ツールの準備、個々ではwikipediaのみを入れている
    tools = load_tools(['wikipedia'], llm=llm)

    # プロンプトの設定
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=['input', 'agent_scratchpad'],
    )

    llm_chain = LLMChain(
        llm=llm,
        verbose=True,
        prompt=prompt
    )

    agent = ZeroShotAgent(llm_chain=llm_chain,
                          tools=tools,
                          return_intermediate_steps=True)

    # toolの繰り返し利用が多くなると入力token数が最大値を超える可能性があるため、max_iteration=2としている
    # また、toolの繰り返し利用上限に達した際に出力が行われるよう、early_stopping_method="generate"とする
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                        tools=tools,
                                                        verbose=True,
                                                        max_iterations=2,
                                                        early_stopping_method="generate")
    output = agent_executor.run(input="織田信勝の没年齢")
