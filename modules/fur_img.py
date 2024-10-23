import asyncio
import random

from graia.amnesia.builtins import aiohttp
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
fursuit_img_list_url = f'https://api.github.com/repos/Hibanaw/CDN/contents/image/fursuit'
fursuit_img_list = []


async def get_fursuit_img_list():
    global fursuit_img_list
    async with aiohttp.ClientSession() as session:
        async with session.get(fursuit_img_list_url) as response:
            if response.status == 200:
                files = await response.json()
                fursuit_img_list = [file['name'] for file in files]
            else:
                print('get_img_list请求失败，状态码:', response.status)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "来只兽兽":
        furry_img_url = f"https://uapis.cn/api/imgapi/furry/img{random.choice(['', 'z', 's'])}4k.php"
        await app.send_message(
            group,
            MessageChain(Image(url=furry_img_url)),
        )
    elif message.display == "来只毛毛":
        if not fursuit_img_list is []:
            fursuit_img_url = f"https://github.com/Hibanaw/CDN/blob/master/image/fursuit/{random.choice(fursuit_img_list)}?raw=true"
            async with aiohttp.ClientSession() as session:
                async with session.get(fursuit_img_url) as response:
                    await app.send_message(
                        group,
                        MessageChain(Image(data_bytes=await response.read())),
                    )

async def main():
    await asyncio.gather(get_fursuit_img_list())

asyncio.run(main())
