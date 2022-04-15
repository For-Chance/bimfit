from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pages.components.showTop_cos import showTop
import json
import sys
import tkinter as tk
from tkinter import filedialog
import time

sys.path.append("../..")
from db.config import *
from pages.components.showTop_cos import showTop

cursor = configDB()


def top():
    showTop(1)


def write(province, city, area, houseType, company, require):
    address = {"province": province, "city": city, "area": area}

    dataWrite = {
        "address": address,
        "housetype": houseType,
        "company": company,
        "require": require,
    }

    with open("initiate_order_data", "w", encoding="utf-8") as f:
        json.dump(dataWrite, f)


def read():
    with open("initiate_order_data", "r", encoding="utf-8") as f:
        dataRead = json.load(f)
        print(dataRead)


def mid():
    # get URL parameters of current page
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    id_query = query["id"]

    img = open("static/img/pic.png", "rb").read()

    # 房屋地址
    province_selected = "湖北省"
    city_selected = "武汉市"

    def getlist(tuple):
        ls = []
        for ele in tuple:
            ls.append(ele[0])
        return ls

    def getProvince():
        cursor.execute("select distinct province from chineseaddress;")
        return getlist(cursor.fetchall())

    def getCity(province):
        if province != "":
            cursor.execute(
                "select distinct city from chineseaddress where province = '{province}';".format(
                    province=province
                )
            )
            return getlist(cursor.fetchall())
        else:
            return [""]

    def getCounty(province, city):
        if province != "" and city != "":
            cursor.execute(
                "select distinct county from chineseaddress where province = '{province}' and city = '{city}';".format(
                    province=province, city=city
                )
            )
            return getlist(cursor.fetchall())
        else:
            return [""]

    def changeProvince(province):
        global province_selected
        if province_selected != province:
            print(province_selected)
            province_selected = province

    houseAddressDiv = put_row(
        [
            None,
            put_text("房屋地址"),
            put_column(
                [
                    put_row(
                        [
                            put_select(
                                "province",
                                options=getProvince(),
                                value="湖北省",
                                scope="province",
                            ),
                            None,
                            put_select(
                                "city",
                                options=getCity(province_selected),
                                value="武汉市",
                                scope="city",
                            ),
                            None,
                            put_select(
                                "county",
                                options=getCounty(province_selected, city_selected),
                                value="洪山区",
                                scope="county",
                            ),
                        ],
                        size="32.5% 5px 32.5% 5px 32.5%",
                    ),
                    put_input("addDetails", placeholder="请输入详细地址"),
                    None,
                ],
                size="40% 40% 20%",
            ),
        ],
        size="5px 25% 75%",
    ).style("height: 80px; width: 480px;")

    # 房屋类型
    houseType = ["商品房", "别墅", "小洋楼", "自建楼", "商铺", "其他"]
    houseTypeDiv = put_row(
        [
            None,
            put_text("房屋类型"),
            put_select("houseType", options=houseType),
        ],
        size="5px 25% 75%",
    ).style("height: 40px; width: 480px;")

    # 房屋型号
    houseVersionDiv = put_row(
        [
            None,
            put_text("版本型号"),
            put_input("houseVersion", placeholder="请输入 V + 数字，例如 V1.1"),
        ],
        size="5px 25% 75%",
    ).style("height: 40px; width: 480px;")

    # 组合“房屋地址”和“选择户型”和“房屋型号”
    add_typeDiv = put_column(
        [houseAddressDiv, None, houseTypeDiv, houseVersionDiv], size="50% 5px 25% 25%"
    ).style("height: 180px; width: 480px;")

    global bimModelFilePath
    bimModelFilePath = ""

    def getLocalFile():
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost',1)
        filePath = filedialog.askopenfilename()
        toast("文件地址是："+filePath)
        toast("暂未开发上传功能", color="error")
        toast("但是你可以使用其他功能", color="success")
        global bimModelFilePath
        bimModelFilePath = "static\\\img\\\BIM.png"

    # 上传按钮
    uploadDiv = (
        put_image(img)
        .onclick(lambda: getLocalFile())
        .style("border: 1px solid #ddd;border-radius: 10px; height: 180px;")
    )

    # 将“房屋地址”，“户型选择”和“上传按钮”组合
    a = put_row([add_typeDiv, uploadDiv], size="60% 40%")

    # 获得装修公司
    cursor.execute("select username from `user` where role = 2;")
    companyName_found = cursor.fetchall()
    companyName = []
    for ls in companyName_found:
        companyName.append(ls[0])

    # 选择装修公司Div
    b = put_row(
        [
            put_text("选择装修公司"),
            put_collapse(
                "点击展开",
                put_scrollable(
                    put_checkbox("companys", options=companyName),
                    height=100,
                    keep_bottom=True,
                ),
                open=True,
            ),
        ],
        size="15% 85%",
    ).style("height: 40px; width: 830px;")

    # 描述要求文本框
    c = put_row(
        [None, put_text("描述要求"), put_textarea("require", rows=6)], size="5px 15% 85%"
    ).style("height: 250px; width: 830px;")

    # 信息填写部分
    upstairs = put_column([a, b, None, c], size="35% 20% 80px 45%")

    def commit(
        userId,
        province,
        city,
        county,
        Details,
        houseType,
        houseVersion,
        companys,
        require,
        bimModelFilePath,
    ):
        if Details=="" or None:
            return toast("提交失败！请填写——房屋地址",color="error")
        elif houseVersion=="" or None:
            return toast("提交失败！请填写——版本型号",color="error")
        elif bimModelFilePath=="" or None:
            return toast("提交失败！请上传——房屋模型或照片",color="error")
        elif companys==[] or None:
            return toast("提交失败！请选择——装修公司",color="error")
        elif require=="" or None:
            return toast("提交失败！请填写——描述要求",color="error")
        
        # 寻找装修公司对应名字的id
        for company in companys:
            cursor.execute(
                "select userId from `user` where username = '{decoratorName}'".format(
                    decoratorName=company
                )
            )
            (decoratorId,) = cursor.fetchone()
            # 会自动提交
            cursor.execute(
                """INSERT INTO `order` 
            (`userId`, `decoratorId`, `version`, `describe`, `status`, `bimModelFilePath`, `buildingName`, `addProvince`, `addCity`, `addCounty`, `addDetails`) 
            VALUES 
            ('{userId}', '{decoratorId}', '{version}', '{describe}', '{status}', '{bimModelFilePath}', '{buildingName}', '{addProvince}', '{addCity}', '{addCounty}', '{addDetails}');""".format(
                    userId=userId,
                    decoratorId=decoratorId,
                    version=houseVersion,
                    describe=require,
                    status=1,
                    bimModelFilePath=bimModelFilePath,
                    buildingName=houseType,
                    addProvince=province,
                    addCity=city,
                    addCounty=county,
                    addDetails=Details,
                )
            )
        toast("提交成功",color="success")
        time.sleep(0.5)
        return run_js("window.location.href='home?id={id}'".format(id=userId))

    # 提交与保存按钮
    downstairs = put_row(
        [
            None,
            put_button("保存", onclick=lambda: toast("保存"), color="light"),
            put_button(
                "提交",
                onclick=lambda: commit(
                    id_query,
                    pin.province,
                    pin.city,
                    pin.county,
                    pin.addDetails,
                    pin.houseType,
                    pin.houseVersion,
                    pin.companys,
                    pin.require,
                    bimModelFilePath,
                ),
                color="primary",
            ),
        ],
        size="80% 10% 10%",
    )

    # 输出内容
    put_column([None, upstairs, downstairs])


def home():
    with use_scope("top", clear=True):
        top()
    with use_scope("mid", clear=True):
        mid()


def main():
    home()
