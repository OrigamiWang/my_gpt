import openai

from py.redis_cache import get_v, update_v
from py.util import read_yaml


def get_name_by_question(question):
    str_len = len(question) if len(question) < 100 else 100
    name = str(question)[0:str_len]
    return name


def chat_stream(messages, sessionId):
    openai.api_key = read_yaml('gpt.key')
    openai.api_base = read_yaml('gpt.url')
    response = openai.ChatCompletion.create(
        # model="gpt-4",
        model=read_yaml('gpt.model'),
        messages=messages,
        temperature=0,
        # max_tokens=1000,
        stream=True,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0,
        # user='Wemio机器人'
    )
    sentence_list = []
    for trunk in response:
        if trunk['choices'][0]['finish_reason'] is not None:
            data = '[DONE]'
        else:
            data = trunk['choices'][0]['delta'].get('content', '')

        sentence_list.append(data)

        yield "data: %s\n\n" % data.replace("\n", "<br>")
    sentence_list.pop()
    sentence = ''.join(sentence_list).strip().replace("'", "\\'").replace("\"", "\\\"")
    content_key = str(sessionId) + "_content"
    # 插入gpt回复的内容
    content_dict = {"sessionId": sessionId, "role": 'assistant', "content": sentence}
    # 获取redis缓存的content并将此次提问加入缓存
    content_arr = list(eval(get_v(content_key)))
    content_arr.append(content_dict)
    # 更新缓存
    update_v(content_key, str(content_arr))
