import requests
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
from easyhid import Enumeration
from time import sleep
import signal
import sys
from datetime import datetime
from datetime import timedelta
import keyboard
import numpy as np
from pytz import timezone
import configparser
import os
import warnings

from requests import api
warnings.filterwarnings("ignore")

def buffer_plot_and_get(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def signal_handler(sig, frame):
    try:
        dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
        dev.close()
        print("\n")
        sys.exit(0)
    except:
        sys.exit(0)

def keyhook(event):
    global xvalue
    global choice
    global compchoice
    global comp
    global basic
    global currencyx
    if event.scan_code == 108:
        if xvalue == -1:
            pass
        else:
            xvalue -= 1
    elif event.scan_code == 109:
        if compchoice == 1:
            if xvalue == (xmax - 1):
                pass
            else:
                xvalue += 1
        else:
            if xvalue == xmax:
                pass
            else:
                xvalue += 1
    if event.scan_code == 107:
        if choice == 0:
            choice = 1
        else:
            choice = 0
    if event.scan_code == 110:
        if compchoice == 0:
            compchoice = 1
            comp = xvalue
        else:
            compchoice = 0
    if event.scan_code == 118:
        if basic < 3:
            basic += 1
        else:
            basic = 0
    if event.scan_code == 106:
        currencyx += 1
        if currencyx == len(currency):
            currencyx = 0
    compare()

def getGraph(currencyx):
    url = 'https://api.coingecko.com/api/v3/coins/{}/market_chart?vs_currency=usd&days=1&interval=minutely'.format(currencyid[currencyx])
    response = requests.get(url)
    response_json = response.json()
    data = response_json
    try:
        plt.clf()
        plt.cla()
    except:
        pass
    x = 0
    listax = []
    listay = []
    for i in data["prices"]:
        listax.append(x)
        listay.append(i[1])
        x = x + 1
    line = plt.plot(listax, listay, "w", linewidth=1.3)
    plt.margins(0)
    ax = plt.axes()
    ax.relim()
    # lim = ax.get_ylim()
    # minlim = lim[0] - 30
    # maxlim = lim[1] + 10
    # ax.set_ylim(minlim, maxlim)
    ax.set_facecolor("black")
    ax.set_position([0, 0, 1, 1])
    fig = plt.gcf()
    fig.patch.set_facecolor('xkcd:black')
    fig.set_size_inches(1.28,0.4)
    img = buffer_plot_and_get(fig)
    l = [listax, listay, img, data, currencyx]
    return l

def getTime(xvalue,data,tz):
    data = data["prices"]
    timeraw = data[xvalue][0]
    time = datetime.fromtimestamp(timeraw/1000, timezone(tz)).strftime("%H:%M")
    return time

def compare():
    global perc
    if comp == xvalue:
        perc = 1
    elif comp < xvalue:
        perc = np.interp(xvalue, graph[0],graph[1]) / np.interp(comp, graph[0],graph[1])
    elif comp > xvalue:
        perc = np.interp(comp, graph[0],graph[1]) / np.interp(xvalue, graph[0],graph[1])

def getBasicInfo(listay):
    usd = listay[-1]
    perc = listay[-1] / listay[0]
    l = [usd, perc]
    return l

def getConf():
    if os.path.isfile("./config.cfg") == False:
        conf = open("config.cfg", "a")
        conf.write("[config]\ntimezone = UTC\n## All possible time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\n## Set to local if you want to use your configured time zone in Windows\n\ncurrency = BTC,ETH,XRP\n## All available currencies: https://www.coingecko.com/en/coins/all\n## You can set multiple currencies just seperate them by using a comma")
        conf.close()
        print("config.cfg was created")
        tz = "UTC"
        currency = ["BTC"]
        currencyid = ["bitcoin"]
    else:
        config = configparser.ConfigParser()
        config.read("config.cfg")
        if config.has_option("config", "timezone") and config.has_option("config", "currency"):
            try:
                tz = config.get("config", "timezone")
                if tz != "local":
                    try:
                        datetime.now().astimezone(timezone(tz))
                        print("Time zone {} has been set".format(tz))
                    except:
                        datetime.now().astimezone(timezone("CET"))
                        tz = "CET"
                        print("Default time zone CET has been set because an invalid time zone was set in the config file")
                else:
                    try:
                        import tzlocal
                        tz = str(tzlocal.get_localzone())
                        print("Time zone {} has been set".format(tz))
                    except:
                        tz = "CET"
                        print("tzlocal not installed, CET set as time zone")
            except configparser.Error:
                print("Default time zone CET has been set")
                tz = "CET"
            try:
                url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
                response = requests.get(url)
                response = response.json()
                currencyo = config.get("config", "currency")
                currencyo = currencyo.split(",")
                currencyo = [i.lower() for i in currencyo]
                currencyid = []
                currencies = {}
                currency = []
                for i in response:
                    currencies[i["symbol"]] = i["id"]
                for i in currencyo:
                    if i not in currencies.keys():
                        print("{} has been removed (not a valid currency)".format(i.upper()))
                    else:
                        currency.append(i)
                        currencyid.append(currencies[i])
                if len(currency) == 0:
                    currency = ["BTC"]
                    currencyid = ["bitcoin"]
                    print("BTC will be used because non of the given currencies were valid")
                else:
                    print(", ".join([i.upper() for i in currency]) + " will be used")
            except configparser.Error:
                print("Invalid currency has been entered, BTC will be used")
                currency = ["BTC"]
                currencyid = ["bitcoin"]
            except:
                print("Something unexpected went wrong, exiting...")
                sys.exit(0)
        else:
            print("Your config file is outdated, fetch a new one!")
            tz = "CET"
            currency = ["BTC"]
            currencyid = ["bitcoin"]
            print("CET has been set as time zone and BTC will be used")
    return tz, currency, currencyid

tz, currency, currencyid = getConf()

signal.signal(signal.SIGINT, signal_handler)

en = Enumeration()

devices = en.find(product="SteelSeries Apex Pro", interface=1)
if not devices:
    devices = en.find(product="SteelSeries Apex Pro TKL", interface=1)
if not devices:
    devices = en.find(product="SteelSeries Apex 7", interface=1)
if not devices:
    devices = en.find(product="SteelSeries Apex 7 TKL", interface=1)
if not devices:
    devices = en.find(product="SteelSeries Apex 5", interface=1)
if not devices:
    print("No devices found, exiting.")
    sys.exit(0)

dev = devices[0]

print("Press Ctrl-C to exit.\n")
dev.open()

im = Image.new('1', (128,40))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("OpenSans-Regular.ttf", 10)

graph = getGraph(0)
basicdata = getBasicInfo(graph[1])

x = 0
for i in range(64):
    x += 2
    im.paste(graph[2])
    draw.rectangle([(x,0),(128,40)], fill=0)
    draw.text((0, 0), currency[0].upper(), font=font, fill=255, stroke_width=2, stroke_fill=0)
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(0.05)

keyboard.on_press(keyhook)

xvalue = -1
timer = 0
basictimer = 0
basic = 0
choice = 0
comp = 0
compchoice = 0
currencyx = 0
while True:
    if currencyx != graph[4]:
        draw.text((0, 0), currency[currencyx].upper(), font=font, fill=255, stroke_width=2, stroke_fill=0)
        data = im.tobytes()
        data = bytearray([0x61]) + data + bytearray([0x00])
        dev.send_feature_report(data)
        graph = getGraph(currencyx)
        sleep(0.5)
        timer = 0
    if timer == 3000:
        graph = getGraph(currencyx)
        draw.text((0, 0), "Updating...", font=font, fill=255, stroke_width=2, stroke_fill=0)
        data = im.tobytes()
        data = bytearray([0x61]) + data + bytearray([0x00])
        dev.send_feature_report(data)
        sleep(1)
        timer = 0
    xmax = len(graph[1])
    draw.rectangle([(0,0),(128,40)], fill=0)
    im.paste(graph[2])
    if xvalue != -1 and xvalue != xmax:
        time = getTime(xvalue,graph[3],tz)
        y = np.interp(xvalue, graph[0],graph[1])
        draw.line([(((xvalue) * (128/xmax)), 0), (((xvalue) * (128/xmax)), 40)], fill=255, width=1)
        
        if compchoice == 1:
            draw.line([(((comp) * (128/xmax)), 2), (((comp) * (128/xmax)), 6)], fill=255, width=1)
            draw.line([(((comp) * (128/xmax)), 10), (((comp) * (128/xmax)), 14)], fill=255, width=1)
            draw.line([(((comp) * (128/xmax)), 18), (((comp) * (128/xmax)), 22)], fill=255, width=1)
            draw.line([(((comp) * (128/xmax)), 26), (((comp) * (128/xmax)), 30)], fill=255, width=1)
            draw.line([(((comp) * (128/xmax)), 34), (((comp) * (128/xmax)), 38)], fill=255, width=1)
            if perc > 1:
                draw.text((64, 40), "".join(("+", str("{:.2f}".format((perc * 100 - 100))), " %")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            else:
                draw.text((64, 40), " ".join((str("{:.2f}".format((perc * 100 - 100))), "%")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        else:
            if choice == 0:
                if y > 10:
                    draw.text((64, 40), " ".join((str("{:.2f}".format(y)), "USD")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
                else:
                    draw.text((64, 40), " ".join((str("{:.4f}".format(y)), "USD")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            elif choice == 1:
                draw.text((64, 40), time, font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
    else:
        if basictimer == 100:
            basicdata = getBasicInfo(graph[1])
            basictimer = 0
        if basic == 1:
            draw.text((0, 40), " ".join((str("{:.2f}".format(basicdata[0])), "USD")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ls")
            if basicdata[1] > 1:
                draw.text((128, 40), "".join(("+", str("{:.2f}".format((basicdata[1] * 100 - 100))), " %")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
            else:
                draw.text((128, 40), " ".join((str("{:.2f}".format((basicdata[1] * 100 - 100))), "%")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
        elif basic == 2:
            draw.text((64, 40), " ".join(("Max:", str("{:.2f}".format(max(graph[1]))))), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        elif basic == 3:
            draw.text((64, 40), " ".join(("Min:", str("{:.2f}".format(min(graph[1]))))), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        basictimer += 1
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(0.1)
    timer += 1
    
    

dev.close()

    
