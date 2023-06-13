from flask import Flask, render_template, request, make_response, jsonify, Response
import os
import sys
from py.chat import get_name_by_question, chat_stream, load_his
from py.mysql_history import insert_content_table, insert_message_table, query_content_list, get_sessionId_by_msgId, \
    update_time
from py.redis_cache import exists_key, set_kv, get_v, update_v, flush_cache
from py.util import get_session_id, tuple_to_list, list_to_dict
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


@app.route('/loadHistory', methods=["POST", "GET"])
def load_history():
    return load_his()


@app.route("/gpt")
@app.route("/gpt/<sessionId>", methods=["POST", "GET"])
def chatgpt(sessionId=None):
    try:
        question = request.args.get("question", "")
        resp = make_response(render_template('chatpgt.html'))
        if question:
            message_key = str(sessionId) + "_message"
            content_key = str(sessionId) + "_content"
            print(exists_key(content_key))
            if not exists_key(content_key):
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
                if not exists_key(message_key):
                    set_kv(message_key, '')
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
            return Response(chat_stream(content_arr, sessionId), mimetype="text/event-stream")
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)


@app.route('/cache/<sessionId>', methods=["POST", "GET"])
def cache_persistent(sessionId):
    message_key = str(sessionId) + "_message"
    content_key = str(sessionId) + "_content"
    content_num_key = str(sessionId) + "_content_num"
    if exists_key(message_key) and get_v(content_key) is not None:
        # 将redis缓存持久化到mysql数据库
        if get_v(content_num_key) is None:
            message_tuple = eval(get_v(message_key))
            message = dict(message_tuple)
            content_arr = list(eval(get_v(content_key)))
            insert_message_table(message)
        else:
            # 注意，如果是通过历史记录进行的对话，一部分对话已经保存到了mysql，只需保存新产生的content，不需要添加message以及历史的content
            # 但是，需要更新message的时间
            update_time(sessionId)
            content_arr = list(eval(get_v(content_key)))[int(get_v(content_num_key)):]
        insert_content_table(content_arr)
        # 清除缓存
        flush_cache(sessionId)

    return "cache"


@app.route('/content/<msg_id>', methods=["GET", "POST"])
def get_content_list(msg_id):
    content_list = tuple_to_list(query_content_list(msg_id))
    session_id = get_sessionId_by_msgId(msg_id)[0][0]
    # 将历史记录、以及历史记录的数量缓存在redis
    content_dict = list_to_dict(content_list)
    set_kv(session_id + "_content", str(content_dict))
    set_kv(session_id + "_content_num", str(len(content_list)))
    return jsonify(session_id=session_id, content_list=content_list)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
