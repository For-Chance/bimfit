from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
from pywebio.session import run_js
import pymysql
import json
import time

# 没找到更好的方法去配置全局数据库
# 先这么操作吧
import sys

sys.path.append("..")
from db.config import *

cursor = configDB()


# 使用print输出字符串
def login():
    cursor.execute("select email,password from user;")
    check = list(cursor.fetchall())
    # print(check)
    # print("上面是check\n")
    data = input_group(
        "用户登录(直接提交进入注册)",
        [
            input("邮箱", name="email"),
            input("密码", name="password", type=PASSWORD),
        ]
    )
    flag = 0
    if data["email"] == "" and data["password"] == "":
        run_js("window.location.href='register'")

    for ls in check:
        if data["email"] == ls[0] and data["password"] == ls[1]:
            toast("登录成功", position="center", color="success", duration=1)
            flag = 1
            cursor.execute(
                "select userId,role from user where email='{email}' and password='{password}';".format(
                    email=str(data["email"]), password=str(data["password"])
                )
            )
            (id_found, role) = cursor.fetchone()
            time.sleep(0.5)
            if role == 1:
                run_js(
                    "window.location.href='/costomerPage/home?id={id_found}'".format(
                        id_found=id_found
                    )
                )
            elif role == 2:
                run_js(
                    "window.location.href='/decoratorPage/home?id={id_found}'".format(
                        id_found=id_found
                    )
                )
    if flag == 0:
        toast("登录失败", position="center", color="error", duration=1)
        time.sleep(0.5)
        run_js("window.location.href='/login'")


def main():
    with use_scope("login", clear=True):
        login()


# start_server(login, port=8086, debug=True)
