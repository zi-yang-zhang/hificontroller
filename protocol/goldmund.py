#!/usr/bin/python
# -*- coding:utf-8 -*-


# Goldmund Rs232 protocol
baudrate = 115200

# standby command


def standby(on):
    return "standby {}\r".format("on" if on else "off")


def toggleStandby():
    return "standby toggle\r"

# volumn command


def volumn(up):
    return "volumn {}\r".format("up" if up else "down")


def setVolumn(level):
    return "volumn {}\r".format(level)

# input command


def nextInput():
    return "input next\r"


def previousInput():
    return "input prev\r"


def setInput(input):
    return "input {}\r".format(input)


# mute command

def mute(on):
    return "mute {}\r".format("on" if on else "off")


def toggleMute():
    return "mute toggle\r"


# query command
standby_command = "standby"
volumn_command = "volumn"
input_command = "input"
mute_command = "mute"

def query(command):
    return "{}\r".format(command)

def parseResponse(response):
    if not response.startswith("ok: "):
        return "", ""
    data = response.split(" ")
    return data[1], data[2]
