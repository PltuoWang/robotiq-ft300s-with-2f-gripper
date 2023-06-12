import serial
import time

def serial_ports():#自动寻找端口
    ports = list(serial.tools.list_ports.comports())  
    for port_no, description, address in ports:
        if 'USB' in description:
            return port_no
        
def CRC(command): #CRC校验
    crc = 0xFFFF
    for b in command:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    command.append(crc & 0xFF)
    command.append((crc >> 8) & 0xFF)
    return command

class Gripper():
    def __init__(self,portname):
        PORTNAME=portname
        BAUDRATE=115200
        TIMEOUT=1
        self.ser = serial.Serial(PORTNAME, BAUDRATE, timeout=TIMEOUT)

    # 激活指令

    def ClearrACT(self):      
        activate_command = [0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x73,0x30]                        
        # 发送激活指令
        self.ser.write(bytes(activate_command))
        time.sleep(0.1)

        # 读取激活指令返回数据
        response = self.ser.read(8)
        return response
    
    def activate(self):      
        activate_command = [0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,0x72,0xE1]                      
        self.ser.write(bytes(activate_command))
        time.sleep(0.1)
        # 读取激活指令返回数据
        response = self.ser.read(8)
        return response
    
    def isavtivated(self):
        activate_command = [0x09, 0x04, 0x07, 0xD0, 0x00, 0x01,0x30,0x0F]
        # 发送激活指令
        self.ser.write(bytes(activate_command)) 
        time.sleep(0.1)
        # 读取激活指令返回数据
        response = self.ser.read(7)
        if response[3]== 0x31: #0x31=
            return True
        return False
    
    def grip(self,command):
        # 抓取指令       CLOSE    09 10 03 E8 00 03 06 09 00 00 FF FF FF 42 29
        grip_command = [0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x09, 0x00, 0x00,command[0],command[1],command[2]]
        # 发送抓取指令
        self.ser.write(bytes(CRC(grip_command)))
        time.sleep(0.1)

        # 读取抓取指令返回数据
        response = self.ser.read(8)
        # print("抓取返回数据:", response)

    def ReadGripperStatus(self):
        # 获取反馈指令
        # feedback_command = [0x09, 0x03, 0x07, 0xD0, 0x00, 0x03, 0x04, 0x0E]
        feedback_command = [0x09,0x04,0x07,0xD0,0x00,0x03,0xB1,0xCE]
        # 发送获取反馈指令

        self.ser.write(bytes(feedback_command))
        time.sleep(0.1)

        # 读取获取反馈指令返回数据
        # 0x79 121 外撑 OK
        # 0xB9 185 夹取 OK
        # 0x39 57  夹爪运动中
        # 0xF9 249 完成动作到制定位置

        response = self.ser.read(11)
        # position=round((-50/255)*response[7]+50,2)
        a=-(50/246)
        b=12462/246
        # x=249*a+b+2-0.048780487804876316
        position=round(response[7]*a+b+2-0.048780487804876316,2)
        # print(response[3],response[7],position)
        return(response[3],response[7],position)

    # 关闭串口连接
    def serclose(self):
        self.ser.close()
