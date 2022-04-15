from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pages.components.showTop_cos import showTop
import sys


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

    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]
    orderId_query = query["orderId"]

    # 通过sql获得页面所需的数据
    cursor.execute(
        "select orderId, username, `describe`, response, `status`, bimModelFilePath, buildingName, `version`, addProvince, addCity, addCounty, addDetails from `order`, `user` where `order`.decoratorId = {id} and `order`.orderId = {orderId} and `order`.userId = `user`.userId;".format(
            id=id_query, orderId=orderId_query
        )
    )
    order = cursor.fetchone()
    # order 中从 0 到 11 排序依次为
    # 0-orderId,
    # 1-decoratorName,
    # 2-describe
    # 3-response,
    # 4-status,
    # 5-bimModelFilePath,
    # 6-buildingName,
    # 7-version
    # 8-addProvince,
    # 9-addCity,
    # 10-addCounty,
    # 11-addDetails,

    def getResponse(response, status, userId, orderId):
        if status == 1:
            return put_markdown("`请先接受订单!`")
        if status >= 3:
            return put_markdown("`订单已结束，无法修改！`")
        if response != "" and response != None:
            return response
        return put_button(
            "点击描述设计",
            onclick=lambda: run_js(
                "window.location.href='response?id={id}&orderId={orderId}'".format(
                    id=id_query, orderId=orderId_query
                )
            ),
        )

    picDiv = put_image(open(order[5], "rb").read())

    colDiv = put_table(
        [
            [put_text("装修公司").style("width: 64px;"), order[1]],
            ["房屋类型", order[6]],
            ["版本型号", order[7]],
            ["房屋地址", order[8] + order[9] + order[10] + order[11]],
            ["订单状态", put_markdown("`{status}`".format(status=getStatus(order[4])))],
            ["装修要求", order[2]],
            [
                "设计描述",
                getResponse(order[3], order[4], id_query, orderId_query),
            ],
        ],
        header=["描述", "内容"],
    )
    put_column([picDiv, None, colDiv]).style("width: 100%;")


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
