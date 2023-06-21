from flask import Flask, render_template, request, make_response, jsonify, Response
import os
from py.chat import chat_stream, load_his, cache_persistent_fun, get_content_list_fun, chatgpt_fun
from py.mysql_history import del_fun
from py.util import get_session_id
import traceback

# sys.stderr = open("log.txt", "a")
# sys.stdin = open("log.txt", "a")
# sys.stdout = open("log.txt", "a")
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
            content_arr = chatgpt_fun(sessionId, question)
            return Response(chat_stream(content_arr, sessionId), mimetype="text/event-stream")
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)


@app.route('/content/<msg_id>', methods=["GET", "POST"])
def get_content_list(msg_id):
    session_id, content_list = get_content_list_fun(msg_id)
    return jsonify(session_id=session_id, content_list=content_list)


@app.route('/cache/<sessionId>', methods=["POST", "GET"])
def cache_persistent(sessionId):
    cache_persistent_fun(sessionId)
    return "cache"


@app.route('/del/<msg_id>', methods=["GET", "POST"])
def del_by_msg_id(msg_id):
    del_fun(msg_id)
    print(msg_id)
    return jsonify("del success!")


@app.route('/mod/<msg_id>', methods=["GET", "POST"])
def modify_by_msg_id(msg_id):
    print(msg_id)
    return jsonify("mod success!")


@app.route('/more/<msg_id>', methods=["GET", "POST"])
def more_by_msg_id(msg_id):
    print(type(msg_id))
    return jsonify("more success!")


@app.route('/tts/<conversation_idx>/<session_id>')
def text_to_speach(conversation_idx, session_id):
    # tts_by_pyttsx4(conversation_idx, session_id)
    return jsonify("text to speach success!")

# if __name__ == '__main__':
#     app.run(host="127.0.0.1", port=5002, debug=True)
