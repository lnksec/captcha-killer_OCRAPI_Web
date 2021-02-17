# encoding:utf-8
import requests
'''
    client_id 为官网获取的AK， client_secret 为官网获取的SK
'''

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=  &client_secret=  '

response = requests.get(host)
if response:
    #print(response.json())
    with open('api_token.json', 'a+') as f:
        f.write(str(response.json()))
        print("API Token saved successful!!!")
