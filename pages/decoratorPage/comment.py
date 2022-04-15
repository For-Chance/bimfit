from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pages.components.showTop_cos import showTop
import sys
import json
import time
from datetime import datetime

sys.path.append("../..")
from db.config import *
from pages.components.showTop_dec import showTop

cursor = configDB()


# 获取类型
def getType(type):
    if type == 1:
        return "用户"
    elif type == 2:
        return "装修公司"
    elif type == 3:
        return "管理者"
    else:
        return "null"


def top():
    showTop(2)


def myContent(username, role, content, create_time):
    infoDiv = put_row(
        [
            None,
            put_markdown("**{username}**".format(username=username)),
            None,
            put_markdown("`普通用户`" if role == 1 else "`装修公司`"),
            None,
            put_markdown(
                "发布时间：`{create_time}`".format(
                    create_time=datetime.fromtimestamp(create_time / 1000.0).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            ),
            None,
        ],
        size="2% 10% 2% 10% 34.5% 39.5% 2%",
    )
    commentDiv = put_row(
        [
            None,
            put_text(json.loads(content)["text"]).style(
                "background-color:#eee;border-radius:6px;"
            ),
            None,
        ],
        size="2% 96% 2%",
    )
    # 只渲染前两个 照片
    if json.loads(content)["photoPath"] == []:
        imgDiv = None
    else:
        imgDiv = put_row(
            [
                None,
                put_image(
                    open(
                        json.loads(content)["photoPath"][0],
                        "rb",
                    ).read()
                ).style("height: 235px; border-radius: 10px;"),
                None,
                put_image(
                    open(
                        json.loads(content)["photoPath"][1],
                        "rb",
                    ).read()
                ).style("height: 235px; border-radius: 10px;"),
                None,
            ],
            size="2% 47% 2% 47% 2%",
        )
    unitDiv = put_column(
        [
            put_column([None, infoDiv], size="25% 75%"),
            commentDiv,
            put_column([imgDiv, None], size="90% 10%"),
        ]
        if imgDiv != None
        else [put_column([None, infoDiv], size="25% 75%"), commentDiv],
        size="auto",
    ).style("background-color: #f9f9f9; border-radius: 10px; border: 1px solid #aaa;")
    return unitDiv


def getUsername(userId):
    cursor.execute(
        "select username from `user` where userId = {userId};".format(userId=userId)
    )
    return cursor.fetchone()[0]


# 评论区
def myComment(comments):
    commentsGroups = []
    if comments != []:
        for ls in comments:
            commentsGroups.append(put_text(getUsername(ls[0]) + "：" + ls[1]))
        return put_collapse("点击展开评论", put_column(commentsGroups), open=True)
    else:
        return put_collapse("点击展开评论", put_text("暂无评论"), open=True)


# 更新信息
def updateMessages(shareId, userId, comments, inputMessage):
    if inputMessage == "":
        toast("请输入非空信息", position="center", color="error")
    else:
        A = [userId, inputMessage]
        comments.append(A)
        remarks = {}
        remarks["remarks"] = comments
        remarks = json.dumps(remarks, ensure_ascii=False)
        print(remarks)
        print(type(remarks))
        cursor.execute(
            "update `share` set remarks = '{remarks}' where shareId = {shareId}".format(
                remarks=remarks, shareId=shareId
            )
        )
        remove(scope="mid")
        with use_scope("mid", clear=True):
            mid()


# 输入
def myInput(shareId, userId, comments):
    textareaDiv = put_input("inputMessage", placeholder="请输入评论", type="text")
    buttonMessage = put_button(
        "发送",
        onclick=lambda: updateMessages(shareId, userId, comments, pin.inputMessage),
    )
    put_column([textareaDiv, buttonMessage], size="60px 60px")


def mid():
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]
    shareId_query = query["shareId"]
    senderId_query = query["senderId"]

    cursor.execute(
        "select username, `role`, content, `share`.create_time, remarks, shareId from `share`,`user` where `user`.userId = senderId and shareId = {shareId} and senderId = {senderId};".format(
            shareId=shareId_query, senderId=senderId_query
        )
    )
    share = cursor.fetchone()
    # order 中从 0 到 4 排序依次为
    # 0-username,
    # 1-role,
    # 2-content,
    # 3-create_time,
    # 4-remarks,
    # 5-shareId

    myContent(share[0], share[1], share[2], share[3])
    myComment(json.loads(share[4])["remarks"])
    myInput(share[5], id_query, json.loads(share[4])["remarks"])
    # put_column([ContentDiv,None, CommentDiv, InputDiv], size="auto")


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
