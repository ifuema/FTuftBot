# 本部分示例需使用 Saya 进行加载
from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

import bot_config
from modules import ai

channel = Channel.current()


# 此处注释的意思是用法类比，不是说这里可以用 GroupMessage
# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def cyc(app: Ariadne, event: NudgeEvent):
    if isinstance(event.subject, Group) and event.supplicant and event.target == bot_config.QQ_ACCOUNT:
        msg = ai.run(f"群友戳了戳你。{ai.short}。")
        await app.send_group_message(event.group_id, MessageChain(msg))
