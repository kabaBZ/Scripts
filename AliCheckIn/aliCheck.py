"""
阿里网盘每日签到脚本
"""
import os
import time
import datetime

import requests
from Utils.DBUtils import RedisOpration, RedisProfile

from Utils.AlertUtils import XiaTuiAlert

XT_Token = os.environ.get("XT_Token")
if not XT_Token:
    raise Exception("系统变量中不存在虾推Token!")

refresh_token = os.environ.get("ali_refresh_token")
if not refresh_token:
    raise Exception("系统变量中不存在阿里网盘Token!")


def get_token():
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    # 获取token
    res = requests.post("https://auth.aliyundrive.com/v2/account/token", json=data)
    tokens = res.json()
    access_token = tokens["access_token"]
    phone = tokens["user_name"]
    access_token2 = "Bearer " + access_token
    return access_token2


def check_in(access_token2):
    # 签到接口
    data = {"_rx-s": "mobile"}
    headers = {"Authorization": access_token2}
    res = requests.post(
        "https://member.aliyundrive.com/v1/activity/sign_in_list",
        headers=headers,
        json=data,
    )
    count = res.json()
    signin_count = count["result"]["signInCount"]
    time.sleep(3)
    return signin_count


def accept_reward(access_token2, signin_count):
    # 领取奖励
    data = {"signInDay": signin_count}
    headers = {"Authorization": access_token2}
    res = requests.post(
        "https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile",
        headers=headers,
        json=data,
    )
    result = res.json()
    return result


def parse_result(signin_count, result):
    if not result["success"]:
        print("签到失败：{}".format(result))
        XiaTuiAlert.send(title="签到失败", msg="签到失败：{}".format(result))
    else:
        print("签到成功, 本月累计签到" + str(signin_count) + "天")
        print(
            "本次签到获得" + result["result"]["name"] + "," + result["result"]["description"]
        )
        XiaTuiAlert.send(
            title="签到成功, 本月累计签到" + str(signin_count) + "天",
            msg="本次签到获得"
            + result["result"]["name"]
            + ","
            + result["result"]["description"],
        )


def run():
    if not RedisOpration(RedisProfile).sadd(
        "aliCheck", str(datetime.datetime.now().date())
    ):
        return
    try:
        access_token2 = get_token()
        signin_count = check_in(access_token2)
        result = accept_reward(access_token2, signin_count)
        if not result["success"]:
            RedisOpration(RedisProfile).srem(
                "aliCheck", str(datetime.datetime.now().date())
            )
        parse_result(signin_count, result)
    except:
        RedisOpration(RedisProfile).srem(
            "aliCheck", str(datetime.datetime.now().date())
        )
