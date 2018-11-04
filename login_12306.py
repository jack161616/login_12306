# *-* coding:utf-8 *-*
# time:2018-11-4
# 实现模拟登陆12306
#登录流程;
# 1.session访问登陆页面：login_page_url = 'https://kyfw.12306.cn/otn/login/init'
# 2.下载验证码，
# 3.效验验证码
# 4.效验用户名和密码，先效验验证码，验证码成功后然后在效验用户名和密码
# 5.获取权限token
# 6.验证token

import requests
import config

# 验证码图片像素坐标位置：
map = {
    '1':'35,77',
    '2':'105,77',
    '3':'175,77',
    '4':'245,77',
    '5':'35,147',
    '6':'105,147',
    '7':'175,147',
    '8':'245,147',
}

# 转换为所需的坐标位置
def get_point(index):
    index = index.split(',')
    print(index)
    temp = []
    for item in index:
        temp.append(map[item])
    print(temp)
    print(','.join(temp))
    return ','.join(temp)

session = requests.session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
session.headers.update(headers)

# 1.访问登陆页面获取cookies值。
login_page_url = 'https://kyfw.12306.cn/otn/login/init'
# login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
session.get(login_page_url)
print(session.cookies)

# 2.下载验证码
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5242071285316263'
captcha_response = session.get(captcha_url)
print(captcha_response)
with open('captcha2.jpg', 'wb') as f:
    f.write(captcha_response.content)

# 3.效验验证码
check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
form_data_captcha = {
    'answer':get_point(input('请输入正确的序号：')),
    'rand':'sjrand',
    'login_site':'E'
}
check_response = session.post(check_captcha_url, data=form_data_captcha)
print('--验证码---：',check_response.json())
if check_response.json()['result_code'] == '4':
    # 验证码验证成功
    # 效验用户名和密码
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    form_data_login = {
        'username':config.username,
        'password':config.password,
        'appid': 'otn'
    }
    login_response = session.post(login_url, data=form_data_login)
    print('----用户登录---：',login_response.json())
    if login_response.json()['result_code'] == 0:
        # 4.验证权限token
        uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        uamtk_response = session.post(uamtk_url, data={'appid':'otn'})
        print('--权限获取--：',uamtk_response.json())
        if uamtk_response.json()['result_code'] == 0:
            # 6.验证权限token
            auth_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            auth_response = session.post(auth_url, data={'tk':uamtk_response.json()['newapptk']})
            print('--token验证---',auth_response.json())
        else:
            print('权限获取失败')
    else:
         print('用户名或者密码错误')
else:
    print('验证码错误')




