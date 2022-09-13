#!/usr/bin/python
# -*- coding:utf-8 -*-


# T+A DAC8 DSD Rs232 protocol
baudrate = 38400

# Power command


def power(on):
    return "PWR {}\r\n".format("ON" if on else "OFF")


# Input command
spDif1 = 1
spDif2 = 2
spDif3 = 3
spDif4 = 4
opt = 5
bnc = 6
aesEbu = 7
sysIn = 8
usb = 9


def selectInput(input):
    return "INP {}\r\n".format(input)


# OVS command
fir1 = 1
fir2 = 2
bezierIIR = 3
bezierSpline = 4


def selectOVS(input):
    return "OVS {}\r\n".format(input)

# INV command


def invertPhase(on):
    return "INV {}\r\n".format("ON" if on else "OFF")

# WIDE command


def wide(on):
    return "WIDE {}\r\n".format("ON" if on else "OFF")

# Mute command


def mute(on):
    return "MUTE {}\r\n".format("ON" if on else "OFF")

# Echo command


def echo(on):
    return "ECHO {}\r\n".format("ON" if on else "OFF")

# Volumn command


def setVolume(level, ramp):
    if level > 64 or level < 0:
        return
    return "VOL{} {}\r\n".format(" Ramp"if ramp else "", level)

# Bridghtness command


def setBrightness(level):
    if level > 8 or level < 0:
        return
    return "BRT {}\r\n".format(level)


# Query command

power = "PWR"
input = "INP"
volume = "VOL"
vos = "VOS"
inv = "INV"
led = "LED"
rate = "RATE"
wide = "WIDE"
mute = "MUTE"
bridgtness = "BRT"
status = "S"
echo = "ECHO"
notify = "NOTIFY"


def query(name):
    return "{} ?\r\n".format(name)


# Notify command
notificationOff = 0
notificationError = 1
notificationALL = 2


def setNotification(input):
    return "NOTIFY {}\r\n".format(input)


def parseResponse(response):
    if not response.startswith(">$"):
        return "", ""
    data = response.split(" ", 1)
    return data[0][len(">$"):], data[1]


def start(op):
    op(echo(True))
    op(notify(notificationALL))
