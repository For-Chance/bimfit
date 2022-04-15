from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import sys
import time
from datetime import datetime

sys.path.append("../..")
from db.config import *

cursor = configDB()


# flag = 0 订单维护
# flag = 1 发起订单
# flag = 2 家装社区
# flag = 3 消息管理
def showTop(flag):
    # 确定 tab 栏中四个按钮的样式
    tabStyle = ["light", "light", "light", "light"]
    tabStyle[flag] = "primary"

    # username button那里需要调整一下输出的样式,不然不好看
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

    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

    # 通过sql获得用户信息
    cursor.execute(
        "select username,email,gender,role,create_time from user where userId={id}".format(
            id=id_query
        )
    )
    (
        username_found,
        email_found,
        gender_found,
        role_found,
        create_time_found,
    ) = cursor.fetchone()

    # 顶部的布置
    img = open("static\img\logo.png", "rb").read()
    put_row(
        [
            put_image(img),
            None,
            put_row(
                [
                    put_button(
                        "订单维护",
                        onclick=lambda: run_js(
                            "window.location.href='home?id={id}'".format(id=id_query)
                        ),
                        color=tabStyle[0],
                    ),
                    None,
                    put_button(
                        "发起订单",
                        onclick=lambda: run_js(
                            "window.location.href='initiateOrder?id={id}'".format(
                                id=id_query
                            )
                        ),
                        color=tabStyle[1],
                    ),
                    None,
                    put_button(
                        "家装社区",
                        onclick=lambda: run_js(
                            "window.location.href='community?id={id}'".format(
                                id=id_query
                            )
                        ),
                        color=tabStyle[2],
                    ),
                    None,
                    put_button(
                        "消息管理",
                        onclick=lambda: run_js(
                            "window.location.href='message?id={id}'".format(id=id_query)
                        ),
                        color=tabStyle[3],
                    ),
                    None,
                ],
                size="25% 10px 25% 10px 25% 10px 25%",
            ),
            None,
            # put_row 内 None, put_button, put_button, 然后第一个put_button onclick后popup显示
            put_row(
                [
                    None,
                    put_button(
                        getUsername("{username}".format(username=username_found)),
                        onclick=lambda: popup(
                            "用户信息",
                            put_table(
                                [
                                    ["描述", "内容"],
                                    ["昵称", username_found],
                                    ["邮箱", email_found],
                                    ["性别", "男" if gender_found == 1 else "女"],
                                    ["用户类型", "普通用户" if role_found == 1 else "装修公司"],
                                    [
                                        "创建时间",
                                        datetime.fromtimestamp(
                                            create_time_found / 1000.0
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                    ],
                                ]
                            ),
                        ),
                        color="info",
                    ),
                    put_button(
                        "退出登录",
                        onclick=lambda: run_js("window.location.href='/login'"),
                        color="dark",
                    ),
                ],
                size="2% 48% 48%",
            ),
        ],
        size="20%  5% 45% 5% 25%",
    )
