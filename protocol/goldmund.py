#!/usr/bin/python
# -*- coding:utf-8 -*-


# Goldmund Rs232 protocol
baudrate = 115200

# standby command


def standby(on):
    return "standby {}\r\n".format("on" if on else "off")


def toggleStandby():
    return "standby toggle\r\n"

# volume command


def volumeUp(up):
    return "volume {}\r\n".format("up" if up else "down")


def setVolume(level):
    return "volume {}\r\n".format(level)

# input command


def nextInput():
    return "input next\r\n"


def previousInput():
    return "input prev\r\n"


def setInput(input):
    return "input {}\r\n".format(input)


# mute command

def mute(on):
    return "mute {}\r\n".format("on" if on else "off")


def toggleMute():
    return "mute toggle\r\n"


# query command
standby_command = "standby"
volume_command = "volume"
input_command = "input"
mute_command = "mute"

def query(command):
    return "{}\r\n".format(command)

# response format:
# $command\r\nok: $response\r\n>
# $command\r\nerr: $response\r\n>
def parseResponse(response):
    responses = response.split("\r\n")
    return responses[1].split(" ", 1)

def isSuccess(code):
    return code == "ok:"