import requests
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
from easyhid import Enumeration
from time import sleep
import signal
import sys
import pickle
from datetime import datetime
import keyboard
import numpy as np
from pytz import timezone
import warnings
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
    if event.scan_code == 108:
        if xvalue == -1:
            pass
        else:
            xvalue -= 1
    elif event.scan_code == 109:
        if compchoice == 1:
            if xvalue == 143:
                pass
            else:
                xvalue += 1
        else:
            if xvalue == 144:
                pass
            else:
                xvalue += 1
    if event.scan_code == 107:
        if choice < 3:
            choice += 1
        else:
            choice = 0
    if event.scan_code == 110:
        if compchoice == 0:
            compchoice = 1
            comp = xvalue
        else:
            compchoice = 0
    if event.scan_code == 118:
        if basic == 0:
            basic = 1
        else:
            basic = 0
    compare()

def getGraph():
    response = requests.get("https://www.sparkpool.com/v1/currency/statsHistory?currency=ETH&zoom=d/")
    response_json = response.json()
    data = response_json["data"]
    try:
        plt.clf()
        plt.cla()
    except:
        pass
    x = 0
    listax = []
    listay = []
    for i in data:
        listax.append(x)
        listay.append(i["usd"])
        x = x + 1
    
    line = plt.plot(listax, listay, "w", linewidth=1.3)
    plt.margins(0)
    ax = plt.axes()
    ax.relim()
    lim = ax.get_ylim()
    minlim = lim[0] - 30
    maxlim = lim[1] + 10
    ax.set_ylim(minlim, maxlim)
    ax.set_facecolor("black")
    ax.set_position([0, 0, 1, 1])
    fig = plt.gcf()
    fig.patch.set_facecolor('xkcd:black')
    fig.set_size_inches(1.28,0.4)
    img = buffer_plot_and_get(fig)
    l = [listax, listay, img, data]
    return l

def getTime(xvalue,data):
    try:
        timeraw = data[xvalue]["time"]
        time = "".join((str(timeraw[11]),str(timeraw[12]),str(timeraw[13]),str(timeraw[14]),str(timeraw[15]),"+0000"))
        timefrom = datetime.strptime(time, "%H:%M%z")
        timeto = timefrom.astimezone(timezone('CET'))
        time = timeto.strftime("%H:%M")
    except:
        time = "error"
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
    response = requests.get("https://www.sparkpool.com/v1/currency/stats?currency=ETH")
    response_json = response.json()
    usd = response_json["data"]["usd"]
    perc = usd / listay[0]
    l = [usd, perc]
    return l
    
    

signal.signal(signal.SIGINT, signal_handler)

en = Enumeration()

devices = en.find(vid=0x1038, pid=0x1618, interface=1)
if not devices:
    devices = en.find(vid=0x1038, pid=0x1610, interface=1)
if not devices:
    print("No devices found, exiting.")
    sys.exit(0)

dev = devices[0]

print("Press Ctrl-C to exit.\n")
dev.open()

keyboard.on_press(keyhook)

im = Image.new('1', (128,40))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("OpenSans-Regular.ttf", 10)

graph = getGraph()
basicdata = getBasicInfo(graph[1])

x = 0
for i in range(64):
    x += 2
    im.paste(graph[2])
    draw.rectangle([(x,0),(128,40)], fill=0)
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(0.05)

xvalue = -1
timer = 0
basictimer = 0
basic = 0
choice = 0
comp = 0
compchoice = 0
while True:
    if timer == 600:
        graph = getGraph()
        draw.text((0, 0), "Updating...", font=font, fill=255, stroke_width=2, stroke_fill=0)
        data = im.tobytes()
        data = bytearray([0x61]) + data + bytearray([0x00])
        dev.send_feature_report(data)
        sleep(1)
        timer = 0
    draw.rectangle([(0,0),(128,40)], fill=0)
    im.paste(graph[2])
    if xvalue != -1 and xvalue != 144:
        time = getTime(xvalue,graph[3])
        y = np.interp(xvalue, graph[0],graph[1])
        draw.line([(((xvalue) * (8/9)), 0), (((xvalue) * (8/9)), 40)], fill=255, width=1)
        
        if compchoice == 1:
            draw.line([(((comp) * (8/9)), 2), (((comp) * (8/9)), 6)], fill=255, width=1)
            draw.line([(((comp) * (8/9)), 10), (((comp) * (8/9)), 14)], fill=255, width=1)
            draw.line([(((comp) * (8/9)), 18), (((comp) * (8/9)), 22)], fill=255, width=1)
            draw.line([(((comp) * (8/9)), 26), (((comp) * (8/9)), 30)], fill=255, width=1)
            draw.line([(((comp) * (8/9)), 34), (((comp) * (8/9)), 38)], fill=255, width=1)
            if perc > 1:
                draw.text((64, 40), "".join(("+", str("{:.2f}".format((perc * 100 - 100))), " %")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            else:
                draw.text((64, 40), " ".join((str("{:.2f}".format((perc * 100 - 100))), "%")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
        else:
            if choice == 0:
                draw.text((64, 40), " ".join((str("{:.2f}".format(y)), "USD")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            elif choice == 1:
                draw.text((64, 40), time, font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            elif choice == 2:
                draw.text((64, 40), " ".join(("Max:", str("{:.2f}".format(max(graph[1]))))), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
            elif choice == 3:
                draw.text((64, 40), " ".join(("Min:", str("{:.2f}".format(min(graph[1]))))), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ms")
    elif basic == 1:
        if basictimer == 50:
            basicdata = getBasicInfo(graph[1])
            basictimer = 0
        draw.text((0, 40), " ".join((str("{:.2f}".format(basicdata[0])), "USD")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="ls")
        if perc > 1:
            draw.text((128, 40), "".join(("+", str("{:.2f}".format((basicdata[1] * 100 - 100))), " %")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
        else:
            draw.text((128, 40), " ".join((str("{:.2f}".format((basicdata[1] * 100 - 100))), "%")), font=font, fill=255, stroke_width=2, stroke_fill=0, anchor="rs")
        basictimer += 1
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(0.1)
    timer += 1
    
    

dev.close()

    
