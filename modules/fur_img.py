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
cdn_fursuit_img_list_url = f'https://api.github.com/repos/Hibanaw/CDN/contents/image/fursuit'
cdn_furry_img_list_url = f'https://api.github.com/repos/Hibanaw/CDN/contents/image/kemono'
cdn_fursuit_img_list = []
cdn_furry_img_list = []


async def get_cdn_fursuit_img_list():
    global cdn_fursuit_img_list
    async with aiohttp.ClientSession() as session:
        async with session.get(cdn_fursuit_img_list_url) as response:
            if response.status == 200:
                files = await response.json()
                cdn_fursuit_img_list = [file['name'] for file in files]
            else:
                print('get_cdn_fursuit_img_list请求失败，状态码:', response.status)

async def get_cdn_furry_img_list():
    global cdn_furry_img_list
    async with aiohttp.ClientSession() as session:
        async with session.get(cdn_furry_img_list_url) as response:
            if response.status == 200:
                files = await response.json()
                cdn_furry_img_list = [file['name'] for file in files]
            else:
                print('get_cdn_furry_img_list请求失败，状态码:', response.status)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "来只兽兽":
        use = random.choices(["uapi", "cdn"], weights=[1, 3])[0]
        if not cdn_furry_img_list is [] and use == "cdn":
            print("cdn")
            cdn_furry_img_url = f"https://github.com/Hibanaw/CDN/blob/master/image/kemono/{random.choice(cdn_furry_img_list)}?raw=true"
            async with aiohttp.ClientSession() as session:
                async with session.get(cdn_furry_img_url) as response:
                    await app.send_message(
                        group,
                        MessageChain(Image(data_bytes=await response.read())),
                    )
        else:
            print("uapi")
            uapi_furry_img_url = f"https://uapis.cn/api/imgapi/furry/img{random.choice(['', 'z', 's'])}4k.php"
            await app.send_message(
                group,
                MessageChain(Image(url=uapi_furry_img_url)),
            )
    elif message.display == "来只毛毛":
        if not cdn_fursuit_img_list is []:
            cdn_fursuit_img_url = f"https://github.com/Hibanaw/CDN/blob/master/image/fursuit/{random.choice(cdn_fursuit_img_list)}?raw=true"
            async with aiohttp.ClientSession() as session:
                async with session.get(cdn_fursuit_img_url) as response:
                    await app.send_message(
                        group,
                        MessageChain(Image(data_bytes=await response.read())),
                    )

async def main():
    await asyncio.gather(get_cdn_fursuit_img_list(), get_cdn_furry_img_list())

asyncio.run(main())
