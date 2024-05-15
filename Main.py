from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from flask import Flask, request, jsonify
import re


SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = 'caa03740'
SPARKAI_API_SECRET = 'OTI0ZGNkZjQ4Y2NlNTM5MmY1MzEyMGI5'
SPARKAI_API_KEY = 'ef41cdb4ae8e723f3f65833c89114f5e'
SPARKAI_DOMAIN = 'generalv3.5'
app = Flask(__name__)

@app.route('/API/AI/<strs>')
def process_information(strs):
    print("[debug]:问题："+strs)
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=strs+",小于200个字的回答"
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])

    # 使用正则表达式匹配 text 和 content 值
    text_match = re.search("text='(.*?)'", str(a))

    # 检查是否找到匹配项，并打印结果
    if text_match:
        text_value = text_match.group(1)
        print("[debug]:回答："+text_value)
        return text_value
    else:
        print("[debug]:错误!")
        return "大模型有点累了，请稍后再问吧~"

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0",port=8088)