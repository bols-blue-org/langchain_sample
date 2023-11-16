import os

import gradio as gr
import openai
import arxiv
import PyPDF2
from io import BytesIO
import requests

from lark.client import Client
from pandas_hdf.data_collector import HDFDataProcessor

testing = False
if testing:
    existing_file_path = 'arXiv_test.h5'
else:
    existing_file_path = 'arXiv.h5'
processor = HDFDataProcessor(existing_file_path, key='url')

def summarize_paper(keyword,a,b,c):
    # 論文の検索とダウンロード
    search_query = f"all:{keyword}"
    c = Client()

    search = arxiv.Search(
        query=search_query,
        max_results=int(a),
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    summaries = []
    pdf_read = False

    for result in arxiv.Client().results(search):

        # PDFをダウンロード
        pdf_url = result.pdf_url
        response = requests.get(pdf_url)
        pdf_file = BytesIO(response.content)
        text = ""
        store_url = True
        if store_url == True:
            if not processor.is_duplicate(result.pdf_url, "url"):
                # 追加する新しいレコードのデータを作成
                new_record = {
                    'url': result.pdf_url,
                    'published': result.published,
                    'updated': result.updated
                }
                # 新しいレコードを追加して保存
                processor.add_record(new_record)
            else:
                continue

        if pdf_read:
            # PDFをテキストに変換
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
        else:
            text = result.summary

        # 論文の要約を生成
        prompt = """
        ### 指示 ###
        論文の内容を理解した上で，重要なポイントを箇条書きで3点書いてください。

        ### 箇条書きの制約 ###
        - 最大3個
        - 日本語
        - 箇条書き1個を20文字以内
        - カンマは使用禁止
        - 「。」は使用禁止
        - 文章の終わりは体言止め（体言止めの例： ｘｘを許容する ⇒ ｘｘを許容）

        ### 対象とする論文の内容 ###
        {0}

        ### 出力形式 ###
        タイトル: 

        - 箇条書き1
        - 箇条書き2
        - 箇条書き3
        """.format(text)
        # ChatGPT APIを呼び出すコード
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはデータサイエンティストの熟練者です。初学者向けに分かりやすく教えるのが得意なスペシャリストです。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        message = response.choices[0].message
        summary = message.content

        # タイトル、URL、要約を保存
        summaries.append({
            "Summary": summary,
            "URL": pdf_url
        })
        print("Summary:{0} \nURL:{1}".format(summary,pdf_url))
        if testing :
            c.message.send_to_chat(chat_id="oc_223fb7451d5265ebdc49fd3029da6392",
                               message="{0} \nURL:{1}".format(summary, pdf_url))
        else:
            c.message.send_to_chat(message="{0} \nURL:{1}".format(summary, pdf_url))

        processor.save_file()
    return display_summary(summaries)

def display_summary(summaries):
    output = ""
    for summary in summaries:
        output += f"Summary:\n{summary['Summary']}\n\n"
        output += f"URL: {summary['URL']}\n"
    return output

if __name__ == '__main__':
    iface = gr.Interface(
        fn=summarize_paper,
        inputs=[
            gr.components.Textbox(label="技術情報のキーワード"),
            gr.components.Textbox(label="検索論文数"),
            gr.components.Radio(choices=["gpt-3.5-turbo", "gpt-4"], value="gpt-3.5-turbo", label="利用する生成AIモデル"),
            gr.components.Slider(minimum=0, maximum=1, label="temperature"),
        ],
        outputs=gr.components.HTML(label="Summarized Papers"),
        title="arXiv論文要約AI",  # "arXivの調査 (by Moro)",
        description="調べたい技術情報のキーワードと，ピックアップして要約する論文数を指定してください。\n - AIで関連キーワードを自動生成して検索に利用 \n - 検索でヒットした論文を要約してポイントを箇条書き",
        theme="default",
        allow_flagging='never',
    )

    iface.launch()
