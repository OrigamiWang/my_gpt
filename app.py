from flask import Flask, render_template, request, make_response
import flask
import os
import sys
from py.chat import get_name_by_question, get_num_by_role, chat_stream
from py.mysql_history import insert_content_table, insert_message_table
from py.util import get_session_id
import traceback

# sys.stderr = open("log.txt", "a")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    return resp


@app.route('/session_id')
def session_id():
    resp = make_response()
    resp.headers['session_id'] = get_session_id()
    return resp


@app.route("/gpt")
@app.route("/gpt/<sessionId>", methods=["POST", "GET"])
def chatgpt(sessionId=None):
    try:
        question = request.args.get("question", "")
        isFirst = request.args.get("isFirst", "")
        resp = make_response(render_template('chatpgt.html'))
        if question:
            # 查看这次提问是否是这个会话的第一次
            if isFirst == 'true':
                # 会话记录存入数据库
                name = get_name_by_question(question)
                insert_message_table(name, sessionId)
                role = 'system'
            else:
                role = 'user'
            # 将用户提问存入数据库
            insert_content_table(sessionId, str(get_num_by_role(role)), question)
            # TODO:获取数据库中所有和当前 session_id 相等的内容（即上下文）
            messages = [
                {"role": role, "content": question}
            ]
            return flask.Response(chat_stream(messages, sessionId), mimetype="text/event-stream")
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
