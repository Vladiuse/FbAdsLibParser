import requests as req

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'


def change_proxy_ip(url:str):
    headers = {
        'User-Agent': USER_AGENT,
    }
    url = url + '&format=json'
    try:
        res = req.get(url, headers=headers)
        print(res.status_code)
        print(res.text)
    except Exception as error:
        print(error)
        print('Change proxy IP error')


if __name__ == '__main__':
    url = 'https://changeip.mobileproxy.space/?proxy_key=0cb0824233c5a074a100cc8a2410dbc9&format=json'
    change_proxy_ip(url)


