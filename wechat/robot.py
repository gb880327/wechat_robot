import requests
import json
import random


def robot(question: str):
    if random.randrange(1, 10000) % 2 == 0:
        answer = itpk_robot(question)
    else:
        answer = ownthink_rebot(question)
        if answer == "":
            answer = itpk_robot(question)
    return answer


def itpk_robot(question: str):
    """
    茉莉机器人
    :param question:
    :return:
    """
    api_url = "http://i.itpk.cn/api.php"
    rep = requests.post(api_url, data={
        "question": question,
        "limit": 8,
        "api_key": "5246e6c2ee919737d39d42f4eae45840",
        "api_secret": "08qpebl7o8ae",
        "type": "普通文本"
    })
    if rep.status_code == 200:
        try:
            json_msg = json.loads(rep.text.encode("UTF-8"))
            msg = ""
            for (k, v) in json_msg.items():
                msg += v + '\n----------------------------\n'
            return msg
        except ValueError:
            return rep.text + '\n----------------------------\n'


def ownthink_rebot(question: str):
    """
    ownthink 机器人
    appid 0b786ac5e8053867a2536b3fcc5f70eb
    secret bc6b69ad8e7e48f0a6eb0219b79a2ab9
    :param question:
    :return:
    """
    api_url = "https://api.ownthink.com/bot"
    rep = requests.post(api_url, data={"spoken": question})
    if rep.status_code == 200:
        data = json.loads(rep.text)
        if data['message'] == 'success':
            return data['data']['info']['text'] + '\n----------------------------\n'
    return ""
