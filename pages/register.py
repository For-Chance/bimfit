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
def register():
    data = input_group(
        "用户注册(直接提交回到登录)",
        [
            input("用户名", name="username", placeholder="不能为空"),
            input("邮箱", name="email", placeholder="不能为空"),
            input("密码", name="password", type=PASSWORD, placeholder="不能为空"),
            input("确认密码", name="confirm", type=PASSWORD, placeholder="不能为空, 与密码保持一致"),
            input("性别", name="gender", placeholder="不能为空，填1或0，1-男，0-女"),
            input("是否为装修公司", name="isCompany", placeholder="不能为空，填1或0，1-是，0-否"),
        ],
    )
    if (
        data["username"] == ""
        and data["email"] == ""
        and data["password"] == ""
        and data["confirm"] == ""
        and data["gender"] == ""
        and data["isCompany"] == ""
    ):
        run_js("window.location.href='login'")
    else:
        if data["username"] == "":
            toast("用户名为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["email"] == "":
            toast("邮箱为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["password"] == "":
            toast("密码为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["confirm"] == "":
            toast("确认密码为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["confirm"] != data["password"]:
            toast("两次密码输入不一致", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["gender"] == "":
            toast("性别为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["gender"] not in ["1", "0"]:
            toast("性别填写不规范", color="error")
            toast("填1或0", color="info")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["isCompany"] == "":
            toast("是否为装修公司为空", color="error")
            time.sleep(1)
            run_js("window.location.href='register'")
        elif data["isCompany"] not in ["1", "0"]:
            toast("是否为装修公司填写不规范", color="error")
            toast("填1或0", color="info")
            time.sleep(1)
            run_js("window.location.href='register'")
        else:
            commit(
                data["username"],
                data["email"],
                data["password"],
                data["gender"],
                data["isCompany"],
            )


def commit(username, email, password, gender, isCompany):
    cursor.execute(
        """insert into `user`
                        (`username`, `email`, `password`, `create_time`, `gender`, `role`)
                        values
                        ('{username}','{email}','{password}','{create_time}',{gender},{role})""".format(
            username=username,
            email=email,
            password=password,
            create_time=int(round(time.time() * 1000)),
            gender=eval(gender),
            role=1 if isCompany == "0" else 2,
        )
    )
    run_js("window.location.href='login'")


def main():
    with use_scope("login", clear=True):
        register()


# start_server(login, port=8086, debug=True)
