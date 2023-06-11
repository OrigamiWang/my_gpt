import os
import time

import yaml


def get_session_id():
    return str(time.time()).replace('.', '')


def get_num_by_role(role):
    role_dict = {'system': 1, 'user': 2, 'assistant': 3}
    return role_dict[role]


def read_yaml(keys):
    try:
        key_list = str(keys).split('.')
        data = None
        # 相对路径，保证不同文件都能访问的到
        file_path = os.path.join(os.path.dirname(__file__), '..\\resources\\config.yml')
        fs = open(file_path, encoding="UTF-8")
        data = yaml.load(fs, Loader=yaml.FullLoader)
        for key in key_list:
            data = data[key]
        return data
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(read_yaml('database'))
