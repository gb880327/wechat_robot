import requests


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
        return rep.text
    return ""
