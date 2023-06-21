from pyttsx3 import init
from os import environ, pathsep
import threading

from py.redis_cache import get_content_by_conversationIdx_and_sessionId

# 将 ffmpeg,exe 添加到环境变量
environ['PATH'] += pathsep + 'ffmpeg.exe'


# init the engine, and set the property


def on_start(name):
    print(f"starting utterance {name}")


def on_end(name, completed):
    print(f"ending utterance {name} with completed={completed}")


engine = init()


def say(sentence: str):
    # 检查是否正在播放，如果是，则停止loop（注意，这个操作只能停止已经播放完了的，不能实现真正的暂停播放）
    if engine._inLoop:
        engine.endLoop()
    engine.say(sentence)
    engine.runAndWait()
    engine.endLoop()


def tts_by_pyttsx4(conversation_id, session_id):
    try:
        # query text by conversation_id and session_id
        sentence = get_content_by_conversationIdx_and_sessionId(conversation_id, session_id)
        print(sentence)
        # 多线程播放语音，避免阻塞
        t = threading.Thread(target=say, args=(sentence,))
        t.start()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    say('hello world')