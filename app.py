from flask import Flask, render_template, request, make_response
import flask
import os
import sys
from py.chat import get_name_by_question, chat_stream
from py.mysql_history import insert_content_table, insert_message_table
from py.redis_cache import exists_key, set_kv, get_v, update_v, flush_cache
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
        resp = make_response(render_template('chatpgt.html'))
        if question:
            message_key = str(sessionId) + "_message"
            content_key = str(sessionId) + "_content"
            print(exists_key(message_key))
            if not exists_key(message_key):
                # 通过查看redis缓存中是否存在这个key，来判断是否是这个会话的第一次
                # 会话记录存入数据库
                role = 'system'
                name = get_name_by_question(question)
                message_dict = {'name': name, 'sessionId': sessionId}
                # message缓存
                set_kv(message_key, str(message_dict))
                # 初始化content缓存
                set_kv(content_key, str([]))
            else:
                role = 'user'
            content_dict = {"sessionId": sessionId, "role": role, "content": question}
            # 获取redis缓存的content并将此次提问加入缓存
            content_arr = list(eval(get_v(content_key)))
            content_arr.append(content_dict)
            # 更新缓存
            update_v(content_key, str(content_arr))
            # 删除一些无关数据(sessionId)
            for content in content_arr:
                content.pop('sessionId')
            return flask.Response(chat_stream(content_arr, sessionId), mimetype="text/event-stream")
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)


@app.route('/cache/<sessionId>', methods=["POST", "GET"])
def cache_persistent(sessionId):
    message_key = str(sessionId) + "_message"
    content_key = str(sessionId) + "_content"
    if exists_key(message_key) and get_v(content_key) is not None:
        # 将redis缓存持久化到mysql数据库
        message = dict(eval(get_v(message_key)))
        content_arr = list(eval(get_v(content_key)))
        insert_message_table(message)
        insert_content_table(content_arr)
        # 清除缓存
        flush_cache(sessionId)
    return "cache"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
