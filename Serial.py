import serial
import time


def find_com():  # autonomously search for the serial port and return
    ser = serial.Serial()
    i = 1
    se = 0
    while i < 1024:
        name = 'COM' + str(i)
        ser.open
        try:
            ser.isOpen
            ser = serial.Serial(name, 9600, timeout=0.1)
            print('————————————————————————————————\r\n尝试串口：' + name)
            tic = time.perf_counter()
            while 1:
                ser.write('A'.encode('gbk'))
                rev = ser.readline()
                # print(rev)
                if rev == b'B\r\n':
                    se = name
                    break
                if time.perf_counter() - tic >= 1:
                    break
        except serial.serialutil.SerialException:
            pass
        if se != 0:
            break
        i += 1
    return se


def serialCMD(ser_local, command):
    if command == 'PAUSE':
        ser_local.write(b'X')
    if command == 'SOFT_MUSIC':
        ser_local.write(b'S')
    if command == 'PASSION_MUSIC':
        ser_local.write(b'P')


def initSerial(ser_local):
    while 1:  # 初始化
        time.sleep(2)
        print('尝试连接下位机')
        ser_local.write(b'K')
        rev2 = ser_local.readline()
        print(rev2)
        if rev2 == b'B\r\n':
            break
    print("下位机连接正常---开始工作")


if __name__ == "__main__":  # current main function
    ser = serial.Serial(find_com(), 9600, timeout=0.1)  # Open the serial port that the search can return
    tic = time.perf_counter()
    while 1:  # initialization
        time.sleep(2)
        ser.write(b'K')
        print("发送")
        rev = ser.readline()
        # print(rev)
        if rev == b'B\r\n':
            break

    serialCMD('PASSION_MUSIC')
    print(ser)
