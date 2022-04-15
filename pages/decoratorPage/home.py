from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import sys
import time
from datetime import datetime

sys.path.append("../..")
from db.config import *
from pages.components.showTop_dec import showTop

cursor = configDB()


def top():
    showTop(0)



def mid():
    def getStatus(status):
        if status == 0:
            return "正在创建"
        elif status == 1:
            return "尚未接受"
        elif status == 2:
            return "尚未完成"
        elif status == 3:
            return "完成订单，订单已结束"
        elif status == 4:
            return "非完成订单原因订单结束"

    def deleteOrder(orderId):
        cursor.execute(
            "delete from `order` where orderId = {orderId};".format(orderId=orderId)
        )
        clear(scope="mid")
        with use_scope("mid", clear=True):
            mid()

    def getDeleteOrderBtn(eachOrder):
        return put_button(
            "删除订单",
            onclick=lambda: deleteOrder(eachOrder[0]),
            color="light",
            disabled=False if eachOrder[3] >= 3 else True,
        )

    def confirmAccept(orderId, status):
        cursor.execute(
            "update `order` set status = 2 where orderId = {orderId};".format(
                orderId=orderId
            )
        )
        clear(scope="mid")
        with use_scope("mid", clear=True):
            mid()

    def getConfirmAcceptBtn(eachOrder):
        return put_button(
            "确认接受",
            onclick=lambda: confirmAccept(eachOrder[0], eachOrder[3]),
            color="light",
            disabled=False if eachOrder[3] == 1 else True,
        )

    def getStatus_text(eachOrder):
        return put_column(
            [
                put_markdown("状态：`{status}`".format(status=getStatus(eachOrder[3]))),
                put_markdown(
                    "欲装修描述：**{response}**".format(
                        response="无"
                        if eachOrder[2] == "" or type(eachOrder[2]=='NoneType')
                        else eachOrder[2]
                        if len(eachOrder[2]) < 40
                        else eachOrder[2][0:38] + "..."
                    )
                ),
            ],
            size="30% 70%",
        ).onclick(
            lambda: run_js(
                "window.location.href='orderDetails?id={id}&orderId={orderId}'".format(
                    id=id_query, orderId=eachOrder[0]
                )
            )
        )

    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

    # 通过sql获得页面所需的数据
    cursor.execute(
        "select orderId, username, response, `status`, bimModelFilePath from `order`, `user` where `order`.decoratorId = {id} and `order`.userId = `user`.userId;".format(
            id=id_query
        )
    )
    orders = cursor.fetchall()

    # 循环所有订单
    div_groups = []
    for eachOrder in orders:
        BIMimg = put_image(open(eachOrder[4], "rb").read()).style(
            "height: 80px; border-radius:10px"
        )
        status_text = getStatus_text(eachOrder)
        btns = put_column(
            [
                put_markdown(
                    "用户：**{username}**".format(
                        username=eachOrder[1]
                        if len(eachOrder[1]) < 8
                        else eachOrder[1][0:6] + "..."
                    )
                ),
                put_row(
                    [
                        getDeleteOrderBtn(eachOrder),
                        getConfirmAcceptBtn(eachOrder),
                    ]
                ),
            ],
            size="35% 65%",
        )
        div = put_row([BIMimg, status_text, btns], size="18% 54% 28%").style(
            "background-color: #eee; border-radius: 10px;"
        )
        div_groups.append(div)
        div_groups.append(None)
    size_groups = "80px 10px " * len(orders)
    o = put_column(div_groups, size=size_groups)
    put_scrollable(o, height=800, keep_bottom=True).style("background-color: #f9f9f9;")


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
