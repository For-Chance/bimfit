from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pages.components.showTop_cos import showTop
from pywebio.pin import *
import sys
import time
from datetime import datetime

sys.path.append("../..")
from db.config import *
from pages.components.showTop_cos import showTop

cursor = configDB()

# 发送信息时的回调函数
def updateMessages(senderId, receiverId, inputMessage):
    if inputMessage == "":
        toast("请输入非空信息", position="center", color="error")
    else:
        cursor.execute(
            """insert into `message`
                            (senderId, receiverId, content, status, sendTime)
                            values
                            ({senderId}, {receiverId}, '{content}', 1, {sendTime})""".format(
                senderId=senderId,
                receiverId=receiverId,
                content=inputMessage,
                sendTime=int(round(time.time() * 1000)),
            )
        )
        clear(scope="mid")
        with use_scope("mid", clear=True):
            mid()


def getUsernameText(userId, senderId):
    cursor.execute(
        "select username from `user` where userId = {userId};".format(userId=userId)
    )
    return cursor.fetchone()[0] if userId != eval(senderId) else "我"


# 获取右侧消息
def getMessageGroups(senderId, receiverId):
    cursor.execute("delete from `message` where status = 0 ")
    cursor.execute(
        "select * from message where (senderId,receiverId) = ({senderId}, {receiverId}) or (senderId,receiverId) = ({receiverId}, {senderId}) order by sendTime;".format(
            senderId=senderId, receiverId=receiverId
        )
    )
    messages = cursor.fetchall()
    groups = []
    for i in range(len(messages)):
        groups.append(
            put_markdown(
                "`{senderName}`".format(
                    senderName=getUsernameText(messages[i][1], senderId)[0:2]
                )
                + messages[i][3]
            )
            # if messages[i][1] != messages[i - 1][1] or i==0
            # else put_text(messages[i][3])
        )
    return put_scrollable(put_column(groups), height=500, keep_bottom=False)


def top():
    showTop(3)


def mid():
    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

    # 联系Ta button的回调函数
    # create_time先用现在的时间，后面再覆盖
    def contactTa(userId):
        cursor.execute(
            """insert into `message`
                            (senderId, receiverId, status, sendTime)
                            values
                            ({senderId}, {receiverId}, 0, {sendTime})""".format(
                senderId=eval(id_query),
                receiverId=userId,
                sendTime=int(round(time.time() * 1000)),
            )
        )
        clear(scope="mid")
        with use_scope("mid", clear=True):
            mid()

    # 选择联系人
    cursor.execute("select userId, username from `user`")
    selects = cursor.fetchall()

    allContacts = []
    allContactsId = []
    for select in selects:
        if select[0] != eval(id_query):
            allContacts.append(select[1])
            allContactsId.append(select[0])
    selectDiv = put_row(
        [
            put_select(
                "select",
                options=allContacts,
                scope="select",
            ),
            None,
            put_button(
                "联系TA",
                onclick=lambda: contactTa(allContactsId[allContacts.index(pin.select)]),
            ),
        ],
        size="auto",
    )

    cursor.execute(
        "select * from message where senderId = {id} or receiverId = {id} order by sendTime desc;".format(
            id=id_query
        )
    )
    messages_found = cursor.fetchall()

    # 提取出所有联系人, 按发布时间
    contact_found = []
    for message_found in messages_found:
        if message_found[1] != eval(id_query) and message_found[1] not in contact_found:
            contact_found.append(message_found[1])
        if message_found[2] != eval(id_query) and message_found[2] not in contact_found:
            contact_found.append(message_found[2])

    def getUsernameBtn(userId, firstId):
        cursor.execute(
            "select username from `user` where userId = {userId};".format(userId=userId)
        )
        username = cursor.fetchone()[0]
        if len(username) > 11:
            usernameShow = username[0:10] + "..."
        else:
            usernameShow = username
        return put_markdown(
            ("`{usernameShow}`" if userId != firstId else "**{usernameShow}**").format(
                usernameShow=usernameShow
            )
        ).onclick(lambda: contactTa(userId))

    # 提取所有联系人
    contacts = []
    for ls in contact_found:
        contacts.append(getUsernameBtn(ls, contact_found[0]))
    contactDiv = put_scrollable(put_column(contacts, size="auto"), height=510)
    leftDiv = put_column([selectDiv, contactDiv], size="40px")

    # 右上消息框
    # 默认为
    receiverId = contact_found[0]
    messagesDiv = getMessageGroups(id_query, receiverId)

    # 右下输入框
    textareaDiv = put_input("inputMessage", placeholder="请输入消息", type="text")
    buttonMessage = put_button(
        "发送",
        onclick=lambda: updateMessages(id_query, contact_found[0], pin.inputMessage),
    )
    buttonRefresh = put_button("刷新", onclick=lambda: refreshMid())
    rightDiv = put_column(
        [
            messagesDiv,
            put_row([textareaDiv, buttonMessage, buttonRefresh], size="76% 12% 12%"),
        ],
        size="auto",
    )
    put_row([leftDiv, None, rightDiv], size="30% 2% 68%")


def refreshMid():
    clear(scope="mid")
    with use_scope("mid", clear=True):
        mid()


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
