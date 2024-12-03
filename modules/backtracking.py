from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Friend, Member

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing_extensions import Annotated

from bot_config import ADMIN_QQ_ACCOUNT, RECALL_GROUPS
from modules.fur_img import img

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[FriendMessage, GroupMessage]))
async def backtracking(app: Ariadne, sender: Friend | Member, message: Annotated[MessageChain, DetectPrefix(["##"])]):
    if sender.id not in ADMIN_QQ_ACCOUNT:
        return
    mes = message.display.split()
    if int(mes[1]) < len(RECALL_GROUPS):
        mes[1] = RECALL_GROUPS[int(mes[1])]
    await globals()[mes[0]](app, await app.get_group(int(mes[1])), MessageChain(mes[2]), member = app.get_member(sender.id))
