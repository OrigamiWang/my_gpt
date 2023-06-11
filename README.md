# MY_GPT

## 架构设计图

![架构设计图](static/my_gpt.jpg)

## 实现历史记录

1. 存入mysql的数据，以历史记录的方式可视化在前端，用户点击访问某一次的记录，可以继续那次的对话
2. 点击历史记录后，从mysql拿到那一次之前的所有消息并缓存在redis
3. sendBeacon() 为了避免chrome在onBeforeUnload事件中禁用fetch
4. mysql查询到的数据是tuple，redis不能用tuple、list，选用string，使用eval将string转化成list、tuple
5. TODO: 点击历史对话 -> 将mysql的数据缓存到redis。**最后同步缓存的时候，只插入新增加的对话**