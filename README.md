# captcha-killer_OCRAPI_Web

 `captcha-killer`通过`python`建立的`web`服务接口调用 `baiduOCR`接口 或者`tesseract `识别验证码，本项目基于`c0ny1`的源码修改(见参考地址)。

#### 0x01 直接调用`baiduOCR`接口识别

* 免费识别次数比较有限,尤其识别精度较高的接口
 
* 不能识别太小的验证码图片，而较大的图片非常容易识别不全甚至也无法识别

* 免费接口就是免费接口，受条件限制比较大，识别效果比较一般...

#### 0x02 利用`python`的`tesseract`模块识别

* 直接安装调用，只可识别部分一般验证码，如4位纯数字验证码，而且精度也是很一般，

需要对tesseract字库进行深度训练来提高识别的精度。

**整体识别流程：**

* 通过`python`启动一个`web`服务器开放一个接口来接收`captcha-killer`传来的验证码图片内容，然后调用`tesseract`来识别，
 
最后返回结果给`captcha-killer`。

#### 0x03  思路

* 通过`python`建立`web`服务，在`python`中调用`baiduOCR`接口（或者`tesseract`模块），再利用`burpsuit`中`captcha-killer`调用该`web`服务

接口从而间接调用`baiduOCR`接口进行识别，`captcha-killer`传入的图片数据进行二次处理（灰度处理）、图片大小调整，然后交由`baiduOCR`接口（或者

`tesseract`模块）进行识别，再将响应（识别）结果返回给`captcha-killer`。


*** PS：细化的内容就这几点，比较鸡肋，如果您有更好的修改或优化建议 ，欢迎评论交流 ~ ***


**参考地址：**

1. [`captcha-killer`调用`tesseract-ocr`识别验证码](https://github.com/c0ny1/captcha-killer/tree/master/doc/case01)

2. [`python`识别图片中方框`Python`中验证码识别的三种解决方案](https://blog.csdn.net/weixin_34959771/article/details/112337901)



