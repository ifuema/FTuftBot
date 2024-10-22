import random

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Member

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from modules import ai

channel = Channel.current()
actions = [
                '揉了揉你的脑袋',
                '摸了摸你的肚皮',
                '挠了挠你的下巴',
                '搓了搓你的尾巴',
                '轻轻捏了捏你的耳朵',
                '给你闻了些猫薄荷',
                '用逗猫棒陪你玩',
                '撸了撸你的小肉丁',
                '蹭了蹭你的肉垫',
                '亲了亲你的脸颊',
                '顺了顺你的后背',
                '投喂了你一罐沙丁鱼罐头',
                '揪了揪你的胡须',
                '指尖划过你的后背',
                '刺挠着你',
                '揉搓你的原始袋',
                '往你的耳朵里吹气',
                '抱着你猛吸了一口',
                '向空中抛出了鸡肉冻干',
                '在你面前使用激光笔',
                '把你抱到了被窝里',
                '用麻袋把你套走了',
                '正在给你做头部按摩',
                '帮助你顺毛',
                '叫着你的名字',
                '碰了碰你的鼻子',
                '对着你眨了眨眼',
                '朝你丢了颗乒乓球',
                '给你变了个纸杯魔术',
                '对着你喵喵叫',
                '把你高高抱起',
                '在你旁边认真工作',
                '和你玩起了躲猫猫',
                '扔出了回旋镖',
            ]


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if message.display == "摸摸小猫":
        mes = ai.run(f"对于'{member.name}'主人{random.choice(actions)}，请富有文采地表达你的愉悦，本次输出请尽量简短，字数最好30字以内，请提及与你互动的主人的名字以及生动描述被互动的部位的状态，输出中坚决不可以出现\"谢谢\"、\"软软的\"、\"舒服\"、\"妙人\"、\"懂猫\"、\"好人\"等词语。")
        await app.send_message(
            group,
            MessageChain(mes),
        )