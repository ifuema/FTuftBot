import random

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "来只兽兽":
         await app.send_message(
            group,
            MessageChain(Image(url=f"https://uapis.cn/api/imgapi/furry/img{random.choice(['', 'z', 's'])}4k.php")),
         )
