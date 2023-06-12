import gripper_demo as GRP
import serial.tools.list_ports
import pyFT300modbus as FTdata
from threading import Thread
import minimalmodbus as mm
from time import sleep

#author      ：王海峰 pluto Wang plutohfw@gmail.com
#creat edate ： 2023/05/16
#参考资料    ：https://robotiq.com/support

def stopstream():
    ser=serial.Serial(port='COM5', baudrate=19200, bytesize=8, parity="N", stopbits=1, timeout=0.2)
    packet = bytearray()
    sendCount=0
    while sendCount<50:
        packet.append(0xff)
        sendCount=sendCount+1
    ser.write(packet)
    ser.close()
    print("stopstream done")
stopstream()   

# def serial_ports():#自动寻找端口
#     ports = list(serial.tools.list_ports.comports())  
#     for port_no, description, address in ports:
#         if 'USB' in description:
#             return port_no
        
class CtrlGrp():
    def __init__(self,portname):
        self.grp=GRP.Gripper(portname)
    
    def ACT(self): #激活夹爪
        self.grp.ClearrACT()
        self.grp.activate()
        while not self.isACTed():
            None
        print('Gripper is activaited')

    def isACTed(self): #夹爪是否被激活
        while not self.grp.isavtivated():
            None
        return self.grp.isavtivated()
                
    def GTO(self,PosSpdFrc): #执行动作
        self.grp.grip(PosSpdFrc)    #[POS,SPEED,SPEED],open=full ,close=0
        while self.OBJ()[0] == 0x39: #0x39=57
            None            
        print('Completed',' Position：%3s/255 %5smm'%(self.OBJ()[1],self.OBJ()[2]))
        return self.OBJ()[1]

    def OBJ(self): #返回当前值
        return self.grp.ReadGripperStatus()
    
    def SerClose(self): #关闭串口
        self.grp.serclose()
class FT300s():
    def __init__(self):
        pass
    
    def ftzero(self):
        ftdatazero=FTdata.FT300().FTzero()
        self.fxzero=ftdatazero[0]
        self.fyzero=ftdatazero[1]
        self.fzzero=ftdatazero[2]
        self.txzero=ftdatazero[3]
        self.tyzero=ftdatazero[4]
        self.tzzero=ftdatazero[5]
    
    def ft(self):
        ftdata=FTdata.FT300().FTzero()
        self.fx=round(ftdata[0]-self.fxzero,2)
        self.fy=round(ftdata[1]-self.fyzero,2)
        self.fz=round(ftdata[2]-self.fzzero,2)
        self.tx=round(ftdata[3]-self.txzero,2)
        self.ty=round(ftdata[4]-self.tyzero,2)
        self.tz=round(ftdata[5]-self.tzzero,2)
        return self.fx,self.fy,self.fz,self.tx,self.ty,self.tz
    
    def fzCheckvalue(self,value):
        # print(self.ft())
        ftdata=self.ft()[2]
        while ftdata > value: 
            ftdata=self.ft()[2]
            pass
        print('fz=%f'%ftdata)

CtrGrp=CtrlGrp('COM6')
ft=FT300s()

CtrGrp.ACT()
ft.ftzero()


while True:
    ft.ftzero()
    ft.fzCheckvalue(-1)
    if CtrGrp.GTO([0x00,0xFF,0x00]) ==3:
        pass
    ft.ftzero()    
    ft.fzCheckvalue(-1)
    CtrGrp.GTO([0xFF,0xFF,0x00])