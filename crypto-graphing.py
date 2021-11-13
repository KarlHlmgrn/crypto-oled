import requests
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
from easyhid import Enumeration
from time import sleep
import signal
import sys
from datetime import datetime
import keyboard
import numpy as np
from pytz import timezone
import configparser
import os

import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use('Agg')

## --- CURRENT VERSION --- ##
version = 3.2
## ----------------------- ##

def bufferImg(fig):
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
    global cursorX, infoToggle, basicInfoChoice, coinIndex, xValues, yValues, graphImage, actualIndex, currentPrice, dailyPercent, timeStamps
    if event.scan_code == 106:
        coinIndex += 1
        if coinIndex == len(coins):
            coinIndex = 0
        xValues, yValues, graphImage, actualIndex, currentPrice, dailyPercent, timeStamps = getGraph(coinIndex)
        if cursorX > xValues[-1]:
            cursorX = xValues[-1]
        drawImage(True)
    else:
        if event.scan_code == 108:
            moveCursor("left")
        elif event.scan_code == 109:
            moveCursor("right")
        if event.scan_code == 107:
            if infoToggle == 0:
                infoToggle = 1
            else:
                infoToggle = 0
        if event.scan_code == 110:
            toggleCompare()
        if event.scan_code == 118:
            if basicInfoChoice < 3:
                basicInfoChoice += 1
            else:
                basicInfoChoice = 0
        drawImage(False)

def toggleCompare():
    global compareToggle, compareX
    if compareToggle == 0:
        compareToggle = 1
        compareX = cursorX
    else:
        compareToggle = 0

def moveCursor(direction):
    global cursorX
    if direction == "right":
        if compareToggle == 1:
            if cursorX == (xmax - 1):
                pass
            else:
                cursorX += 1
        else:
            if cursorX == xmax:
                cursorX = 0
            else:
                cursorX += 1
    else:
        if cursorX == -1:
            cursorX = xmax - 1
        else:
            cursorX -= 1

def getGraph(coinIndex):
    url = 'https://api.coingecko.com/api/v3/coins/{}/market_chart?vs_currency=usd&days=1&interval=minutely'.format(coinIDs[coinIndex])
    response = requests.get(url)
    response_json = response.json()
    dataAPI = response_json
    try:
        plt.clf()
        plt.cla()
    except:
        pass
    x = 0
    xValues = []
    yValues = []
    for i in dataAPI["prices"]:
        xValues.append(x)
        yValues.append(i[1])
        x = x + 1
    ax = plt.axes((0, 0, 1, 1), facecolor="black")
    line, = plt.plot(xValues, yValues, "w", linewidth=0.2)
    line.set_antialiased(False) 
    plt.margins(0)
    ax.relim()
    fig = plt.gcf()
    fig.patch.set_facecolor('xkcd:black')
    fig.set_size_inches(1.28,0.4)
    graphImage = bufferImg(fig)

    currentPrice = yValues[-1]
    dailyPercent = yValues[-1] / yValues[0]

    timeStamps = []
    for timeraw in dataAPI["prices"]:
        timeStamps.append(datetime.fromtimestamp(timeraw[0]/1000, timezone(tz)).strftime("%H:%M"))

    return xValues, yValues, graphImage, coinIndex, currentPrice, dailyPercent, timeStamps

