from io import BytesIO

import requests
from graia.amnesia.builtins import aiohttp
from graia.ariadne import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from typing_extensions import Annotated
from PIL import Image as PILImage

from modules import ai

channel = Channel.current()
countdown_url = "https://api.furryfusion.net/service/countdown"
details_url = "https://api.furryfusion.net/service/details?"


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def countdown(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "兽聚":
        async with aiohttp.ClientSession() as session:
            async with session.get(countdown_url) as response:
                if response.status != 200:
                    print(f"请求失败，状态码：{response.status}")
                    return
                res = await response.json()
        msg = ""
        for i, sj in enumerate(res["data"]):
            msg += f"{i + 1}. "
            msg += f"{sj['title']}{'（' + sj['name'] + '）' if sj['name'] != sj['title'] else ''}\n"
            msg += f"{sj['address_province']}·{sj['address_city']}\n"
            msg += f"{sj['time_start']} - {sj['time_end']}\n\n"
        msg += "回复 sj#<序号> 查看展会详细信息"
        await app.send_message(
            group,
            MessageChain(msg),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def details(app: Ariadne, group: Group, message: Annotated[MessageChain, DetectPrefix(["sj#"])]):
    async with aiohttp.ClientSession() as session:
        async with session.get(countdown_url) as response:
            if response.status != 200:
                print(f"请求失败，状态码：{response.status}")
                return
            sj_list = (await response.json())["data"]
        if not message.display.isdigit() or not 0 < int(message.display) < len(sj_list) + 1:
            await app.send_message(
                group,
                MessageChain(ai.run(f"群友输入序号错误给出提醒，{ai.short}")),
            )
            return
        async with session.get(details_url + "title=" + sj_list[int(message.display) - 1]["title"]) as response:
            if response.status != 200:
                print(f"请求失败，状态码：{response.status}")
                return
            res = await response.json()
        data = res["data"]
        info = res["info"][0]
        msg = ""
        msg += f"{data['title']}{'（' + info['name'] + '）' if info['name'] != '' else ''}\n"
        msg += f"{info['address']}\n"
        msg += f"{info['time_start']} - {info['time_end']}\n"
        msg += "状态: "
        if info['state'] == 0:
            msg += "🔴活动结束\n"
        elif info['state'] == 1:
            msg += "🟡预告中\n"
        elif info['state'] == 2:
            msg += "🟢售票中\n"
        elif info['state'] == 3:
            msg += "🟣活动中\n"
        elif info['state'] == 4:
            msg += "🔴活动取消\n"
        msg += "\n"
        if data['brief'] != "":
            msg += data['brief'] + "\n\n"
        if data['url'] != "":
            msg += f"官网: {data['url']}\n"
        if data['bilibili']['url'] != "":
            msg += f"哔哩哔哩: {data['bilibili']['url']}\n"
        if data['weibo']['url'] != "":
            msg += f"微博: {data['weibo']['url']}\n"
        if data['groups']:
            for i, info_group in enumerate(data['groups']):
                msg += f"{chr(9312 + i)}群: {info_group}\n"
        # 下载图片
        response = requests.get(info['image'])
        response.raise_for_status()
        # 打开并转换图像
        image = PILImage.open(BytesIO(response.content)).convert("RGB")
        # 将PNG图像保存到字节流中
        png_bytes = BytesIO()
        image.save(png_bytes, format="PNG")
        # 获取字节数据
        png_bytes_data = png_bytes.getvalue()
        await app.send_message(
            group,
            MessageChain(Image(data_bytes=png_bytes_data)) + MessageChain(msg),
        )
