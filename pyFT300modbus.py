import minimalmodbus as mm
from math import *
import serial
import serial.tools.list_ports

# def serial_ports():#自动寻找端口
#     ports = list(serial.tools.list_ports.comports())  
#     for port_no, description, address in ports:
#         if 'USB' in description:
#             return port_no
        
class FT300():
    def __init__(self,portname='COM5'):
      PORTNAME=portname
      SLAVEADDRESS=9

      mm.BAUDRATE=19200
      mm.BYTESIZE=8
      mm.PARITY="N"
      mm.STOPBITS=1
      mm.TIMEOUT=0.2     
      self.ft300=mm.Instrument(PORTNAME, slaveaddress=SLAVEADDRESS)

    def forceConverter(self,forceRegisterValue):
      force=0
      forceRegisterBin=bin(forceRegisterValue)[2:] 
      forceRegisterBin="{:0>{}}".format(forceRegisterBin, 16)
      if forceRegisterBin[0]=="1": #判断是否是负数
        force=-1*(int("1111111111111111",2)-int(forceRegisterBin,2)+1)/100
      else: #positive forces
        force=int(forceRegisterBin,2)/100
      return force

    def torqueConverter(self,torqueRegisterValue):
      torque=0
      torqueRegisterBin=bin(torqueRegisterValue)[2:]
      torqueRegisterBin="0"*(16-len(torqueRegisterBin))+torqueRegisterBin
      if torqueRegisterBin[0]=="1":
        torque=-1*(int("1111111111111111",2)-int(torqueRegisterBin,2)+1)/1000
      else:
        torque=int(torqueRegisterBin,2)/1000
      return torque

    def FTzero(self):
        registers=self.ft300.read_registers(180,6)
        fx=self.forceConverter(registers[0])
        fy=self.forceConverter(registers[1])
        fz=self.forceConverter(registers[2])
        tx=self.torqueConverter(registers[3])
        ty=self.torqueConverter(registers[4])
        tz=self.torqueConverter(registers[5])
        return fx,fy,fz,tx,ty,tz
    
