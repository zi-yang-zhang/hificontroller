#!/usr/bin/python
# -*- coding:utf-8 -*-

import serial

# dev = "/dev/ttySC0"

class config(object):
    def __init__(ser, Baudrate = 115200, dev = "/dev/ttyS0"):
        print (dev)
        ser.dev = dev
        ser.serial = serial.Serial(ser.dev, Baudrate)

    def Uart_SendByte(ser, value): 
        ser.serial.write(value.encode('ascii')) 
    
    def Uart_SendString(ser, value): 
        ser.serial.write(value.encode('ascii'))

    def Uart_ReceiveByte(ser): 
        return ser.serial.read(1).decode("utf-8")

    def Uart_ReceiveString(ser, value): 
        data = ser.serial.read(value)
        return data.decode("utf-8")

    def Uart_ReceiveStringLines(ser, lines):
        data = ser.serial.readlines(lines)
        response = ""
        for l in data:
            response += l.decode("utf-8")
        return response

    def Uart_ReceiveStringUntil(ser, terminal):
        data = ser.serial.read_until(terminal)
        return data.decode("utf-8")
        
    def Uart_Set_Baudrate(ser, Baudrate):
         ser.serial = serial.Serial(ser.dev, Baudrate)
    
    
        
         
         
         