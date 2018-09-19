# -*- coding:utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 19:09:05 2018

@author: Snailclimb
@description使用图灵机器人自动与指定好友聊天
"""

from wxpy import Bot,Tuling,embed,ensure_one
bot = Bot()
my_friend = ensure_one(bot.search('郑凯'))  #想和机器人聊天的好友的备注
tuling = Tuling(api_key='你申请的apikey')
@bot.register(my_friend)  # 使用图灵机器人自动与指定好友聊天
def reply_my_friend(msg):
    tuling.do_reply(msg)
embed()


'''

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 18:55:04 2018

@author: Administrator
"""

from wxpy import Bot,Tuling,embed
bot = Bot(cache_path=True)
my_group = bot.groups().search('群聊名称')[0]  # 记得把名字改成想用机器人的群
tuling = Tuling(api_key='你申请的apikey')  # 一定要添加，不然实现不了
@bot.register(my_group, except_self=False)  # 使用图灵机器人自动在指定群聊天
def reply_my_friend(msg):
    print(tuling.do_reply(msg))
embed()

'''
