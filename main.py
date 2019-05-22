#import urequests as requests
import urequests
import json
import time
from machine import SPI,Pin   #导入SPI、Pin库
import ssd1306                #导入OLED显示屏驱动库
from ds3231 import DS3231     #导入DS3231时钟模块库
from machine import Timer     #导入Timer库

#-----------------------DS3231模块-----------------------#
ds=DS3231()            #ds3231初始化
NOW_DATE = ''
#-----------------------OLED显示屏-----------------------#
#SPI接口对应的引脚定义
spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(12,Pin.OUT), mosi=Pin(13,Pin.OUT), miso=Pin(2))
#OLED显示屏的设置，128宽 64高 spi对象 DC接的G15 RES接的G16 CS接的G5
display = ssd1306.SSD1306_SPI(128, 64, spi, Pin(15),Pin(16), Pin(5))
display.poweron()                   #打开显示屏
display.init_display()              #初始化显示
display.text('Waiting.....',1,1)    #显示的内容，x坐标，y坐标
display.show()                      #进行显示

def getNetTime():
    url = 'http://quan.suning.com/getSysTime.do'
    res=urequests.get(url).text
    print(res)
    j=json.loads(res)
    t2_date = j['sysTime2'].split()[0] #日期
    t2_time = j['sysTime2'].split()[1] #时间
    display.fill(0)                  #清屏
    display.text(t2_date,1,2)
    display.text(t2_time,1,15)
    display.show()
    #初始日期和时间，设置一次即可
    ds.DATE([int(x) for x in t2_date[2:].split('-')])   #设置初始日期年、月、日
    ds.TIME([int(x) for x in t2_time.split(':')])   #设置初始时间时、分、秒

def updateTime(t):
    global NOW_DATE
    #读取日期和时间，拼接成正常的时间格式
    date = '20'+'-'.join(ds.DATE())
    time = ':'.join(ds.TIME())
    if NOW_DATE != date:
        getNetTime()       #设定每天校对一下时间
        NOW_DATE = date
    else:
        display.fill(0)                  #清屏
        display.text(date,1,2)
        display.text(time,1,15)
        display.show()

if __name__ == '__main__':
    getNetTime()
    time.sleep(1)
    #-----------------------Timer定时器-----------------------#
    tim = Timer(-1)  #新建一个定时器
    #每隔1秒执行一次updateTime函数调用，用于更新OLED显示屏上的时间
    tim.init(period=1000, mode=Timer.PERIODIC, callback=updateTime)