def drawImage(changeCoin):
    global timer
    if changeCoin:
        draw.text((0, 0), coins[coinIndex].upper(), font=font, fill=255, stroke_width=2, stroke_fill=0)
        data = im.tobytes()
        data = bytearray([0x61]) + data + bytearray([0x00])
        dev.send_feature_report(data)
        sleep(0.5)
        timer = 0
    draw.rectangle([(0,0),(128,40)], fill=0)
    im.paste(graphImage)
    if cursorX != -1 and cursorX != xmax:
        yValue = np.interp(cursorX, xValues, yValues)
        draw.line([(((cursorX) * (128/xmax)), 0), (((cursorX) * (128/xmax)), 40)], fill=255, width=1)
        draw.ellipse((cursorX * (128/xmax) - 2, 38 - (yValue-min(yValues)) * (40/(max(yValues)-min(yValues))), cursorX * (128/xmax) + 2, 42 - (yValue-min(yValues)) * (40/(max(yValues)-min(yValues)))), fill=255)
        
        if compareToggle == 1:
            draw.line([(((compareX) * (128/xmax)), 2), (((compareX) * (128/xmax)), 6)], fill=255, width=1)
            draw.line([(((compareX) * (128/xmax)), 10), (((compareX) * (128/xmax)), 14)], fill=255, width=1)
            draw.line([(((compareX) * (128/xmax)), 18), (((compareX) * (128/xmax)), 22)], fill=255, width=1)
            draw.line([(((compareX) * (128/xmax)), 26), (((compareX) * (128/xmax)), 30)], fill=255, width=1)
            draw.line([(((compareX) * (128/xmax)), 34), (((compareX) * (128/xmax)), 38)], fill=255, width=1)
            yValue = np.interp(compareX, xValues, yValues)
            draw.ellipse((compareX * (128/xmax) - 2, 38 - (yValue-min(yValues)) * (40/(max(yValues)-min(yValues))), compareX * (128/xmax) + 2, 42 - (yValue-min(yValues)) * (40/(max(yValues)-min(yValues)))), fill=255)
            if compareX == cursorX:
                comparePercent = 1
            elif compareX < cursorX:
                comparePercent = np.interp(cursorX, xValues, yValues) / np.interp(compareX, xValues, yValues)
            elif compareX > cursorX:
                comparePercent = np.interp(compareX, xValues, yValues) / np.interp(cursorX, xValues, yValues)
            if comparePercent > 1:
                draw.text((64, 40), ("+" + f"{(comparePercent * 100 - 100):.2f}" + " %"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            else:
                draw.text((64, 40), (f"{(comparePercent * 100 - 100):.2f}" + " %"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        else:
            if infoToggle == 0:
                if yValue > 10:
                    draw.text((64, 40), (f"{yValue:.2f}" + " USD"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
                else:
                    draw.text((64, 40), (f"{yValue:.4f}" + " USD"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            elif infoToggle == 1:
                draw.text((64, 40), timeStamps[cursorX], font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
    else:
        if basicInfoChoice == 1:
            if currentPrice > 10:
                draw.text((0, 40), (f"{currentPrice:.2f}" + " USD"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ls")
            else:
                draw.text((0, 40), (f"{currentPrice:.4f}" + " USD"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ls")
            if dailyPercent > 1:
                draw.text((128, 40), ("+" + f"{(dailyPercent * 100 - 100):.2f}" + " %"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
            else:
                draw.text((128, 40), (f"{(dailyPercent * 100 - 100):.2f}" + " %"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
        elif basicInfoChoice == 2:
            if max(yValues) > 10:
                draw.text((64, 40), ("Max: " + f"{max(yValues):.2f}"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            else:
                draw.text((64, 40), ("Max: " + f"{max(yValues):.4f}"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        elif basicInfoChoice == 3:
            if min(yValues) > 10:
                draw.text((64, 40), ("Min: " + f"{min(yValues):.2f}"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            else:
                draw.text((64, 40), ("Min: " + f"{min(yValues):.4f}"), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)

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

tz, coins, coinIDs = getConf()

latestVersion = requests.get("https://api.github.com/repos/KarlHlmgrn/crypto-oled/releases/latest")
if latestVersion.status_code == 200:
    latestVersionJSON = latestVersion.json()
    if ("v" + str(version)) != latestVersionJSON["tag_name"]:
        print("\nThere is a new version of crypto-oled available, get it at https://github.com/KarlHlmgrn/crypto-oled/releases/tag/" + str(latestVersionJSON["tag_name"]) + "\n")
    else:
        print("You are running the latest version of crypto-oled!")

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

cursorX = -1
timer, basicInfoChoice, infoToggle, compareX, compareToggle, coinIndex = 0, 0, 0, 0, 0, 0

xValues, yValues, graphImage, actualIndex, currentPrice, dailyPercent, timeStamps = getGraph(coinIndex)
xmax = xValues[-1]

x = 0
for i in range(64):
    x += 2
    im.paste(graphImage)
    draw.rectangle([(x,0),(128,40)], fill=0)
    draw.text((0, 0), coins[0].upper(), font=font, fill=255, stroke_width=2, stroke_fill=0)
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(0.05)

drawImage(False)
keyboard.on_press(keyhook)
toggleVolume = False
def toggleVolume():
    global toggleVolume
    if toggleVolume == True:
        toggleVolume = False
        keyboard.remove_hotkey(-175)
        keyboard.remove_hotkey(-174)
        keyboard.remove_hotkey(-173)
    else:
        toggleVolume = True
        keyboard.add_hotkey(-175, lambda: moveCursor("right"), suppress=True)
        keyboard.add_hotkey(-174, lambda: moveCursor("left"), suppress=True)
        keyboard.add_hotkey(-173, lambda: toggleCompare(), suppress=True)

keyboard.add_hotkey('ctrl+shift+v', toggleVolume, suppress=True)

while True:
    if timer == 600:
            xValues, yValues, graphImage, actualIndex, currentPrice, dailyPercent, timeStamps = getGraph(coinIndex)
            if cursorX > xValues[-1]:
                cursorX = xValues[-1]
            xmax = xValues[-1]
            draw.text((0, 0), "Updating...", font=font, fill=255, stroke_width=2, stroke_fill=0)
            data = im.tobytes()
            data = bytearray([0x61]) + data + bytearray([0x00])
            dev.send_feature_report(data)
            sleep(0.5)
            timer = 0
            drawImage(False)
            
    sleep(0.1)
    timer += 1


