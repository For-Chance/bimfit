from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pages.components.showTop_cos import showTop
import sys

# import time
# from datetime import datetime

sys.path.append("../..")
from db.config import *
from pages.components.showTop_cos import showTop

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

    def initiateOrderAgain(id, orderId):
        return run_js("window.location.href='initiateOrder?id={id}'".format(id=id))

    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]
    orderId_query = query["orderId"]

    # 通过sql获得页面所需的数据
    cursor.execute(
        "select orderId, username as decoratorName, `describe`, response, `status`, bimModelFilePath, buildingName, `version`, addProvince, addCity, addCounty, addDetails from `order`, `user` where `order`.userId = {id} and `order`.orderId = {orderId} and `order`.decoratorId = `user`.userId;".format(
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

    picDiv = put_image(open(order[5], "rb").read())

    colDiv = put_table(
        [
            [put_text("装修公司").style("width: 64px;"), order[1]],
            ["房屋类型", order[6]],
            ["版本型号", order[7]],
            ["房屋地址", order[8] + order[9] + order[10] + order[11]],
            ["订单状态", put_markdown("`{status}`".format(status=getStatus(order[4])))],
            ["装修要求", order[2]],
            ["设计描述", order[3]],
            [
                "后续操作",
                put_buttons(
                    [
                        dict(label="联系装修公司", value="1", color="light"),
                        dict(label="重新发起订单", value="1", color="light"),
                    ],
                    onclick=[lambda: toast("联系装修公司"), lambda: initiateOrderAgain(id_query, order[0])],
                ),
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
