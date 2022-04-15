from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import sys
import json
import time
from datetime import datetime

sys.path.append("../..")
from db.config import *
from pages.components.showTop_dec import showTop

cursor = configDB()


def top():
    showTop(2)


def mid():
    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

    # 获得所有信息
    cursor.execute(
        "select shareId, senderId, username, `role`, content, `share`.create_time from `share`,`user` where `user`.userId = senderId order by `share`.create_time desc;"
    )
    shares = cursor.fetchall()

    def getText(text):
        if len(text) >= 150:
            return text[0:148] + "..."
        else:
            return text

    put_button(
        "我也发一条动态",
        onclick=lambda: run_js(
            "window.location.href='post?id={id}'".format(id=id_query)
        ),
    )

    def getUsername(username):
        # 假设要么全是中文，要么全是英文
        # 全是中文不超过4个，全是英文不超过8个
        isChinese = True
        for _char in username:
            if not "\u4e00" <= _char <= "\u9fa5":
                isChinese = False
        if isChinese:
            return username[0:4]
        else:
            return username[0:8]

    # 循环所有动态
    # print(json.loads(shares[0][2])["photoPath"][0])
    shareDiv = []
    size_groups = ""
    for eachShare in shares:
        infoDiv = put_row(
            [
                None,
                put_markdown("**{username}**".format(username=getUsername(eachShare[2]))),
                None,
                put_markdown("`普通用户`" if eachShare[3] == 1 else "`装修公司`"),
                None,
                put_markdown(
                    "发布时间：`{create_time}`".format(
                        create_time=datetime.fromtimestamp(
                            eachShare[5] / 1000.0
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    )
                ),
                None,
            ],
            size="2% 10% 2% 10% 34.5% 39.5% 2%",
        )
        contentDiv = put_row(
            [
                None,
                put_text(getText(json.loads(eachShare[4])["text"])).style(
                    "background-color:#eee;border-radius:6px;"
                ),
                None,
            ],
            size="2% 96% 2%",
        )
        # 只渲染前两个 照片
        if json.loads(eachShare[4])["photoPath"] == []:
            imgDiv = None
        else:
            imgDiv = put_row(
                [
                    None,
                    put_image(
                        open(
                            json.loads(eachShare[4])["photoPath"][0],
                            "rb",
                        ).read()
                    ).style("height: 235px; border-radius: 10px;"),
                    None,
                    put_image(
                        open(
                            json.loads(eachShare[4])["photoPath"][1],
                            "rb",
                        ).read()
                    ).style("height: 235px; border-radius: 10px;"),
                    None,
                ],
                size="2% 47% 2% 47% 2%",
            )

        def getUnitDiv(eachShare):
            return (
                put_column(
                    [infoDiv, contentDiv, imgDiv]
                    if imgDiv != None
                    else [infoDiv, contentDiv],
                    size="auto",
                )
                .onclick(
                    lambda: run_js(
                        "window.location.href='comment?id={id}&shareId={shareId}&senderId={senderId}'".format(
                            id=id_query, shareId=eachShare[0], senderId=eachShare[1]
                        )
                    )
                )
                .style(
                    "background-color: #f9f9f9; border-radius: 10px; border: 1px solid #aaa;"
                )
            )

        unitDiv = getUnitDiv(eachShare)
        shareDiv.append(unitDiv)
        size_groups = size_groups + "376px" if imgDiv != None else "120px"
    p = put_column(shareDiv, size=size_groups)
    put_scrollable(p, height=1600, keep_bottom=True)


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
