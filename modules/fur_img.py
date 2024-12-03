import os
import random

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import bot_config

channel = Channel.current()


def get_img_list(img_url):
    img_list = []
    for root, dirs, files in os.walk(img_url):
        for file in files:
            file_path = os.path.join(root, file)
            img_list.append(file_path)  # 将文件名添加到列表中
    return img_list


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def img(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "来只兽兽":
        r_furry_img_url = random.choice(furry_img_list)
        print(r_furry_img_url)
        await app.send_message(
            group,
            MessageChain(Image(path=r_furry_img_url)),
        )
    elif message.display == "来只毛毛":
        r_fursuit_img_url = random.choice(fursuit_img_list)
        print(r_fursuit_img_url)
        await app.send_message(
            group,
            MessageChain(Image(path=r_fursuit_img_url)),
        )


fursuit_img_list = get_img_list(bot_config.FURSUIT_IMG_URL)
furry_img_list = get_img_list(bot_config.FURRY_IMG_URL)
print("fursuit:", len(fursuit_img_list))
print("furry:", len(furry_img_list))
