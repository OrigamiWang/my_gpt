# MY_GPT

## 架构设计图
![架构设计图](static/my_gpt.jpg)

## 实现历史记录

1. 存入mysql的数据，以历史记录的方式可视化在前端，用户点击访问某一次的记录，可以继续那次的对话
2. 点击历史记录后，从mysql拿到那一次之前的所有消息并缓存在redis
