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
from pages.components.showTop_cos import showTop

cursor = configDB()


def top():
    showTop(2)


def mid():
    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

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
            put_textarea("postText", rows=6, placeholder="分享你的动态").style(
                "height: 160px"
            ),
            None,
            put_image(img).onclick(lambda: getLocalFile()).style("width: 100px"),
            None,
        ],
        size="auto",
    )

    def commit(text, photoPath, userId):
        if text == "" or None:
            return toast("提交失败！请填写——文字内容", color="error")

        # 获取现在的时间戳
        create_time = int(round(time.time() * 1000))
        # 获得 remarks
        remarks = {}
        remarks["remarks"] = []
        remarks_json = json.dumps(remarks, ensure_ascii=False)
        # 拼接 content
        content = {}
        content["text"] = text
        content["photoPath"] = photoPath
        content_json = json.dumps(content, ensure_ascii=False)

        cursor.execute(
            """insert into `share` 
                            (`senderId`, `content`, `remarks`, `create_time`)
                            values
                            ({senderId}, '{content}', '{remarks}', '{create_time}')""".format(
                senderId=userId,
                content=content_json,
                remarks=remarks_json,
                create_time=create_time,
            )
        )
        toast("提交成功",color="success")
        time.sleep(0.5)
        return run_js("window.location.href='community?id={id}'".format(id=userId))

    btn = put_row(
        [
            None,
            put_button(
                "取消",
                onclick=lambda: run_js(
                    "window.location.href='community?id={id}'".format(id=id_query)
                ),
                color="light",
            ),
            put_button(
                "发表",
                onclick=lambda: commit(pin.postText, photoPath, id_query),
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
