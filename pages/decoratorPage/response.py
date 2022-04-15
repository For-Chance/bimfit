from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import sys
import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

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
    orderId_query = query["orderId"]

    global photoPath
    photoPath = []

    def getLocalFile():
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        filePath = filedialog.askopenfilename()
        toast("文件地址是：" + filePath)
        toast("暂未开发上传功能", color="error")
        toast("但是你可以使用其他功能", color="success")
        global photoPath
        photoPath = []

    img = open("static/img/pic3.png", "rb").read()
    contentDiv = put_column(
        [
            put_textarea("postText", rows=6, placeholder="描述你的设计").style(
                "height: 160px"
            ),
            None,
            put_image(img).onclick(lambda: getLocalFile()).style("width: 100px"),
            None,
        ],
        size="auto",
    )

    def commit(response, orderId, userId):
        if response == "" or None:
            return toast("提交失败！请填写——描述设计", color="error")

        cursor.execute(
            """update `order`
                            set response = '{response}'
                            where orderId = {orderId}""".format(
                response=response, orderId=orderId
            )
        )
        toast("提交成功", color="success")
        time.sleep(0.5)
        return run_js(
            "window.location.href='orderDetails?id={id}&orderId={orderId}'".format(
                id=userId, orderId=orderId_query
            )
        )

    btn = put_row(
        [
            None,
            put_button(
                "取消",
                onclick=lambda: run_js(
                    "window.location.href='orderDetails?id={id}&orderId={orderId}'".format(
                        id=id_query, orderId=orderId_query
                    )
                ),
                color="light",
            ),
            put_button(
                "提交",
                # 目前只提交 response
                onclick=lambda: commit(pin.postText, orderId_query, id_query),
                color="primary",
            ),
        ],
        size="80% 10% 10%",
    )

    put_column([None, contentDiv, btn], size="50px")


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
