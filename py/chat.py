import openai

from py.mysql_history import insert_content_table
from py.util import read_yaml


def get_name_by_question(question):
    str_len = len(question) if len(question) < 100 else 100
    name = str(question)[0:str_len]
    return name


def get_num_by_role(role):
    role_dict = {'system': 1, 'user': 2, 'assistant': 3}
    return role_dict[role]


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

    # 插入gpt回复的内容
    insert_content_table(sessionId, str(get_num_by_role('assistant')), sentence)


if __name__ == '__main__':
    print(get_num_by_role('user'))
