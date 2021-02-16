#encoding: utf-8
import base64
import requests
# import pytesseract
from flask import Flask,request
from PIL import Image

#对于flask框架的基本使用，请自行百度学习~
app = Flask(__name__)

@app.route('/')
def body_content():
    return 'post image=<@URLENCODE><@BASE64><@IMG_RAW></@IMG_RAW></@BASE64></@URLENCODE> to /img2text'

@app.route('/img2text', methods=['post'])
def img2text():
    '''
    接收接口调用者传来的图片内容
    '''
    b64_img = request.form['image']
    '''
    #模拟接收接口调用者传来的图片二进制数据，最初调试代码用，测试无误换回接收接口
    img = "source.png"
    img_bin = open(img, 'rb')
    b64_img = base64.b64encode(img_bin.read())
    '''
    if b64_img:
        img_name = SaveAndResizeImage(b64_img)
        return run(img_name)
    else:
        return 'img is null !'

def SaveAndResizeImage(b64_img,img_out='rzimg_out.png', scale=5):
    """
    将图片数据进行base64解码、调整图片大小并保存为文件 -> rzimg_out.png
    b64_img:   输入图片
    img_out:   输出图片
    width:     输出图片宽度
    height:    输出图片宽度
    _type:     输出图片类型（png, jpg, jpeg...）
    """
    bin_img = base64.b64decode(b64_img)
    with open(img_out, 'wb') as f:
        f.write(bin_img)
    img = Image.open(img_out)
    print("\033[34m[*]Original img：\033[0m\033[4m%s\033[0m"%str(img))
    img= convert_img(img, 150)
    width = int(img.size[0] * scale)
    height = int(img.size[1] * scale)
    _type = img.format
    '''
    Image.NEAREST ： 低质量
    Image.BILINEAR： 双线性
    Image.BICUBIC ： 三次样条插值
    Image.ANTIALIAS：高质量
    '''
    rzimg = img.resize((width, height), Image.ANTIALIAS)
    print("\033[34m[*]Resize img：\033[0m\033[4m%s\033[0m"%str(rzimg))
    rzimg.save(img_out, _type)
    img_name = img_out
    return img_name

def convert_img(img, threshold):
    '''
    二次处理     -> 灰度处理
    threshold  -> 二值化阈值
    '''
    img = img.convert("L")
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    print("\033[34m[*]Grey processing：\033[0m\033[4m%s\033[0m"%str(img))
    return img

def baiduOCR_API(img_name):
    '''
    调用百度OCR-API -> 通用文字识别(高精度版)
    '''
    baiduOCR_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    img_bin = open(img_name, 'rb')
    base64_img = base64.b64encode(img_bin.read())
    params = {"image":base64_img}
    '''
    调用百度OCR Access Token[ access_token获取方法：https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu ]
    '''
    access_token = '【百度OCR Access Token】'
    request_url = baiduOCR_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # Bcaptcha = response.json()  #一般建议使用此行返回响应值，然后在captcha-killer中正则匹配
        Bcaptcha = response.json()['words_result'][0]['words']  #由于本案例是简单的4位数字验证码，这里直接取识别的数字
        # print (Bcaptcha)
        return Bcaptcha

def run(img_name):
    '''
    这里主要调用的是baiduOCR
    
    可选择调用 tesseract识别图片 -> 提高验证码识别率需要自行对其字库进行深度训练！
    在本案例中并未对它进行深度训练，(它还是个婴儿~)竟然识别不了本案例中的二维码！经测试本案例外的验证码部分可识别(限定4位纯数字)
    '''
     # reCaptchaimg = pytesseract.image_to_string(img_name, lang='eng').replace(' ', '')
    reCaptchaimg = baiduOCR_API(img_name)
    if reCaptchaimg:
        print("\033[32m[+]\033[0m\033[35mCaptcha Recognition successful!\033[0m\r\n"+" "*3+"\033[32m-> Result：%s\033[0m"%str(reCaptchaimg))
        return reCaptchaimg
    else:
        print("\033[31m[-]Captcha Recognition filed！\033[0m")
        return "\033[31m[-]Captcha Recognition filed！\033[0m"

if __name__ == '__main__':
    # img2text()
    # app.debug = True
    app.run(threaded=True, port=8001, host='0.0.0.0')

