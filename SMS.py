# coding=utf-8
#only for Python 3
import urllib
import urllib.request
import hashlib

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()
def SMS_send(name, elder_name):
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    smsapi = "http://api.smsbao.com/"
    # message platfrom ID
    user = 'ray009'
    # message platfrom password
    password = md5('7373494259a')
    # message content
    content = '我草你码' + name+ '哈哈哈'+ elder_name +'你妈的头'
    # phone number
    phone = '18146600669'

    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print (statusStr[the_page])

