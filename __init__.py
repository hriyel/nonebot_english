from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.message import Message

# 存储已使用的单词
used_words = set()

# 接龙的单词列表
word_chain = []

# 接龙的规则：单词首字母必须与上一个单词的尾字母相同
def is_valid_word(word: str) -> bool:
    if not word_chain:
        return True  # 如果是第一个单词，直接通过
    last_word = word_chain[-1]
    return word[0] == last_word[-1]

# 接龙消息处理
chain = on_command("接龙",aliases={"en"},rule=to_me(), priority=5)

@chain.handle()
async def handle_word_chain(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    global used_words
    global word_chain

    msg = args.extract_plain_text().strip()
    msg = msg.lower()
    if not msg.isalpha():
        await chain.finish("请输入有效的单词！")

    if msg in used_words:
        await chain.finish("这个单词已经用过了！")
    elif not is_valid_word(msg):
        await chain.finish("单词不符合接龙规则！")
    else:
        used_words.add(msg)
        word_chain.append(msg)
        await chain.finish(f"接龙成功！当前单词：{msg}")

# 重置命令
reset_chain = on_command("重置接龙",aliases={"reset"},rule=to_me(), priority=5)

@reset_chain.handle()
async def handle_reset(bot: Bot, event: Event, state: T_State):
    global used_words
    global word_chain

    used_words = set()
    word_chain = []
    await reset_chain.finish("接龙已重置！")

# 查询已使用单词
query_used_words = on_command("查询已用单词", rule=to_me(), priority=5)

@query_used_words.handle()
async def handle_query(bot: Bot, event: Event, state: T_State):
    global used_words
    if not used_words:
        await query_used_words.finish("目前还没有使用过任何单词！")
    else:
        words_list = "\n".join(sorted(used_words))
        await query_used_words.finish(f"已使用的单词：\n{words_list}")