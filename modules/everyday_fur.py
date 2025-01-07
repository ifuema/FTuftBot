import random

from graia.amnesia.builtins import aiohttp
from graia.ariadne import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from graia.saya import Channel

import bot_config
from modules.fur_img import get_img_list

channel = Channel.current()
shouyunji_random = "https://cloud.foxtail.cn/api/function/random?type=1"
shouyunji_pictures = "https://cloud.foxtail.cn/api/function/pictures?model=1&"


# @channel.use(SchedulerSchema(timers.crontabify(bot_config.EVERYDAY_FUR_TIME)))
# async def everyday_fur(app: Ariadne):
#     for group in bot_config.EVERYDAY_FUR_GROUPS:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(shouyunji_random, ssl=False) as response:
#                 if response.status != 200:
#                     print(f"请求失败，状态码：{response.status}")
#                     return
#                 p_id = (await response.json())['picture']['id']
#             async with session.get(shouyunji_pictures + "picture=" + p_id, ssl=False) as response:
#                 if response.status != 200:
#                     print(f"请求失败，状态码：{response.status}")
#                     return
#                 res = await response.json()
#             await app.send_group_message(group, MessageChain("【每日一毛】" + res['name']) + MessageChain(Image(url=res['url'])))


@channel.use(SchedulerSchema(timers.crontabify(bot_config.EVERYDAY_FUR_TIME)))
async def everyday_fur(app: Ariadne):
    for group in bot_config.EVERYDAY_FUR_GROUPS:
        r_furry_img_url = random.choice(page_img_list)
        print(r_furry_img_url)
        with open(r_furry_img_url.rsplit('/', 1)[0] + "/fursuit_profile.txt", 'r', encoding='utf-8') as file:
            content = file.read()
        await app.send_group_message(
            group,
            MessageChain("【每日一毛】\n" + content) +
            MessageChain(Image(path=r_furry_img_url)),
        )


page_img_list = get_img_list(bot_config.PAGE_IMG_URL)
print("page:", len(page_img_list))