from graia.amnesia.builtins import aiohttp
from graia.ariadne import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from graia.saya import Channel

import bot_config

channel = Channel.current()
shouyunji_random = "https://cloud.foxtail.cn/api/function/random?type=1"
shouyunji_pictures = "https://cloud.foxtail.cn/api/function/pictures?model=1&"


@channel.use(SchedulerSchema(timers.crontabify(bot_config.EVERYDAY_FUR_TIME)))
async def everyday_fur(app: Ariadne):
    for group in bot_config.EVERYDAY_FUR_GROUPS:
        async with aiohttp.ClientSession() as session:
            async with session.get(shouyunji_random, ssl=False) as response:
                if response.status != 200:
                    print(f"请求失败，状态码：{response.status}")
                    return
                p_id = (await response.json())['picture']['id']
            async with session.get(shouyunji_pictures + "picture=" + p_id) as response:
                if response.status != 200:
                    print(f"请求失败，状态码：{response.status}")
                    return
                res = await response.json()
            await app.send_group_message(group, MessageChain("【每日一毛】" + res['name']) + MessageChain(Image(url=res['url'])))
